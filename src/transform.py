"""
ETL transformation pipeline for OpsPulse.

This module performs:
1. Load raw weather JSON files
2. Merge datasets
3. Validate dataset
4. Clean dataset
5. Feature engineering
6. Export processed dataset
"""

from pathlib import Path
import json

import pandas as pd

from src.logger import get_logger

logger = get_logger(__name__)


# ===================================================
# Extraction
# ===================================================

def load_weather_data(raw_folder: Path) -> list[pd.DataFrame]:
    """
    Reads all weather JSON files and converts them into
    individual city DataFrames.

    Parameters
    ----------
    raw_folder : Path
        Folder containing raw JSON files.

    Returns
    -------
    list[pd.DataFrame]
    """

    dataframes = []

    json_files = sorted(raw_folder.glob("*.json"))

    if not json_files:
        logger.error(
            f"No JSON files found inside {raw_folder}"
        )

        raise FileNotFoundError(
            f"No JSON files found inside {raw_folder}"
        )

    for file in json_files:

        logger.info(f"Processing {file.name}")

        city = file.stem

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

        except json.JSONDecodeError:
            logger.exception(f"Invalid JSON: {file.name}")
            continue

        hourly_df = pd.DataFrame(data["hourly"])

        hourly_df.insert(0, "city", city)

        dataframes.append(hourly_df)

    logger.info(
    f"Successfully processed {len(dataframes)} cities."
    )

    return dataframes


# ===================================================
# Merge
# ===================================================

def merge_dataframes(
    dataframes: list[pd.DataFrame]
) -> pd.DataFrame:
    """
    Combines multiple city DataFrames.

    Parameters
    ----------
    dataframes : list[pd.DataFrame]

    Returns
    -------
    pd.DataFrame
    """

    if not dataframes:
        logger.error("No dataframes to merge.")
        raise ValueError("No dataframes supplied.")

    merged_df = pd.concat(
    dataframes,
    ignore_index=True
    )

    logger.info(
        f"Merged {len(dataframes)} dataframes "
        f"into shape {merged_df.shape}"
    )

    return merged_df


# ===================================================
# Validation
# ===================================================

def validate_dataset(df: pd.DataFrame) -> True:
    """
    Performs basic data validation on the processed dataset.
    """

    logger.info("=" * 60)
    logger.info("Starting dataset validation.")

    # Dataset Shape
    logger.info(f"Dataset Shape: {df.shape}")

    # Columns
    logger.info(f"Columns: {list(df.columns)}")

    # Data Types
    logger.info(f"Data Types:\n{df.dtypes}")

    # Missing Values
    missing_values = df.isnull().sum().sum()

    if missing_values == 0:
        logger.info("No missing values found.")
    else:
        logger.warning(
            f"Dataset contains {missing_values} missing value(s)."
        )
        logger.warning(f"\n{df.isnull().sum()}")

    # Duplicate Rows
    duplicate_rows = df.duplicated().sum()

    if duplicate_rows == 0:
        logger.info("No duplicate rows found.")
    else:
        logger.warning(
            f"Dataset contains {duplicate_rows} duplicate row(s)."
        )

    # Unique Cities
    logger.info(
        f"Number of Cities: {df['city'].nunique()}"
    )

    # Records per City
    logger.info(
        f"Records per City:\n{df['city'].value_counts()}"
    )

    # is_day Values
    logger.info(
        f"Unique values in 'is_day': "
        f"{df['is_day'].unique().tolist()}"
    )

    # Time Range
    logger.info(
        f"Time Range: "
        f"{df['time'].min()} --> {df['time'].max()}"
    )

    logger.info("Dataset validation completed successfully.")
    logger.info("=" * 60)


# ===================================================
# Cleaning
# ===================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset.
    """

    df = df.copy(deep=False)

    logger.info(
    "Converting 'time' column to datetime."
    )

    df["time"] = pd.to_datetime(df["time"])

    logger.info(
    "Dataset cleaned successfully."
    )

    return df


# ===================================================
# Feature Engineering
# ===================================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates analytical features.
    """

    logger.info(
    "Starting feature engineering."
    )

    df = df.copy(deep=False)

    df.insert(2, "date", df["time"].dt.date)

    df.insert(3, "hour", df["time"].dt.hour)

    df.insert(4, "day_of_week", df["time"].dt.day_name())

    df.insert(5, "month", df["time"].dt.month)

    df.insert(
        6,
        "is_weekend",
        df["day_of_week"].isin(
            ["Saturday", "Sunday"]
        ),
    )

    logger.info(
    "Created features: "
    "date, hour, day_of_week, month, is_weekend"
    )

    logger.info(
    f"Final dataset shape: {df.shape}"
    )

    return df

# ===================================================
# Export
# ===================================================

def export_dataset(
    df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Exports processed dataset.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        output_path,
        index=False,
    )

    logger.info(
    f"Processed dataset exported to "
    f"{output_path}"
    )