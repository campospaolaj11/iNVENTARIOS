"""
Endpoints para funcionalidad de scanner móvil
"""

from fastapi import APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import Optional, List
import sys
import os

# Agregar directorio utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.qr_generator import QRGenerator

router = APIRouter(prefix="/api/scanner", tags=["Scanner Móvil"])


class ScanResult(BaseModel):
    """Resultado de escaneo"""
    codigo: str
    tipo: str  # 'producto' o 'ubicacion'
    data: dict


class MovimientoRapido(BaseModel):
    """Movimiento rápido desde móvil"""
    codigo_producto: str
    tipo_movimiento: str  # ENTRADA o SALIDA
    cantidad: int
    referencia: Optional[str] = None
    usuario_movil: str


@router.post("/escanear")
async def procesar_escaneo(codigo: str):
    """
    Procesa el código escaneado y retorna información del producto o ubicación
    
    Args:
        codigo: Código de barras o QR escaneado
    
    Returns:
        Información del producto o ubicación
    """
    
    # Detectar tipo de código
    if codigo.startswith("PROD"):
        # Es un código de producto
        # TODO: Buscar en base de datos real
        producto = {
            'codigo': codigo,
            'nombre': 'Producto Ejemplo',
            'stock_actual': 150,
            'stock_minimo': 50,
            'ubicacion_bodega': 'A-01',
            'categoria': 'Ferretería',
            'precio_venta': 15.00,
            'foto_url': None
        }
        
        return {
            'tipo': 'producto',
            'encontrado': True,
            'data': producto,
            'acciones_disponibles': [
                {'id': 'agregar', 'label': '➕ Agregar Stock', 'color': 'green'},
                {'id': 'remover', 'label': '➖ Remover Stock', 'color': 'red'},
                {'id': 'ver_historial', 'label': '📊 Ver Historial', 'color': 'blue'},
                {'id': 'editar', 'label': '✏️ Editar Producto', 'color': 'orange'}
            ]
        }
    
    elif codigo.count('-') == 1:
        # Parece una ubicación (ej: A-01)
        # TODO: Buscar productos en esa ubicación
        productos_en_ubicacion = [
            {'codigo': 'PROD001', 'nombre': 'Tornillo M8x20', 'stock': 150},
            {'codigo': 'PROD002', 'nombre': 'Tuerca M8', 'stock': 200}
        ]
        
        return {
            'tipo': 'ubicacion',
            'encontrado': True,
            'data': {
                'ubicacion': codigo,
                'productos': productos_en_ubicacion,
                'total_productos': len(productos_en_ubicacion)
            },
            'acciones_disponibles': [
                {'id': 'ver_productos', 'label': '📦 Ver Productos', 'color': 'blue'},
                {'id': 'mover_productos', 'label': '🔄 Mover Productos', 'color': 'orange'},
                {'id': 'inventario_fisico', 'label': '✅ Inventario Físico', 'color': 'green'}
            ]
        }
    
    else:
        # Código no reconocido
        raise HTTPException(
            status_code=404,
            detail={
                'mensaje': 'Código no encontrado',
                'codigo': codigo,
                'sugerencia': 'Verifica que el código sea correcto o regístralo como nuevo producto'
            }
        )


@router.post("/movimiento-rapido")
async def crear_movimiento_rapido(movimiento: MovimientoRapido):
    """
    Crea un movimiento de inventario desde la app móvil
    
    Args:
        movimiento: Datos del movimiento
    
    Returns:
        Confirmación del movimiento
    """
    
    # TODO: Validar que el producto existe
    # TODO: Insertar en base de datos
    # TODO: Actualizar stock
    
    return {
        'exito': True,
        'mensaje': f'✅ Movimiento registrado: {movimiento.tipo_movimiento} de {movimiento.cantidad} unidades',
        'movimiento_id': 12345,
        'producto_codigo': movimiento.codigo_producto,
        'nuevo_stock': 175,  # TODO: Calcular stock real
        'fecha': '2025-12-08T15:30:00',
        'usuario': movimiento.usuario_movil
    }


@router.get("/generar-qrs/productos")
async def generar_qrs_productos():
    """
    Genera códigos QR para todos los productos
    
    Returns:
        Lista de QRs generados
    """
    
    # TODO: Obtener productos de la base de datos
    productos = [
        {'codigo': 'PROD001', 'nombre': 'Tornillo M8x20'},
        {'codigo': 'PROD002', 'nombre': 'Tuerca M8'},
        {'codigo': 'PROD003', 'nombre': 'Arandela M8'},
        {'codigo': 'PROD004', 'nombre': 'Cable 2x14 AWG'},
        {'codigo': 'PROD005', 'nombre': 'Interruptor Simple'}
    ]
    
    generator = QRGenerator()
    resultado = generator.generar_qrs_masivos_productos(productos)
    
    return {
        'mensaje': '✅ QRs de productos generados',
        'total': resultado['total_productos'],
        'exitosos': resultado['generados_exitosos'],
        'errores': resultado['errores'],
        'directorio': resultado['directorio'],
        'archivos': resultado['archivos']
    }


@router.get("/generar-qrs/ubicaciones")
async def generar_qrs_ubicaciones():
    """
    Genera códigos QR para todas las ubicaciones de bodega
    
    Returns:
        Lista de QRs generados
    """
    
    ubicaciones = [
        'A-01', 'A-02', 'A-03', 'A-04', 'A-05',
        'B-01', 'B-02', 'B-03', 'B-04', 'B-05',
        'C-01', 'C-02', 'C-03', 'C-04', 'C-05',
        'D-01', 'D-02', 'E-01', 'E-02'
    ]
    
    generator = QRGenerator()
    resultado = generator.generar_qrs_masivos_ubicaciones(ubicaciones)
    
    # Generar hoja A4 para impresión
    qr_files = [a['archivo'] for a in resultado['archivos'] if a['status'] == 'success']
    hoja_a4 = None
    
    if qr_files:
        hoja_a4 = generator.generar_hoja_impresion_a4(qr_files[:12])
    
    return {
        'mensaje': '✅ QRs de ubicaciones generados',
        'total': resultado['total_ubicaciones'],
        'exitosos': resultado['generados_exitosos'],
        'errores': resultado['errores'],
        'directorio': resultado['directorio'],
        'hoja_impresion_a4': hoja_a4,
        'instrucciones': [
            '1. Descarga la hoja A4',
            '2. Imprime en papel adhesivo o papel normal',
            '3. Recorta los QRs',
            '4. Pega cada QR en su ubicación',
            '5. Escanea con la app móvil para verificar'
        ],
        'archivos': resultado['archivos']
    }


@router.post("/inventario-fisico")
async def iniciar_inventario_fisico(ubicacion: Optional[str] = None):
    """
    Inicia proceso de inventario físico (conteo manual)
    
    Args:
        ubicacion: Ubicación específica (opcional)
    
    Returns:
        Lista de productos a contar
    """
    
    # TODO: Obtener productos de la ubicación
    productos_a_contar = [
        {
            'codigo': 'PROD001',
            'nombre': 'Tornillo M8x20',
            'stock_sistema': 150,
            'stock_fisico': None,  # Se llenará con el conteo
            'ubicacion': 'A-01'
        },
        {
            'codigo': 'PROD002',
            'nombre': 'Tuerca M8',
            'stock_sistema': 200,
            'stock_fisico': None,
            'ubicacion': 'A-02'
        }
    ]
    
    return {
        'sesion_id': 'INV-2025-001',
        'fecha_inicio': '2025-12-08T15:30:00',
        'ubicacion': ubicacion or 'TODAS',
        'productos': productos_a_contar,
        'total_productos': len(productos_a_contar),
        'instrucciones': [
            '1. Escanea el QR del producto',
            '2. Cuenta físicamente las unidades',
            '3. Ingresa la cantidad contada',
            '4. El sistema calculará diferencias automáticamente'
        ]
    }


@router.post("/inventario-fisico/registrar-conteo")
async def registrar_conteo(codigo: str, cantidad_fisica: int, sesion_id: str):
    """
    Registra el conteo físico de un producto
    
    Args:
        codigo: Código del producto
        cantidad_fisica: Cantidad contada físicamente
        sesion_id: ID de la sesión de inventario
    
    Returns:
        Diferencia calculada
    """
    
    # TODO: Obtener stock del sistema
    stock_sistema = 150
    diferencia = cantidad_fisica - stock_sistema
    
    # TODO: Guardar en base de datos
    
    return {
        'producto_codigo': codigo,
        'stock_sistema': stock_sistema,
        'stock_fisico': cantidad_fisica,
        'diferencia': diferencia,
        'ajuste_necesario': abs(diferencia) > 0,
        'tipo_ajuste': 'ENTRADA' if diferencia > 0 else 'SALIDA' if diferencia < 0 else 'NINGUNO',
        'mensaje': f"{'✅ Sin diferencias' if diferencia == 0 else f'⚠️ Diferencia de {abs(diferencia)} unidades'}"
    }


@router.get("/historial-movimientos/{codigo_producto}")
async def obtener_historial_movimientos(codigo_producto: str, limite: int = 10):
    """
    Obtiene historial de movimientos de un producto para mostrar en móvil
    
    Args:
        codigo_producto: Código del producto
        limite: Cantidad de movimientos a retornar
    
    Returns:
        Historial de movimientos
    """
    
    # TODO: Obtener de base de datos
    movimientos = [
        {
            'id': 1,
            'tipo': 'ENTRADA',
            'cantidad': 100,
            'fecha': '2025-12-01T09:00:00',
            'usuario': 'Juan Pérez',
            'referencia': 'PO-2025-001'
        },
        {
            'id': 2,
            'tipo': 'SALIDA',
            'cantidad': 50,
            'fecha': '2025-12-03T14:30:00',
            'usuario': 'María García',
            'referencia': 'SO-2025-001'
        }
    ]
    
    return {
        'producto_codigo': codigo_producto,
        'total_movimientos': len(movimientos),
        'movimientos': movimientos,
        'stock_actual': 150,
        'ultimo_movimiento': movimientos[0] if movimientos else None
    }
