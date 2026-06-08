"""
Habilidades Técnicas Repository
Data access layer for Habilidades Técnicas module
"""

import logging
from typing import Optional, Dict, Any

from app.utils.google_sheets_connector import GoogleSheetsConnector
from app.etl.habilidades_tecnicas_etl import HabilidadesTecnicasETL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HabilidadesTecnicasRepository:
    """
    Repository pattern for Habilidades Técnicas data access.
    Uses its own GoogleSheetsConnector instance (independent from Blandas).
    Passes raw_data directly to the ETL — does NOT call clean_data().
    """

    def __init__(self, google_sheets_url: str):
        self.connector = GoogleSheetsConnector(google_sheets_url)
        self.etl: Optional[HabilidadesTecnicasETL] = None
        self._cache_valid: bool = False

    def load_data(self, force_refresh: bool = False) -> Optional[HabilidadesTecnicasETL]:
        """Load and cache data from Google Sheets."""
        if self._cache_valid and not force_refresh and self.etl is not None:
            logger.info("Returning cached Habilidades Técnicas data")
            return self.etl

        logger.info("Loading fresh data from Google Sheets for Habilidades Técnicas...")

        if not self.connector.connect():
            logger.error("Failed to connect to Google Sheets for Habilidades Técnicas")
            self._cache_valid = False
            return None

        df = self.connector.raw_data

        if df is None or df.empty:
            logger.error("No data available after connecting to Google Sheets")
            self._cache_valid = False
            return None

        self.etl = HabilidadesTecnicasETL(df)
        self._cache_valid = True

        logger.info(f"Habilidades Técnicas data loaded. Total records: {len(df)}")
        return self.etl

    def get_dashboard_data(self, force_refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Get complete dashboard data dict."""
        etl = self.load_data(force_refresh)
        if etl is None:
            return None
        return etl.get_complete_dashboard_data()

    def invalidate_cache(self) -> None:
        """Invalidate the in-memory cache."""
        self._cache_valid = False
        logger.info("Cache invalidated for Habilidades Técnicas")
