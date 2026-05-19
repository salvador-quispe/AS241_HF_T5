"""
Student Profile Schemas
Pydantic models for request/response validation
"""

from typing import List
from pydantic import BaseModel, Field


class KPIMetricsSchema(BaseModel):
    total_estudiantes: int = Field(..., description="Total de estudiantes encuestados")
    porcentaje_crecimiento: float = Field(..., description="Crecimiento vs ciclo anterior")
    edad_promedio: float = Field(..., description="Edad promedio de estudiantes")
    edad_minima: int = Field(..., description="Edad mínima")
    edad_maxima: int = Field(..., description="Edad máxima")
    estudiantes_riesgo: int = Field(..., description="Estudiantes que requieren reforzamiento")
    meta_institucional: int = Field(..., description="Meta institucional de satisfacción (%)")
    logro_institucional: float = Field(..., description="Logro actual institucional (%)")


class DistribucionGeneroSchema(BaseModel):
    hombres: int = Field(..., description="Cantidad de hombres")
    mujeres: int = Field(..., description="Cantidad de mujeres")
    porcentaje_hombres: float = Field(..., description="Porcentaje de hombres")
    porcentaje_mujeres: float = Field(..., description="Porcentaje de mujeres")


class DistribucionCarreraSchema(BaseModel):
    carrera: str = Field(..., description="Nombre de la carrera")
    hombres: int = Field(..., description="Cantidad de hombres")
    mujeres: int = Field(..., description="Cantidad de mujeres")
    total: int = Field(..., description="Total de estudiantes")
    porcentaje: float = Field(..., description="Porcentaje del total")


class DistribucionDistritoSchema(BaseModel):
    distrito: str = Field(..., description="Nombre del distrito")
    provincia: str = Field(..., description="Provincia")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje_participacion: float = Field(..., description="Porcentaje de participación")


class DistribucionSemestreSchema(BaseModel):
    semestre: int = Field(..., description="Número de semestre")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje: float = Field(..., description="Porcentaje del total")


class DistribucionEdadSchema(BaseModel):
    rango_edad: str = Field(..., description="Rango de edad")
    cantidad_estudiantes: int = Field(..., description="Cantidad de estudiantes")
    porcentaje: float = Field(..., description="Porcentaje del total")


class RiesgoPorSemestreSchema(BaseModel):
    semestre: int = Field(..., description="Número de semestre")
    total_estudiantes: int = Field(..., description="Total de estudiantes en el semestre")
    estudiantes_riesgo: int = Field(..., description="Estudiantes en riesgo académico")
    porcentaje_riesgo: float = Field(..., description="Porcentaje de riesgo")


class DashboardPerfilEstudiante(BaseModel):
    indicadores_kpi: KPIMetricsSchema
    distribucion_genero: DistribucionGeneroSchema
    distribucion_carreras: List[DistribucionCarreraSchema]
    distribucion_distritos: List[DistribucionDistritoSchema]
    distribucion_semestres: List[DistribucionSemestreSchema]
    distribucion_edades: List[DistribucionEdadSchema]
    riesgo_por_semestre: List[RiesgoPorSemestreSchema]
    analisis_insights: str = Field(..., description="Insights y recomendaciones del análisis")