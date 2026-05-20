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
    
    def clean_data(self) -> Optional[pd.DataFrame]:
        """
        Clean and prepare data for analysis
        
        Returns:
            pd.DataFrame: Cleaned data ready for ETL processing
        """
        if self.raw_data is None:
            logger.error("❌ No raw data available. Call connect() first.")
            return None
        
        try:
            logger.info("🧹 Cleaning data...")
            df = self.raw_data.copy()
            
            # Remove completely empty rows
            df = df.dropna(how='all')
            
            # Basic data type conversions
            if 'Edad (en años)' in df.columns:
                df['Edad (en años)'] = pd.to_numeric(df['Edad (en años)'], errors='coerce')
            
            # Remove rows with critical missing data (DNI, Age)
            critical_cols = ['Ingrese su número de Documento Nacional de Identidad (DNI)', 'Edad (en años)']
            for col in critical_cols:
                if col in df.columns:
                    df = df.dropna(subset=[col])
            
            self.cleaned_data = df
            logger.info(f"✅ Data cleaned successfully! {len(df)} valid records")
            return df
            
        except Exception as e:
            logger.error(f"❌ Data cleaning failed: {e}")
            return None
    
    def get_connection_status(self) -> dict:
        """
        Get current connection status and data info
        
        Returns:
            dict: Connection status information
        """
        return {
            'connected': self.raw_data is not None,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'raw_records': len(self.raw_data) if self.raw_data is not None else 0,
            'clean_records': len(self.cleaned_data) if self.cleaned_data is not None else 0,
            'url': self.url_csv
        }