import 'package:flutter/services.dart';

class SoundService {
  static const MethodChannel _channel = MethodChannel('inventario_scanner/sound');

  /// Reproducir sonido de éxito (escaneo exitoso)
  static Future<void> playSuccess() async {
    try {
      await _channel.invokeMethod('playSuccess');
    } on PlatformException catch (e) {
      print("Error reproduciendo sonido: ${e.message}");
    }
  }

  /// Reproducir sonido de error
  static Future<void> playError() async {
    try {
      await _channel.invokeMethod('playError');
    } on PlatformException catch (e) {
      print("Error reproduciendo sonido: ${e.message}");
    }
  }

  /// Reproducir sonido de alerta
  static Future<void> playWarning() async {
    try {
      await _channel.invokeMethod('playWarning');
    } on PlatformException catch (e) {
      print("Error reproduciendo sonido: ${e.message}");
    }
  }
}
