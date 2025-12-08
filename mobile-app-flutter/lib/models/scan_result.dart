import 'producto.dart';

class ScanResult {
  final String tipo;
  final bool encontrado;
  final dynamic data;
  final List<AccionDisponible>? accionesDisponibles;

  ScanResult({
    required this.tipo,
    required this.encontrado,
    required this.data,
    this.accionesDisponibles,
  });

  factory ScanResult.fromJson(Map<String, dynamic> json) {
    return ScanResult(
      tipo: json['tipo'] ?? '',
      encontrado: json['encontrado'] ?? false,
      data: json['data'],
      accionesDisponibles: json['acciones_disponibles'] != null
          ? (json['acciones_disponibles'] as List)
              .map((a) => AccionDisponible.fromJson(a))
              .toList()
          : null,
    );
  }

  bool get esProducto => tipo == 'producto';
  bool get esUbicacion => tipo == 'ubicacion';

  Producto? get producto {
    if (esProducto && data != null) {
      return Producto.fromJson(data as Map<String, dynamic>);
    }
    return null;
  }
}

class AccionDisponible {
  final String id;
  final String label;
  final String color;

  AccionDisponible({
    required this.id,
    required this.label,
    required this.color,
  });

  factory AccionDisponible.fromJson(Map<String, dynamic> json) {
    return AccionDisponible(
      id: json['id'] ?? '',
      label: json['label'] ?? '',
      color: json['color'] ?? 'blue',
    );
  }
}
