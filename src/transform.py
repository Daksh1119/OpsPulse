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
        raise FileNotFoundError(
            f"No JSON files found inside {raw_folder}"
        )

    for file in json_files:

        print(f"Processing {file.name}")

        city = file.stem

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        hourly_df = pd.DataFrame(data["hourly"])

        hourly_df.insert(0, "city", city)

        dataframes.append(hourly_df)

    print(f"\nProcessed {len(dataframes)} cities.")

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

    return pd.concat(dataframes, ignore_index=True)


# ===================================================
# Validation
# ===================================================

def validate_dataset(df: pd.DataFrame) -> None:
    """
    Performs basic data validation.
    """

    print("\n" + "=" * 60)
    print("DATASET SHAPE")
    print(df.shape)

    print("\n" + "=" * 60)
    print("SAMPLE DATA")
    print(df.head())

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print(df.isnull().sum())

    print("\n" + "=" * 60)
    print("DUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print(df.describe())

    print("\n" + "=" * 60)
    print("UNIQUE CITIES")
    print(df["city"].nunique())

    print("\n" + "=" * 60)
    print("RECORDS PER CITY")
    print(df["city"].value_counts())

    print("\n" + "=" * 60)
    print("UNIQUE VALUES IN is_day")
    print(df["is_day"].unique())

    print("\n" + "=" * 60)
    print("TIME RANGE")
    print(df["time"].min())
    print(df["time"].max())


# ===================================================
# Cleaning
# ===================================================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset.
    """

    df = df.copy()

    df["time"] = pd.to_datetime(df["time"])

    return df


# ===================================================
# Feature Engineering
# ===================================================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates analytical features.
    """

    df = df.copy()

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

    print("\nDataset exported successfully.")
    print(output_path)