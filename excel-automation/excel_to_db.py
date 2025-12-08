import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

class ExcelToDatabase:
    def __init__(self):
        self.connection_string = (
            f"DRIVER={{{os.getenv('DATABASE_DRIVER')}}};"
            f"SERVER={os.getenv('DATABASE_SERVER')};"
            f"DATABASE={os.getenv('DATABASE_NAME')};"
            f"UID={os.getenv('DATABASE_USER')};"
            f"PWD={os.getenv('DATABASE_PASSWORD')}"
        )
    
    def connect(self):
        """Conectar a SQL Server"""
        try:
            conn = pyodbc.connect(self.connection_string)
            print("✅ Conexión exitosa a SQL Server")
            return conn
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None
    
    def leer_excel(self, archivo_path):
        """Leer archivo Excel con pandas"""
        try:
            df = pd.read_excel(archivo_path)
            print(f"✅ Archivo leído: {len(df)} filas")
            return df
        except Exception as e:
            print(f"❌ Error al leer Excel: {e}")
            return None
    
    def importar_productos(self, df, conn):
        """Importar productos desde DataFrame a SQL Server"""
        cursor = conn.cursor()
        contador = 0
        
        for index, row in df.iterrows():
            try:
                # Verificar si el producto ya existe
                cursor.execute(
                    "SELECT id FROM productos WHERE codigo = ?",
                    row['codigo']
                )
                existe = cursor.fetchone()
                
                if existe:
                    # Actualizar producto existente
                    cursor.execute("""
                        UPDATE productos 
                        SET nombre = ?, 
                            stock_actual = ?,
                            costo_unitario = ?,
                            precio_venta = ?,
                            fecha_actualizacion = GETDATE()
                        WHERE codigo = ?
                    """, 
                    row['nombre'], 
                    row['stock_actual'], 
                    row['costo_unitario'],
                    row['precio_venta'],
                    row['codigo'])
                    
                    print(f"📝 Actualizado: {row['codigo']}")
                else:
                    # Insertar nuevo producto
                    cursor.execute("""
                        INSERT INTO productos 
                        (codigo, nombre, categoria, stock_actual, stock_minimo, 
                         costo_unitario, precio_venta, ubicacion_bodega)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    row['codigo'],
                    row['nombre'],
                    row.get('categoria', 'General'),
                    row['stock_actual'],
                    row.get('stock_minimo', 10),
                    row['costo_unitario'],
                    row['precio_venta'],
                    row.get('ubicacion', 'A-00'))
                    
                    print(f"✅ Insertado: {row['codigo']}")
                
                contador += 1
                
            except Exception as e:
                print(f"❌ Error en fila {index}: {e}")
        
        conn.commit()
        print(f"\n✅ Proceso completado: {contador} productos procesados")
        return contador
    
    def exportar_kpis_a_excel(self, archivo_salida):
        """Exportar KPIs de la base de datos a Excel"""
        conn = self.connect()
        if not conn:
            return
        
        try:
            # Obtener KPIs
            query_kpis = "SELECT TOP 1 * FROM kpis ORDER BY fecha_calculo DESC"
            df_kpis = pd.read_sql(query_kpis, conn)
            
            # Obtener productos críticos
            query_criticos = "SELECT * FROM vw_productos_criticos"
            df_criticos = pd.read_sql(query_criticos, conn)
            
            # Obtener valor por categoría
            query_valor = "SELECT * FROM vw_valor_inventario"
            df_valor = pd.read_sql(query_valor, conn)
            
            # Crear Excel con múltiples hojas
            with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
                df_kpis.to_excel(writer, sheet_name='KPIs', index=False)
                df_criticos.to_excel(writer, sheet_name='Stock Crítico', index=False)
                df_valor.to_excel(writer, sheet_name='Valor por Categoría', index=False)
            
            print(f"✅ KPIs exportados a: {archivo_salida}")
            
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
        finally:
            conn.close()

# Ejemplo de uso
if __name__ == "__main__":
    etl = ExcelToDatabase()
    
    # Ejemplo: Importar desde Excel
    # df = etl.leer_excel("inventario.xlsx")
    # if df is not None:
    #     conn = etl.connect()
    #     if conn:
    #         etl.importar_productos(df, conn)
    #         conn.close()
    
    # Ejemplo: Exportar KPIs
    # etl.exportar_kpis_a_excel("kpis_inventario.xlsx")
    
    print("🚀 Script de automatización listo")
