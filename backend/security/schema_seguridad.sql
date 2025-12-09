-- SCRIPT DE CREACIÓN DE TABLAS DE SEGURIDAD
-- Base de datos: InventariosDB

USE InventariosDB;
GO

-- ==============================================
-- TABLA: usuarios
-- Gestiona usuarios del sistema con roles
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'usuarios')
BEGIN
    CREATE TABLE usuarios (
        id INT PRIMARY KEY IDENTITY(1,1),
        username NVARCHAR(100) NOT NULL UNIQUE,
        email NVARCHAR(255) NOT NULL UNIQUE,
        hashed_password NVARCHAR(255) NOT NULL,
        nombre_completo NVARCHAR(200) NOT NULL,
        rol NVARCHAR(50) NOT NULL CHECK (rol IN ('administrador', 'gerente', 'operador', 'auditor')),
        activo BIT DEFAULT 1,
        intentos_fallidos INT DEFAULT 0,
        bloqueado_hasta DATETIME NULL,
        ultimo_acceso DATETIME NULL,
        fecha_creacion DATETIME DEFAULT GETDATE(),
        fecha_modificacion DATETIME DEFAULT GETDATE(),
        creado_por INT NULL,
        modificado_por INT NULL,
        telefono NVARCHAR(20) NULL,
        ubicaciones_permitidas NVARCHAR(MAX) NULL, -- JSON con coordenadas GPS
        dispositivos_autorizados NVARCHAR(MAX) NULL, -- JSON con IDs de dispositivos
        requiere_cambio_password BIT DEFAULT 0,
        ultimo_cambio_password DATETIME NULL,
        token_2fa NVARCHAR(100) NULL,
        habilitado_2fa BIT DEFAULT 0,
        CONSTRAINT CK_rol_valido CHECK (rol IN ('administrador', 'gerente', 'operador', 'auditor'))
    );
    
    PRINT 'Tabla usuarios creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla usuarios ya existe';
END
GO

-- ==============================================
-- TABLA: roles_permisos
-- Define permisos por rol
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'roles_permisos')
BEGIN
    CREATE TABLE roles_permisos (
        id INT PRIMARY KEY IDENTITY(1,1),
        rol NVARCHAR(50) NOT NULL,
        permiso NVARCHAR(100) NOT NULL,
        descripcion NVARCHAR(500),
        activo BIT DEFAULT 1,
        UNIQUE(rol, permiso)
    );
    
    PRINT 'Tabla roles_permisos creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla roles_permisos ya existe';
END
GO

-- ==============================================
-- TABLA: auditoria_movimientos
-- Registra TODOS los movimientos con hash
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'auditoria_movimientos')
BEGIN
    CREATE TABLE auditoria_movimientos (
        id INT PRIMARY KEY IDENTITY(1,1),
        fecha_hora DATETIME NOT NULL DEFAULT GETDATE(),
        usuario_id INT NOT NULL,
        usuario_nombre NVARCHAR(200),
        accion NVARCHAR(50) NOT NULL CHECK (accion IN ('ENTRADA', 'SALIDA', 'MODIFICACION', 'ELIMINACION', 'CONSULTA', 'LOGIN', 'LOGOUT')),
        tipo_entidad NVARCHAR(50) NOT NULL,
        entidad_id NVARCHAR(100),
        datos_anteriores NVARCHAR(MAX), -- JSON
        datos_nuevos NVARCHAR(MAX), -- JSON
        ip_address NVARCHAR(45),
        dispositivo NVARCHAR(200),
        ubicacion_gps NVARCHAR(100),
        stock_antes INT NULL,
        stock_despues INT NULL,
        cantidad_movida INT NULL,
        motivo NVARCHAR(500),
        aprobado_por INT NULL,
        hash_integridad NVARCHAR(64) NOT NULL, -- SHA256
        hash_anterior NVARCHAR(64) NOT NULL, -- Hash del registro anterior (blockchain-like)
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (aprobado_por) REFERENCES usuarios(id)
    );
    
    -- Índices para optimizar consultas
    CREATE INDEX IDX_auditoria_fecha ON auditoria_movimientos(fecha_hora DESC);
    CREATE INDEX IDX_auditoria_usuario ON auditoria_movimientos(usuario_id);
    CREATE INDEX IDX_auditoria_accion ON auditoria_movimientos(accion);
    CREATE INDEX IDX_auditoria_entidad ON auditoria_movimientos(tipo_entidad, entidad_id);
    
    PRINT 'Tabla auditoria_movimientos creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla auditoria_movimientos ya existe';
END
GO

-- ==============================================
-- TABLA: alertas_fraude
-- Registra alertas de detección de fraudes
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'alertas_fraude')
BEGIN
    CREATE TABLE alertas_fraude (
        id INT PRIMARY KEY IDENTITY(1,1),
        fecha_hora DATETIME NOT NULL DEFAULT GETDATE(),
        tipo NVARCHAR(100) NOT NULL,
        gravedad NVARCHAR(20) NOT NULL CHECK (gravedad IN ('baja', 'media', 'alta', 'critica')),
        usuario_id INT NOT NULL,
        usuario_nombre NVARCHAR(200),
        descripcion NVARCHAR(1000),
        datos_adicionales NVARCHAR(MAX), -- JSON
        requiere_accion BIT DEFAULT 0,
        notificado BIT DEFAULT 0,
        resuelto BIT DEFAULT 0,
        fecha_resolucion DATETIME NULL,
        resuelto_por INT NULL,
        notas_resolucion NVARCHAR(MAX),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (resuelto_por) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IDX_alertas_fecha ON alertas_fraude(fecha_hora DESC);
    CREATE INDEX IDX_alertas_gravedad ON alertas_fraude(gravedad);
    CREATE INDEX IDX_alertas_usuario ON alertas_fraude(usuario_id);
    CREATE INDEX IDX_alertas_resuelto ON alertas_fraude(resuelto);
    
    PRINT 'Tabla alertas_fraude creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla alertas_fraude ya existe';
END
GO

-- ==============================================
-- TABLA: sesiones_activas
-- Rastrea sesiones activas para control
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'sesiones_activas')
BEGIN
    CREATE TABLE sesiones_activas (
        id INT PRIMARY KEY IDENTITY(1,1),
        usuario_id INT NOT NULL,
        token_sesion NVARCHAR(500) NOT NULL UNIQUE,
        fecha_inicio DATETIME NOT NULL DEFAULT GETDATE(),
        fecha_expiracion DATETIME NOT NULL,
        ultimo_uso DATETIME NOT NULL DEFAULT GETDATE(),
        ip_address NVARCHAR(45),
        dispositivo NVARCHAR(200),
        ubicacion_gps NVARCHAR(100),
        activa BIT DEFAULT 1,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    
    CREATE INDEX IDX_sesiones_usuario ON sesiones_activas(usuario_id);
    CREATE INDEX IDX_sesiones_activa ON sesiones_activas(activa);
    CREATE INDEX IDX_sesiones_expiracion ON sesiones_activas(fecha_expiracion);
    
    PRINT 'Tabla sesiones_activas creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla sesiones_activas ya existe';
END
GO

-- ==============================================
-- TABLA: configuracion_seguridad
-- Configuraciones del sistema de seguridad
-- ==============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'configuracion_seguridad')
BEGIN
    CREATE TABLE configuracion_seguridad (
        id INT PRIMARY KEY IDENTITY(1,1),
        clave NVARCHAR(100) NOT NULL UNIQUE,
        valor NVARCHAR(MAX) NOT NULL,
        tipo NVARCHAR(50) NOT NULL, -- 'string', 'int', 'bool', 'json'
        descripcion NVARCHAR(500),
        fecha_modificacion DATETIME DEFAULT GETDATE(),
        modificado_por INT NULL,
        FOREIGN KEY (modificado_por) REFERENCES usuarios(id)
    );
    
    PRINT 'Tabla configuracion_seguridad creada exitosamente';
END
ELSE
BEGIN
    PRINT 'Tabla configuracion_seguridad ya existe';
END
GO

-- ==============================================
-- INSERTAR PERMISOS PREDEFINIDOS
-- ==============================================
IF NOT EXISTS (SELECT * FROM roles_permisos WHERE rol = 'administrador')
BEGIN
    -- Permisos de ADMINISTRADOR
    INSERT INTO roles_permisos (rol, permiso, descripcion) VALUES
    ('administrador', 'ver_todo', 'Ver toda la información del sistema'),
    ('administrador', 'crear_producto', 'Crear nuevos productos'),
    ('administrador', 'modificar_producto', 'Modificar productos existentes'),
    ('administrador', 'eliminar_producto', 'Eliminar productos'),
    ('administrador', 'registrar_movimiento', 'Registrar entradas y salidas'),
    ('administrador', 'aprobar_movimiento', 'Aprobar movimientos grandes'),
    ('administrador', 'ver_auditoria', 'Ver registros de auditoría'),
    ('administrador', 'gestionar_usuarios', 'Crear y modificar usuarios');
    
    -- Permisos de GERENTE
    INSERT INTO roles_permisos (rol, permiso, descripcion) VALUES
    ('gerente', 'ver_todo', 'Ver toda la información del sistema'),
    ('gerente', 'crear_producto', 'Crear nuevos productos'),
    ('gerente', 'modificar_producto', 'Modificar productos existentes'),
    ('gerente', 'registrar_movimiento', 'Registrar entradas y salidas'),
    ('gerente', 'aprobar_movimiento', 'Aprobar movimientos grandes'),
    ('gerente', 'ver_auditoria', 'Ver registros de auditoría');
    
    -- Permisos de OPERADOR
    INSERT INTO roles_permisos (rol, permiso, descripcion) VALUES
    ('operador', 'ver_todo', 'Ver toda la información del sistema'),
    ('operador', 'registrar_movimiento', 'Registrar entradas y salidas');
    
    -- Permisos de AUDITOR
    INSERT INTO roles_permisos (rol, permiso, descripcion) VALUES
    ('auditor', 'ver_todo', 'Ver toda la información del sistema'),
    ('auditor', 'ver_auditoria', 'Ver registros de auditoría');
    
    PRINT 'Permisos predefinidos insertados';
END
GO

-- ==============================================
-- INSERTAR CONFIGURACIONES INICIALES
-- ==============================================
IF NOT EXISTS (SELECT * FROM configuracion_seguridad WHERE clave = 'max_intentos_login')
BEGIN
    INSERT INTO configuracion_seguridad (clave, valor, tipo, descripcion) VALUES
    ('max_intentos_login', '5', 'int', 'Máximo de intentos de login fallidos antes de bloquear cuenta'),
    ('tiempo_bloqueo_minutos', '30', 'int', 'Minutos que dura el bloqueo de cuenta'),
    ('limite_requests_por_minuto', '100', 'int', 'Límite de requests por IP por minuto'),
    ('cantidad_requiere_aprobacion', '100', 'int', 'Cantidad mínima que requiere aprobación de supervisor'),
    ('habilitar_2fa', 'false', 'bool', 'Habilitar autenticación de dos factores'),
    ('horario_laboral_inicio', '06:00', 'string', 'Hora de inicio del horario laboral'),
    ('horario_laboral_fin', '22:00', 'string', 'Hora de fin del horario laboral'),
    ('dias_expiracion_password', '90', 'int', 'Días hasta que expire la contraseña'),
    ('ubicaciones_gps_permitidas', '[]', 'json', 'Lista de ubicaciones GPS permitidas para operaciones');
    
    PRINT 'Configuraciones de seguridad insertadas';
END
GO

-- ==============================================
-- CREAR USUARIO ADMINISTRADOR POR DEFECTO
-- Password: Admin123!
-- Hash generado con bcrypt
-- ==============================================
IF NOT EXISTS (SELECT * FROM usuarios WHERE username = 'admin')
BEGIN
    INSERT INTO usuarios (username, email, hashed_password, nombre_completo, rol, activo) VALUES
    ('admin', 'admin@inventarios.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYFP.dY6oBw1VZu', 'Administrador del Sistema', 'administrador', 1);
    
    PRINT 'Usuario administrador creado (usuario: admin, password: Admin123!)';
    PRINT '⚠️ IMPORTANTE: Cambiar esta contraseña en producción';
END
GO

-- ==============================================
-- VISTAS ÚTILES
-- ==============================================

-- Vista de usuarios activos con su último acceso
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_usuarios_activos')
    DROP VIEW v_usuarios_activos;
GO

CREATE VIEW v_usuarios_activos AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.nombre_completo,
    u.rol,
    u.ultimo_acceso,
    COUNT(s.id) as sesiones_activas,
    u.intentos_fallidos
FROM usuarios u
LEFT JOIN sesiones_activas s ON u.id = s.usuario_id AND s.activa = 1
WHERE u.activo = 1
GROUP BY u.id, u.username, u.email, u.nombre_completo, u.rol, u.ultimo_acceso, u.intentos_fallidos;
GO

-- Vista de alertas pendientes
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_alertas_pendientes')
    DROP VIEW v_alertas_pendientes;
GO

CREATE VIEW v_alertas_pendientes AS
SELECT 
    a.id,
    a.fecha_hora,
    a.tipo,
    a.gravedad,
    a.usuario_nombre,
    a.descripcion,
    DATEDIFF(HOUR, a.fecha_hora, GETDATE()) as horas_desde_alerta
FROM alertas_fraude a
WHERE a.resuelto = 0 AND a.requiere_accion = 1
ORDER BY 
    CASE a.gravedad
        WHEN 'critica' THEN 1
        WHEN 'alta' THEN 2
        WHEN 'media' THEN 3
        WHEN 'baja' THEN 4
    END,
    a.fecha_hora DESC;
GO

-- Vista de auditoría reciente
IF EXISTS (SELECT * FROM sys.views WHERE name = 'v_auditoria_reciente')
    DROP VIEW v_auditoria_reciente;
GO

CREATE VIEW v_auditoria_reciente AS
SELECT TOP 1000
    a.id,
    a.fecha_hora,
    a.usuario_nombre,
    a.accion,
    a.tipo_entidad,
    a.entidad_id,
    a.cantidad_movida,
    a.ip_address,
    a.dispositivo
FROM auditoria_movimientos a
ORDER BY a.fecha_hora DESC;
GO

PRINT '====================================';
PRINT 'SCRIPT DE SEGURIDAD COMPLETADO';
PRINT '====================================';
PRINT '';
PRINT 'Tablas creadas:';
PRINT '  ✓ usuarios';
PRINT '  ✓ roles_permisos';
PRINT '  ✓ auditoria_movimientos';
PRINT '  ✓ alertas_fraude';
PRINT '  ✓ sesiones_activas';
PRINT '  ✓ configuracion_seguridad';
PRINT '';
PRINT 'Usuario por defecto:';
PRINT '  Username: admin';
PRINT '  Password: Admin123!';
PRINT '  ⚠️ CAMBIAR CONTRASEÑA EN PRODUCCIÓN';
PRINT '';
PRINT 'Próximos pasos:';
PRINT '  1. Cambiar contraseña del usuario admin';
PRINT '  2. Crear usuarios con roles apropiados';
PRINT '  3. Configurar ubicaciones GPS permitidas';
PRINT '  4. Habilitar 2FA si es necesario';
PRINT '  5. Revisar configuraciones de seguridad';
GO
