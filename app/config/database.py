"""
Database Configuration
Carga datos desde Google Sheet público como fuente principal.
"""

import pandas as pd
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GOOGLE_SHEET_URL = os.getenv(
    "GOOGLE_SHEET_URL",
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSBNPpHFjJU7QmGpDNwIP7TfkLE8B0hgSlISuUUjKtVrbTXQhgLRFo72YypW4yf6g7s2v3K0lJgGUQK"
    "/pub?gid=1157215314&single=true&output=csv"
)

# Mapeo de columnas del CSV a nombres internos
COLUMN_MAP = {
    "Marca temporal": "marca_temporal",
    "Ingrese su número de Documento Nacional de Identidad (DNI)": "dni",
    "Edad (en años)": "edad",
    "Distrito de residencia del estudiante": "distrito",
    "Semestre académico actual": "semestre",
    "Carrera Profesional del Estudiante": "carrera",
    "¿Cómo calificas tu nivel de conocimientos técnicos en tu carrera?": "nivel_conocimientos_tecnicos",
    "¿Qué tan preparado te sientes para aplicar tus conocimientos en un entorno laboral real?": "preparacion_laboral",
    "¿Con qué frecuencia utilizas herramientas relacionadas a tu carrera?": "frecuencia_uso_carrera",
    "¿Qué tan importante considera la comunicación efectiva en su formación profesional?": "importancia_comunicacion",
    "¿Qué tan importante considera el trabajo en equipo en el ámbito académico y laboral?": "importancia_trabajo_equipo",
    "¿Qué tan importante considera la capacidad para resolver problemas en su desarrollo profesional?": "importancia_resolucion_problemas",
    "¿Qué tan importante considera la adaptabilidad frente a cambios o nuevas situaciones?": "importancia_adaptabilidad",
    "¿Qué tan importante considera la organización y el manejo del tiempo en su desempeño académico?": "importancia_organizacion",
    "¿Cómo calificas tu nivel de dominio de herramientas digitales?": "nivel_dominio_herramientas_digitales",
    "¿Con qué frecuencia utilizas herramientas digitales en tu formación o actividades?": "frecuencia_uso_herramientas_digitales",
    "¿Has recibido formación en herramientas digitales aplicadas a tu carrera?": "formacion_herramientas_digitales",
    "¿Qué tan preparado te sientes para ingresar al mercado laboral?": "preparacion_mercado_laboral",
    "¿Has realizado prácticas preprofesionales o laborales?": "practicas_realizadas",
    "¿Qué tan difícil crees que será conseguir trabajo en tu área?": "dificultad_conseguir_trabajo",
    "¿Qué habilidades consideras que necesitas mejorar?": "habilidades_a_mejorar",
    "¿Sientes que tu institución te ha preparado adecuadamente?": "institucion_preparo_adecuadamente",
    "¿Te gustaría recibir más formación en habilidades profesionales?": "desea_mas_formacion",
}


def get_data() -> pd.DataFrame:
    """
    Carga y normaliza los datos desde Google Sheet.
    Retorna un DataFrame con columnas renombradas y limpias.
    """
    try:
        logger.info(f"Cargando datos desde Google Sheet...")
        df = pd.read_csv(GOOGLE_SHEET_URL)
        logger.info(f"Datos cargados: {len(df)} registros, {len(df.columns)} columnas")

        # Renombrar columnas que existan en el CSV
        rename = {k: v for k, v in COLUMN_MAP.items() if k in df.columns}
        df.rename(columns=rename, inplace=True)

        # Detectar columna de herramientas digitales (puede tener salto de línea)
        for col in df.columns:
            if "herramientas digitales" in col.lower() and "frecuencia" not in col.lower() and "formación" not in col.lower() and "formacion" not in col.lower() and "nivel" not in col.lower():
                df.rename(columns={col: "herramientas_digitales"}, inplace=True)
                break

        # Limpiar DNI
        if "dni" in df.columns:
            df = df[df["dni"].notna()]
            df["dni"] = df["dni"].astype(str).str.strip()

        # Normalizar nivel de dominio a numérico
        if "nivel_dominio_herramientas_digitales" in df.columns:
            df["nivel_dominio_herramientas_digitales"] = pd.to_numeric(
                df["nivel_dominio_herramientas_digitales"], errors="coerce"
            ).fillna(0)

        logger.info(f"ETL completado: {len(df)} registros procesados")
        return df

    except Exception as e:
        logger.error(f"Error al cargar datos: {e}")
        raise Exception(f"No se pudo cargar el Google Sheet: {str(e)}")
