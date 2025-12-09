# Configuración de Twilio WhatsApp

## 1. Crear cuenta de Twilio
- Registrarse en: https://www.twilio.com/try-twilio
- Verificar correo electrónico
- Completar onboarding

## 2. Configurar WhatsApp Sandbox
1. Ir a: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. Seguir instrucciones para conectar tu WhatsApp personal
3. Enviar mensaje desde tu WhatsApp al número de Twilio (ejemplo: "join <código>")

## 3. Obtener credenciales
En el Dashboard de Twilio:
- Account SID: ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
- Auth Token: tu_auth_token_secreto

## 4. Configurar variables de entorno
Crear/actualizar archivo `backend/.env`:

```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=tu_auth_token_secreto
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

# Números de teléfono para alertas (formato: +521234567890)
ADMIN_WHATSAPP=whatsapp:+5219999999999
MANAGER_WHATSAPP=whatsapp:+5218888888888
```

## 5. Probar integración
```bash
# Desde el directorio del backend
curl -X GET "http://localhost:8000/api/notificaciones/test-whatsapp?telefono=whatsapp:+5219999999999"
```

## 6. Uso en producción
Para producción (enviar a cualquier número sin sandbox):
1. Actualizar cuenta de Twilio a plan de pago
2. Solicitar número de WhatsApp Business
3. Configurar plantillas de mensajes aprobadas
4. Actualizar `TWILIO_WHATSAPP_FROM` con tu número business

## Endpoints disponibles:

### POST /api/notificaciones/whatsapp/stock-critico
```json
{
  "telefono_destino": "whatsapp:+5219999999999",
  "codigo_producto": "PROD-001",
  "nombre_producto": "Laptop Dell XPS",
  "stock_actual": 2,
  "stock_minimo": 5
}
```

### POST /api/notificaciones/whatsapp/movimiento-importante
```json
{
  "telefono_destino": "whatsapp:+5219999999999",
  "tipo_movimiento": "SALIDA",
  "codigo_producto": "PROD-001",
  "nombre_producto": "Laptop Dell XPS",
  "cantidad": 50,
  "usuario": "Juan Pérez"
}
```

### POST /api/notificaciones/whatsapp/reporte-diario
```json
{
  "telefono_destino": "whatsapp:+5219999999999",
  "total_entradas": 150,
  "total_salidas": 120,
  "productos_criticos": 3,
  "fecha": "09/12/2025"
}
```

### POST /api/notificaciones/whatsapp/alerta-personalizada
```json
{
  "telefono_destino": "whatsapp:+5219999999999",
  "titulo": "Alerta de Sistema",
  "mensaje": "El servidor se reiniciará en 5 minutos"
}
```

## Notas importantes:
- En modo sandbox, solo puedes enviar a números que hayan enviado "join <código>"
- Los mensajes tienen límite de 1600 caracteres
- Rate limits: 1 mensaje/segundo en sandbox, más en producción
- Costo aproximado: $0.005 USD por mensaje en producción
