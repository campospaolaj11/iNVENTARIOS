"""
Sistema de Detección de Fraudes
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class NivelGravedad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"

@dataclass
class AlertaFraude:
    """Representa una alerta de fraude detectada"""
    id: int
    tipo: str
    gravedad: NivelGravedad
    fecha_hora: datetime
    usuario_id: int
    usuario_nombre: str
    descripcion: str
    datos_adicionales: Dict
    requiere_accion_inmediata: bool
    notificado: bool = False

class DetectorFraudes:
    """
    Sistema de detección de patrones sospechosos y fraudes
    """
    
    def __init__(self, db_session, servicio_notificaciones):
        self.db = db_session
        self.notificaciones = servicio_notificaciones
        self.alertas: List[AlertaFraude] = []
        self.contador_alertas = 0
    
    def analizar_movimiento(
        self,
        usuario_id: int,
        usuario_nombre: str,
        accion: str,
        producto_id: str,
        cantidad: int,
        hora: datetime,
        ubicacion_gps: Optional[str] = None,
        dispositivo: Optional[str] = None
    ) -> List[AlertaFraude]:
        """
        Analiza un movimiento y detecta patrones sospechosos
        Retorna lista de alertas generadas
        """
        alertas_generadas = []
        
        # 1. MOVIMIENTO FUERA DE HORARIO
        if self._es_horario_sospechoso(hora):
            alerta = self._crear_alerta(
                tipo="MOVIMIENTO_FUERA_HORARIO",
                gravedad=NivelGravedad.ALTA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion=f"Movimiento registrado fuera del horario laboral: {hora.strftime('%H:%M')}",
                datos_adicionales={
                    "hora": hora.isoformat(),
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "accion": accion
                },
                requiere_accion=True
            )
            alertas_generadas.append(alerta)
        
        # 2. CANTIDAD INUSUAL
        if self._es_cantidad_inusual(producto_id, cantidad):
            alerta = self._crear_alerta(
                tipo="CANTIDAD_INUSUAL",
                gravedad=NivelGravedad.MEDIA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion=f"Movimiento de cantidad inusual: {cantidad} unidades de {producto_id}",
                datos_adicionales={
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "promedio_historico": self._obtener_promedio_movimientos(producto_id)
                },
                requiere_accion=False
            )
            alertas_generadas.append(alerta)
        
        # 3. MÚLTIPLES MOVIMIENTOS RÁPIDOS
        if self._detectar_movimientos_rapidos(usuario_id, producto_id):
            alerta = self._crear_alerta(
                tipo="MOVIMIENTOS_RAPIDOS_CONSECUTIVOS",
                gravedad=NivelGravedad.ALTA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion=f"Múltiples movimientos del mismo producto en corto tiempo",
                datos_adicionales={
                    "producto_id": producto_id,
                    "movimientos_ultimos_15min": self._contar_movimientos_recientes(usuario_id, producto_id)
                },
                requiere_accion=True
            )
            alertas_generadas.append(alerta)
        
        # 4. UBICACIÓN GPS INCONSISTENTE
        if ubicacion_gps and self._es_ubicacion_sospechosa(usuario_id, ubicacion_gps):
            alerta = self._crear_alerta(
                tipo="UBICACION_GPS_SOSPECHOSA",
                gravedad=NivelGravedad.CRITICA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion=f"Movimiento desde ubicación no autorizada: {ubicacion_gps}",
                datos_adicionales={
                    "ubicacion_actual": ubicacion_gps,
                    "ubicaciones_permitidas": self._obtener_ubicaciones_permitidas(usuario_id)
                },
                requiere_accion=True
            )
            alertas_generadas.append(alerta)
        
        # 5. DISPOSITIVO NO RECONOCIDO
        if dispositivo and self._es_dispositivo_nuevo(usuario_id, dispositivo):
            alerta = self._crear_alerta(
                tipo="DISPOSITIVO_NO_RECONOCIDO",
                gravedad=NivelGravedad.MEDIA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion=f"Acceso desde dispositivo no reconocido: {dispositivo}",
                datos_adicionales={
                    "dispositivo": dispositivo,
                    "dispositivos_conocidos": self._obtener_dispositivos_conocidos(usuario_id)
                },
                requiere_accion=False
            )
            alertas_generadas.append(alerta)
        
        # 6. PATRÓN DE ROBO CONOCIDO
        if self._detectar_patron_robo(usuario_id, producto_id, cantidad, hora):
            alerta = self._crear_alerta(
                tipo="PATRON_ROBO_DETECTADO",
                gravedad=NivelGravedad.CRITICA,
                usuario_id=usuario_id,
                usuario_nombre=usuario_nombre,
                descripcion="Patrón de comportamiento coincide con casos de robo previos",
                datos_adicionales={
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "patron_coincidente": "ROBO_HORMIGA"
                },
                requiere_accion=True
            )
            alertas_generadas.append(alerta)
        
        # Procesar alertas
        for alerta in alertas_generadas:
            self._procesar_alerta(alerta)
        
        return alertas_generadas
    
    def _crear_alerta(
        self,
        tipo: str,
        gravedad: NivelGravedad,
        usuario_id: int,
        usuario_nombre: str,
        descripcion: str,
        datos_adicionales: Dict,
        requiere_accion: bool
    ) -> AlertaFraude:
        """Crea una nueva alerta de fraude"""
        self.contador_alertas += 1
        alerta = AlertaFraude(
            id=self.contador_alertas,
            tipo=tipo,
            gravedad=gravedad,
            fecha_hora=datetime.now(),
            usuario_id=usuario_id,
            usuario_nombre=usuario_nombre,
            descripcion=descripcion,
            datos_adicionales=datos_adicionales,
            requiere_accion_inmediata=requiere_accion
        )
        self.alertas.append(alerta)
        return alerta
    
    def _procesar_alerta(self, alerta: AlertaFraude):
        """Procesa una alerta: notifica y/o toma acciones"""
        # Enviar notificación según gravedad
        if alerta.gravedad in [NivelGravedad.ALTA, NivelGravedad.CRITICA]:
            # Notificar por WhatsApp a administradores
            self.notificaciones.enviar_alerta_fraude(alerta)
            alerta.notificado = True
        
        # Si requiere acción inmediata
        if alerta.requiere_accion_inmediata:
            # Bloquear temporalmente al usuario
            self._bloquear_usuario_temporal(alerta.usuario_id)
            
            # Requerir aprobación de supervisor
            self._solicitar_aprobacion_supervisor(alerta)
        
        # Guardar en base de datos
        self._guardar_alerta_db(alerta)
    
    def _es_horario_sospechoso(self, hora: datetime) -> bool:
        """Detecta si el movimiento es fuera de horario laboral"""
        hora_dia = hora.hour
        # Horario laboral: 6am - 10pm
        return hora_dia < 6 or hora_dia >= 22
    
    def _es_cantidad_inusual(self, producto_id: str, cantidad: int) -> bool:
        """Detecta si la cantidad es inusual comparada con histórico"""
        promedio = self._obtener_promedio_movimientos(producto_id)
        return cantidad > promedio * 3  # 3x el promedio
    
    def _detectar_movimientos_rapidos(self, usuario_id: int, producto_id: str) -> bool:
        """Detecta múltiples movimientos del mismo producto en poco tiempo"""
        movimientos_recientes = self._contar_movimientos_recientes(usuario_id, producto_id)
        return movimientos_recientes >= 5  # 5+ movimientos en 15 minutos
    
    def _es_ubicacion_sospechosa(self, usuario_id: int, ubicacion_gps: str) -> bool:
        """Verifica si la ubicación GPS está fuera de las permitidas"""
        # Implementar lógica de geofencing
        # Por ahora, retorna False
        return False
    
    def _es_dispositivo_nuevo(self, usuario_id: int, dispositivo: str) -> bool:
        """Verifica si el dispositivo es nuevo para el usuario"""
        dispositivos_conocidos = self._obtener_dispositivos_conocidos(usuario_id)
        return dispositivo not in dispositivos_conocidos
    
    def _detectar_patron_robo(
        self,
        usuario_id: int,
        producto_id: str,
        cantidad: int,
        hora: datetime
    ) -> bool:
        """
        Detecta patrones conocidos de robo:
        - Robo hormiga: Pequeñas cantidades frecuentes
        - Robo masivo: Grandes cantidades únicas
        - Robo coordinado: Múltiples usuarios mismo producto
        """
        # Robo hormiga: 5+ movimientos pequeños en 1 semana
        hace_semana = hora - timedelta(days=7)
        # Implementar consulta a DB
        return False
    
    def _obtener_promedio_movimientos(self, producto_id: str) -> float:
        """Obtiene el promedio histórico de movimientos de un producto"""
        # Implementar consulta a DB
        return 50.0
    
    def _contar_movimientos_recientes(self, usuario_id: int, producto_id: str) -> int:
        """Cuenta movimientos en los últimos 15 minutos"""
        # Implementar consulta a DB
        return 0
    
    def _obtener_ubicaciones_permitidas(self, usuario_id: int) -> List[str]:
        """Obtiene lista de ubicaciones GPS permitidas para usuario"""
        # Implementar consulta a DB
        return ["Almacén Principal"]
    
    def _obtener_dispositivos_conocidos(self, usuario_id: int) -> List[str]:
        """Obtiene lista de dispositivos conocidos del usuario"""
        # Implementar consulta a DB
        return []
    
    def _bloquear_usuario_temporal(self, usuario_id: int):
        """Bloquea temporalmente a un usuario sospechoso"""
        # Implementar lógica de bloqueo
        pass
    
    def _solicitar_aprobacion_supervisor(self, alerta: AlertaFraude):
        """Solicita aprobación de supervisor para continuar operación"""
        # Implementar flujo de aprobación
        pass
    
    def _guardar_alerta_db(self, alerta: AlertaFraude):
        """Guarda la alerta en base de datos"""
        # Implementar guardado
        pass
    
    def obtener_alertas_pendientes(self) -> List[AlertaFraude]:
        """Retorna alertas que requieren atención"""
        return [
            alerta for alerta in self.alertas
            if alerta.requiere_accion_inmediata and not alerta.notificado
        ]
    
    def generar_reporte_seguridad(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Dict:
        """
        Genera un reporte de seguridad con estadísticas
        """
        alertas_periodo = [
            a for a in self.alertas
            if fecha_inicio <= a.fecha_hora <= fecha_fin
        ]
        
        return {
            "periodo": {
                "inicio": fecha_inicio.isoformat(),
                "fin": fecha_fin.isoformat()
            },
            "total_alertas": len(alertas_periodo),
            "por_gravedad": {
                "critica": len([a for a in alertas_periodo if a.gravedad == NivelGravedad.CRITICA]),
                "alta": len([a for a in alertas_periodo if a.gravedad == NivelGravedad.ALTA]),
                "media": len([a for a in alertas_periodo if a.gravedad == NivelGravedad.MEDIA]),
                "baja": len([a for a in alertas_periodo if a.gravedad == NivelGravedad.BAJA])
            },
            "por_tipo": self._agrupar_por_tipo(alertas_periodo),
            "usuarios_con_mas_alertas": self._usuarios_mas_alertas(alertas_periodo),
            "productos_mas_afectados": self._productos_mas_afectados(alertas_periodo)
        }
    
    def _agrupar_por_tipo(self, alertas: List[AlertaFraude]) -> Dict[str, int]:
        """Agrupa alertas por tipo"""
        tipos = {}
        for alerta in alertas:
            tipos[alerta.tipo] = tipos.get(alerta.tipo, 0) + 1
        return tipos
    
    def _usuarios_mas_alertas(self, alertas: List[AlertaFraude]) -> List[Dict]:
        """Identifica usuarios con más alertas"""
        usuarios = {}
        for alerta in alertas:
            if alerta.usuario_id not in usuarios:
                usuarios[alerta.usuario_id] = {
                    "usuario_id": alerta.usuario_id,
                    "nombre": alerta.usuario_nombre,
                    "cantidad_alertas": 0
                }
            usuarios[alerta.usuario_id]["cantidad_alertas"] += 1
        
        return sorted(usuarios.values(), key=lambda x: x["cantidad_alertas"], reverse=True)[:10]
    
    def _productos_mas_afectados(self, alertas: List[AlertaFraude]) -> List[Dict]:
        """Identifica productos más afectados por alertas"""
        productos = {}
        for alerta in alertas:
            producto_id = alerta.datos_adicionales.get("producto_id")
            if producto_id:
                productos[producto_id] = productos.get(producto_id, 0) + 1
        
        return [
            {"producto_id": k, "cantidad_alertas": v}
            for k, v in sorted(productos.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
