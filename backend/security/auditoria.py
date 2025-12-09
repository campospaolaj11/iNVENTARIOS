"""
Sistema de Auditoría y Trazabilidad
"""
from datetime import datetime
from typing import Optional, Dict, Any
import hashlib
import json
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AuditoriaMovimiento(Base):
    """Modelo de auditoría para rastrear todos los movimientos"""
    __tablename__ = "auditoria_movimientos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime, nullable=False, default=datetime.utcnow)
    usuario_id = Column(Integer, nullable=False)
    usuario_nombre = Column(String(200))
    accion = Column(String(50), nullable=False)  # ENTRADA, SALIDA, MODIFICACION, ELIMINACION
    tipo_entidad = Column(String(50), nullable=False)  # PRODUCTO, USUARIO, CONFIGURACION
    entidad_id = Column(String(100))
    datos_anteriores = Column(Text)  # JSON
    datos_nuevos = Column(Text)  # JSON
    ip_address = Column(String(45))
    dispositivo = Column(String(200))
    ubicacion_gps = Column(String(100))
    stock_antes = Column(Integer)
    stock_despues = Column(Integer)
    cantidad_movida = Column(Integer)
    motivo = Column(String(500))
    aprobado_por = Column(Integer)  # ID del usuario que aprobó
    hash_integridad = Column(String(64), nullable=False)
    hash_anterior = Column(String(64))  # Hash del registro anterior (blockchain-like)

class ServicioAuditoria:
    """Servicio para registrar y verificar auditorías"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.ultimo_hash = self._obtener_ultimo_hash()
    
    def _obtener_ultimo_hash(self) -> str:
        """Obtiene el hash del último registro de auditoría"""
        ultimo = self.db.query(AuditoriaMovimiento).order_by(
            AuditoriaMovimiento.id.desc()
        ).first()
        return ultimo.hash_integridad if ultimo else "0" * 64
    
    def _calcular_hash(self, datos: Dict[str, Any], hash_anterior: str) -> str:
        """
        Calcula el hash de integridad del registro
        Incluye datos del movimiento + hash anterior (como blockchain)
        """
        datos_para_hash = {
            "fecha_hora": datos.get("fecha_hora", datetime.utcnow()).isoformat(),
            "usuario_id": datos.get("usuario_id"),
            "accion": datos.get("accion"),
            "entidad_id": datos.get("entidad_id"),
            "datos": datos.get("datos_nuevos"),
            "hash_anterior": hash_anterior
        }
        
        cadena = json.dumps(datos_para_hash, sort_keys=True)
        return hashlib.sha256(cadena.encode()).hexdigest()
    
    def registrar_movimiento(
        self,
        usuario_id: int,
        usuario_nombre: str,
        accion: str,
        tipo_entidad: str,
        entidad_id: str,
        datos_anteriores: Optional[Dict] = None,
        datos_nuevos: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        dispositivo: Optional[str] = None,
        ubicacion_gps: Optional[str] = None,
        stock_antes: Optional[int] = None,
        stock_despues: Optional[int] = None,
        cantidad_movida: Optional[int] = None,
        motivo: Optional[str] = None,
        aprobado_por: Optional[int] = None
    ) -> AuditoriaMovimiento:
        """
        Registra un movimiento en la auditoría con hash de integridad
        """
        datos_log = {
            "fecha_hora": datetime.utcnow(),
            "usuario_id": usuario_id,
            "usuario_nombre": usuario_nombre,
            "accion": accion,
            "tipo_entidad": tipo_entidad,
            "entidad_id": entidad_id,
            "datos_anteriores": json.dumps(datos_anteriores) if datos_anteriores else None,
            "datos_nuevos": json.dumps(datos_nuevos) if datos_nuevos else None,
            "ip_address": ip_address,
            "dispositivo": dispositivo,
            "ubicacion_gps": ubicacion_gps,
            "stock_antes": stock_antes,
            "stock_despues": stock_despues,
            "cantidad_movida": cantidad_movida,
            "motivo": motivo,
            "aprobado_por": aprobado_por
        }
        
        # Calcular hash de integridad
        hash_integridad = self._calcular_hash(datos_log, self.ultimo_hash)
        datos_log["hash_integridad"] = hash_integridad
        datos_log["hash_anterior"] = self.ultimo_hash
        
        # Crear registro
        auditoria = AuditoriaMovimiento(**datos_log)
        self.db.add(auditoria)
        self.db.commit()
        
        # Actualizar último hash
        self.ultimo_hash = hash_integridad
        
        return auditoria
    
    def verificar_integridad(self, desde_id: Optional[int] = None) -> tuple[bool, list]:
        """
        Verifica la integridad de la cadena de auditoría
        Retorna (es_integro, registros_alterados)
        """
        query = self.db.query(AuditoriaMovimiento).order_by(AuditoriaMovimiento.id)
        
        if desde_id:
            query = query.filter(AuditoriaMovimiento.id >= desde_id)
        
        registros = query.all()
        registros_alterados = []
        hash_esperado = "0" * 64
        
        for registro in registros:
            # Recalcular hash
            datos = {
                "fecha_hora": registro.fecha_hora,
                "usuario_id": registro.usuario_id,
                "accion": registro.accion,
                "entidad_id": registro.entidad_id,
                "datos_nuevos": registro.datos_nuevos
            }
            
            hash_calculado = self._calcular_hash(datos, hash_esperado)
            
            # Verificar si coincide
            if hash_calculado != registro.hash_integridad:
                registros_alterados.append({
                    "id": registro.id,
                    "fecha": registro.fecha_hora,
                    "hash_esperado": hash_calculado,
                    "hash_almacenado": registro.hash_integridad
                })
            
            hash_esperado = registro.hash_integridad
        
        return len(registros_alterados) == 0, registros_alterados
    
    def obtener_historial_entidad(
        self,
        tipo_entidad: str,
        entidad_id: str,
        limite: int = 50
    ) -> list[AuditoriaMovimiento]:
        """Obtiene el historial completo de una entidad"""
        return self.db.query(AuditoriaMovimiento).filter(
            AuditoriaMovimiento.tipo_entidad == tipo_entidad,
            AuditoriaMovimiento.entidad_id == entidad_id
        ).order_by(AuditoriaMovimiento.fecha_hora.desc()).limit(limite).all()
    
    def obtener_movimientos_usuario(
        self,
        usuario_id: int,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> list[AuditoriaMovimiento]:
        """Obtiene todos los movimientos de un usuario en un rango de fechas"""
        query = self.db.query(AuditoriaMovimiento).filter(
            AuditoriaMovimiento.usuario_id == usuario_id
        )
        
        if fecha_inicio:
            query = query.filter(AuditoriaMovimiento.fecha_hora >= fecha_inicio)
        if fecha_fin:
            query = query.filter(AuditoriaMovimiento.fecha_hora <= fecha_fin)
        
        return query.order_by(AuditoriaMovimiento.fecha_hora.desc()).all()
    
    def detectar_movimientos_sospechosos(self) -> list[Dict]:
        """
        Detecta patrones sospechosos en los movimientos
        """
        alertas = []
        
        # 1. Movimientos fuera de horario (10pm - 6am)
        movimientos_nocturnos = self.db.query(AuditoriaMovimiento).filter(
            AuditoriaMovimiento.accion.in_(["ENTRADA", "SALIDA"])
        ).all()
        
        for mov in movimientos_nocturnos:
            hora = mov.fecha_hora.hour
            if hora >= 22 or hora < 6:
                alertas.append({
                    "tipo": "MOVIMIENTO_NOCTURNO",
                    "gravedad": "ALTA",
                    "movimiento_id": mov.id,
                    "usuario": mov.usuario_nombre,
                    "fecha": mov.fecha_hora,
                    "descripcion": f"Movimiento fuera de horario: {mov.accion} a las {mov.fecha_hora}"
                })
        
        # 2. Múltiples movimientos del mismo producto en poco tiempo
        # (Implementar lógica de detección de patrones)
        
        # 3. Movimientos grandes sin aprobación
        movimientos_grandes = self.db.query(AuditoriaMovimiento).filter(
            AuditoriaMovimiento.cantidad_movida > 100,
            AuditoriaMovimiento.aprobado_por.is_(None)
        ).all()
        
        for mov in movimientos_grandes:
            alertas.append({
                "tipo": "MOVIMIENTO_GRANDE_SIN_APROBACION",
                "gravedad": "CRITICA",
                "movimiento_id": mov.id,
                "usuario": mov.usuario_nombre,
                "cantidad": mov.cantidad_movida,
                "descripcion": f"Movimiento de {mov.cantidad_movida} unidades sin aprobación"
            })
        
        return alertas
