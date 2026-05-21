"""
Habilidades Blandas Controller
Handles HTTP requests for Habilidades Blandas module
"""

from fastapi import APIRouter, Query
from typing import List

from app.services.habilidades_blandas_service import (
    build_dashboard,
    get_kpi_metrics,
    get_promedios_habilidades,
    get_habilidades_a_mejorar,
    get_satisfaccion_institucion,
    get_interes_formacion,
    get_insights,
    invalidate_cache
)
from app.schemas.habilidades_blandas_schema import (
    DashboardHabilidadesBlandasSchema,
    KPIMetricsBlandasSchema,
    HabilidadPromedioSchema,
    CategorizacionHabilidadSchema,
    SatisfaccionDetalleSchema
)

router = APIRouter(prefix="/api/habilidades-blandas", tags=["Habilidades Blandas"])


@router.get("/dashboard", response_model=DashboardHabilidadesBlandasSchema)
def get_habilidades_dashboard(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """
    Dashboard completo de habilidades blandas.
    
    Incluye:
    - Indicadores KPI
    - Promedios de las 5 habilidades
    - Frecuencias de habilidades a mejorar
    - Satisfacción con la institución
    - Interés en formación
    - Análisis de Insights
    """
    return build_dashboard(force_refresh=force_refresh)


@router.get("/kpi", response_model=KPIMetricsBlandasSchema)
def get_kpi(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener únicamente indicadores KPI principales"""
    return get_kpi_metrics(force_refresh=force_refresh)


@router.get("/promedios", response_model=List[HabilidadPromedioSchema])
def get_promedios(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener el promedio de puntuación por cada habilidad blanda"""
    return get_promedios_habilidades(force_refresh=force_refresh)


@router.get("/mejorar", response_model=List[CategorizacionHabilidadSchema])
def get_mejorar(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener la distribución categorizada de las habilidades que necesitan mejorar"""
    return get_habilidades_a_mejorar(force_refresh=force_refresh)


@router.get("/satisfaccion", response_model=List[SatisfaccionDetalleSchema])
def get_satisfaccion(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener detalle de satisfacción de preparación institucional"""
    return get_satisfaccion_institucion(force_refresh=force_refresh)


@router.get("/interes", response_model=List[SatisfaccionDetalleSchema])
def get_interes(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener detalle de interés en recibir más formación"""
    return get_interes_formacion(force_refresh=force_refresh)


@router.get("/insights", response_model=str)
def get_insights_endpoint(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener insights redactados y análisis de tendencias"""
    return get_insights(force_refresh=force_refresh)


@router.post("/reload")
def reload_data_endpoint():
    """Fuerza la invalidación de la caché y recarga de datos"""
    invalidate_cache()
    # Force a load to repopulate cache
    build_dashboard(force_refresh=True)
    return {"message": "Caché de Habilidades Blandas invalidada y recargada con éxito"}
