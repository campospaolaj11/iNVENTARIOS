class Movimiento {
  final int id;
  final String tipo;
  final int cantidad;
  final String fecha;
  final String usuario;
  final String? referencia;

  Movimiento({
    required this.id,
    required this.tipo,
    required this.cantidad,
    required this.fecha,
    required this.usuario,
    this.referencia,
  });

  factory Movimiento.fromJson(Map<String, dynamic> json) {
    return Movimiento(
      id: json['id'] ?? 0,
      tipo: json['tipo'] ?? '',
      cantidad: json['cantidad'] ?? 0,
      fecha: json['fecha'] ?? '',
      usuario: json['usuario'] ?? '',
      referencia: json['referencia'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'tipo': tipo,
      'cantidad': cantidad,
      'fecha': fecha,
      'usuario': usuario,
      'referencia': referencia,
    };
  }

  bool get esEntrada => tipo == 'ENTRADA';
  bool get esSalida => tipo == 'SALIDA';
}
