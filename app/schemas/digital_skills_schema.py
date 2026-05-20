"""
Digital Skills Schemas
Pydantic models for request/response validation
"""

from typing import List
from pydantic import BaseModel, Field


class KPIMetricsDigitalSkillsSchema(BaseModel):
    dominio_promedio: float = Field(..., description="Dominio promedio de herramientas digitales (1-5)")
    capacitacion_completada: float = Field(..., description="Porcentaje de estudiantes con capacitación")
    uso_diario_promedio: float = Field(..., description="Horas promedio de uso diario")
    alertas_nivel_bajo: int = Field(..., description="Estudiantes que requieren capacitación inmediata")
    total_estudiantes: int = Field(..., description="Total de estudiantes evaluados")


class HerramientaOfimáticaSchema(BaseModel):
    herramienta: str = Field(..., description="Nombre de la herramienta ofimática")
    categoria: str = Field(..., description="Categoría de la herramienta (Ofimática/Programación/IA/Otras)")
    porcentaje_dominio: float = Field(..., description="Porcentaje de dominio")
    nivel_promedio: float = Field(..., description="Nivel promedio de dominio")
    estudiantes_usan: int = Field(..., description="Cantidad de estudiantes que la usan")


class PlataformaLenguajeSchema(BaseModel):
    categoria: str = Field(..., description="Categoría de la plataforma/lenguaje")
    dominio: int = Field(..., ge=1, le=5, description="Nivel de dominio (1-5)")
    capacitacion: str = Field(..., description="Ha recibido capacitación (Si/No)")
    nivel_texto: str = Field(..., description="Nivel en texto (Básico/Intermedio/Avanzado)")
    estudiantes: int = Field(..., description="Cantidad de estudiantes que usan esta herramienta")


class EstudianteHabilidadesSchema(BaseModel):
    expediente: str = Field(..., description="Número de expediente del estudiante")
    estudiante: str = Field(..., description="Nombre del estudiante")
    ofimatica: float = Field(..., description="Puntuación en ofimática")
    programacion: float = Field(..., description="Puntuación en programación")
    frecuencia_hrs: float = Field(..., description="Horas de uso frecuente")
    estado: str = Field(..., description="Estado de competencia")


class DashboardHabilidadesDigitales(BaseModel):
    indicadores_kpi: KPIMetricsDigitalSkillsSchema
    herramientas_ofimaticas: List[HerramientaOfimáticaSchema]
    plataformas_lenguajes: List[PlataformaLenguajeSchema]
    estudiantes_habilidades: List[EstudianteHabilidadesSchema]
    conclusiones_modulo: str = Field(..., description="Conclusiones del análisis")
    acciones_recomendadas: List[str] = Field(..., description="Acciones recomendadas")
    proxima_evaluacion: str = Field(..., description="Fecha de próxima evaluación")