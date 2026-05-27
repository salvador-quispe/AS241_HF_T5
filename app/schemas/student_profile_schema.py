"""
Student Profile Schemas
Pydantic models for request/response validation
"""

from typing import List
from pydantic import BaseModel, Field


class KPIMetricsSchema(BaseModel):
    total_estudiantes: int = Field(..., description="Total de estudiantes encuestados")
    edad_promedio: float = Field(..., description="Edad promedio de estudiantes")
    edad_minima: int = Field(..., description="Edad mínima")
    edad_maxima: int = Field(..., description="Edad máxima")
    estudiantes_riesgo: int = Field(..., description="Estudiantes con baja preparación laboral")
    logro_institucional: float = Field(..., description="Estudiantes que indicaron preparación institucional adecuada (%)")


class PreparacionLaboralSchema(BaseModel):
    level: str = Field(..., description="Nivel de preparacion laboral")
    student_count: int = Field(..., description="Cantidad de estudiantes")
    percentage: float = Field(..., description="Porcentaje del total")


class DistribucionDistritoSchema(BaseModel):
    distrito: str = Field(..., description="Nombre del distrito")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje_participacion: float = Field(..., description="Porcentaje de participación")


class DistribucionSemestreSchema(BaseModel):
    semestre: str = Field(..., description="Semestre académico")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje: float = Field(..., description="Porcentaje del total")


class DistribucionEdadSchema(BaseModel):
    rango_edad: str = Field(..., description="Rango de edad")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje: float = Field(..., description="Porcentaje del total")


class RiesgoPorSemestreSchema(BaseModel):
    semestre: str = Field(..., description="Semestre académico")
    total_estudiantes: int = Field(..., description="Total de estudiantes en el semestre")
    estudiantes_riesgo: int = Field(..., description="Estudiantes en riesgo académico")
    porcentaje_riesgo: float = Field(..., description="Porcentaje de riesgo")


class DashboardPerfilEstudiante(BaseModel):
    indicadores_kpi: KPIMetricsSchema
    job_readiness_distribution: List[PreparacionLaboralSchema]
    distribucion_distritos: List[DistribucionDistritoSchema]
    distribucion_semestres: List[DistribucionSemestreSchema]
    distribucion_edades: List[DistribucionEdadSchema]
    riesgo_por_semestre: List[RiesgoPorSemestreSchema]
    analisis_insights: str = Field(..., description="Insights descriptivos del análisis")
