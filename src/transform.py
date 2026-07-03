"""
transform.py

Transforms raw weather JSON files into a cleaned and analytics-ready dataset.
"""

from pathlib import Path
import json
import pandas as pd

# ==============================
# Configuration
# ==============================

RAW_FOLDER = Path("data/raw")
PROCESSED_FOLDER = Path("data/processed")
OUTPUT_FILE = PROCESSED_FOLDER / "weather_processed.csv"


# ==============================
# ETL Functions
# ==============================

def load_weather_data(raw_folder: Path) -> list[pd.DataFrame]:
    """
    Reads all JSON files from the raw folder and returns
    a list of city-wise DataFrames.
    """

    all_dataframes = []

    for file in raw_folder.glob("*.json"):

        print(f"Processing: {file.name}")

        city = file.stem

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        hourly_df = pd.DataFrame(data["hourly"])

        hourly_df.insert(0, "city", city)

        all_dataframes.append(hourly_df)

    print(f"\nProcessed {len(all_dataframes)} cities.")

    return all_dataframes


def merge_dataframes(dataframes: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Merges all city DataFrames into one master DataFrame.
    """

    return pd.concat(dataframes, ignore_index=True)


# ==============================
# Validation
# ==============================

def validate_dataset(df: pd.DataFrame) -> None:
    """
    Prints useful validation statistics.
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
    print(df["city"].unique())

    print("\n" + "=" * 60)
    print("RECORDS PER CITY")
    print(df["city"].value_counts())

    print("\n" + "=" * 60)
    print("UNIQUE VALUES IN is_day")
    print(df["is_day"].unique())

    print("\n" + "=" * 60)
    print("FIRST FIVE TIMESTAMPS")
    print(df["time"].head())

    print("\n" + "=" * 60)
    print("TIME RANGE")
    print(df["time"].min())
    print(df["time"].max())


# ==============================
# Cleaning
# ==============================

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset.
    """

    df["time"] = pd.to_datetime(df["time"])

    return df


# ==============================
# Feature Engineering
# ==============================

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates additional analytical features.
    """

    df.insert(2, "date", df["time"].dt.date)

    df.insert(3, "hour", df["time"].dt.hour)

    df.insert(4, "day_of_week", df["time"].dt.day_name())

    df.insert(5, "month", df["time"].dt.month)

    df.insert(
        6,
        "is_weekend",
        df["day_of_week"].isin(["Saturday", "Sunday"])
    )

    return df


# ==============================
# Export
# ==============================

def export_dataset(df: pd.DataFrame, output_path: Path) -> None:
    """
    Exports the processed dataset to CSV.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print("\nData exported successfully!")

    print(output_path)


# ==============================
# Main Pipeline
# ==============================

def main():

    all_dataframes = load_weather_data(RAW_FOLDER)

    cities_df = merge_dataframes(all_dataframes)

    validate_dataset(cities_df)

    cities_df = clean_dataset(cities_df)

    cities_df = engineer_features(cities_df)

    export_dataset(cities_df, OUTPUT_FILE)


# ==============================
# Entry Point
# ==============================

if __name__ == "__main__":
    main()