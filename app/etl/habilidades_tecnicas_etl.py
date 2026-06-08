"""
Habilidades Técnicas ETL Module
Data transformations and queries for Habilidades Técnicas BI dashboard
"""

import pandas as pd
import re
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================
# DATACLASSES
# ============================================

@dataclass
class ResumenGlobalTecnico:
    """Summary metrics for the technical skills module"""
    total_encuestados: int
    total_mapeados: int
    porcentaje_impacto_global: float

    def to_dict(self) -> dict:
        return {
            "total_encuestados": self.total_encuestados,
            "total_mapeados": self.total_mapeados,
            "porcentaje_impacto_global": round(self.porcentaje_impacto_global, 1)
        }


@dataclass
class NivelTecnicoMetrics:
    """Metrics for technical knowledge level and job readiness"""
    conocimiento_tecnico_promedio: float   # Likert mean × 20/5  (scale 0–20)
    porcentaje_aplicacion_real: float      # Likert mean × 100/5 (scale 0–100%)
    promedio_conocimiento_raw: float       # Raw Likert mean 1–5
    promedio_aplicacion_raw: float         # Raw Likert mean 1–5
    total_respondentes: int

    def to_dict(self) -> dict:
        return {
            "conocimiento_tecnico_promedio": round(self.conocimiento_tecnico_promedio, 2),
            "porcentaje_aplicacion_real": round(self.porcentaje_aplicacion_real, 2),
            "promedio_conocimiento_raw": round(self.promedio_conocimiento_raw, 2),
            "promedio_aplicacion_raw": round(self.promedio_aplicacion_raw, 2),
            "total_respondentes": self.total_respondentes,
        }


@dataclass
class SubcategoriaTecnica:
    """Category breakdown for a technical skill"""
    categoria: str
    votos: int
    porcentaje_del_subtotal: float

    def to_dict(self) -> dict:
        return {
            "categoria": self.categoria,
            "votos": self.votos,
            "porcentaje_del_subtotal": round(self.porcentaje_del_subtotal, 1)
        }


@dataclass
class HabilidadesTecnicasDashboard:
    """Complete dashboard data for habilidades técnicas module"""
    resumen_global: ResumenGlobalTecnico
    subcategorias_tecnicas: List[SubcategoriaTecnica]
    last_updated: str
    analisis_insights: str

    def to_dict(self) -> dict:
        return {
            "resumen_global": self.resumen_global.to_dict(),
            "subcategorias_tecnicas": [s.to_dict() for s in self.subcategorias_tecnicas],
            "last_updated": self.last_updated,
            "analisis_insights": self.analisis_insights
        }


# ============================================
# REGEX PATTERNS — Mutually Exclusive, Priority Order
# ============================================

PATRONES_TECNICOS = {
    "Lógica y Algoritmia (Seudocódigo/Flujograma)": r"logica|lógica|seudocó|pseudocó|flujograma|algorit",
    "Bases de Datos y Análisis (SQL/Sheets)": r"base de datos|bases de datos|sql|mysql|sheets|excel|herramientas avanzadas",
    "Refuerzo General y Práctica Constante": r"seguir practicando|todo de la carrera|practica constante|practca constante|carrera",
    "Desarrollo Frontend (HTML/CSS)": r"html|css|sitios web|frontend|oaginas|paginas",
    "Arquitectura, Backend y DevOps (Docker)": r"arquitectura|backend|docker|kubernetes|distribuid|proyectos backend",
    "Infraestructura, Redes y AWS": r"aws|visual estudio|redes|ciberseguridad",
    "Programación y Código General": r"programac|cód|cod|lenguaje|memoriz|versiones|implementar|tecnic|digital|programas",
}


# ============================================
# ETL CLASS
# ============================================

class HabilidadesTecnicasETL:
    """
    ETL processor for Habilidades Técnicas data.
    Receives a raw DataFrame and accesses column 27 (0-based) for responses.
    """

    def __init__(self, df: pd.DataFrame):
        if df is None:
            raise ValueError("DataFrame is required for ETL")

        self.df = df.copy()
        self.total_encuestados = len(self.df)
        self._categorias: Optional[pd.Series] = None

        # Extract and classify responses from column 27
        try:
            self._respuestas = self.df.iloc[:, 27]
            self._categorias = self._respuestas.apply(self._clasificador)
            self._df_mapeados = self.df[self._categorias.notna()]
            self.total_mapeados = len(self._df_mapeados)
        except IndexError:
            logger.error(
                f"DataFrame has only {len(self.df.columns)} columns — "
                f"column 27 (0-based) not found. Treating all rows as unmapped."
            )
            self._respuestas = pd.Series([], dtype=str)
            self._categorias = pd.Series([], dtype=str)
            self._df_mapeados = self.df.iloc[0:0]  # empty
            self.total_mapeados = 0

        logger.info(
            f"HabilidadesTecnicasETL initialized: "
            f"{self.total_encuestados} rows, {self.total_mapeados} mapped"
        )

    def _clasificador(self, texto) -> Optional[str]:
        """Classify a response using PATRONES_TECNICOS (first match wins, mutually exclusive)."""
        if pd.isna(texto):
            return None
        texto_limpio = " ".join(str(texto).lower().strip().split())
        for categoria, patron in PATRONES_TECNICOS.items():
            if re.search(patron, texto_limpio):
                return categoria
        return None

    # ============================================
    # 1. RESUMEN GLOBAL
    # ============================================

    def get_resumen_global(self) -> ResumenGlobalTecnico:
        """Return global summary: total surveyed, mapped, and impact percentage."""
        if self.total_encuestados > 0:
            pct = round((self.total_mapeados / self.total_encuestados) * 100, 1)
        else:
            pct = 0.0

        return ResumenGlobalTecnico(
            total_encuestados=self.total_encuestados,
            total_mapeados=self.total_mapeados,
            porcentaje_impacto_global=pct
        )

    # ============================================
    # 2. SUBCATEGORÍAS TÉCNICAS
    # ============================================

    def get_subcategorias_tecnicas(self) -> List[SubcategoriaTecnica]:
        """Return list of categories sorted descending by votes (only votos > 0)."""
        if self.total_mapeados == 0:
            return []

        conteos = self._categorias.dropna().value_counts()
        results = []
        for cat, votos in conteos.items():
            if votos > 0:
                pct = round((votos / self.total_mapeados) * 100, 1)
                results.append(SubcategoriaTecnica(
                    categoria=str(cat),
                    votos=int(votos),
                    porcentaje_del_subtotal=pct
                ))

        return sorted(results, key=lambda x: x.votos, reverse=True)

    # ============================================
    # 3. MATRIZ OPERACIONAL
    # ============================================

    def get_matriz_operacional(self) -> List[SubcategoriaTecnica]:
        """Return the Matriz Operacional — identical to get_subcategorias_tecnicas()."""
        return self.get_subcategorias_tecnicas()

    # ============================================
    # 4. COMPLETE DASHBOARD DATA
    # ============================================

    def get_complete_dashboard_data(self) -> Dict[str, Any]:
        """Return consolidated dashboard dict with 3 keys: resumen_global, subcategorias_tecnicas, last_updated."""
        resumen = self.get_resumen_global()
        subcats = self.get_subcategorias_tecnicas()
        insights = self.generate_insights()

        dashboard = HabilidadesTecnicasDashboard(
            resumen_global=resumen,
            subcategorias_tecnicas=subcats,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            analisis_insights=insights
        )

        return dashboard.to_dict()

    # ============================================
    # 5. INSIGHTS
    # ============================================

    def generate_insights(self) -> str:
        """Generate business insights string with at least 2 numeric observations."""
        resumen = self.get_resumen_global()
        subcats = self.get_subcategorias_tecnicas()
        insights = []

        # Insight 1: Coverage
        insights.append(
            f"Del total de {resumen.total_encuestados} estudiantes encuestados, "
            f"{resumen.total_mapeados} ({resumen.porcentaje_impacto_global}%) "
            f"indicaron habilidades técnicas específicas que desean mejorar."
        )

        # Insight 2: Top category
        if subcats:
            top = subcats[0]
            insights.append(
                f"La categoría técnica con mayor demanda es '{top.categoria}' "
                f"con {top.votos} estudiantes ({top.porcentaje_del_subtotal}% del total mapeado)."
            )

        # Insight 3: Bottom category (if more than 1)
        if len(subcats) >= 2:
            bottom = subcats[-1]
            insights.append(
                f"La categoría con menor demanda es '{bottom.categoria}' "
                f"con {bottom.votos} estudiantes ({bottom.porcentaje_del_subtotal}%)."
            )

        return " ".join(insights)

    # ============================================
    # 6. NIVEL TÉCNICO Y APLICACIÓN REAL
    # ============================================

    def get_nivel_tecnico(self) -> NivelTecnicoMetrics:
        """
        Calculate technical knowledge level and job readiness metrics.

        Column 8  (0-based): ¿Cómo calificas tu nivel de conocimientos técnicos en tu carrera?
                              → Likert 1-5 → score sobre 20 (× 20/5)
        Column 9  (0-based): ¿Qué tan preparado te sientes para aplicar tus conocimientos?
                              → Likert 1-5 → porcentaje sobre 100 (× 100/5)
        """
        col_conocimiento = None
        col_aplicacion = None

        try:
            col_conocimiento = pd.to_numeric(self.df.iloc[:, 8], errors="coerce")
        except IndexError:
            logger.error("Column 8 (conocimiento técnico) not found in DataFrame")

        try:
            col_aplicacion = pd.to_numeric(self.df.iloc[:, 9], errors="coerce")
        except IndexError:
            logger.error("Column 9 (aplicación real) not found in DataFrame")

        # Conocimiento técnico: mean Likert × 20/5 → scale 0–20
        if col_conocimiento is not None and col_conocimiento.count() > 0:
            mean_con = float(col_conocimiento.mean())
            conocimiento_promedio = round(mean_con * 20 / 5, 2)
            total = int(col_conocimiento.count())
        else:
            mean_con = 0.0
            conocimiento_promedio = 0.0
            total = 0

        # Aplicación real: mean Likert × 100/5 → scale 0–100%
        if col_aplicacion is not None and col_aplicacion.count() > 0:
            mean_apl = float(col_aplicacion.mean())
            porcentaje_aplicacion = round(mean_apl * 100 / 5, 2)
            if total == 0:
                total = int(col_aplicacion.count())
        else:
            mean_apl = 0.0
            porcentaje_aplicacion = 0.0

        return NivelTecnicoMetrics(
            conocimiento_tecnico_promedio=conocimiento_promedio,
            porcentaje_aplicacion_real=porcentaje_aplicacion,
            promedio_conocimiento_raw=round(mean_con, 4),
            promedio_aplicacion_raw=round(mean_apl, 4),
            total_respondentes=total,
        )
