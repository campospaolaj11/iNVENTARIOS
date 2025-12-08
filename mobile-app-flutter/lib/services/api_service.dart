import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/producto.dart';
import '../models/movimiento.dart';
import '../models/scan_result.dart';

class ApiService {
  // Para emulador Android usa: http://10.0.2.2:8000/api
  // Para dispositivo físico usa: http://192.168.22.61:8000/api
  // Para producción usa tu backend desplegado en Railway/Render
  static const String baseUrl = 'http://10.0.2.2:8000/api';
  
  // Timeout para requests
  static const Duration timeout = Duration(seconds: 10);

  // Headers comunes
  Map<String, String> get headers => {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  /// Escanear código QR/Barras
  Future<ScanResult> escanearCodigo(String codigo) async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/scanner/escanear?codigo=$codigo'),
            headers: headers,
          )
          .timeout(timeout);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return ScanResult.fromJson(data);
      } else if (response.statusCode == 404) {
        throw Exception('Código no encontrado');
      } else {
        throw Exception('Error al escanear: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Crear movimiento rápido
  Future<Map<String, dynamic>> crearMovimientoRapido({
    required String codigoProducto,
    required String tipoMovimiento,
    required int cantidad,
    String? referencia,
    String? usuarioMovil,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/scanner/movimiento-rapido'),
            headers: headers,
            body: json.encode({
              'codigo_producto': codigoProducto,
              'tipo_movimiento': tipoMovimiento,
              'cantidad': cantidad,
              'referencia': referencia,
              'usuario_movil': usuarioMovil ?? 'Usuario Móvil',
            }),
          )
          .timeout(timeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al crear movimiento: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Obtener historial de movimientos
  Future<List<Movimiento>> obtenerHistorial(String codigoProducto, {int limite = 10}) async {
    try {
      final response = await http
          .get(
            Uri.parse('$baseUrl/scanner/historial-movimientos/$codigoProducto?limite=$limite'),
            headers: headers,
          )
          .timeout(timeout);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> movimientosJson = data['movimientos'];
        return movimientosJson.map((json) => Movimiento.fromJson(json)).toList();
      } else {
        throw Exception('Error al obtener historial: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Iniciar inventario físico
  Future<Map<String, dynamic>> iniciarInventarioFisico({String? ubicacion}) async {
    try {
      final url = ubicacion != null
          ? '$baseUrl/scanner/inventario-fisico?ubicacion=$ubicacion'
          : '$baseUrl/scanner/inventario-fisico';

      final response = await http
          .post(Uri.parse(url), headers: headers)
          .timeout(timeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al iniciar inventario: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Registrar conteo físico
  Future<Map<String, dynamic>> registrarConteo({
    required String codigo,
    required int cantidadFisica,
    required String sesionId,
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/scanner/inventario-fisico/registrar-conteo'),
            headers: headers,
            body: json.encode({
              'codigo': codigo,
              'cantidad_fisica': cantidadFisica,
              'sesion_id': sesionId,
            }),
          )
          .timeout(timeout);

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al registrar conteo: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Health check
  Future<bool> checkConnection() async {
    try {
      final response = await http
          .get(Uri.parse('${baseUrl.replaceAll('/api', '')}/health'))
          .timeout(const Duration(seconds: 5));
      
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
