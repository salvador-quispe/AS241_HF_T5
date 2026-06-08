"""
Habilidades Técnicas Schemas
Pydantic v2 models for API request/response serialization
"""

from pydantic import BaseModel, ConfigDict
from typing import List


class ResumenGlobalTecnicoSchema(BaseModel):
    """Global summary metrics schema for technical skills"""
    model_config = ConfigDict(from_attributes=True)

    total_encuestados: int
    total_mapeados: int
    porcentaje_impacto_global: float


class SubcategoriaTecnicaSchema(BaseModel):
    """Category breakdown schema for a technical skill"""
    model_config = ConfigDict(from_attributes=True)

    categoria: str
    votos: int
    porcentaje_del_subtotal: float


class DashboardHabilidadesTecnicasSchema(BaseModel):
    """Complete dashboard schema for Habilidades Técnicas"""
    model_config = ConfigDict(from_attributes=True)

    resumen_global: ResumenGlobalTecnicoSchema
    subcategorias_tecnicas: List[SubcategoriaTecnicaSchema]
    last_updated: str
    analisis_insights: str


class MatrizOperacionalSchema(BaseModel):
    """Matriz Operacional de Requerimientos response schema"""
    model_config = ConfigDict(from_attributes=True)

    subcategorias: List[SubcategoriaTecnicaSchema]


class KPITecnicasSchema(BaseModel):
    """KPI metrics schema for Habilidades Técnicas"""
    model_config = ConfigDict(from_attributes=True)

    total_encuestados: int
    total_mapeados: int
    porcentaje_impacto_global: float
    categoria_lider: str


class NivelTecnicoSchema(BaseModel):
    """Technical knowledge level and job readiness metrics schema"""
    model_config = ConfigDict(from_attributes=True)

    conocimiento_tecnico_promedio: float   # scale 0–20
    porcentaje_aplicacion_real: float      # scale 0–100
    promedio_conocimiento_raw: float       # Likert 1–5
    promedio_aplicacion_raw: float         # Likert 1–5
    total_respondentes: int
