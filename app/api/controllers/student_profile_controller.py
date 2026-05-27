"""
Student Profile Controller
Handles HTTP requests for student profile module
"""

from fastapi import APIRouter, Query
from typing import List

from app.services.student_profile_service import (
    build_dashboard,
    get_kpi_metrics,
    get_job_readiness_distribution,
    get_district_distribution,
    get_semester_distribution,
    get_age_distribution,
    get_risk_by_semester,
    get_insights
)
from app.schemas.student_profile_schema import (
    DashboardPerfilEstudiante,
    KPIMetricsSchema,
    PreparacionLaboralSchema,
    DistribucionDistritoSchema,
    DistribucionSemestreSchema,
    DistribucionEdadSchema,
    RiesgoPorSemestreSchema
)

router = APIRouter(prefix="/api/perfil-estudiante", tags=["Perfil del Estudiante"])


@router.get("/dashboard", response_model=DashboardPerfilEstudiante)
def get_perfil_dashboard():
    """
    Dashboard completo del perfil del estudiante.
    
    Incluye:
    - KPI principales (total estudiantes, edad promedio, etc.)
    - Distribución por preparación laboral
    - Distribución por distrito
    - Distribución por semestre
    - Distribución por rangos de edad
    - Riesgo académico por semestre
    - Insights descriptivos
    """
    return build_dashboard()


@router.get("/kpi", response_model=KPIMetricsSchema)
def get_kpi():
    """Solo indicadores KPI principales"""
    return get_kpi_metrics()


@router.get("/job-readiness-distribution", response_model=List[PreparacionLaboralSchema])
def get_job_readiness_distribution_endpoint():
    """Distribución por preparación laboral"""
    return get_job_readiness_distribution()


@router.get("/distritos", response_model=List[DistribucionDistritoSchema])
def get_distritos(
    top_n: int = Query(6, ge=1, le=20, description="Número de distritos a mostrar")
):
    """Distribución por distrito de procedencia"""
    return get_district_distribution(top_n)


@router.get("/semestres", response_model=List[DistribucionSemestreSchema])
def get_semestres():
    """Distribución por semestre académico"""
    return get_semester_distribution()


@router.get("/edades", response_model=List[DistribucionEdadSchema])
def get_edades():
    """Distribución por rangos de edad"""
    return get_age_distribution()


@router.get("/riesgo", response_model=List[RiesgoPorSemestreSchema])
def get_riesgo():
    """Estudiantes en riesgo académico por semestre"""
    return get_risk_by_semester()


@router.get("/insights", response_model=str)
def get_insights_endpoint():
    """Insights descriptivos del análisis"""
    return get_insights()
