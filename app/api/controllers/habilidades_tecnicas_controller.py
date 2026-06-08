"""
Habilidades Técnicas Controller
Handles HTTP requests for Habilidades Técnicas module
"""

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

from app.services.habilidades_tecnicas_service import (
    build_dashboard,
    get_kpi_metrics,
    get_matriz_operacional,
    get_nivel_tecnico,
    invalidate_cache,
)
from app.schemas.habilidades_tecnicas_schema import (
    DashboardHabilidadesTecnicasSchema,
    MatrizOperacionalSchema,
    KPITecnicasSchema,
    NivelTecnicoSchema,
)

router = APIRouter(prefix="/api/habilidades-tecnicas", tags=["Habilidades Técnicas"])


@router.get("/dashboard", response_model=DashboardHabilidadesTecnicasSchema)
def get_tecnicas_dashboard(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """
    Dashboard completo de habilidades técnicas.

    Incluye:
    - Resumen global (total encuestados, mapeados, % impacto)
    - Subcategorías técnicas con votos y porcentajes
    - Timestamp de última actualización
    - Análisis de insights
    """
    try:
        return build_dashboard(force_refresh=force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matriz", response_model=MatrizOperacionalSchema)
def get_matriz(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener la Matriz Operacional de Requerimientos — distribución de categorías técnicas."""
    try:
        return get_matriz_operacional(force_refresh=force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kpi", response_model=KPITecnicasSchema)
def get_kpi(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """Obtener indicadores KPI del módulo técnico, incluyendo categoría líder."""
    try:
        return get_kpi_metrics(force_refresh=force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reload")
def reload_data():
    """Invalida la caché y fuerza recarga completa desde Google Sheets."""
    invalidate_cache()
    build_dashboard(force_refresh=True)
    return {"message": "Caché de Habilidades Técnicas invalidada y recargada con éxito"}


@router.get("/nivel", response_model=NivelTecnicoSchema)
def get_nivel(
    force_refresh: bool = Query(default=False, description="Forzar recarga desde Google Sheets")
):
    """
    Obtener métricas de nivel técnico y preparación laboral.

    - **conocimiento_tecnico_promedio**: promedio Likert escalado a 0–20
    - **porcentaje_aplicacion_real**: promedio Likert escalado a 0–100%
    """
    try:
        return get_nivel_tecnico(force_refresh=force_refresh)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
