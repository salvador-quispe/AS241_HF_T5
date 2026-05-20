"""
Digital Skills Repository
Data access layer for digital skills module
"""

import pandas as pd
from typing import Optional, Dict, Any
import logging

from app.utils.google_sheets_connector import GoogleSheetsConnector
from app.etl.digital_skills_etl import DigitalSkillsETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DigitalSkillsRepository:
    """
    Repository pattern for digital skills data access
    Handles all data retrieval operations
    """
    
    def __init__(self, google_sheets_url: str):
        """
        Initialize repository with Google Sheets URL
        
        Args:
            google_sheets_url: CSV export URL from Google Sheets
        """
        self.connector = GoogleSheetsConnector(google_sheets_url)
        self.etl = None
        self._data_cache = None
        self._cache_valid = False
    
    def load_data(self, force_refresh: bool = False) -> DigitalSkillsETL:
        """
        Load and process data from Google Sheets
        
        Args:
            force_refresh: Force refresh from source even if cache is valid
            
        Returns:
            DigitalSkillsETL instance with processed data
        """
        if self._cache_valid and not force_refresh and self.etl is not None:
            logger.info("Returning cached digital skills data")
            return self.etl
        
        logger.info("Loading fresh digital skills data from Google Sheets...")
        
        # Connect and load data
        if not self.connector.connect():
            logger.error("Failed to connect to Google Sheets")
            return None
        
        # Clean data
        df = self.connector.clean_data()
        
        if df is None or df.empty:
            logger.error("No digital skills data available after cleaning")
            return None
        
        # Create ETL instance
        self.etl = DigitalSkillsETL()
        self._cache_valid = True
        
        logger.info(f"Digital skills data loaded successfully. Total records: {len(df)}")
        return self.etl
    
    def get_dashboard_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get complete digital skills dashboard data
        
        Args:
            force_refresh: Force refresh from source
            
        Returns:
            Dictionary with all dashboard metrics
        """
        etl = self.load_data(force_refresh)
        
        if etl is None:
            return None
        
        return etl.get_complete_dashboard_data()
    
    def get_kpi_metrics(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Get only KPI metrics for digital skills"""
        etl = self.load_data(force_refresh)
        if etl:
            return etl.get_kpi_metrics()
        return None
    
    def get_herramientas_ofimaticas(self, force_refresh: bool = False) -> Optional[list]:
        """Get office tools usage data"""
        etl = self.load_data(force_refresh)
        if etl:
            return etl.get_herramientas_ofimaticas()
        return None
    
    def get_plataformas_lenguajes(self, force_refresh: bool = False) -> Optional[list]:
        """Get programming platforms and languages data"""
        etl = self.load_data(force_refresh)
        if etl:
            return etl.get_plataformas_lenguajes()
        return None
    
    def get_estudiantes_habilidades(self, limit: int = 10, force_refresh: bool = False) -> Optional[list]:
        """Get individual student digital skills data"""
        etl = self.load_data(force_refresh)
        if etl:
            return etl.get_estudiantes_habilidades(limit)
        return None
    
    def invalidate_cache(self):
        """Invalidate the data cache to force refresh on next request"""
        self._cache_valid = False
        logger.info("Digital skills cache invalidated")