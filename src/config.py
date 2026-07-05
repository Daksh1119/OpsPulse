"""
Project configuration.

Stores:
- Project paths
- Logging configuration
- Environment variables
"""

from pathlib import Path

from dotenv import load_dotenv
import os

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

# =====================================================
# Project Paths
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_FOLDER = DATA_FOLDER / "raw"

PROCESSED_FOLDER = DATA_FOLDER / "processed"

OUTPUT_FILE = PROCESSED_FOLDER / "weather_processed.csv"

LOG_FOLDER = PROJECT_ROOT / "logs"

LOG_FILE = LOG_FOLDER / "opspulse.log"

# =====================================================
# API Configuration
# =====================================================

BASE_URL = os.getenv(
    "BASE_URL",
    "https://api.open-meteo.com/v1/forecast"
)

# =====================================================
# Supabase Configuration
# =====================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_SERVICE_ROLE_KEY = os.getenv(
    "SUPABASE_SERVICE_ROLE_KEY"
)