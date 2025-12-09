"""
Sistema de Autenticación y Autorización
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuración de seguridad
SECRET_KEY = "TU_CLAVE_SECRETA_SUPER_SEGURA_CAMBIAR_EN_PRODUCCION"  # CAMBIAR EN .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Roles y permisos
class Rol:
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    OPERADOR = "operador"
    AUDITOR = "auditor"

class Permiso:
    VER_TODO = "ver_todo"
    CREAR_PRODUCTO = "crear_producto"
    MODIFICAR_PRODUCTO = "modificar_producto"
    ELIMINAR_PRODUCTO = "eliminar_producto"
    REGISTRAR_MOVIMIENTO = "registrar_movimiento"
    APROBAR_MOVIMIENTO = "aprobar_movimiento"
    VER_AUDITORIA = "ver_auditoria"
    GESTIONAR_USUARIOS = "gestionar_usuarios"

# Mapa de permisos por rol
PERMISOS_POR_ROL = {
    Rol.ADMINISTRADOR: [
        Permiso.VER_TODO,
        Permiso.CREAR_PRODUCTO,
        Permiso.MODIFICAR_PRODUCTO,
        Permiso.ELIMINAR_PRODUCTO,
        Permiso.REGISTRAR_MOVIMIENTO,
        Permiso.APROBAR_MOVIMIENTO,
        Permiso.VER_AUDITORIA,
        Permiso.GESTIONAR_USUARIOS
    ],
    Rol.GERENTE: [
        Permiso.VER_TODO,
        Permiso.CREAR_PRODUCTO,
        Permiso.MODIFICAR_PRODUCTO,
        Permiso.REGISTRAR_MOVIMIENTO,
        Permiso.APROBAR_MOVIMIENTO,
        Permiso.VER_AUDITORIA
    ],
    Rol.OPERADOR: [
        Permiso.VER_TODO,
        Permiso.REGISTRAR_MOVIMIENTO
    ],
    Rol.AUDITOR: [
        Permiso.VER_TODO,
        Permiso.VER_AUDITORIA
    ]
}

# Modelos
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    rol: Optional[str] = None

class Usuario(BaseModel):
    id: int
    username: str
    email: str
    nombre_completo: str
    rol: str
    activo: bool
    intentos_fallidos: int = 0
    ultimo_acceso: Optional[datetime] = None

class UsuarioCreate(BaseModel):
    username: str
    email: str
    password: str
    nombre_completo: str
    rol: str

class UsuarioDB(Usuario):
    hashed_password: str

# Funciones de utilidad
def verificar_password(password_plano: str, hashed_password: str) -> bool:
    """Verifica que la contraseña coincida con el hash"""
    return pwd_context.verify(password_plano, hashed_password)

def obtener_hash_password(password: str) -> str:
    """Genera el hash de una contraseña"""
    return pwd_context.hash(password)

def crear_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Crea un token JWT de acceso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def crear_refresh_token(data: dict):
    """Crea un token JWT de refresco"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str) -> TokenData:
    """Verifica y decodifica un token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        rol: str = payload.get("rol")
        
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username, rol=rol)
        return token_data
    except JWTError:
        raise credentials_exception

def usuario_tiene_permiso(usuario: Usuario, permiso: str) -> bool:
    """Verifica si un usuario tiene un permiso específico"""
    permisos = PERMISOS_POR_ROL.get(usuario.rol, [])
    return permiso in permisos

def requiere_permiso(permiso: str):
    """Decorador para requerir un permiso específico"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Aquí se verificaría el usuario actual
            # y se validaría si tiene el permiso
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Validaciones de seguridad
def validar_password_segura(password: str) -> tuple[bool, str]:
    """
    Valida que la contraseña cumpla con políticas de seguridad
    Retorna (es_valida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not any(c.isupper() for c in password):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not any(c.islower() for c in password):
        return False, "La contraseña debe contener al menos una minúscula"
    
    if not any(c.isdigit() for c in password):
        return False, "La contraseña debe contener al menos un número"
    
    caracteres_especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in caracteres_especiales for c in password):
        return False, "La contraseña debe contener al menos un carácter especial"
    
    return True, "Contraseña válida"

def validar_movimiento_requiere_aprobacion(cantidad: int, usuario: Usuario) -> bool:
    """
    Determina si un movimiento requiere aprobación adicional
    """
    # Movimientos grandes requieren aprobación de gerente
    if cantidad > 100 and usuario.rol == Rol.OPERADOR:
        return True
    
    # Movimientos masivos requieren aprobación de administrador
    if cantidad > 1000 and usuario.rol in [Rol.OPERADOR, Rol.GERENTE]:
        return True
    
    return False
