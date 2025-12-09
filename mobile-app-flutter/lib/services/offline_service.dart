import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/producto.dart';
import '../models/movimiento.dart';

class OfflineService {
  static const String _keyPendingScans = 'pending_scans';
  static const String _keyPendingMovements = 'pending_movements';
  static const String _keyCachedProducts = 'cached_products';
  static const String _keyLastSync = 'last_sync';

  /// Guardar escaneo pendiente (sin conexión)
  Future<void> guardarEscaneo(String codigo, DateTime timestamp) async {
    final prefs = await SharedPreferences.getInstance();
    final pendingScans = await obtenerEscaneosPendientes();
    
    pendingScans.add({
      'codigo': codigo,
      'timestamp': timestamp.toIso8601String(),
    });
    
    await prefs.setString(_keyPendingScans, jsonEncode(pendingScans));
  }

  /// Guardar movimiento pendiente (sin conexión)
  Future<void> guardarMovimientoPendiente({
    required String codigoProducto,
    required String tipo,
    required int cantidad,
    required String observaciones,
    required DateTime timestamp,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final pendingMovements = await obtenerMovimientosPendientes();
    
    pendingMovements.add({
      'codigo_producto': codigoProducto,
      'tipo_movimiento': tipo,
      'cantidad': cantidad,
      'observaciones': observaciones,
      'timestamp': timestamp.toIso8601String(),
    });
    
    await prefs.setString(_keyPendingMovements, jsonEncode(pendingMovements));
  }

  /// Obtener escaneos pendientes
  Future<List<Map<String, dynamic>>> obtenerEscaneosPendientes() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_keyPendingScans);
    if (data == null) return [];
    
    return List<Map<String, dynamic>>.from(jsonDecode(data));
  }

  /// Obtener movimientos pendientes
  Future<List<Map<String, dynamic>>> obtenerMovimientosPendientes() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_keyPendingMovements);
    if (data == null) return [];
    
    return List<Map<String, dynamic>>.from(jsonDecode(data));
  }

  /// Limpiar escaneos pendientes (después de sincronizar)
  Future<void> limpiarEscaneosPendientes() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyPendingScans);
  }

  /// Limpiar movimientos pendientes (después de sincronizar)
  Future<void> limpiarMovimientosPendientes() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyPendingMovements);
  }

  /// Guardar producto en caché
  Future<void> cachearProducto(Producto producto) async {
    final prefs = await SharedPreferences.getInstance();
    final cachedProducts = await obtenerProductosCacheados();
    
    // Eliminar producto existente con mismo código
    cachedProducts.removeWhere((p) => p['codigo'] == producto.codigo);
    
    // Agregar producto actualizado
    cachedProducts.add({
      'codigo': producto.codigo,
      'nombre': producto.nombre,
      'descripcion': producto.descripcion,
      'precio': producto.precio,
      'stock_actual': producto.stockActual,
      'stock_minimo': producto.stockMinimo,
      'stock_maximo': producto.stockMaximo,
      'ubicacion': producto.ubicacion,
      'categoria': producto.categoria,
      'cached_at': DateTime.now().toIso8601String(),
    });
    
    // Mantener solo los últimos 50 productos
    if (cachedProducts.length > 50) {
      cachedProducts.removeAt(0);
    }
    
    await prefs.setString(_keyCachedProducts, jsonEncode(cachedProducts));
  }

  /// Obtener productos cacheados
  Future<List<Map<String, dynamic>>> obtenerProductosCacheados() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_keyCachedProducts);
    if (data == null) return [];
    
    return List<Map<String, dynamic>>.from(jsonDecode(data));
  }

  /// Buscar producto en caché por código
  Future<Producto?> buscarProductoEnCache(String codigo) async {
    final cachedProducts = await obtenerProductosCacheados();
    
    try {
      final productData = cachedProducts.firstWhere(
        (p) => p['codigo'] == codigo,
      );
      
      return Producto.fromJson(productData);
    } catch (e) {
      return null;
    }
  }

  /// Actualizar timestamp de última sincronización
  Future<void> actualizarUltimaSync() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyLastSync, DateTime.now().toIso8601String());
  }

  /// Obtener timestamp de última sincronización
  Future<DateTime?> obtenerUltimaSync() async {
    final prefs = await SharedPreferences.getInstance();
    final data = prefs.getString(_keyLastSync);
    if (data == null) return null;
    
    return DateTime.parse(data);
  }

  /// Contar operaciones pendientes
  Future<int> contarOperacionesPendientes() async {
    final scans = await obtenerEscaneosPendientes();
    final movements = await obtenerMovimientosPendientes();
    return scans.length + movements.length;
  }

  /// Limpiar toda la caché (útil para logout o reset)
  Future<void> limpiarTodo() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyPendingScans);
    await prefs.remove(_keyPendingMovements);
    await prefs.remove(_keyCachedProducts);
    await prefs.remove(_keyLastSync);
  }
}
