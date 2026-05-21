"""
Habilidades Blandas Data Models
Data classes for type-safe data handling — Módulo Habilidades Blandas
"""

from dataclasses import dataclass
from typing import List


@dataclass
class KPIMetricsBlandas:
    """KPI metrics for habilidades blandas dashboard summary cards"""
    total_estudiantes: int
    promedio_general: float
    satisfaccion_institucion_pct: float
    interes_formacion_pct: float

    def to_dict(self) -> dict:
        return {
            'total_estudiantes': self.total_estudiantes,
            'promedio_general': self.promedio_general,
            'satisfaccion_institucion_pct': self.satisfaccion_institucion_pct,
            'interes_formacion_pct': self.interes_formacion_pct
        }


@dataclass
class HabilidadPromedio:
    """Average score and description for a specific soft skill"""
    habilidad: str
    promedio: float
    nivel: str

    def to_dict(self) -> dict:
        return {
            'habilidad': self.habilidad,
            'promedio': round(self.promedio, 2),
            'nivel': self.nivel
        }


@dataclass
class CategorizacionHabilidad:
    """Categorized response counts for open-ended text answers"""
    categoria: str
    cantidad_estudiantes: int
    porcentaje: float

    def to_dict(self) -> dict:
        return {
            'categoria': self.categoria,
            'cantidad_estudiantes': self.cantidad_estudiantes,
            'porcentaje': round(self.porcentaje, 1)
        }


@dataclass
class SatisfaccionDetalle:
    """Counts and percentages for discrete choice questions (Yes/No)"""
    respuesta: str
    cantidad: int
    porcentaje: float

    def to_dict(self) -> dict:
        return {
            'respuesta': self.respuesta,
            'cantidad': self.cantidad,
            'porcentaje': round(self.porcentaje, 1)
        }


@dataclass
class HabilidadesBlandasDashboard:
    """Complete dashboard data for habilidades blandas module"""
    indicadores_kpi: KPIMetricsBlandas
    promedios_habilidades: List[HabilidadPromedio]
    habilidades_a_mejorar: List[CategorizacionHabilidad]
    satisfaccion_institucion: List[SatisfaccionDetalle]
    interes_formacion: List[SatisfaccionDetalle]
    last_updated: str
    analisis_insights: str

    def to_dict(self) -> dict:
        return {
            'indicadores_kpi': self.indicadores_kpi.to_dict(),
            'promedios_habilidades': [p.to_dict() for p in self.promedios_habilidades],
            'habilidades_a_mejorar': [h.to_dict() for h in self.habilidades_a_mejorar],
            'satisfaccion_institucion': [s.to_dict() for s in self.satisfaccion_institucion],
            'interes_formacion': [i.to_dict() for i in self.interes_formacion],
            'last_updated': self.last_updated,
            'analisis_insights': self.analisis_insights
        }
