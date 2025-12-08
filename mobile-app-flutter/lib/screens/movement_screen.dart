import 'package:flutter/material.dart';

class MovementScreen extends StatelessWidget {
  const MovementScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final args = ModalRoute.of(context)?.settings.arguments as Map<String, dynamic>?;
    final tipo = args?['tipo'] ?? 'ENTRADA';

    return Scaffold(
      appBar: AppBar(
        title: Text('Movimiento - $tipo'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              tipo == 'ENTRADA' ? Icons.add_box : Icons.remove_circle,
              size: 80,
              color: tipo == 'ENTRADA' ? Colors.green : Colors.red,
            ),
            const SizedBox(height: 20),
            Text(
              'Pantalla de $tipo',
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () {
                Navigator.pushNamed(context, '/scanner');
              },
              icon: const Icon(Icons.qr_code_scanner),
              label: const Text('Escanear Producto'),
            ),
          ],
        ),
      ),
    );
  }
}
