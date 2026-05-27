"""
Database configuration with Google Sheets connection and caching
"""

import pandas as pd
import os
import time
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SHEET_URL = os.getenv("GOOGLE_SHEET_URL", "")
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "30"))

# Column names mapping (must match Google Sheets structure)
COLUMN_NAMES = [
    "timestamp",
    "puntuacion",
    "dni",
    "edad",
    "distrito",
    "semestre",
    "carrera",
    "importancia_centro_evaluacion",
    "nivel_conocimientos_tecnicos",
    "preparado_aplicar_conocimientos",
    "frecuencia_uso_herramientas_carrera",
    "importancia_comunicacion_efectiva",
    "importancia_trabajo_equipo",
    "importancia_resolucion_problemas",
    "importancia_adaptabilidad",
    "importancia_organizacion_tiempo",
    "herramientas_digitales",
    "nivel_dominio_herramientas_digitales",
    "frecuencia_uso_herramientas_digitales",
    "formacion_herramientas_digitales",
    "_dup_herramientas_digitales",
    "_dup_nivel_dominio",
    "_dup_frecuencia_uso",
    "_dup_formacion",
    "preparado_ingresar_mercado_laboral",
    "realizo_practicas_preprofesionales",
    "dificultad_conseguir_trabajo",
    "habilidades_a_mejorar",
    "institucion_preparo_adecuadamente",
    "recibir_mas_formacion",
]

NUMERIC_COLS = [
    "edad",
    "importancia_centro_evaluacion",
    "nivel_conocimientos_tecnicos",
    "preparado_aplicar_conocimientos",
    "importancia_comunicacion_efectiva",
    "importancia_trabajo_equipo",
    "importancia_resolucion_problemas",
    "importancia_adaptabilidad",
    "importancia_organizacion_tiempo",
    "nivel_dominio_herramientas_digitales",
    "preparado_ingresar_mercado_laboral",
]

DROP_COLS = {"puntuacion", "_dup_herramientas_digitales", "_dup_nivel_dominio",
             "_dup_frecuencia_uso", "_dup_formacion"}

_cache = {"df": None, "ts": 0.0}


def _fetch_and_transform() -> pd.DataFrame:
    """Fetch data from Google Sheets and apply transformations"""
    logger.info("Fetching sheet from %s", SHEET_URL)
    df = pd.read_csv(SHEET_URL, header=None, skiprows=1, encoding="utf-8")
    logger.info("Fetched %d rows, %d columns", len(df), len(df.columns))

    ncols = len(df.columns)
    names = COLUMN_NAMES[:ncols]
    df.columns = names

    for col in DROP_COLS:
        if col in df.columns:
            df = df.drop(columns=[col])

    df["dni"] = df["dni"].astype(str).str.strip()

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", dayfirst=True)

    return df


def get_data(force: bool = False) -> pd.DataFrame:
    """
    Get data from cache or fetch from Google Sheets
    
    Args:
        force: If True, bypass cache and fetch fresh data
        
    Returns:
        DataFrame with cleaned survey data
    """
    global _cache
    now = time.time()
    if force or _cache["df"] is None or (now - _cache["ts"]) > CACHE_TTL:
        _cache["df"] = _fetch_and_transform()
        _cache["ts"] = now
        logger.info("Cache updated with %d rows", len(_cache["df"]))
    return _cache["df"].copy()


def reload_data() -> pd.DataFrame:
    """Force reload data from Google Sheets"""
    return get_data(force=True)
