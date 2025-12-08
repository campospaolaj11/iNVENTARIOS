class Producto {
  final String codigo;
  final String nombre;
  final int stockActual;
  final int stockMinimo;
  final String ubicacionBodega;
  final String categoria;
  final double precioVenta;
  final String? fotoUrl;

  Producto({
    required this.codigo,
    required this.nombre,
    required this.stockActual,
    required this.stockMinimo,
    required this.ubicacionBodega,
    required this.categoria,
    required this.precioVenta,
    this.fotoUrl,
  });

  factory Producto.fromJson(Map<String, dynamic> json) {
    return Producto(
      codigo: json['codigo'] ?? '',
      nombre: json['nombre'] ?? '',
      stockActual: json['stock_actual'] ?? 0,
      stockMinimo: json['stock_minimo'] ?? 0,
      ubicacionBodega: json['ubicacion_bodega'] ?? '',
      categoria: json['categoria'] ?? '',
      precioVenta: (json['precio_venta'] ?? 0.0).toDouble(),
      fotoUrl: json['foto_url'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'codigo': codigo,
      'nombre': nombre,
      'stock_actual': stockActual,
      'stock_minimo': stockMinimo,
      'ubicacion_bodega': ubicacionBodega,
      'categoria': categoria,
      'precio_venta': precioVenta,
      'foto_url': fotoUrl,
    };
  }

  bool get stockCritico => stockActual <= stockMinimo;
  
  double get valorInventario => stockActual * precioVenta;
}
