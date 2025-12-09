"""
Endpoints para notificaciones y alertas
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from ..services.whatsapp_service import WhatsAppService
from datetime import datetime

router = APIRouter(prefix="/api/notificaciones", tags=["Notificaciones"])

# Modelos de request
class AlertaStockCritico(BaseModel):
    telefono_destino: str
    codigo_producto: str
    nombre_producto: str
    stock_actual: int
    stock_minimo: int

class AlertaMovimiento(BaseModel):
    telefono_destino: str
    tipo_movimiento: str
    codigo_producto: str
    nombre_producto: str
    cantidad: int
    usuario: str = "Sistema"

class ReporteDiario(BaseModel):
    telefono_destino: str
    total_entradas: int
    total_salidas: int
    productos_criticos: int
    fecha: Optional[str] = None

class AlertaPersonalizada(BaseModel):
    telefono_destino: str
    titulo: str
    mensaje: str

class ConfiguracionNotificaciones(BaseModel):
    telefono_admin: str
    activar_stock_critico: bool = True
    activar_movimientos_importantes: bool = False
    activar_reportes_diarios: bool = True
    umbral_movimiento_importante: int = 100  # Cantidad mínima para notificar

# Instancia del servicio
whatsapp_service = WhatsAppService()

@router.post("/whatsapp/stock-critico")
async def enviar_alerta_stock_critico(alerta: AlertaStockCritico):
    """
    Envía una alerta de stock crítico por WhatsApp
    """
    try:
        sid = whatsapp_service.enviar_alerta_stock_critico(
            telefono_destino=alerta.telefono_destino,
            codigo_producto=alerta.codigo_producto,
            nombre_producto=alerta.nombre_producto,
            stock_actual=alerta.stock_actual,
            stock_minimo=alerta.stock_minimo
        )
        
        if sid:
            return {
                "success": True,
                "message": "Alerta enviada exitosamente",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Error al enviar la alerta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/movimiento-importante")
async def enviar_alerta_movimiento(alerta: AlertaMovimiento):
    """
    Envía una alerta de movimiento importante por WhatsApp
    """
    try:
        sid = whatsapp_service.enviar_alerta_movimiento_importante(
            telefono_destino=alerta.telefono_destino,
            tipo_movimiento=alerta.tipo_movimiento,
            codigo_producto=alerta.codigo_producto,
            nombre_producto=alerta.nombre_producto,
            cantidad=alerta.cantidad,
            usuario=alerta.usuario
        )
        
        if sid:
            return {
                "success": True,
                "message": "Alerta enviada exitosamente",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Error al enviar la alerta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/reporte-diario")
async def enviar_reporte_diario(reporte: ReporteDiario):
    """
    Envía un reporte diario por WhatsApp
    """
    try:
        fecha = reporte.fecha or datetime.now().strftime("%d/%m/%Y")
        
        sid = whatsapp_service.enviar_reporte_diario(
            telefono_destino=reporte.telefono_destino,
            total_entradas=reporte.total_entradas,
            total_salidas=reporte.total_salidas,
            productos_criticos=reporte.productos_criticos,
            fecha=fecha
        )
        
        if sid:
            return {
                "success": True,
                "message": "Reporte enviado exitosamente",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Error al enviar el reporte")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/whatsapp/alerta-personalizada")
async def enviar_alerta_personalizada(alerta: AlertaPersonalizada):
    """
    Envía una alerta personalizada por WhatsApp
    """
    try:
        sid = whatsapp_service.enviar_alerta_personalizada(
            telefono_destino=alerta.telefono_destino,
            titulo=alerta.titulo,
            mensaje=alerta.mensaje
        )
        
        if sid:
            return {
                "success": True,
                "message": "Alerta enviada exitosamente",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Error al enviar la alerta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-whatsapp")
async def test_whatsapp(telefono: str):
    """
    Endpoint de prueba para verificar la configuración de WhatsApp
    """
    try:
        sid = whatsapp_service.enviar_alerta_personalizada(
            telefono_destino=telefono,
            titulo="🧪 Prueba de Conexión",
            mensaje="Si recibiste este mensaje, la integración con WhatsApp está funcionando correctamente."
        )
        
        if sid:
            return {
                "success": True,
                "message": "Mensaje de prueba enviado exitosamente",
                "sid": sid
            }
        else:
            raise HTTPException(status_code=500, detail="Error al enviar mensaje de prueba")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
