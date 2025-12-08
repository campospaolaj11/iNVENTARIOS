from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base

class Producto(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500))
    categoria = Column(String(100))
    
    # Inventario
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=10)
    stock_maximo = Column(Integer, default=1000)
    
    # Costos
    costo_unitario = Column(Float, default=0.0)
    precio_venta = Column(Float, default=0.0)
    costo_almacenamiento = Column(Float, default=0.0)
    
    # Ubicación
    ubicacion_bodega = Column(String(100))
    
    # Metadatos
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

class Movimiento(Base):
    __tablename__ = "movimientos"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, nullable=False, index=True)
    
    tipo_movimiento = Column(String(20), nullable=False)  # ENTRADA, SALIDA, AJUSTE
    cantidad = Column(Integer, nullable=False)
    
    referencia = Column(String(100))  # Número de pedido, factura, etc.
    observaciones = Column(String(500))
    
    fecha_movimiento = Column(DateTime(timezone=True), server_default=func.now())

class KPI(Base):
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_calculo = Column(DateTime(timezone=True), server_default=func.now())
    
    # Métricas
    total_productos = Column(Integer, default=0)
    productos_criticos = Column(Integer, default=0)
    valor_inventario = Column(Float, default=0.0)
    rotacion_promedio = Column(Float, default=0.0)
    costo_almacenamiento_total = Column(Float, default=0.0)
