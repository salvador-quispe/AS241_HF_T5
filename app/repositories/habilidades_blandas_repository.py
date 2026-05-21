"""
Habilidades Blandas Repository
Data access layer for Habilidades Blandas module
"""

import pandas as pd
from typing import Optional, Dict, Any
import logging

from app.utils.google_sheets_connector import GoogleSheetsConnector
from app.etl.habilidades_blandas_etl import HabilidadesBlandasETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HabilidadesBlandasRepository:
    """
    Repository pattern for Habilidades Blandas data access
    Handles all data retrieval operations using GoogleSheetsConnector
    """

    def __init__(self, google_sheets_url: str):
        """
        Initialize repository with Google Sheets URL
        """
        self.connector = GoogleSheetsConnector(google_sheets_url)
        self.etl = None
        self._data_cache = None
        self._cache_valid = False

    def load_data(self, force_refresh: bool = False) -> Optional[HabilidadesBlandasETL]:
        """
        Load and process data from Google Sheets
        """
        if self._cache_valid and not force_refresh and self.etl is not None:
            logger.info("Returning cached Habilidades Blandas data")
            return self.etl

        logger.info("Loading fresh data from Google Sheets for Habilidades Blandas...")

        # Connect and load data
        if not self.connector.connect():
            logger.error("Failed to connect to Google Sheets")
            return None

        # Clean data using connector (if implemented)
        df = self.connector.clean_data()

        if df is None or df.empty:
            logger.error("No data available after cleaning")
            return None

        # Create ETL instance
        self.etl = HabilidadesBlandasETL(df)
        self._cache_valid = True

        logger.info(f"Habilidades Blandas data loaded successfully. Total records: {len(df)}")
        return self.etl

    def get_dashboard_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get complete dashboard data
        """
        etl = self.load_data(force_refresh)
        if etl is None:
            return None
        return etl.get_complete_dashboard_data()

    def invalidate_cache(self):
        """Invalidate the data cache to force refresh on next request"""
        self._cache_valid = False
        logger.info("Cache invalidated for Habilidades Blandas")
