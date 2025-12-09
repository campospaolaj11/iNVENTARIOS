import 'package:flutter/foundation.dart';
import 'offline_service.dart';
import 'api_service.dart';

class SyncService extends ChangeNotifier {
  final ApiService _apiService = ApiService();
  final OfflineService _offlineService = OfflineService();
  
  bool _isSyncing = false;
  int _pendingOperations = 0;
  String? _lastSyncStatus;
  DateTime? _lastSyncTime;

  bool get isSyncing => _isSyncing;
  int get pendingOperations => _pendingOperations;
  String? get lastSyncStatus => _lastSyncStatus;
  DateTime? get lastSyncTime => _lastSyncTime;

  SyncService() {
    _initializeSync();
  }

  Future<void> _initializeSync() async {
    await _updatePendingCount();
    _lastSyncTime = await _offlineService.obtenerUltimaSync();
    notifyListeners();
  }

  /// Actualizar contador de operaciones pendientes
  Future<void> _updatePendingCount() async {
    _pendingOperations = await _offlineService.contarOperacionesPendientes();
    notifyListeners();
  }

  /// Sincronizar todas las operaciones pendientes
  Future<bool> sincronizarTodo() async {
    if (_isSyncing) {
      return false; // Ya hay una sincronización en progreso
    }

    _isSyncing = true;
    _lastSyncStatus = 'Sincronizando...';
    notifyListeners();

    try {
      // Sincronizar movimientos pendientes
      final movimientos = await _offlineService.obtenerMovimientosPendientes();
      int movimientosExitosos = 0;
      
      for (final mov in movimientos) {
        try {
          await _apiService.crearMovimientoRapido(
            codigoProducto: mov['codigo_producto'],
            tipoMovimiento: mov['tipo_movimiento'],
            cantidad: mov['cantidad'],
            observaciones: mov['observaciones'],
          );
          movimientosExitosos++;
        } catch (e) {
          debugPrint('Error sincronizando movimiento: $e');
          // Continuar con los siguientes
        }
      }

      // Si todos se sincronizaron, limpiar la cola
      if (movimientosExitosos == movimientos.length) {
        await _offlineService.limpiarMovimientosPendientes();
      }

      // Limpiar escaneos pendientes (solo registros, no hay que enviar)
      await _offlineService.limpiarEscaneosPendientes();

      // Actualizar timestamp de sincronización
      await _offlineService.actualizarUltimaSync();
      _lastSyncTime = DateTime.now();

      // Actualizar estado
      await _updatePendingCount();
      
      if (_pendingOperations == 0) {
        _lastSyncStatus = 'Sincronización completa';
      } else {
        _lastSyncStatus = 'Sincronización parcial (${movimientos.length - movimientosExitosos} errores)';
      }

      _isSyncing = false;
      notifyListeners();
      
      return true;
    } catch (e) {
      _lastSyncStatus = 'Error: ${e.toString()}';
      _isSyncing = false;
      notifyListeners();
      return false;
    }
  }

  /// Verificar si hay operaciones pendientes
  Future<bool> hayOperacionesPendientes() async {
    await _updatePendingCount();
    return _pendingOperations > 0;
  }
}
