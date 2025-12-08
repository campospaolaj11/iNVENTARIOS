-- =============================================
-- Sistema de Inventarios - SQL Server Schema
-- =============================================

-- Crear base de datos (ejecutar primero)
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'InventariosDB')
BEGIN
    CREATE DATABASE InventariosDB;
END
GO

USE InventariosDB;
GO

-- =============================================
-- Tabla: Productos
-- =============================================
IF OBJECT_ID('productos', 'U') IS NOT NULL
    DROP TABLE productos;
GO

CREATE TABLE productos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    codigo NVARCHAR(50) UNIQUE NOT NULL,
    nombre NVARCHAR(200) NOT NULL,
    descripcion NVARCHAR(500),
    categoria NVARCHAR(100),
    
    -- Inventario
    stock_actual INT DEFAULT 0,
    stock_minimo INT DEFAULT 10,
    stock_maximo INT DEFAULT 1000,
    
    -- Costos
    costo_unitario DECIMAL(18, 2) DEFAULT 0.0,
    precio_venta DECIMAL(18, 2) DEFAULT 0.0,
    costo_almacenamiento DECIMAL(18, 2) DEFAULT 0.0,
    
    -- Ubicación
    ubicacion_bodega NVARCHAR(100),
    
    -- Metadatos
    activo BIT DEFAULT 1,
    fecha_creacion DATETIME2 DEFAULT GETDATE(),
    fecha_actualizacion DATETIME2,
    
    INDEX idx_codigo (codigo),
    INDEX idx_categoria (categoria)
);
GO

-- =============================================
-- Tabla: Movimientos
-- =============================================
IF OBJECT_ID('movimientos', 'U') IS NOT NULL
    DROP TABLE movimientos;
GO

CREATE TABLE movimientos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    producto_id INT NOT NULL,
    
    tipo_movimiento NVARCHAR(20) NOT NULL CHECK (tipo_movimiento IN ('ENTRADA', 'SALIDA', 'AJUSTE')),
    cantidad INT NOT NULL,
    
    referencia NVARCHAR(100),
    observaciones NVARCHAR(500),
    
    fecha_movimiento DATETIME2 DEFAULT GETDATE(),
    
    FOREIGN KEY (producto_id) REFERENCES productos(id),
    INDEX idx_producto_id (producto_id),
    INDEX idx_fecha (fecha_movimiento)
);
GO

-- =============================================
-- Tabla: KPIs
-- =============================================
IF OBJECT_ID('kpis', 'U') IS NOT NULL
    DROP TABLE kpis;
GO

CREATE TABLE kpis (
    id INT IDENTITY(1,1) PRIMARY KEY,
    fecha_calculo DATETIME2 DEFAULT GETDATE(),
    
    -- Métricas
    total_productos INT DEFAULT 0,
    productos_criticos INT DEFAULT 0,
    valor_inventario DECIMAL(18, 2) DEFAULT 0.0,
    rotacion_promedio DECIMAL(10, 2) DEFAULT 0.0,
    costo_almacenamiento_total DECIMAL(18, 2) DEFAULT 0.0,
    
    INDEX idx_fecha_calculo (fecha_calculo)
);
GO

-- =============================================
-- Vista: Productos con Stock Crítico
-- =============================================
CREATE OR ALTER VIEW vw_productos_criticos AS
SELECT 
    p.id,
    p.codigo,
    p.nombre,
    p.categoria,
    p.stock_actual,
    p.stock_minimo,
    (p.stock_minimo - p.stock_actual) AS unidades_faltantes
FROM productos p
WHERE p.stock_actual <= p.stock_minimo
    AND p.activo = 1;
GO

-- =============================================
-- Vista: Valor de Inventario
-- =============================================
CREATE OR ALTER VIEW vw_valor_inventario AS
SELECT 
    p.categoria,
    COUNT(*) AS total_productos,
    SUM(p.stock_actual) AS unidades_totales,
    SUM(p.stock_actual * p.costo_unitario) AS valor_total
FROM productos p
WHERE p.activo = 1
GROUP BY p.categoria;
GO

-- =============================================
-- Stored Procedure: Calcular KPIs
-- =============================================
CREATE OR ALTER PROCEDURE sp_calcular_kpis
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @total_productos INT;
    DECLARE @productos_criticos INT;
    DECLARE @valor_inventario DECIMAL(18, 2);
    DECLARE @costo_almacenamiento DECIMAL(18, 2);
    
    -- Total de productos activos
    SELECT @total_productos = COUNT(*) 
    FROM productos 
    WHERE activo = 1;
    
    -- Productos en stock crítico
    SELECT @productos_criticos = COUNT(*) 
    FROM productos 
    WHERE stock_actual <= stock_minimo 
        AND activo = 1;
    
    -- Valor total del inventario
    SELECT @valor_inventario = ISNULL(SUM(stock_actual * costo_unitario), 0)
    FROM productos 
    WHERE activo = 1;
    
    -- Costo de almacenamiento total
    SELECT @costo_almacenamiento = ISNULL(SUM(stock_actual * costo_almacenamiento), 0)
    FROM productos 
    WHERE activo = 1;
    
    -- Insertar KPIs calculados
    INSERT INTO kpis (
        total_productos,
        productos_criticos,
        valor_inventario,
        costo_almacenamiento_total
    )
    VALUES (
        @total_productos,
        @productos_criticos,
        @valor_inventario,
        @costo_almacenamiento
    );
    
    SELECT 
        @total_productos AS total_productos,
        @productos_criticos AS productos_criticos,
        @valor_inventario AS valor_inventario,
        @costo_almacenamiento AS costo_almacenamiento_total;
END;
GO

-- =============================================
-- Datos de ejemplo
-- =============================================
INSERT INTO productos (codigo, nombre, descripcion, categoria, stock_actual, stock_minimo, stock_maximo, costo_unitario, precio_venta, costo_almacenamiento, ubicacion_bodega)
VALUES 
    ('PROD001', 'Tornillo M8x20', 'Tornillo métrico 8mm x 20mm', 'Ferretería', 150, 50, 500, 0.15, 0.30, 0.01, 'A-01'),
    ('PROD002', 'Tuerca M8', 'Tuerca hexagonal M8', 'Ferretería', 200, 50, 500, 0.10, 0.20, 0.01, 'A-02'),
    ('PROD003', 'Arandela M8', 'Arandela plana M8', 'Ferretería', 30, 50, 500, 0.05, 0.10, 0.01, 'A-03'),
    ('PROD004', 'Cable 2x14 AWG', 'Cable eléctrico 2x14 (metro)', 'Eléctricos', 500, 100, 2000, 1.50, 3.00, 0.05, 'B-01'),
    ('PROD005', 'Interruptor Simple', 'Interruptor simple 15A', 'Eléctricos', 80, 20, 200, 2.50, 5.00, 0.02, 'B-02');
GO

-- Insertar algunos movimientos de ejemplo
INSERT INTO movimientos (producto_id, tipo_movimiento, cantidad, referencia, observaciones)
VALUES 
    (1, 'ENTRADA', 100, 'PO-2024-001', 'Compra inicial'),
    (1, 'SALIDA', 50, 'SO-2024-001', 'Venta cliente A'),
    (2, 'ENTRADA', 200, 'PO-2024-002', 'Compra inicial'),
    (3, 'ENTRADA', 100, 'PO-2024-003', 'Compra inicial'),
    (3, 'SALIDA', 70, 'SO-2024-002', 'Venta cliente B');
GO

-- Calcular KPIs iniciales
EXEC sp_calcular_kpis;
GO

PRINT 'Schema creado exitosamente!';
