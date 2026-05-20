"""
Digital Skills Data Models
Data classes for type-safe data handling
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class KPIMetricsDigitalSkills:
    """KPI metrics for digital skills summary cards"""
    dominio_promedio: float
    capacitacion_completada: float
    uso_diario_promedio: float
    alertas_nivel_bajo: int
    total_estudiantes: int
    
    def to_dict(self) -> dict:
        return {
            'dominio_promedio': self.dominio_promedio,
            'capacitacion_completada': self.capacitacion_completada,
            'uso_diario_promedio': self.uso_diario_promedio,
            'alertas_nivel_bajo': self.alertas_nivel_bajo,
            'total_estudiantes': self.total_estudiantes
        }


@dataclass
class HerramientaOfimática:
    """Dominio de herramientas ofimáticas"""
    herramienta: str
    porcentaje_dominio: float
    nivel_promedio: float
    estudiantes_usan: int
    
    def to_dict(self) -> dict:
        return {
            'herramienta': self.herramienta,
            'porcentaje_dominio': self.porcentaje_dominio,
            'nivel_promedio': self.nivel_promedio,
            'estudiantes_usan': self.estudiantes_usan
        }


@dataclass
class PlataformaLenguaje:
    """Plataformas y lenguajes de programación"""
    categoria: str
    dominio: int  # 1-5 scale
    capacitacion: str  # Si/No
    nivel_texto: str  # Básico/Intermedio/Avanzado
    
    def to_dict(self) -> dict:
        return {
            'categoria': self.categoria,
            'dominio': self.dominio,
            'capacitacion': self.capacitacion,
            'nivel_texto': self.nivel_texto
        }


@dataclass
class EstudianteHabilidades:
    """Desglose individual de habilidades por estudiante"""
    expediente: str
    estudiante: str
    ofimatica: float
    programacion: float
    frecuencia_hrs: float
    estado: str  # COMPETENTE/EXCELENTE/EN FORMACIÓN/REGULAR
    
    def to_dict(self) -> dict:
        return {
            'expediente': self.expediente,
            'estudiante': self.estudiante,
            'ofimatica': self.ofimatica,
            'programacion': self.programacion,
            'frecuencia_hrs': self.frecuencia_hrs,
            'estado': self.estado
        }


@dataclass
class DigitalSkillsDashboard:
    """Complete dashboard data for digital skills module"""
    kpi_metrics: KPIMetricsDigitalSkills
    herramientas_ofimaticas: List[HerramientaOfimática]
    plataformas_lenguajes: List[PlataformaLenguaje]
    estudiantes_habilidades: List[EstudianteHabilidades]
    conclusiones_modulo: str
    acciones_recomendadas: List[str]
    proxima_evaluacion: str
    last_updated: str
    
    def to_dict(self) -> dict:
        return {
            'kpi_metrics': self.kpi_metrics.to_dict(),
            'herramientas_ofimaticas': [h.to_dict() for h in self.herramientas_ofimaticas],
            'plataformas_lenguajes': [p.to_dict() for p in self.plataformas_lenguajes],
            'estudiantes_habilidades': [e.to_dict() for e in self.estudiantes_habilidades],
            'conclusiones_modulo': self.conclusiones_modulo,
            'acciones_recomendadas': self.acciones_recomendadas,
            'proxima_evaluacion': self.proxima_evaluacion,
            'last_updated': self.last_updated
        }