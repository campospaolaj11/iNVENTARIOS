"""
Script de automatización programada para actualizar inventarios
Puede ejecutarse con Task Scheduler de Windows o manualmente
"""

import pandas as pd
import json
from datetime import datetime
import os

class AutomationInventario:
    def __init__(self):
        self.ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.ruta_base, "automation_log.txt")
    
    def log(self, mensaje):
        """Registrar mensaje en log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {mensaje}"
        print(log_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def actualizar_desde_csv(self, csv_file="entrada_datos.csv"):
        """
        Actualizar inventario desde archivo CSV
        (Simula datos exportados de máquinas o sistemas externos)
        """
        try:
            self.log(f"📥 Leyendo archivo CSV: {csv_file}")
            
            # Leer CSV
            df = pd.read_csv(csv_file)
            self.log(f"✅ Leídos {len(df)} registros")
            
            # Validar columnas requeridas
            columnas_requeridas = ['codigo', 'nombre', 'stock_actual']
            for col in columnas_requeridas:
                if col not in df.columns:
                    raise ValueError(f"Falta columna requerida: {col}")
            
            # Convertir a JSON
            productos = df.to_dict('records')
            json_file = os.path.join(self.ruta_base, "productos_actualizados.json")
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(productos, f, indent=2, ensure_ascii=False)
            
            self.log(f"✅ JSON generado: {json_file}")
            return True
            
        except FileNotFoundError:
            self.log(f"❌ Archivo no encontrado: {csv_file}")
            return False
        except Exception as e:
            self.log(f"❌ Error: {str(e)}")
            return False
    
    def calcular_kpis_automatico(self, excel_file="inventario_completo.xlsx"):
        """Calcular KPIs automáticamente desde Excel"""
        try:
            self.log("📊 Calculando KPIs...")
            
            df = pd.read_excel(excel_file, sheet_name='Inventario')
            
            kpis = {
                'fecha_calculo': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'total_productos': len(df),
                'productos_criticos': len(df[df['stock_actual'] <= df['stock_minimo']]),
                'valor_inventario': float(df['valor_stock'].sum()),
                'stock_total': int(df['stock_actual'].sum())
            }
            
            # Guardar KPIs
            kpis_file = os.path.join(self.ruta_base, "kpis_calculados.json")
            with open(kpis_file, 'w', encoding='utf-8') as f:
                json.dump(kpis, f, indent=2)
            
            self.log(f"✅ KPIs calculados y guardados")
            self.log(f"   📦 Total productos: {kpis['total_productos']}")
            self.log(f"   ⚠️  Críticos: {kpis['productos_criticos']}")
            self.log(f"   💰 Valor: ${kpis['valor_inventario']:,.2f}")
            
            return kpis
            
        except Exception as e:
            self.log(f"❌ Error al calcular KPIs: {str(e)}")
            return None
    
    def generar_reporte_diario(self):
        """Generar reporte diario en Excel"""
        try:
            fecha = datetime.now().strftime("%Y-%m-%d")
            self.log(f"📄 Generando reporte diario: {fecha}")
            
            # Leer datos actuales
            df = pd.read_excel("inventario_completo.xlsx", sheet_name='Inventario')
            
            # Crear reporte
            reporte_file = f"reporte_diario_{fecha}.xlsx"
            
            with pd.ExcelWriter(reporte_file, engine='openpyxl') as writer:
                # Productos críticos
                df_criticos = df[df['estado'] == 'CRÍTICO']
                df_criticos.to_excel(writer, sheet_name='Alertas Críticas', index=False)
                
                # Productos a reabastecer
                df_reabastecer = df[df['pedido_sugerido'] > 0]
                df_reabastecer.to_excel(writer, sheet_name='Pedidos Sugeridos', index=False)
                
                # Movimientos del día (simulado)
                movimientos = pd.DataFrame({
                    'Hora': [datetime.now().strftime("%H:%M")],
                    'Tipo': ['ACTUALIZACIÓN'],
                    'Registros': [len(df)],
                    'Usuario': ['Sistema Automático']
                })
                movimientos.to_excel(writer, sheet_name='Movimientos', index=False)
            
            self.log(f"✅ Reporte generado: {reporte_file}")
            return reporte_file
            
        except Exception as e:
            self.log(f"❌ Error al generar reporte: {str(e)}")
            return None
    
    def ejecutar_automatizacion_completa(self):
        """Ejecutar toda la secuencia de automatización"""
        self.log("="*60)
        self.log("🚀 INICIANDO AUTOMATIZACIÓN COMPLETA")
        self.log("="*60)
        
        # 1. Calcular KPIs
        kpis = self.calcular_kpis_automatico()
        
        # 2. Generar reporte
        reporte = self.generar_reporte_diario()
        
        # 3. Resumen final
        self.log("="*60)
        self.log("✅ AUTOMATIZACIÓN COMPLETADA")
        self.log("="*60)
        
        return {
            'exito': True,
            'kpis': kpis,
            'reporte': reporte
        }

def crear_csv_ejemplo():
    """Crear CSV de ejemplo para pruebas"""
    datos_ejemplo = {
        'codigo': ['PROD001', 'PROD002', 'PROD003'],
        'nombre': ['Producto A', 'Producto B', 'Producto C'],
        'stock_actual': [100, 50, 200],
        'stock_minimo': [20, 30, 40],
        'costo_unitario': [10.50, 25.00, 15.00],
        'precio_venta': [15.00, 35.00, 22.00],
        'categoria': ['Categoría A', 'Categoría B', 'Categoría A'],
        'ubicacion': ['A-01', 'B-02', 'A-03']
    }
    
    df = pd.DataFrame(datos_ejemplo)
    df.to_csv('entrada_datos.csv', index=False)
    print("✅ CSV de ejemplo creado: entrada_datos.csv")

if __name__ == "__main__":
    print("🤖 Sistema de Automatización de Inventarios\n")
    
    # Crear instancia
    automation = AutomationInventario()
    
    # Ejecutar automatización
    resultado = automation.ejecutar_automatizacion_completa()
    
    print("\n" + "="*60)
    print("📋 RESUMEN DE EJECUCIÓN")
    print("="*60)
    print(f"Estado: {'✅ EXITOSO' if resultado['exito'] else '❌ ERROR'}")
    print(f"Log: automation_log.txt")
    print(f"\nPara ver el log completo ejecuta:")
    print(f"  type automation_log.txt")
