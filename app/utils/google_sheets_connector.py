"""
Google Sheets Connector - Real-time data ingestion from Google Sheets
Uses pandas to read CSV export from Google Forms/Sheets
"""

import pandas as pd
import logging
from typing import Optional, Tuple
from datetime import datetime

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
            # Forzar UTF-8 para mantener los textos de la encuesta correctamente codificados.
            self.raw_data = pd.read_csv(
                self.url_csv,
                encoding='utf-8'
            )
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
        Clean and transform raw data for BI analysis
        
        Returns:
            pd.DataFrame: Cleaned dataset
        """
        if self.raw_data is None:
            logger.warning("No data loaded. Call connect() first")
            return None
        
        df = self.raw_data.copy()
        
        # Limpiar espacios en nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Debug: imprimir nombres reales de columnas
        logger.info("Actual column names from Google Sheets:")
        for i, col in enumerate(df.columns):
            logger.info(f"  {i+1}. {col}")
        
        # Mapeo de nombres correctos (usando los nombres reales que ves en el debug)
        column_mapping = {
            'Marca temporal': 'survey_date',
            'Edad (en años)': 'age',
            'Distrito de residencia del estudiante': 'district',
            'Semestre académico actual': 'semester',
            'Carrera Profesional del Estudiante': 'career',
            'Ingrese su número de Documento Nacional de Identidad (DNI)': 'dni',
            '¿Cómo calificas tu nivel de conocimientos técnicos en tu carrera?': 'tech_knowledge',
            '¿Qué tan preparado te sientes para aplicar tus conocimientos en un entorno laboral real?': 'practical_readiness',
            '¿Qué tan preparado te sientes para ingresar al mercado laboral?': 'job_readiness',
            '¿Sientes que tu institución te ha preparado adecuadamente?': 'institution_preparation',
            '¿Qué tan importante considera la comunicación efectiva en su formación profesional?': 'communication_importance',
            '¿Qué tan importante considera el trabajo en equipo en el ámbito académico y laboral?': 'teamwork_importance',
            '¿Qué tan importante considera la capacidad para resolver problemas en su desarrollo profesional?': 'problem_solving_importance',
            '¿Qué tan importante considera la adaptabilidad frente a cambios o nuevas situaciones?': 'adaptability_importance',
            '¿Qué tan importante considera la organización y el manejo del tiempo en su desempeño académico?': 'organization_importance'
        }
        
        # Aplicar mapeo solo para columnas que existen
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Convertir edad a numérico
        if 'age' in df.columns:
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
        
        # Limpiar semestre (extraer número)
        if 'semester' in df.columns:
            df['semester'] = df['semester'].astype(str).str.replace('° Semestre', '').str.strip()
            df['semester'] = pd.to_numeric(df['semester'], errors='coerce')
        
        # Eliminar filas con valores críticos nulos
        initial_count = len(df)
        critical_cols = ['age', 'semester']
        existing_critical = [col for col in critical_cols if col in df.columns]
        if existing_critical:
            df = df.dropna(subset=existing_critical)
        
        if initial_count > len(df):
            logger.warning(f"Removed {initial_count - len(df)} rows with null critical values")
        
        self.cleaned_data = df
        logger.info(f"✅ Data cleaning complete! {len(df)} valid records")
        
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
