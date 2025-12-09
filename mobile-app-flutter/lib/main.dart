import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'screens/home_screen.dart';
import 'screens/scanner_screen.dart';
import 'screens/product_detail_screen.dart';
import 'screens/movement_screen.dart';
import 'screens/history_screen.dart';
import 'screens/chart_screen.dart';
import 'providers/inventory_provider.dart';
import 'services/api_service.dart';
import 'services/sync_service.dart';

void main() {
  runApp(const InventarioApp());
}

class InventarioApp extends StatelessWidget {
  const InventarioApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => InventoryProvider(ApiService()),
        ),
        ChangeNotifierProvider(
          create: (_) => SyncService(),
        ),
      ],
      child: MaterialApp(
        title: 'Inventario Scanner',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xff0284c7),
            brightness: Brightness.light,
          ),
          useMaterial3: true,
          appBarTheme: const AppBarTheme(
            centerTitle: true,
            elevation: 0,
            backgroundColor: Color(0xff0284c7),
            foregroundColor: Colors.white,
          ),
          floatingActionButtonTheme: const FloatingActionButtonThemeData(
            backgroundColor: Color(0xff0284c7),
            foregroundColor: Colors.white,
          ),
          cardTheme: const CardThemeData(
            elevation: 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(16)),
            ),
          ),
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const HomeScreen(),
          '/scanner': (context) => const ScannerScreen(),
          '/product-detail': (context) => const ProductDetailScreen(),
          '/movement': (context) => const MovementScreen(),
          '/history': (context) => const HistoryScreen(),
          '/charts': (context) => const ChartScreen(),
        },
      ),
    );
  }
}
