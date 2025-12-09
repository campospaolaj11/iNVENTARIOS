"""
Middleware de Seguridad y Rate Limiting
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar requests por IP
    Previene ataques de fuerza bruta y DDoS
    """
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.blocked_ips: Dict[str, datetime] = {}
    
    async def dispatch(self, request: Request, call_next):
        # Obtener IP del cliente
        client_ip = request.client.host
        
        # Verificar si la IP está bloqueada
        if client_ip in self.blocked_ips:
            tiempo_bloqueo = self.blocked_ips[client_ip]
            if datetime.now() < tiempo_bloqueo:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "detail": "IP bloqueada temporalmente por exceso de peticiones",
                        "retry_after": (tiempo_bloqueo - datetime.now()).seconds
                    }
                )
            else:
                # Desbloquear IP
                del self.blocked_ips[client_ip]
        
        # Obtener timestamp actual
        now = time.time()
        minute_ago = now - 60
        
        # Limpiar requests antiguos
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if req_time > minute_ago
        ]
        
        # Verificar límite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            # Bloquear IP por 15 minutos
            self.blocked_ips[client_ip] = datetime.now() + timedelta(minutes=15)
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Límite de {self.requests_per_minute} requests por minuto excedido",
                    "retry_after": 900  # 15 minutos
                }
            )
        
        # Registrar request
        self.requests[client_ip].append(now)
        
        # Continuar con la petición
        response = await call_next(request)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para agregar headers de seguridad
    """
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Headers de seguridad recomendados
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response


class LoginAttemptTracker:
    """
    Rastrea intentos de login fallidos
    Bloquea cuentas después de múltiples intentos
    """
    
    def __init__(self):
        self.intentos: Dict[str, list] = defaultdict(list)
        self.cuentas_bloqueadas: Dict[str, datetime] = {}
        self.max_intentos = 5
        self.tiempo_bloqueo_minutos = 30
    
    def registrar_intento_fallido(self, username: str) -> Tuple[bool, int, int]:
        """
        Registra un intento fallido de login
        Retorna (esta_bloqueado, intentos_restantes, minutos_bloqueo)
        """
        # Verificar si ya está bloqueado
        if username in self.cuentas_bloqueadas:
            tiempo_desbloqueo = self.cuentas_bloqueadas[username]
            if datetime.now() < tiempo_desbloqueo:
                minutos_restantes = int((tiempo_desbloqueo - datetime.now()).seconds / 60)
                return True, 0, minutos_restantes
            else:
                # Desbloquear cuenta
                del self.cuentas_bloqueadas[username]
                self.intentos[username] = []
        
        # Registrar intento
        now = datetime.now()
        self.intentos[username].append(now)
        
        # Limpiar intentos antiguos (mayores a 1 hora)
        hora_atras = now - timedelta(hours=1)
        self.intentos[username] = [
            intento for intento in self.intentos[username]
            if intento > hora_atras
        ]
        
        # Verificar si se alcanzó el límite
        intentos_recientes = len(self.intentos[username])
        if intentos_recientes >= self.max_intentos:
            # Bloquear cuenta
            tiempo_bloqueo = now + timedelta(minutes=self.tiempo_bloqueo_minutos)
            self.cuentas_bloqueadas[username] = tiempo_bloqueo
            return True, 0, self.tiempo_bloqueo_minutos
        
        intentos_restantes = self.max_intentos - intentos_recientes
        return False, intentos_restantes, 0
    
    def registrar_intento_exitoso(self, username: str):
        """Limpia intentos fallidos después de login exitoso"""
        if username in self.intentos:
            del self.intentos[username]
        if username in self.cuentas_bloqueadas:
            del self.cuentas_bloqueadas[username]
    
    def esta_bloqueado(self, username: str) -> Tuple[bool, int]:
        """
        Verifica si una cuenta está bloqueada
        Retorna (esta_bloqueado, minutos_restantes)
        """
        if username in self.cuentas_bloqueadas:
            tiempo_desbloqueo = self.cuentas_bloqueadas[username]
            if datetime.now() < tiempo_desbloqueo:
                minutos_restantes = int((tiempo_desbloqueo - datetime.now()).seconds / 60)
                return True, minutos_restantes
            else:
                del self.cuentas_bloqueadas[username]
        
        return False, 0


class InputValidator:
    """
    Validador de inputs para prevenir inyecciones SQL y XSS
    """
    
    @staticmethod
    def sanitizar_sql(input_str: str) -> str:
        """Sanitiza input para prevenir inyección SQL"""
        if not input_str:
            return ""
        
        # Caracteres peligrosos para SQL
        caracteres_peligrosos = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_", "DROP", "DELETE", "INSERT", "UPDATE"]
        
        resultado = input_str
        for char in caracteres_peligrosos:
            resultado = resultado.replace(char, "")
        
        return resultado
    
    @staticmethod
    def sanitizar_xss(input_str: str) -> str:
        """Sanitiza input para prevenir XSS"""
        if not input_str:
            return ""
        
        # Reemplazar caracteres HTML peligrosos
        reemplazos = {
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
            "&": "&amp;",
            "/": "&#x2F;"
        }
        
        resultado = input_str
        for char, replacement in reemplazos.items():
            resultado = resultado.replace(char, replacement)
        
        return resultado
    
    @staticmethod
    def validar_codigo_producto(codigo: str) -> bool:
        """Valida formato de código de producto"""
        # Solo alfanumérico, guiones y guiones bajos
        import re
        patron = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(patron, codigo))
    
    @staticmethod
    def validar_cantidad(cantidad: any) -> Tuple[bool, str]:
        """Valida que la cantidad sea válida"""
        try:
            cant = int(cantidad)
            if cant < 0:
                return False, "La cantidad no puede ser negativa"
            if cant > 1000000:
                return False, "La cantidad excede el límite permitido"
            return True, ""
        except (ValueError, TypeError):
            return False, "La cantidad debe ser un número entero"
    
    @staticmethod
    def validar_ubicacion(ubicacion: str) -> bool:
        """Valida formato de ubicación"""
        # Formato esperado: Almacén A - Estante 1 - Nivel 2
        if not ubicacion or len(ubicacion) > 200:
            return False
        
        # Verificar que no contenga caracteres extraños
        import re
        patron = r'^[a-zA-Z0-9\s\-áéíóúñÁÉÍÓÚÑ]+$'
        return bool(re.match(patron, ubicacion))


# Instancias globales
login_tracker = LoginAttemptTracker()
input_validator = InputValidator()
