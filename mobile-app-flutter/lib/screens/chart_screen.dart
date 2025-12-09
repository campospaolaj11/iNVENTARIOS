import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';
import '../models/movimiento.dart';

class ChartScreen extends StatefulWidget {
  const ChartScreen({super.key});

  @override
  State<ChartScreen> createState() => _ChartScreenState();
}

class _ChartScreenState extends State<ChartScreen> {
  final ApiService _apiService = ApiService();
  List<Movimiento> _movimientos = [];
  bool _isLoading = true;
  String _selectedPeriod = 'day'; // day, week, month
  
  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  Future<void> _cargarDatos() async {
    setState(() => _isLoading = true);
    
    try {
      // Aquí podrías filtrar por fecha según el período seleccionado
      final movimientos = await _apiService.obtenerHistorial();
      
      setState(() {
        _movimientos = movimientos;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error al cargar datos: $e')),
        );
      }
    }
  }

  Map<String, int> _obtenerMovimientosPorTipo() {
    int entradas = 0;
    int salidas = 0;
    
    for (var mov in _movimientos) {
      if (mov.tipoMovimiento == 'ENTRADA') {
        entradas += mov.cantidad;
      } else if (mov.tipoMovimiento == 'SALIDA') {
        salidas += mov.cantidad;
      }
    }
    
    return {'ENTRADA': entradas, 'SALIDA': salidas};
  }

  Map<DateTime, int> _obtenerMovimientosPorDia() {
    final Map<DateTime, int> movimientosPorDia = {};
    
    for (var mov in _movimientos) {
      final fecha = DateTime(
        mov.fechaMovimiento.year,
        mov.fechaMovimiento.month,
        mov.fechaMovimiento.day,
      );
      
      movimientosPorDia[fecha] = (movimientosPorDia[fecha] ?? 0) + mov.cantidad;
    }
    
    return movimientosPorDia;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Estadísticas'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _cargarDatos,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Selector de período
                  _buildPeriodSelector(),
                  const SizedBox(height: 24),
                  
                  // Tarjetas de resumen
                  _buildSummaryCards(),
                  const SizedBox(height: 24),
                  
                  // Gráfico circular (Entradas vs Salidas)
                  _buildPieChartSection(),
                  const SizedBox(height: 32),
                  
                  // Gráfico de líneas (Movimientos por día)
                  _buildLineChartSection(),
                  const SizedBox(height: 32),
                  
                  // Gráfico de barras (Top productos)
                  _buildBarChartSection(),
                ],
              ),
            ),
    );
  }

  Widget _buildPeriodSelector() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(8),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _buildPeriodButton('Hoy', 'day'),
            _buildPeriodButton('Semana', 'week'),
            _buildPeriodButton('Mes', 'month'),
          ],
        ),
      ),
    );
  }

  Widget _buildPeriodButton(String label, String period) {
    final isSelected = _selectedPeriod == period;
    
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 4),
        child: ElevatedButton(
          onPressed: () {
            setState(() => _selectedPeriod = period);
            _cargarDatos();
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: isSelected
                ? Theme.of(context).colorScheme.primary
                : Theme.of(context).colorScheme.surfaceContainerHighest,
            foregroundColor: isSelected
                ? Theme.of(context).colorScheme.onPrimary
                : Theme.of(context).colorScheme.onSurface,
          ),
          child: Text(label),
        ),
      ),
    );
  }

  Widget _buildSummaryCards() {
    final datos = _obtenerMovimientosPorTipo();
    final total = datos['ENTRADA']! + datos['SALIDA']!;
    
    return Row(
      children: [
        Expanded(
          child: Card(
            color: Colors.green.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Icon(Icons.arrow_upward, color: Colors.green.shade700, size: 32),
                  const SizedBox(height: 8),
                  Text(
                    '${datos['ENTRADA']}',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: Colors.green.shade700,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'Entradas',
                    style: TextStyle(color: Colors.green.shade700),
                  ),
                ],
              ),
            ),
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Card(
            color: Colors.red.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Icon(Icons.arrow_downward, color: Colors.red.shade700, size: 32),
                  const SizedBox(height: 8),
                  Text(
                    '${datos['SALIDA']}',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                      color: Colors.red.shade700,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    'Salidas',
                    style: TextStyle(color: Colors.red.shade700),
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildPieChartSection() {
    final datos = _obtenerMovimientosPorTipo();
    final total = datos['ENTRADA']! + datos['SALIDA']!;
    
    if (total == 0) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(32),
          child: Center(
            child: Text('No hay movimientos para mostrar'),
          ),
        ),
      );
    }
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Distribución de Movimientos',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(
                      value: datos['ENTRADA']!.toDouble(),
                      title: '${((datos['ENTRADA']! / total) * 100).toStringAsFixed(1)}%',
                      color: Colors.green,
                      radius: 80,
                      titleStyle: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    PieChartSectionData(
                      value: datos['SALIDA']!.toDouble(),
                      title: '${((datos['SALIDA']! / total) * 100).toStringAsFixed(1)}%',
                      color: Colors.red,
                      radius: 80,
                      titleStyle: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                  sectionsSpace: 2,
                  centerSpaceRadius: 40,
                ),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildLegendItem('Entradas', Colors.green),
                _buildLegendItem('Salidas', Colors.red),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLegendItem(String label, Color color) {
    return Row(
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(width: 8),
        Text(label),
      ],
    );
  }

  Widget _buildLineChartSection() {
    final movimientosPorDia = _obtenerMovimientosPorDia();
    
    if (movimientosPorDia.isEmpty) {
      return const SizedBox.shrink();
    }
    
    final fechas = movimientosPorDia.keys.toList()..sort();
    final spots = <FlSpot>[];
    
    for (int i = 0; i < fechas.length; i++) {
      spots.add(FlSpot(i.toDouble(), movimientosPorDia[fechas[i]]!.toDouble()));
    }
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Movimientos por Día',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 200,
              child: LineChart(
                LineChartData(
                  gridData: FlGridData(show: true),
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true, reservedSize: 40),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 30,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() >= 0 && value.toInt() < fechas.length) {
                            final fecha = fechas[value.toInt()];
                            return Text(
                              DateFormat('dd/MM').format(fecha),
                              style: const TextStyle(fontSize: 10),
                            );
                          }
                          return const Text('');
                        },
                      ),
                    ),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  borderData: FlBorderData(show: true),
                  lineBarsData: [
                    LineChartBarData(
                      spots: spots,
                      isCurved: true,
                      color: Theme.of(context).colorScheme.primary,
                      barWidth: 3,
                      dotData: FlDotData(show: true),
                      belowBarData: BarAreaData(
                        show: true,
                        color: Theme.of(context).colorScheme.primary.withOpacity(0.3),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildBarChartSection() {
    // Agrupar movimientos por producto
    final Map<String, int> movimientosPorProducto = {};
    
    for (var mov in _movimientos) {
      movimientosPorProducto[mov.codigoProducto] = 
          (movimientosPorProducto[mov.codigoProducto] ?? 0) + mov.cantidad;
    }
    
    // Ordenar y tomar top 5
    final topProductos = movimientosPorProducto.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    final top5 = topProductos.take(5).toList();
    
    if (top5.isEmpty) {
      return const SizedBox.shrink();
    }
    
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Top 5 Productos Más Movidos',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 200,
              child: BarChart(
                BarChartData(
                  alignment: BarChartAlignment.spaceAround,
                  maxY: top5.first.value.toDouble() * 1.2,
                  barTouchData: BarTouchData(enabled: true),
                  titlesData: FlTitlesData(
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(showTitles: true, reservedSize: 40),
                    ),
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() >= 0 && value.toInt() < top5.length) {
                            return Text(
                              top5[value.toInt()].key,
                              style: const TextStyle(fontSize: 10),
                            );
                          }
                          return const Text('');
                        },
                      ),
                    ),
                    topTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                    rightTitles: AxisTitles(sideTitles: SideTitles(showTitles: false)),
                  ),
                  borderData: FlBorderData(show: false),
                  barGroups: List.generate(
                    top5.length,
                    (index) => BarChartGroupData(
                      x: index,
                      barRods: [
                        BarChartRodData(
                          toY: top5[index].value.toDouble(),
                          color: Theme.of(context).colorScheme.primary,
                          width: 20,
                          borderRadius: BorderRadius.circular(4),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
