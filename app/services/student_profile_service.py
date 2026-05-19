"""
Student Profile Service
Business logic layer for student profile module
"""

import logging

from app.schemas.student_profile_schema import (
    DashboardPerfilEstudiante,
    KPIMetricsSchema,
    DistribucionGeneroSchema,
    DistribucionCarreraSchema,
    DistribucionDistritoSchema,
    DistribucionSemestreSchema,
    DistribucionEdadSchema,
    RiesgoPorSemestreSchema
)
from app.etl.student_profile_etl import StudentProfileETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_dashboard() -> DashboardPerfilEstudiante:
    """Build complete student profile dashboard"""
    logger.info("Building student profile dashboard...")
    
    etl = StudentProfileETL()
    data = etl.get_complete_dashboard_data()
    
    return DashboardPerfilEstudiante(
        indicadores_kpi=KPIMetricsSchema(**data['indicadores_kpi']),
        distribucion_genero=DistribucionGeneroSchema(**data['distribucion_genero']),
        distribucion_carreras=[DistribucionCarreraSchema(**c) for c in data['distribucion_carreras']],
        distribucion_distritos=[DistribucionDistritoSchema(**d) for d in data['distribucion_distritos']],
        distribucion_semestres=[DistribucionSemestreSchema(**s) for s in data['distribucion_semestres']],
        distribucion_edades=[DistribucionEdadSchema(**a) for a in data['distribucion_edades']],
        riesgo_por_semestre=[RiesgoPorSemestreSchema(**r) for r in data['riesgo_por_semestre']],
        analisis_insights=data['analisis_insights']
    )


def get_kpi_metrics() -> KPIMetricsSchema:
    """Get only KPI metrics"""
    etl = StudentProfileETL()
    return KPIMetricsSchema(**etl.get_kpi_metrics())


def get_gender_distribution() -> DistribucionGeneroSchema:
    """Get gender distribution"""
    etl = StudentProfileETL()
    return DistribucionGeneroSchema(**etl.get_gender_distribution())


def get_career_distribution() -> list:
    """Get career distribution"""
    etl = StudentProfileETL()
    return [DistribucionCarreraSchema(**c) for c in etl.get_career_distribution()]


def get_district_distribution(top_n: int = 6) -> list:
    """Get district distribution"""
    etl = StudentProfileETL()
    return [DistribucionDistritoSchema(**d) for d in etl.get_district_distribution(top_n)]


def get_semester_distribution() -> list:
    """Get semester distribution"""
    etl = StudentProfileETL()
    return [DistribucionSemestreSchema(**s) for s in etl.get_semester_distribution()]


def get_age_distribution() -> list:
    """Get age distribution"""
    etl = StudentProfileETL()
    return [DistribucionEdadSchema(**a) for a in etl.get_age_distribution()]


def get_risk_by_semester() -> list:
    """Get risk distribution by semester"""
    etl = StudentProfileETL()
    return [RiesgoPorSemestreSchema(**r) for r in etl.get_risk_by_semester()]


def get_insights() -> str:
    """Get analysis insights"""
    etl = StudentProfileETL()
    return etl.generate_insights()
def get_tasa_retencion():
    """
    Tasa de retención académica
    """
    return {
        "tasa_actual": 92.0,
        "meta_institucional": 95.0,
        "cumple_meta": False,
        "diferencia": -3.0
    }
