"""
Google Sheets Connector - Real-time data ingestion from Google Sheets
Uses pandas to read CSV export from Google Forms/Sheets
"""

import pandas as pd
import logging
import ssl
from typing import Optional, Tuple
from datetime import datetime

# Bypass SSL context verification for macOS compatibility
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleSheetsConnector:
    """
    Connector to read data from Google Sheets in real-time
    Uses the published CSV URL from Google Sheets
    """
    
    def __init__(self, url_csv: str, timeout: int = 30):
        """
        Initialize the connector with the CSV URL
        
        Args:
            url_csv: Google Sheets CSV export URL 
                    (File > Share > Publish to web > CSV)
            timeout: Request timeout in seconds
        """
        self.url_csv = url_csv
        self.timeout = timeout
        self.raw_data = None
        self.cleaned_data = None
        self.last_update = None
    
    def connect(self) -> bool:
        """
        Establish connection and load data from Google Sheets
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            logger.info("🔄 Connecting to Google Sheets...")
            # Forzar encoding UTF-8-SIG para manejar tildes y ñ correctamente
            self.raw_data = pd.read_csv(self.url_csv, encoding='utf-8-sig')
            self.last_update = datetime.now()
            logger.info(f"✅ Connection successful! {len(self.raw_data)} records loaded")
            return True
        except UnicodeDecodeError:
            # Si falla UTF-8-SIG, probar con latin-1
            try:
                self.raw_data = pd.read_csv(self.url_csv, encoding='latin-1')
                self.last_update = datetime.now()
                logger.info(f"✅ Connection successful (latin-1)! {len(self.raw_data)} records loaded")
                return True
            except Exception as e:
                logger.error(f"❌ Connection failed with latin-1: {e}")
                return False
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            return False
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and transform raw data using positional mapping matching database.py.
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        if self.raw_data is None:
            logger.warning("No data loaded. Call connect() first")
            return None
        
        # Exact mapping for Habilidades Blandas ONLY
        habilidades_mapping = {
            '¿Qué tan importante considera la comunicación efectiva en su formación profesional?': 'importancia_comunicacion_efectiva',
            '¿Qué tan importante considera el trabajo en equipo en el ámbito académico y laboral?': 'importancia_trabajo_equipo',
            '¿Qué tan importante considera la capacidad para resolver problemas en su desarrollo profesional?': 'importancia_resolucion_problemas',
            '¿Qué tan importante considera la adaptabilidad frente a cambios o nuevas situaciones?': 'importancia_adaptabilidad',
            '¿Qué tan importante considera la organización y el manejo del tiempo en su desempeño académico?': 'importancia_organizacion_tiempo',
            '¿Sientes que tu institución te ha preparado adecuadamente?': 'institucion_preparo_adecuadamente',
            '¿Te gustaría recibir más formación en habilidades profesionales?': 'recibir_mas_formacion',
            '¿Qué habilidades consideras que necesitas mejorar?': 'habilidades_a_mejorar'
        }
        
        # Keep only the relevant columns based on exact string match (stripped)
        df = self.raw_data.copy()
        df.columns = df.columns.str.strip()
        cols_to_keep = [col for col in df.columns if col in habilidades_mapping]
        df = df[cols_to_keep].copy()
        
        # Rename them to the backend keys
        df = df.rename(columns=habilidades_mapping)
        
        # Convert numeric columns
        NUMERIC_COLS = [
            "importancia_comunicacion_efectiva",
            "importancia_trabajo_equipo", "importancia_resolucion_problemas",
            "importancia_adaptabilidad", "importancia_organizacion_tiempo"
        ]
        
        for col in NUMERIC_COLS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        
        self.cleaned_data = df
        logger.info(f"✅ Data cleaning complete! {len(df)} records processed")
        return df
    
    def refresh(self) -> pd.DataFrame:
        """
        Refresh data from Google Sheets and return cleaned dataset
        
        Returns:
            pd.DataFrame: Fresh cleaned dataset
        """
        self.connect()
        return self.clean_data()
    
    def get_last_update(self) -> str:
        """Get last update timestamp as formatted string"""
        if self.last_update:
            return self.last_update.strftime("%Y-%m-%d %H:%M:%S")
        return "Not updated yet"