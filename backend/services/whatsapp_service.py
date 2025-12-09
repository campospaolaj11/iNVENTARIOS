"""
Servicio de notificaciones por WhatsApp usando Twilio
"""
from twilio.rest import Client
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("Faltan credenciales de Twilio. Configura TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN en .env")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def enviar_alerta_stock_critico(
        self,
        telefono_destino: str,
        codigo_producto: str,
        nombre_producto: str,
        stock_actual: int,
        stock_minimo: int
    ) -> Optional[str]:
        """
        Envía alerta de stock crítico por WhatsApp
        
        Args:
            telefono_destino: Número de teléfono en formato +521234567890
            codigo_producto: Código del producto
            nombre_producto: Nombre del producto
            stock_actual: Stock actual del producto
            stock_minimo: Stock mínimo configurado
            
        Returns:
            SID del mensaje si fue exitoso, None si falló
        """
        try:
            mensaje = f"""
🚨 *ALERTA DE STOCK CRÍTICO*

📦 *Producto:* {nombre_producto}
🔢 *Código:* {codigo_producto}
📊 *Stock Actual:* {stock_actual} unidades
⚠️ *Stock Mínimo:* {stock_minimo} unidades

*Acción requerida:* Reabastecer inventario urgentemente.
            """.strip()
            
            if not telefono_destino.startswith('whatsapp:'):
                telefono_destino = f'whatsapp:{telefono_destino}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                body=mensaje,
                to=telefono_destino
            )
            
            return message.sid
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return None
    
    def enviar_alerta_movimiento_importante(
        self,
        telefono_destino: str,
        tipo_movimiento: str,
        codigo_producto: str,
        nombre_producto: str,
        cantidad: int,
        usuario: str
    ) -> Optional[str]:
        """
        Envía alerta de movimiento importante por WhatsApp
        
        Args:
            telefono_destino: Número de teléfono en formato +521234567890
            tipo_movimiento: ENTRADA o SALIDA
            codigo_producto: Código del producto
            nombre_producto: Nombre del producto
            cantidad: Cantidad del movimiento
            usuario: Usuario que realizó el movimiento
            
        Returns:
            SID del mensaje si fue exitoso, None si falló
        """
        try:
            emoji = "📥" if tipo_movimiento == "ENTRADA" else "📤"
            
            mensaje = f"""
{emoji} *MOVIMIENTO IMPORTANTE DE INVENTARIO*

*Tipo:* {tipo_movimiento}
📦 *Producto:* {nombre_producto}
🔢 *Código:* {codigo_producto}
📊 *Cantidad:* {cantidad} unidades
👤 *Usuario:* {usuario}

✅ Movimiento registrado exitosamente.
            """.strip()
            
            if not telefono_destino.startswith('whatsapp:'):
                telefono_destino = f'whatsapp:{telefono_destino}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                body=mensaje,
                to=telefono_destino
            )
            
            return message.sid
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return None
    
    def enviar_reporte_diario(
        self,
        telefono_destino: str,
        total_entradas: int,
        total_salidas: int,
        productos_criticos: int,
        fecha: str
    ) -> Optional[str]:
        """
        Envía reporte diario por WhatsApp
        
        Args:
            telefono_destino: Número de teléfono en formato +521234567890
            total_entradas: Total de entradas del día
            total_salidas: Total de salidas del día
            productos_criticos: Productos con stock crítico
            fecha: Fecha del reporte
            
        Returns:
            SID del mensaje si fue exitoso, None si falló
        """
        try:
            mensaje = f"""
📊 *REPORTE DIARIO DE INVENTARIO*
📅 *Fecha:* {fecha}

📥 *Entradas:* {total_entradas} movimientos
📤 *Salidas:* {total_salidas} movimientos
⚠️ *Productos Críticos:* {productos_criticos}

🔄 Balance: {'+' if total_entradas > total_salidas else ''}{total_entradas - total_salidas}

✅ Sistema de Inventarios Automatizado
            """.strip()
            
            if not telefono_destino.startswith('whatsapp:'):
                telefono_destino = f'whatsapp:{telefono_destino}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                body=mensaje,
                to=telefono_destino
            )
            
            return message.sid
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return None
    
    def enviar_alerta_personalizada(
        self,
        telefono_destino: str,
        titulo: str,
        mensaje: str
    ) -> Optional[str]:
        """
        Envía una alerta personalizada por WhatsApp
        
        Args:
            telefono_destino: Número de teléfono en formato +521234567890
            titulo: Título del mensaje
            mensaje: Cuerpo del mensaje
            
        Returns:
            SID del mensaje si fue exitoso, None si falló
        """
        try:
            mensaje_completo = f"""
*{titulo}*

{mensaje}

✅ Sistema de Inventarios
            """.strip()
            
            if not telefono_destino.startswith('whatsapp:'):
                telefono_destino = f'whatsapp:{telefono_destino}'
            
            message = self.client.messages.create(
                from_=self.whatsapp_from,
                body=mensaje_completo,
                to=telefono_destino
            )
            
            return message.sid
        except Exception as e:
            print(f"Error enviando WhatsApp: {e}")
            return None
