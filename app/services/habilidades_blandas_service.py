"""
Habilidades Blandas Service
Business logic layer for Habilidades Blandas module
"""

import logging
from typing import Dict, Any, List

from app.config.database import SHEET_URL
from app.repositories.habilidades_blandas_repository import HabilidadesBlandasRepository
from app.schemas.habilidades_blandas_schema import (
    DashboardHabilidadesBlandasSchema,
    KPIMetricsBlandasSchema,
    HabilidadPromedioSchema,
    CategorizacionHabilidadSchema,
    SatisfaccionDetalleSchema
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate singleton repository
repository = HabilidadesBlandasRepository(SHEET_URL)


def build_dashboard(force_refresh: bool = False) -> DashboardHabilidadesBlandasSchema:
    """
    Build the complete Habilidades Blandas dashboard
    """
    logger.info("Building Habilidades Blandas dashboard...")
    data = repository.get_dashboard_data(force_refresh=force_refresh)

    if not data:
        logger.warning("No data retrieved from repository")
        return DashboardHabilidadesBlandasSchema(
            indicadores_kpi=KPIMetricsBlandasSchema(
                total_estudiantes=0,
                promedio_general=0.0,
                satisfaccion_institucion_pct=0.0,
                interes_formacion_pct=0.0
            ),
            promedios_habilidades=[],
            habilidades_a_mejorar=[],
            satisfaccion_institucion=[],
            interes_formacion=[],
            last_updated="",
            analisis_insights=""
        )

    return DashboardHabilidadesBlandasSchema(
        indicadores_kpi=KPIMetricsBlandasSchema(**data['indicadores_kpi']),
        promedios_habilidades=[HabilidadPromedioSchema(**p) for p in data['promedios_habilidades']],
        habilidades_a_mejorar=[CategorizacionHabilidadSchema(**h) for h in data['habilidades_a_mejorar']],
        satisfaccion_institucion=[SatisfaccionDetalleSchema(**s) for s in data['satisfaccion_institucion']],
        interes_formacion=[SatisfaccionDetalleSchema(**i) for i in data['interes_formacion']],
        last_updated=data['last_updated'],
        analisis_insights=data['analisis_insights']
    )


def get_kpi_metrics(force_refresh: bool = False) -> KPIMetricsBlandasSchema:
    """Get only KPI metrics for Habilidades Blandas"""
    etl = repository.load_data(force_refresh)
    if etl:
        kpi = etl.get_kpi_metrics()
        return KPIMetricsBlandasSchema(
            total_estudiantes=kpi.total_estudiantes,
            promedio_general=kpi.promedio_general,
            satisfaccion_institucion_pct=kpi.satisfaccion_institucion_pct,
            interes_formacion_pct=kpi.interes_formacion_pct
        )
    return KPIMetricsBlandasSchema(
        total_estudiantes=0,
        promedio_general=0.0,
        satisfaccion_institucion_pct=0.0,
        interes_formacion_pct=0.0
    )


def get_promedios_habilidades(force_refresh: bool = False) -> List[HabilidadPromedioSchema]:
    """Get soft skills average scores list"""
    etl = repository.load_data(force_refresh)
    if etl:
        return [HabilidadPromedioSchema(
            habilidad=p.habilidad,
            promedio=p.promedio,
            nivel=p.nivel
        ) for p in etl.get_promedios_habilidades()]
    return []


def get_habilidades_a_mejorar(force_refresh: bool = False) -> List[CategorizacionHabilidadSchema]:
    """Get open response categorization distribution"""
    etl = repository.load_data(force_refresh)
    if etl:
        return [CategorizacionHabilidadSchema(
            categoria=h.categoria,
            cantidad_estudiantes=h.cantidad_estudiantes,
            porcentaje=h.porcentaje
        ) for h in etl.get_habilidades_a_mejorar()]
    return []


def get_satisfaccion_institucion(force_refresh: bool = False) -> List[SatisfaccionDetalleSchema]:
    """Get institutional prep satisfaction detail"""
    etl = repository.load_data(force_refresh)
    if etl:
        return [SatisfaccionDetalleSchema(
            respuesta=s.respuesta,
            cantidad=s.cantidad,
            porcentaje=s.porcentaje
        ) for s in etl.get_satisfaccion_institucion()]
    return []


def get_interes_formacion(force_refresh: bool = False) -> List[SatisfaccionDetalleSchema]:
    """Get training interest detail"""
    etl = repository.load_data(force_refresh)
    if etl:
        return [SatisfaccionDetalleSchema(
            respuesta=i.respuesta,
            cantidad=i.cantidad,
            porcentaje=i.porcentaje
        ) for i in etl.get_interes_formacion()]
    return []


def get_insights(force_refresh: bool = False) -> str:
    """Get soft skills analysis insights text"""
    etl = repository.load_data(force_refresh)
    if etl:
        return etl.generate_insights()
    return ""


def invalidate_cache():
    """Clear repository caching"""
    repository.invalidate_cache()
