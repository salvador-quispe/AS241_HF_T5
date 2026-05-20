"""
Digital Skills Controller
Handles HTTP requests for digital skills module
"""

from fastapi import APIRouter, Query
from typing import List

from app.services.digital_skills_service import (
    build_dashboard,
    get_kpi_metrics,
    get_herramientas_ofimaticas,
    get_plataformas_lenguajes,
    get_estudiantes_habilidades,
    get_conclusions,
    get_recommended_actions,
    get_next_evaluation
)
from app.schemas.digital_skills_schema import (
    DashboardHabilidadesDigitales,
    KPIMetricsDigitalSkillsSchema,
    HerramientaOfimáticaSchema,
    PlataformaLenguajeSchema,
    EstudianteHabilidadesSchema
)

router = APIRouter(prefix="/api/habilidades-digitales", tags=["Habilidades Digitales"])


@router.get("/dashboard", response_model=DashboardHabilidadesDigitales)
def get_habilidades_digitales_dashboard():
    """
    Dashboard completo de habilidades digitales.
    
    Incluye:
    - KPI principales (dominio promedio, capacitación, uso diario, alertas)
    - Dominio de herramientas ofimáticas
    - Plataformas y lenguajes de programación
    - Desglose individual por estudiante
    - Conclusiones del módulo
    - Acciones recomendadas
    - Próxima evaluación
    """
    return build_dashboard()


@router.get("/kpi", response_model=KPIMetricsDigitalSkillsSchema)
def get_kpi():
    """Indicadores KPI principales de habilidades digitales"""
    return get_kpi_metrics()


@router.get("/herramientas-ofimaticas", response_model=List[HerramientaOfimáticaSchema])
def get_herramientas():
    """Dominio de herramientas ofimáticas (Excel, Word, PowerPoint, Teams)"""
    return get_herramientas_ofimaticas()


@router.get("/plataformas-lenguajes", response_model=List[PlataformaLenguajeSchema])
def get_plataformas():
    """Plataformas y lenguajes de programación (SQL, Python, LMS, Web)"""
    return get_plataformas_lenguajes()


@router.get("/estudiantes", response_model=List[EstudianteHabilidadesSchema])
def get_estudiantes(
    limit: int = Query(10, ge=1, le=50, description="Número de estudiantes a mostrar")
):
    """Desglose de habilidades por estudiante individual"""
    return get_estudiantes_habilidades(limit)


@router.get("/conclusiones", response_model=str)
def get_conclusiones():
    """Conclusiones del análisis de habilidades digitales"""
    return get_conclusions()


@router.get("/acciones-recomendadas", response_model=List[str])
def get_acciones():
    """Acciones recomendadas basadas en el análisis"""
    return get_recommended_actions()


@router.get("/proxima-evaluacion", response_model=str)
def get_evaluacion():
    """Fecha de la próxima evaluación"""
    return get_next_evaluation()