import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/inventory_provider.dart';
import 'package:intl/intl.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<InventoryProvider>(context);
    final movimientos = provider.movimientos;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Historial de Movimientos'),
      ),
      body: provider.isLoading
          ? const Center(child: CircularProgressIndicator())
          : movimientos.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.history,
                        size: 80,
                        color: Colors.grey.shade400,
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No hay movimientos registrados',
                        style: TextStyle(
                          fontSize: 16,
                          color: Colors.grey.shade600,
                        ),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: movimientos.length,
                  itemBuilder: (context, index) {
                    final movimiento = movimientos[index];
                    final isEntrada = movimiento.esEntrada;

                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      child: ListTile(
                        leading: Container(
                          width: 50,
                          height: 50,
                          decoration: BoxDecoration(
                            color: isEntrada
                                ? Colors.green.withOpacity(0.1)
                                : Colors.red.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: Icon(
                            isEntrada ? Icons.add_box : Icons.remove_circle,
                            color: isEntrada ? Colors.green : Colors.red,
                          ),
                        ),
                        title: Text(
                          movimiento.tipo,
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            color: isEntrada ? Colors.green : Colors.red,
                          ),
                        ),
                        subtitle: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text('Cantidad: ${movimiento.cantidad}'),
                            Text('Usuario: ${movimiento.usuario}'),
                            if (movimiento.referencia != null)
                              Text('Ref: ${movimiento.referencia}'),
                          ],
                        ),
                        trailing: Text(
                          _formatDate(movimiento.fecha),
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey.shade600,
                          ),
                        ),
                      ),
                    );
                  },
                ),
    );
  }

  String _formatDate(String fecha) {
    try {
      final date = DateTime.parse(fecha);
      return DateFormat('dd/MM HH:mm').format(date);
    } catch (e) {
      return fecha;
    }
  }
}
