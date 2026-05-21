"""
Habilidades Blandas Schemas
Pydantic models for API request/response serialization
"""

from pydantic import BaseModel
from typing import List


class KPIMetricsBlandasSchema(BaseModel):
    """KPI metrics schema for soft skills"""
    total_estudiantes: int
    promedio_general: float
    satisfaccion_institucion_pct: float
    interes_formacion_pct: float

    class Config:
        from_attributes = True


class HabilidadPromedioSchema(BaseModel):
    """Average rating schema for a soft skill"""
    habilidad: str
    promedio: float
    nivel: str

    class Config:
        from_attributes = True


class CategorizacionHabilidadSchema(BaseModel):
    """Categorized open response schema"""
    categoria: str
    cantidad_estudiantes: int
    porcentaje: float

    class Config:
        from_attributes = True


class SatisfaccionDetalleSchema(BaseModel):
    """Yes/No response frequency detail schema"""
    respuesta: str
    cantidad: int
    porcentaje: float

    class Config:
        from_attributes = True


class DashboardHabilidadesBlandasSchema(BaseModel):
    """Complete dashboard metrics schema for Habilidades Blandas"""
    indicadores_kpi: KPIMetricsBlandasSchema
    promedios_habilidades: List[HabilidadPromedioSchema]
    habilidades_a_mejorar: List[CategorizacionHabilidadSchema]
    satisfaccion_institucion: List[SatisfaccionDetalleSchema]
    interes_formacion: List[SatisfaccionDetalleSchema]
    last_updated: str
    analisis_insights: str

    class Config:
        from_attributes = True
