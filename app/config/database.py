"""
Database configuration and environment variables
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Google Sheets public URL exported as CSV
SHEET_URL = os.getenv("GOOGLE_SHEET_URL", "")
SHEET_URL_TECNICAS = os.getenv("GOOGLE_SHEET_TECNICAS_URL", "")

# Cache Time To Live (TTL) in seconds
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", "30"))