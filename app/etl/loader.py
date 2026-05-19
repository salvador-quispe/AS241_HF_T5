import logging
from app.config.database import get_data, reload_data

logger = logging.getLogger(__name__)


def run_etl() -> int:
    df = reload_data()
    logger.info("ETL completed: %d records loaded", len(df))
    return len(df)
