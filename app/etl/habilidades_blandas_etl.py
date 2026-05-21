"""
Habilidades Blandas ETL Module
Data transformations and queries for Habilidades Blandas BI dashboard
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Any
from datetime import datetime

from app.models.habilidades_blandas_model import (
    KPIMetricsBlandas,
    HabilidadPromedio,
    CategorizacionHabilidad,
    SatisfaccionDetalle,
    HabilidadesBlandasDashboard
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mutually Exclusive Regex Patterns for categorizing open-ended text
PATRONES_HABILIDADES_BLANDAS = {
    "Lógica y Algoritmia (Seudocódigo/Flujograma)": r"logica|lógica|seudocó|pseudocó|flujograma|algorit",
    "Bases de Datos y Análisis (SQL/Sheets)": r"base de datos|bases de datos|sql|mysql|sheets|excel|herramientas avanzadas",
    "Refuerzo General y Práctica Constante": r"seguir practicando|todo de la carrera|practica constante|practca constante|carrera",
    "Desarrollo Frontend (HTML/CSS)": r"html|css|sitios web|frontend|oaginas|paginas",
    "Arquitectura, Backend y DevOps (Docker)": r"arquitectura|backend|docker|kubernetes|distribuid|proyectos backend",
    "Infraestructura, Redes y AWS": r"aws|visual estudio|redes|ciberseguridad",
    "Programación y Código General": r"programac|cód|cod|lenguaje|memoriz|versiones|implementar|tecnic|digital|programas",
    "Trabajo en Equipo y Habilidades Blandas": r"trabajar mejor|equipo|hablar|comunicación|blanda|liderazgo|retención de información|retencion"
}


class HabilidadesBlandasETL:
    """
    ETL processor for Habilidades Blandas data
    Contains all transformations and analytics queries for soft skills
    """

    def __init__(self, df: pd.DataFrame = None):
        """
        Initialize ETL with either an existing DataFrame or fetch from the database
        """
        if df is None:
            raise ValueError("DataFrame is required for ETL")
        else:
            self.df = df.copy()

        self.total_students = len(self.df)
        logger.info(f"Habilidades Blandas ETL initialized with {self.total_students} records")

    def _clasificador(self, texto_usuario) -> str:
        """Categorize raw survey response using predefined regex rules (mutually exclusive)"""
        if pd.isna(texto_usuario):
            return "Sin Respuesta"

        texto_limpio = str(texto_usuario).lower().strip().replace('\n', ' ')
        texto_limpio = " ".join(texto_limpio.split())

        for categoria, patron in PATRONES_HABILIDADES_BLANDAS.items():
            if re.search(patron, texto_limpio):
                return categoria

        return "Otras Habilidades"

    # ============================================
    # 1. KPI METRICS
    # ============================================

    def get_kpi_metrics(self) -> KPIMetricsBlandas:
        """
        Calculate KPI metrics for the summary cards
        """
        soft_skills_cols = [
            "importancia_comunicacion_efectiva",
            "importancia_trabajo_equipo",
            "importancia_resolucion_problemas",
            "importancia_adaptabilidad",
            "importancia_organizacion_tiempo"
        ]

        # Calculate general average across all 5 Likert scale columns
        available_cols = [col for col in soft_skills_cols if col in self.df.columns]
        if available_cols:
            mean_series = self.df[available_cols].mean(axis=1)
            promedio_general = float(mean_series.mean())
        else:
            promedio_general = 0.0

        # Calculate satisfaction with institutional prep
        satisfaccion_pct = 0.0
        if "institucion_preparo_adecuadamente" in self.df.columns:
            total_valid = self.df["institucion_preparo_adecuadamente"].dropna().count()
            if total_valid > 0:
                satisfied = self.df["institucion_preparo_adecuadamente"].astype(str).str.strip().str.lower() == "si"
                satisfaccion_pct = (satisfied.sum() / total_valid) * 100

        # Calculate interest in soft skills training
        interes_pct = 0.0
        if "recibir_mas_formacion" in self.df.columns:
            total_valid = self.df["recibir_mas_formacion"].dropna().count()
            if total_valid > 0:
                interested = self.df["recibir_mas_formacion"].astype(str).str.strip().str.lower() == "si"
                interes_pct = (interested.sum() / total_valid) * 100

        return KPIMetricsBlandas(
            total_estudiantes=self.total_students,
            promedio_general=round(promedio_general, 2),
            satisfaccion_institucion_pct=round(satisfaccion_pct, 1),
            interes_formacion_pct=round(interes_pct, 1)
        )

    # ============================================
    # 2. SOFT SKILLS AVERAGES
    # ============================================

    def get_promedios_habilidades(self) -> List[HabilidadPromedio]:
        """
        Calculate average ratings (1-5) for each soft skill
        """
        mapping_nombres = {
            "importancia_comunicacion_efectiva": "Comunicación Efectiva",
            "importancia_trabajo_equipo": "Trabajo en Equipo",
            "importancia_resolucion_problemas": "Resolución de Problemas",
            "importancia_adaptabilidad": "Adaptabilidad",
            "importancia_organizacion_tiempo": "Organización del Tiempo"
        }

        results = []
        for col_raw, col_pretty in mapping_nombres.items():
            if col_raw in self.df.columns:
                promedio = float(self.df[col_raw].mean())
                if pd.isna(promedio):
                    promedio = 0.0

                # Determine soft skill level
                if promedio >= 4.5:
                    nivel = "Alto"
                elif promedio >= 3.5:
                    nivel = "Medio"
                else:
                    nivel = "Bajo"

                results.append(HabilidadPromedio(
                    habilidad=col_pretty,
                    promedio=promedio,
                    nivel=nivel
                ))
            else:
                results.append(HabilidadPromedio(
                    habilidad=col_pretty,
                    promedio=0.0,
                    nivel="N/A"
                ))

        # Sort from highest to lowest average score
        return sorted(results, key=lambda x: x.promedio, reverse=True)

    # ============================================
    # 3. OPEN QUESTIONS CATEGORIZATION
    # ============================================

    def get_habilidades_a_mejorar(self) -> List[CategorizacionHabilidad]:
        """
        Categorize the open responses of skills to improve and return counts
        """
        if "habilidades_a_mejorar" not in self.df.columns:
            return []

        # Run classification
        categorias_serie = self.df["habilidades_a_mejorar"].apply(self._clasificador)
        counts = categorias_serie.value_counts()
        total_respuestas = len(categorias_serie)

        results = []
        for cat, val in counts.items():
            pct = (val / total_respuestas) * 100 if total_respuestas > 0 else 0.0
            results.append(CategorizacionHabilidad(
                categoria=str(cat),
                cantidad_estudiantes=int(val),
                porcentaje=pct
            ))

        # Sort by student count descending
        return sorted(results, key=lambda x: x.cantidad_estudiantes, reverse=True)

    # ============================================
    # 4. INSTITUTIONAL SATISFACTION DETAILS
    # ============================================

    def get_satisfaccion_institucion(self) -> List[SatisfaccionDetalle]:
        """
        Get discrete detail for institutional preparation satisfaction
        """
        if "institucion_preparo_adecuadamente" not in self.df.columns:
            return []

        # Cleanup and count values
        serie = self.df["institucion_preparo_adecuadamente"].astype(str).str.strip().str.capitalize()
        # Normalizar a Sí / No
        serie = serie.replace({"Si": "Sí", "No": "No"})
        counts = serie.value_counts()
        total = len(serie)

        results = []
        for resp, val in counts.items():
            pct = (val / total) * 100 if total > 0 else 0.0
            results.append(SatisfaccionDetalle(
                respuesta=str(resp),
                cantidad=int(val),
                porcentaje=pct
            ))

        return results

    # ============================================
    # 5. TRAINING DETAILS INTEREST
    # ============================================

    def get_interes_formacion(self) -> List[SatisfaccionDetalle]:
        """
        Get discrete detail for soft skills training interest
        """
        if "recibir_mas_formacion" not in self.df.columns:
            return []

        # Cleanup and count values
        serie = self.df["recibir_mas_formacion"].astype(str).str.strip().str.capitalize()
        serie = serie.replace({"Si": "Sí", "No": "No"})
        counts = serie.value_counts()
        total = len(serie)

        results = []
        for resp, val in counts.items():
            pct = (val / total) * 100 if total > 0 else 0.0
            results.append(SatisfaccionDetalle(
                respuesta=str(resp),
                cantidad=int(val),
                porcentaje=pct
            ))

        return results

    # ============================================
    # 6. BUSINESS INSIGHTS
    # ============================================

    def generate_insights(self) -> str:
        """
        Generate business insights from the soft skills data
        """
        insights = []

        kpis = self.get_kpi_metrics()
        promedios = self.get_promedios_habilidades()
        habilidades_mejorar = self.get_habilidades_a_mejorar()

        # Insight 1: General Average
        if kpis.promedio_general >= 4.0:
            insights.append(
                f"Los estudiantes otorgan una alta importancia promedio ({kpis.promedio_general} de 5.0) a las habilidades blandas."
            )
        else:
            insights.append(
                f"La percepción de importancia general sobre habilidades blandas es moderada ({kpis.promedio_general} de 5.0)."
            )

        # Insight 2: Highest vs Lowest soft skill
        if len(promedios) >= 2:
            highest = promedios[0]
            lowest = promedios[-1]
            insights.append(
                f"La habilidad más valorada es '{highest.habilidad}' ({round(highest.promedio, 2)}), "
                f"mientras que '{lowest.habilidad}' presenta el promedio más bajo ({round(lowest.promedio, 2)})."
            )

        # Insight 3: Skills to Improve text feedback
        if habilidades_mejorar:
            top_improvement = habilidades_mejorar[0]
            if top_improvement.categoria != "Sin Respuesta":
                insights.append(
                    f"El principal reto identificado de mejora es '{top_improvement.categoria}' "
                    f"con {top_improvement.cantidad_estudiantes} comentarios ({round(top_improvement.porcentaje, 1)}% del total)."
                )

        # Insight 4: Institutional Prep vs Training Interest
        insights.append(
            f"El {kpis.interes_formacion_pct}% de los alumnos desea recibir más capacitación en habilidades profesionales, "
            f"lo cual se alinea a que un {round(100.0 - kpis.satisfaccion_institucion_pct, 1)}% considera que la preparación actual de la institución podría optimizarse."
        )

        return " ".join(insights)

    # ============================================
    # 7. CONSOLIDATED DATA
    # ============================================

    def get_complete_dashboard_data(self) -> Dict[str, Any]:
        """
        Consolidate all soft skills analytics queries
        """
        logger.info("Generating complete habilidades blandas dashboard data...")

        indicadores_kpi = self.get_kpi_metrics()
        promedios_habilidades = self.get_promedios_habilidades()
        habilidades_a_mejorar = self.get_habilidades_a_mejorar()
        satisfaccion_institucion = self.get_satisfaccion_institucion()
        interes_formacion = self.get_interes_formacion()
        analisis_insights = self.generate_insights()

        dashboard = HabilidadesBlandasDashboard(
            indicadores_kpi=indicadores_kpi,
            promedios_habilidades=promedios_habilidades,
            habilidades_a_mejorar=habilidades_a_mejorar,
            satisfaccion_institucion=satisfaccion_institucion,
            interes_formacion=interes_formacion,
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            analisis_insights=analisis_insights
        )

        logger.info("Soft skills dashboard data generation complete")
        return dashboard.to_dict()
