import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/producto.dart';
import '../models/movimiento.dart';
import '../models/scan_result.dart';

class InventoryProvider extends ChangeNotifier {
  final ApiService _apiService;

  InventoryProvider(this._apiService);

  // Estado
  bool _isLoading = false;
  String? _errorMessage;
  ScanResult? _lastScanResult;
  Producto? _selectedProduct;
  List<Movimiento> _movimientos = [];

  // Getters
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  ScanResult? get lastScanResult => _lastScanResult;
  Producto? get selectedProduct => _selectedProduct;
  List<Movimiento> get movimientos => _movimientos;

  /// Escanear código
  Future<void> escanearCodigo(String codigo) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _lastScanResult = await _apiService.escanearCodigo(codigo);
      
      if (_lastScanResult?.esProducto ?? false) {
        _selectedProduct = _lastScanResult?.producto;
      }
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Crear movimiento rápido
  Future<bool> crearMovimientoRapido({
    required String codigoProducto,
    required String tipoMovimiento,
    required int cantidad,
    String? referencia,
  }) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final resultado = await _apiService.crearMovimientoRapido(
        codigoProducto: codigoProducto,
        tipoMovimiento: tipoMovimiento,
        cantidad: cantidad,
        referencia: referencia,
      );

      _isLoading = false;
      notifyListeners();
      
      return resultado['exito'] ?? false;
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Obtener historial
  Future<void> obtenerHistorial(String codigoProducto) async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _movimientos = await _apiService.obtenerHistorial(codigoProducto);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Limpiar resultado de escaneo
  void clearScanResult() {
    _lastScanResult = null;
    _selectedProduct = null;
    _errorMessage = null;
    notifyListeners();
  }

  /// Verificar conexión con API
  Future<bool> checkConnection() async {
    return await _apiService.checkConnection();
  }
}
