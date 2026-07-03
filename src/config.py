"""
Project configuration.
Stores all project paths and constants.
"""

from pathlib import Path

# ============================
# Project Paths
# ============================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"

PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = PROCESSED_FOLDER / "weather_processed.csv"