"""
Generador de códigos QR para productos y ubicaciones de bodega
"""

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

class QRGenerator:
    """Genera códigos QR profesionales para inventario"""
    
    def __init__(self, output_dir="static/qr_codes"):
        self.output_dir = output_dir
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
    
    def generar_qr_producto(self, codigo_producto: str, nombre: str, base_url: str = "https://sistemas-inventario.netlify.app"):
        """
        Genera QR para un producto específico
        
        Args:
            codigo_producto: Código único del producto (ej: PROD001)
            nombre: Nombre del producto
            base_url: URL base del dashboard
        
        Returns:
            str: Ruta del archivo QR generado
        """
        
        # URL que abrirá el dashboard con filtro del producto
        data = f"{base_url}/producto/{codigo_producto}"
        
        # Crear QR con alta resolución
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta corrección de errores
            box_size=15,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Generar imagen QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a PIL Image para agregar texto
        img = img.convert('RGB')
        
        # Agregar espacio para texto
        new_height = img.height + 100
        new_img = Image.new('RGB', (img.width, new_height), 'white')
        new_img.paste(img, (0, 0))
        
        # Agregar texto con información
        draw = ImageDraw.Draw(new_img)
        
        try:
            # Intentar usar fuente del sistema
            font_title = ImageFont.truetype("arial.ttf", 24)
            font_code = ImageFont.truetype("arial.ttf", 18)
        except:
            # Usar fuente por defecto si no encuentra arial
            font_title = ImageFont.load_default()
            font_code = ImageFont.load_default()
        
        # Centrar texto
        text_y = img.height + 10
        
        # Título
        title_bbox = draw.textbbox((0, 0), nombre, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (img.width - title_width) // 2
        draw.text((title_x, text_y), nombre, fill='black', font=font_title)
        
        # Código
        code_text = f"Código: {codigo_producto}"
        code_bbox = draw.textbbox((0, 0), code_text, font=font_code)
        code_width = code_bbox[2] - code_bbox[0]
        code_x = (img.width - code_width) // 2
        draw.text((code_x, text_y + 35), code_text, fill='gray', font=font_code)
        
        # Instrucciones
        instructions = "Escanea con tu móvil"
        inst_bbox = draw.textbbox((0, 0), instructions, font=font_code)
        inst_width = inst_bbox[2] - inst_bbox[0]
        inst_x = (img.width - inst_width) // 2
        draw.text((inst_x, text_y + 65), instructions, fill='blue', font=font_code)
        
        # Guardar imagen
        filename = f"producto_{codigo_producto}.png"
        filepath = os.path.join(self.output_dir, filename)
        new_img.save(filepath)
        
        return filepath
    
    def generar_qr_ubicacion(self, ubicacion: str, base_url: str = "https://sistemas-inventario.netlify.app"):
        """
        Genera QR para una ubicación de bodega
        
        Args:
            ubicacion: Código de ubicación (ej: A-01, B-02)
            base_url: URL base del dashboard
        
        Returns:
            str: Ruta del archivo QR generado
        """
        
        # URL con filtro de ubicación
        data = f"{base_url}/ubicacion/{ubicacion}"
        
        # Crear QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=15,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Generar imagen
        img = qr.make_image(fill_color="#0284c7", back_color="white")  # Color azul corporativo
        img = img.convert('RGB')
        
        # Agregar espacio para texto
        new_height = img.height + 120
        new_img = Image.new('RGB', (img.width, new_height), 'white')
        new_img.paste(img, (0, 0))
        
        # Agregar texto
        draw = ImageDraw.Draw(new_img)
        
        try:
            font_title = ImageFont.truetype("arial.ttf", 32)
            font_subtitle = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
        
        text_y = img.height + 10
        
        # Ubicación en grande
        title_text = f"📍 {ubicacion}"
        title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (img.width - title_width) // 2
        draw.text((title_x, text_y), title_text, fill='#0284c7', font=font_title)
        
        # Subtítulo
        subtitle = "Ubicación de Bodega"
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (img.width - sub_width) // 2
        draw.text((sub_x, text_y + 45), subtitle, fill='black', font=font_subtitle)
        
        # Instrucciones
        inst_text = "Escanea para ver productos"
        inst_bbox = draw.textbbox((0, 0), inst_text, font=font_subtitle)
        inst_width = inst_bbox[2] - inst_bbox[0]
        inst_x = (img.width - inst_width) // 2
        draw.text((inst_x, text_y + 80), inst_text, fill='gray', font=font_subtitle)
        
        # Guardar
        filename = f"ubicacion_{ubicacion.replace('-', '_')}.png"
        filepath = os.path.join(self.output_dir, filename)
        new_img.save(filepath)
        
        return filepath
    
    def generar_qrs_masivos_productos(self, productos: list, base_url: str = "https://sistemas-inventario.netlify.app"):
        """
        Genera QRs para múltiples productos
        
        Args:
            productos: Lista de diccionarios con 'codigo' y 'nombre'
            base_url: URL base del dashboard
        
        Returns:
            dict: Resumen de QRs generados
        """
        archivos_generados = []
        
        for producto in productos:
            try:
                filepath = self.generar_qr_producto(
                    codigo_producto=producto['codigo'],
                    nombre=producto['nombre'],
                    base_url=base_url
                )
                archivos_generados.append({
                    'codigo': producto['codigo'],
                    'archivo': filepath,
                    'status': 'success'
                })
            except Exception as e:
                archivos_generados.append({
                    'codigo': producto['codigo'],
                    'error': str(e),
                    'status': 'error'
                })
        
        return {
            'total_productos': len(productos),
            'generados_exitosos': len([a for a in archivos_generados if a['status'] == 'success']),
            'errores': len([a for a in archivos_generados if a['status'] == 'error']),
            'archivos': archivos_generados,
            'directorio': self.output_dir
        }
    
    def generar_qrs_masivos_ubicaciones(self, ubicaciones: list, base_url: str = "https://sistemas-inventario.netlify.app"):
        """
        Genera QRs para múltiples ubicaciones de bodega
        
        Args:
            ubicaciones: Lista de códigos de ubicación ['A-01', 'A-02', ...]
            base_url: URL base del dashboard
        
        Returns:
            dict: Resumen de QRs generados
        """
        archivos_generados = []
        
        for ubicacion in ubicaciones:
            try:
                filepath = self.generar_qr_ubicacion(
                    ubicacion=ubicacion,
                    base_url=base_url
                )
                archivos_generados.append({
                    'ubicacion': ubicacion,
                    'archivo': filepath,
                    'status': 'success'
                })
            except Exception as e:
                archivos_generados.append({
                    'ubicacion': ubicacion,
                    'error': str(e),
                    'status': 'error'
                })
        
        return {
            'total_ubicaciones': len(ubicaciones),
            'generados_exitosos': len([a for a in archivos_generados if a['status'] == 'success']),
            'errores': len([a for a in archivos_generados if a['status'] == 'error']),
            'archivos': archivos_generados,
            'directorio': self.output_dir,
            'instrucciones': '📋 Imprime los QRs y pega en las ubicaciones correspondientes'
        }
    
    def generar_hoja_impresion_a4(self, qr_paths: list, output_filename: str = "hoja_qrs_impresion.png"):
        """
        Genera una hoja A4 con múltiples QRs listos para imprimir
        
        Args:
            qr_paths: Lista de rutas a archivos QR
            output_filename: Nombre del archivo de salida
        
        Returns:
            str: Ruta del archivo generado
        """
        # Tamaño A4 en píxeles (300 DPI)
        a4_width = 2480
        a4_height = 3508
        
        # Crear hoja en blanco
        hoja = Image.new('RGB', (a4_width, a4_height), 'white')
        
        # Configuración de grid (3x4 = 12 QRs por hoja)
        qrs_por_fila = 3
        qrs_por_columna = 4
        margen = 100
        espacio_entre_qrs = 50
        
        # Calcular tamaño de cada QR
        qr_width = (a4_width - 2 * margen - (qrs_por_fila - 1) * espacio_entre_qrs) // qrs_por_fila
        qr_height = (a4_height - 2 * margen - (qrs_por_columna - 1) * espacio_entre_qrs) // qrs_por_columna
        
        # Pegar QRs en grid
        for idx, qr_path in enumerate(qr_paths[:12]):  # Máximo 12 por hoja
            if not os.path.exists(qr_path):
                continue
            
            # Calcular posición
            fila = idx // qrs_por_fila
            columna = idx % qrs_por_fila
            
            x = margen + columna * (qr_width + espacio_entre_qrs)
            y = margen + fila * (qr_height + espacio_entre_qrs)
            
            # Cargar y redimensionar QR
            qr_img = Image.open(qr_path)
            qr_img = qr_img.resize((qr_width, qr_height), Image.Resampling.LANCZOS)
            
            # Pegar en hoja
            hoja.paste(qr_img, (x, y))
        
        # Agregar título en la parte superior
        draw = ImageDraw.Draw(hoja)
        try:
            font_title = ImageFont.truetype("arial.ttf", 40)
        except:
            font_title = ImageFont.load_default()
        
        titulo = "CÓDIGOS QR - SISTEMA DE INVENTARIOS"
        fecha = f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        
        draw.text((margen, 30), titulo, fill='#0284c7', font=font_title)
        draw.text((margen, 80), fecha, fill='gray', font=font_title)
        
        # Guardar hoja
        output_path = os.path.join(self.output_dir, output_filename)
        hoja.save(output_path, quality=95, dpi=(300, 300))
        
        return output_path


# Funciones auxiliares para uso rápido
def generar_qrs_bodega_completa():
    """Genera QRs para toda la bodega (productos + ubicaciones)"""
    
    generator = QRGenerator()
    
    # Ubicaciones de ejemplo
    ubicaciones = [
        'A-01', 'A-02', 'A-03', 'A-04', 'A-05',
        'B-01', 'B-02', 'B-03', 'B-04', 'B-05',
        'C-01', 'C-02', 'C-03', 'C-04', 'C-05',
        'D-01', 'D-02', 'E-01', 'E-02'
    ]
    
    # Generar QRs de ubicaciones
    resultado_ubicaciones = generator.generar_qrs_masivos_ubicaciones(ubicaciones)
    
    print(f"✅ {resultado_ubicaciones['generados_exitosos']} QRs de ubicaciones generados")
    print(f"📁 Archivos en: {resultado_ubicaciones['directorio']}")
    
    # Generar hoja de impresión A4
    qr_files = [a['archivo'] for a in resultado_ubicaciones['archivos'] if a['status'] == 'success']
    
    if qr_files:
        hoja_a4 = generator.generar_hoja_impresion_a4(qr_files[:12])
        print(f"📄 Hoja de impresión A4 generada: {hoja_a4}")
        print("\n🖨️  Pasos siguientes:")
        print("   1. Abre el archivo con el visor de imágenes")
        print("   2. Imprime en papel A4")
        print("   3. Recorta los QRs")
        print("   4. Pega cada QR en su ubicación correspondiente")
    
    return resultado_ubicaciones


if __name__ == "__main__":
    print("🚀 Generador de QR Codes - Sistema de Inventarios\n")
    
    # Generar QRs para toda la bodega
    resultado = generar_qrs_bodega_completa()
    
    print(f"\n✅ Proceso completado!")
    print(f"📊 Total generados: {resultado['generados_exitosos']}")
