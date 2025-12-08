import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/inventory_provider.dart';
import '../models/producto.dart';

class ProductDetailScreen extends StatefulWidget {
  const ProductDetailScreen({super.key});

  @override
  State<ProductDetailScreen> createState() => _ProductDetailScreenState();
}

class _ProductDetailScreenState extends State<ProductDetailScreen> {
  String _tipoMovimiento = 'ENTRADA';
  int _cantidad = 1;

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<InventoryProvider>(context);
    final producto = provider.selectedProduct;

    if (producto == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Producto')),
        body: const Center(
          child: Text('No hay producto seleccionado'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalle del Producto'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history),
            onPressed: () {
              provider.obtenerHistorial(producto.codigo);
              Navigator.pushNamed(context, '/history');
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header con imagen (placeholder)
            Container(
              height: 200,
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    const Color(0xff0284c7),
                    const Color(0xff0284c7).withOpacity(0.8),
                  ],
                ),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    producto.stockCritico ? Icons.warning : Icons.inventory_2,
                    size: 80,
                    color: Colors.white,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    producto.nombre,
                    style: const TextStyle(
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      producto.codigo,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Tarjetas de información
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Row(
                    children: [
                      Expanded(
                        child: _buildInfoCard(
                          title: 'Stock Actual',
                          value: '${producto.stockActual}',
                          icon: Icons.inventory,
                          color: producto.stockCritico ? Colors.red : Colors.blue,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildInfoCard(
                          title: 'Stock Mínimo',
                          value: '${producto.stockMinimo}',
                          icon: Icons.show_chart,
                          color: Colors.orange,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: _buildInfoCard(
                          title: 'Precio Venta',
                          value: '\$${producto.precioVenta.toStringAsFixed(2)}',
                          icon: Icons.attach_money,
                          color: Colors.green,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: _buildInfoCard(
                          title: 'Valor Total',
                          value: '\$${producto.valorInventario.toStringAsFixed(2)}',
                          icon: Icons.account_balance_wallet,
                          color: Colors.purple,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  _buildInfoCard(
                    title: 'Ubicación',
                    value: producto.ubicacionBodega,
                    icon: Icons.location_on,
                    color: Colors.indigo,
                  ),

                  // Alerta de stock crítico
                  if (producto.stockCritico) ...[
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.red.shade50,
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.red.shade200),
                      ),
                      child: Row(
                        children: [
                          Icon(Icons.warning, color: Colors.red.shade700),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              '⚠️ Stock crítico: Cantidad por debajo del mínimo',
                              style: TextStyle(
                                color: Colors.red.shade700,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],

                  const SizedBox(height: 24),
                  const Divider(),
                  const SizedBox(height: 16),

                  // Movimiento rápido
                  const Text(
                    'Movimiento Rápido',
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Botones de tipo de movimiento
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () {
                            setState(() {
                              _tipoMovimiento = 'ENTRADA';
                            });
                          },
                          icon: const Icon(Icons.add_box),
                          label: const Text('Entrada'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: _tipoMovimiento == 'ENTRADA'
                                ? Colors.green
                                : Colors.grey.shade300,
                            foregroundColor: _tipoMovimiento == 'ENTRADA'
                                ? Colors.white
                                : Colors.grey.shade700,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () {
                            setState(() {
                              _tipoMovimiento = 'SALIDA';
                            });
                          },
                          icon: const Icon(Icons.remove_circle),
                          label: const Text('Salida'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: _tipoMovimiento == 'SALIDA'
                                ? Colors.red
                                : Colors.grey.shade300,
                            foregroundColor: _tipoMovimiento == 'SALIDA'
                                ? Colors.white
                                : Colors.grey.shade700,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                          ),
                        ),
                      ),
                    ],
                  ),

                  const SizedBox(height: 16),

                  // Input de cantidad
                  TextField(
                    keyboardType: TextInputType.number,
                    decoration: const InputDecoration(
                      labelText: 'Cantidad',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.numbers),
                    ),
                    onChanged: (value) {
                      setState(() {
                        _cantidad = int.tryParse(value) ?? 1;
                      });
                    },
                  ),

                  const SizedBox(height: 16),

                  // Botón confirmar
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: provider.isLoading ? null : _confirmarMovimiento,
                      icon: provider.isLoading
                          ? const SizedBox(
                              width: 20,
                              height: 20,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(Icons.check_circle),
                      label: Text(
                        provider.isLoading ? 'Procesando...' : 'Confirmar Movimiento',
                      ),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xff0284c7),
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                        textStyle: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 8),
              Text(
                title,
                style: TextStyle(
                  fontSize: 12,
                  color: Colors.grey.shade600,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _confirmarMovimiento() async {
    if (_cantidad <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('La cantidad debe ser mayor a 0'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    final provider = context.read<InventoryProvider>();
    final producto = provider.selectedProduct;

    if (producto == null) return;

    final exito = await provider.crearMovimientoRapido(
      codigoProducto: producto.codigo,
      tipoMovimiento: _tipoMovimiento,
      cantidad: _cantidad,
    );

    if (mounted) {
      if (exito) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              '✅ Movimiento registrado: $_tipoMovimiento de $_cantidad unidades',
            ),
            backgroundColor: Colors.green,
          ),
        );
        Navigator.pop(context);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(provider.errorMessage ?? 'Error al registrar movimiento'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
}
