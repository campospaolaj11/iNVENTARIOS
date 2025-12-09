import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:provider/provider.dart';
import '../providers/inventory_provider.dart';
import '../services/sound_service.dart';
import '../services/offline_service.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  MobileScannerController cameraController = MobileScannerController(
    detectionSpeed: DetectionSpeed.normal,
    facing: CameraFacing.back,
    torchEnabled: false,
  );

  bool _isProcessing = false;
  final OfflineService _offlineService = OfflineService();

  @override
  void dispose() {
    cameraController.dispose();
    super.dispose();
  }

  void _onDetect(BarcodeCapture capture) async {
    if (_isProcessing) return;

    final List<Barcode> barcodes = capture.barcodes;
    
    if (barcodes.isEmpty) return;

    final String? code = barcodes.first.rawValue;

    if (code == null) return;

    setState(() {
      _isProcessing = true;
    });

    // Vibración
    // HapticFeedback.vibrate();

    // Escanear código
    final provider = context.read<InventoryProvider>();
    
    try {
      await provider.escanearCodigo(code);

      if (mounted) {
        if (provider.errorMessage != null) {
          // Sonido de error
          await SoundService.playError();
          
          // Guardar en offline para intentar después
          await _offlineService.guardarEscaneo(code, DateTime.now());
          
          // Mostrar error
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('${provider.errorMessage}\n(Guardado offline)'),
              backgroundColor: Colors.orange,
              duration: const Duration(seconds: 3),
            ),
          );
          setState(() {
            _isProcessing = false;
          });
        } else {
          // Sonido de éxito
          await SoundService.playSuccess();
          
          // Cachear producto
          if (provider.selectedProduct != null) {
            await _offlineService.cachearProducto(provider.selectedProduct!);
          }
          
          // Navegar a detalles
          Navigator.pushNamed(context, '/product-detail').then((_) {
            setState(() {
              _isProcessing = false;
            });
          });
        }
      }
    } catch (e) {
      // Error de conexión - modo offline
      await SoundService.playWarning();
      
      // Guardar escaneo offline
      await _offlineService.guardarEscaneo(code, DateTime.now());
      
      // Buscar en caché
      final cachedProduct = await _offlineService.buscarProductoEnCache(code);
      
      if (mounted) {
        if (cachedProduct != null) {
          provider.setSelectedProduct(cachedProduct);
          
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Modo Offline: Producto desde caché'),
              backgroundColor: Colors.blue,
            ),
          );
          
          Navigator.pushNamed(context, '/product-detail').then((_) {
            setState(() {
              _isProcessing = false;
            });
          });
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text('Sin conexión. Escaneo guardado para sincronizar.'),
              backgroundColor: Colors.orange,
            ),
          );
          setState(() {
            _isProcessing = false;
          });
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Escanear Código'),
        actions: [
          IconButton(
            icon: ValueListenableBuilder(
              valueListenable: cameraController.torchState,
              builder: (context, state, child) {
                return Icon(
                  state == TorchState.off ? Icons.flash_off : Icons.flash_on,
                );
              },
            ),
            onPressed: () => cameraController.toggleTorch(),
          ),
          IconButton(
            icon: const Icon(Icons.flip_camera_ios),
            onPressed: () => cameraController.switchCamera(),
          ),
        ],
      ),
      body: Stack(
        children: [
          // Cámara
          MobileScanner(
            controller: cameraController,
            onDetect: _onDetect,
          ),

          // Overlay con marco
          CustomPaint(
            painter: ScannerOverlayPainter(),
            child: Container(),
          ),

          // Instrucciones
          Positioned(
            bottom: 100,
            left: 0,
            right: 0,
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 40),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(12),
              ),
              child: const Column(
                children: [
                  Icon(
                    Icons.qr_code_scanner,
                    color: Colors.white,
                    size: 40,
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Apunta la cámara al código QR o de barras',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
          ),

          // Loading overlay
          if (_isProcessing)
            Container(
              color: Colors.black.withOpacity(0.5),
              child: const Center(
                child: CircularProgressIndicator(
                  color: Colors.white,
                ),
              ),
            ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // Entrada manual
          _showManualInputDialog();
        },
        child: const Icon(Icons.keyboard),
      ),
    );
  }

  void _showManualInputDialog() {
    final TextEditingController controller = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Entrada Manual'),
        content: TextField(
          controller: controller,
          decoration: const InputDecoration(
            labelText: 'Código del producto',
            hintText: 'PROD001',
            border: OutlineInputBorder(),
          ),
          autofocus: true,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () async {
              final code = controller.text.trim();
              if (code.isNotEmpty) {
                Navigator.pop(context);
                
                setState(() {
                  _isProcessing = true;
                });

                final provider = context.read<InventoryProvider>();
                await provider.escanearCodigo(code);

                if (mounted) {
                  if (provider.errorMessage != null) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(provider.errorMessage!),
                        backgroundColor: Colors.red,
                      ),
                    );
                    setState(() {
                      _isProcessing = false;
                    });
                  } else {
                    Navigator.pushNamed(context, '/product-detail').then((_) {
                      setState(() {
                        _isProcessing = false;
                      });
                    });
                  }
                }
              }
            },
            child: const Text('Buscar'),
          ),
        ],
      ),
    );
  }
}

class ScannerOverlayPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final double scanAreaSize = size.width * 0.7;
    final double left = (size.width - scanAreaSize) / 2;
    final double top = (size.height - scanAreaSize) / 2;

    // Dibujar overlay oscuro
    final backgroundPaint = Paint()
      ..color = Colors.black.withOpacity(0.5)
      ..style = PaintingStyle.fill;

    canvas.drawPath(
      Path()
        ..addRect(Rect.fromLTWH(0, 0, size.width, size.height))
        ..addRect(Rect.fromLTWH(left, top, scanAreaSize, scanAreaSize))
        ..fillType = PathFillType.evenOdd,
      backgroundPaint,
    );

    // Dibujar esquinas del marco
    final cornerPaint = Paint()
      ..color = const Color(0xff0284c7)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 4
      ..strokeCap = StrokeCap.round;

    const cornerLength = 30.0;

    // Esquina superior izquierda
    canvas.drawLine(Offset(left, top), Offset(left + cornerLength, top), cornerPaint);
    canvas.drawLine(Offset(left, top), Offset(left, top + cornerLength), cornerPaint);

    // Esquina superior derecha
    canvas.drawLine(
      Offset(left + scanAreaSize, top),
      Offset(left + scanAreaSize - cornerLength, top),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(left + scanAreaSize, top),
      Offset(left + scanAreaSize, top + cornerLength),
      cornerPaint,
    );

    // Esquina inferior izquierda
    canvas.drawLine(
      Offset(left, top + scanAreaSize),
      Offset(left + cornerLength, top + scanAreaSize),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(left, top + scanAreaSize),
      Offset(left, top + scanAreaSize - cornerLength),
      cornerPaint,
    );

    // Esquina inferior derecha
    canvas.drawLine(
      Offset(left + scanAreaSize, top + scanAreaSize),
      Offset(left + scanAreaSize - cornerLength, top + scanAreaSize),
      cornerPaint,
    );
    canvas.drawLine(
      Offset(left + scanAreaSize, top + scanAreaSize),
      Offset(left + scanAreaSize, top + scanAreaSize - cornerLength),
      cornerPaint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
