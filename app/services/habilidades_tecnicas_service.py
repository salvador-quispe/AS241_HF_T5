"""
Habilidades Técnicas Service
Business logic layer for Habilidades Técnicas module
"""

import logging
from typing import List

from app.config.database import SHEET_URL_TECNICAS
from app.repositories.habilidades_tecnicas_repository import HabilidadesTecnicasRepository
from app.etl.habilidades_tecnicas_etl import PATRONES_TECNICOS
from app.schemas.habilidades_tecnicas_schema import (
    DashboardHabilidadesTecnicasSchema,
    ResumenGlobalTecnicoSchema,
    SubcategoriaTecnicaSchema,
    MatrizOperacionalSchema,
    KPITecnicasSchema,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Singleton repository instance
repository = HabilidadesTecnicasRepository(SHEET_URL_TECNICAS)


def build_dashboard(force_refresh: bool = False) -> DashboardHabilidadesTecnicasSchema:
    """Build the complete Habilidades Técnicas dashboard."""
    logger.info("Building Habilidades Técnicas dashboard...")
    data = repository.get_dashboard_data(force_refresh=force_refresh)

    if not data:
        logger.warning("No data retrieved from repository — returning defaults")
        return DashboardHabilidadesTecnicasSchema(
            resumen_global=ResumenGlobalTecnicoSchema(
                total_encuestados=0,
                total_mapeados=0,
                porcentaje_impacto_global=0.0
            ),
            subcategorias_tecnicas=[],
            last_updated="",
            analisis_insights=""
        )

    return DashboardHabilidadesTecnicasSchema(
        resumen_global=ResumenGlobalTecnicoSchema(**data["resumen_global"]),
        subcategorias_tecnicas=[
            SubcategoriaTecnicaSchema(**s) for s in data["subcategorias_tecnicas"]
        ],
        last_updated=data["last_updated"],
        analisis_insights=data["analisis_insights"]
    )


def get_kpi_metrics(force_refresh: bool = False) -> KPITecnicasSchema:
    """Get KPI metrics including the leading technical category."""
    etl = repository.load_data(force_refresh)

    if etl is None:
        return KPITecnicasSchema(
            total_encuestados=0,
            total_mapeados=0,
            porcentaje_impacto_global=0.0,
            categoria_lider=""
        )

    resumen = etl.get_resumen_global()
    subcats = etl.get_subcategorias_tecnicas()

    # Determine categoria_lider — tie-break by PATRONES_TECNICOS declaration order
    categoria_lider = ""
    if subcats:
        max_votos = subcats[0].votos  # already sorted desc
        # Among tied leaders, pick the one that appears first in PATRONES_TECNICOS
        patrones_order = list(PATRONES_TECNICOS.keys())
        tied = [s for s in subcats if s.votos == max_votos]
        if len(tied) == 1:
            categoria_lider = tied[0].categoria
        else:
            for patron_cat in patrones_order:
                match = next((s for s in tied if s.categoria == patron_cat), None)
                if match:
                    categoria_lider = match.categoria
                    break

    return KPITecnicasSchema(
        total_encuestados=resumen.total_encuestados,
        total_mapeados=resumen.total_mapeados,
        porcentaje_impacto_global=resumen.porcentaje_impacto_global,
        categoria_lider=categoria_lider
    )


def get_matriz_operacional(force_refresh: bool = False) -> MatrizOperacionalSchema:
    """Get the Matriz Operacional de Requerimientos distribution."""
    etl = repository.load_data(force_refresh)

    if etl is None:
        return MatrizOperacionalSchema(subcategorias=[])

    subcats = etl.get_matriz_operacional()
    return MatrizOperacionalSchema(
        subcategorias=[
            SubcategoriaTecnicaSchema(
                categoria=s.categoria,
                votos=s.votos,
                porcentaje_del_subtotal=s.porcentaje_del_subtotal
            )
            for s in subcats
        ]
    )


def invalidate_cache() -> None:
    """Invalidate the repository cache."""
    try:
        repository.invalidate_cache()
    except Exception as e:
        logger.error(f"Error invalidating cache: {e}")
