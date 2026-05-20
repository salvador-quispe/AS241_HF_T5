"""
Digital Skills Service
Business logic layer for digital skills module
"""

import logging

from app.schemas.digital_skills_schema import (
    DashboardHabilidadesDigitales,
    KPIMetricsDigitalSkillsSchema,
    HerramientaOfimáticaSchema,
    PlataformaLenguajeSchema,
    EstudianteHabilidadesSchema
)
from app.etl.digital_skills_etl import DigitalSkillsETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_dashboard() -> DashboardHabilidadesDigitales:
    """Build complete digital skills dashboard"""
    logger.info("Building digital skills dashboard...")
    
    etl = DigitalSkillsETL()
    data = etl.get_complete_dashboard_data()
    
    return DashboardHabilidadesDigitales(
        indicadores_kpi=KPIMetricsDigitalSkillsSchema(**data['indicadores_kpi']),
        herramientas_ofimaticas=[HerramientaOfimáticaSchema(**h) for h in data['herramientas_ofimaticas']],
        plataformas_lenguajes=[PlataformaLenguajeSchema(**p) for p in data['plataformas_lenguajes']],
        estudiantes_habilidades=[EstudianteHabilidadesSchema(**e) for e in data['estudiantes_habilidades']],
        conclusiones_modulo=data['conclusiones_modulo'],
        acciones_recomendadas=data['acciones_recomendadas'],
        proxima_evaluacion=data['proxima_evaluacion']
    )


def get_kpi_metrics() -> KPIMetricsDigitalSkillsSchema:
    """Get only KPI metrics for digital skills"""
    etl = DigitalSkillsETL()
    return KPIMetricsDigitalSkillsSchema(**etl.get_kpi_metrics())


def get_herramientas_ofimaticas() -> list:
    """Get office tools usage data"""
    etl = DigitalSkillsETL()
    return [HerramientaOfimáticaSchema(**h) for h in etl.get_herramientas_ofimaticas()]


def get_plataformas_lenguajes() -> list:
    """Get programming platforms and languages data"""
    etl = DigitalSkillsETL()
    return [PlataformaLenguajeSchema(**p) for p in etl.get_plataformas_lenguajes()]


def get_estudiantes_habilidades(limit: int = 10) -> list:
    """Get individual student digital skills data"""
    etl = DigitalSkillsETL()
    return [EstudianteHabilidadesSchema(**e) for e in etl.get_estudiantes_habilidades(limit)]


def get_conclusions() -> str:
    """Get analysis conclusions"""
    etl = DigitalSkillsETL()
    return etl.generate_conclusions()


def get_recommended_actions() -> list:
    """Get recommended actions"""
    etl = DigitalSkillsETL()
    return etl.generate_recommended_actions()


def get_next_evaluation() -> str:
    """Get next evaluation date"""
    etl = DigitalSkillsETL()
    return etl.get_proxima_evaluacion()