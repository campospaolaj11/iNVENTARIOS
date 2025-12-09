"""
Rutas de Autenticación y Autorización
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

from security.auth import (
    Token, Usuario, UsuarioCreate,
    verificar_password, obtener_hash_password,
    crear_access_token, crear_refresh_token, verificar_token,
    validar_password_segura, oauth2_scheme,
    Rol, Permiso, usuario_tiene_permiso,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from security.middleware import login_tracker
from security.auditoria import ServicioAuditoria

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

# Dependencia para obtener la sesión de base de datos
def get_db():
    # TODO: Implementar con tu conexión a SQL Server
    # from database import SessionLocal
    # db = SessionLocal()
    # try:
    #     yield db
    # finally:
    #     db.close()
    pass

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Endpoint de autenticación con JWT
    
    Características:
    - Validación de credenciales
    - Protección contra fuerza bruta (5 intentos)
    - Bloqueo temporal de cuenta (30 minutos)
    - Auditoría de intentos
    - Tokens JWT (access + refresh)
    """
    username = form_data.username
    password = form_data.password
    
    # 1. Verificar si la cuenta está bloqueada
    esta_bloqueado, minutos_restantes = login_tracker.esta_bloqueado(username)
    if esta_bloqueado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cuenta bloqueada por múltiples intentos fallidos. Intente en {minutos_restantes} minutos."
        )
    
    # 2. Buscar usuario en base de datos
    # TODO: Implementar consulta real a SQL Server
    # Por ahora, usuario por defecto
    if username == "admin" and password == "Admin123!":
        usuario = Usuario(
            id=1,
            username="admin",
            email="admin@inventarios.com",
            nombre_completo="Administrador del Sistema",
            rol=Rol.ADMINISTRADOR,
            activo=True,
            intentos_fallidos=0,
            ultimo_acceso=datetime.now()
        )
    else:
        # Registrar intento fallido
        bloqueado, intentos_restantes, mins_bloqueo = login_tracker.registrar_intento_fallido(username)
        
        if bloqueado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Cuenta bloqueada por múltiples intentos fallidos. Intente en {mins_bloqueo} minutos."
            )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Usuario o contraseña incorrectos. Intentos restantes: {intentos_restantes}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Verificar que el usuario esté activo
    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado. Contacte al administrador."
        )
    
    # 4. Login exitoso - limpiar intentos fallidos
    login_tracker.registrar_intento_exitoso(username)
    
    # 5. Crear tokens JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_access_token(
        data={"sub": usuario.username, "rol": usuario.rol},
        expires_delta=access_token_expires
    )
    refresh_token = crear_refresh_token(
        data={"sub": usuario.username}
    )
    
    # 6. Registrar en auditoría
    # auditoria = ServicioAuditoria(db)
    # auditoria.registrar_movimiento(
    #     usuario_id=usuario.id,
    #     usuario_nombre=usuario.nombre_completo,
    #     accion="LOGIN",
    #     tipo_entidad="USUARIO",
    #     entidad_id=str(usuario.id),
    #     ip_address=request.client.host,
    #     dispositivo=request.headers.get("User-Agent")
    # )
    
    # 7. Actualizar último acceso
    # TODO: UPDATE usuarios SET ultimo_acceso = NOW(), intentos_fallidos = 0 WHERE id = usuario.id
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token_endpoint(refresh_token: str):
    """
    Refresca el access token usando el refresh token
    """
    try:
        token_data = verificar_token(refresh_token)
        
        # Verificar que sea un refresh token
        # TODO: Agregar validación de tipo de token
        
        # Crear nuevo access token
        access_token = crear_access_token(
            data={"sub": token_data.username, "rol": token_data.rol}
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido o expirado"
        )

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Cierra la sesión del usuario
    """
    token_data = verificar_token(token)
    
    # TODO: Invalidar token en base de datos
    # UPDATE sesiones_activas SET activa = 0 WHERE token_sesion = token
    
    # Registrar en auditoría
    # auditoria = ServicioAuditoria(db)
    # auditoria.registrar_movimiento(...)
    
    return {"message": "Sesión cerrada exitosamente"}

@router.post("/register", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    usuario_nuevo: UsuarioCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo usuario
    Solo administradores pueden crear usuarios
    """
    # Verificar permisos
    if not usuario_tiene_permiso(current_user, Permiso.GESTIONAR_USUARIOS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para crear usuarios"
        )
    
    # Validar contraseña segura
    es_valida, mensaje = validar_password_segura(usuario_nuevo.password)
    if not es_valida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )
    
    # Verificar que el username no exista
    # TODO: SELECT * FROM usuarios WHERE username = usuario_nuevo.username
    
    # Verificar que el email no exista
    # TODO: SELECT * FROM usuarios WHERE email = usuario_nuevo.email
    
    # Crear usuario
    hashed_password = obtener_hash_password(usuario_nuevo.password)
    
    # TODO: INSERT INTO usuarios (username, email, hashed_password, nombre_completo, rol) VALUES (...)
    
    return Usuario(
        id=999,  # TODO: ID real de la base de datos
        username=usuario_nuevo.username,
        email=usuario_nuevo.email,
        nombre_completo=usuario_nuevo.nombre_completo,
        rol=usuario_nuevo.rol,
        activo=True,
        intentos_fallidos=0
    )

@router.get("/me", response_model=Usuario)
async def obtener_usuario_actual(current_user: Usuario = Depends(get_current_user)):
    """
    Obtiene información del usuario autenticado
    """
    return current_user

@router.get("/usuarios", response_model=List[Usuario])
async def listar_usuarios(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Lista todos los usuarios
    Solo administradores
    """
    if not usuario_tiene_permiso(current_user, Permiso.GESTIONAR_USUARIOS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para ver usuarios"
        )
    
    # TODO: SELECT * FROM usuarios
    
    return []

@router.put("/usuarios/{usuario_id}/activar")
async def activar_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Activa/desactiva un usuario
    Solo administradores
    """
    if not usuario_tiene_permiso(current_user, Permiso.GESTIONAR_USUARIOS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permiso para modificar usuarios"
        )
    
    # TODO: UPDATE usuarios SET activo = NOT activo WHERE id = usuario_id
    
    return {"message": "Usuario actualizado"}

@router.put("/usuarios/cambiar-password")
async def cambiar_password(
    password_actual: str,
    password_nueva: str,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambia la contraseña del usuario actual
    """
    # Validar contraseña nueva
    es_valida, mensaje = validar_password_segura(password_nueva)
    if not es_valida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=mensaje
        )
    
    # TODO: Verificar password actual
    # TODO: UPDATE usuarios SET hashed_password = nuevo_hash, ultimo_cambio_password = NOW()
    
    return {"message": "Contraseña actualizada exitosamente"}

# Dependencia: Usuario actual (para usar en otros routers)
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    """
    Obtiene el usuario actual desde el token JWT
    Úsalo como dependencia en tus endpoints:
    
    @app.get("/api/productos")
    async def obtener_productos(current_user: Usuario = Depends(get_current_user)):
        # current_user contiene toda la info del usuario autenticado
        pass
    """
    token_data = verificar_token(token)
    
    # TODO: Consultar usuario de base de datos
    # usuario = db.query(Usuario).filter(Usuario.username == token_data.username).first()
    # if not usuario or not usuario.activo:
    #     raise HTTPException(status_code=401, detail="Usuario inválido")
    
    # Por ahora, retornar usuario ficticio
    return Usuario(
        id=1,
        username=token_data.username,
        email="admin@inventarios.com",
        nombre_completo="Administrador",
        rol=token_data.rol or Rol.ADMINISTRADOR,
        activo=True,
        intentos_fallidos=0
    )

# Dependencia: Verificar permiso específico
def require_permission(permiso: str):
    """
    Verifica que el usuario tenga un permiso específico
    
    Ejemplo de uso:
    @app.delete("/api/productos/{id}")
    async def eliminar_producto(
        id: int,
        current_user: Usuario = Depends(require_permission(Permiso.ELIMINAR_PRODUCTO))
    ):
        pass
    """
    async def permission_checker(current_user: Usuario = Depends(get_current_user)):
        if not usuario_tiene_permiso(current_user, permiso):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tiene el permiso requerido: {permiso}"
            )
        return current_user
    
    return permission_checker
