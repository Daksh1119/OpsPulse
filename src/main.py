"""
Main entry point for the OpsPulse ETL pipeline.
"""

from config import (
    RAW_FOLDER,
    OUTPUT_FILE,
)

from transform import (
    load_weather_data,
    merge_dataframes,
    validate_dataset,
    clean_dataset,
    engineer_features,
    export_dataset,
)


def main() -> None:
    """
    Executes the complete ETL pipeline.
    """

    # Extract

    dataframes = load_weather_data(RAW_FOLDER)

    # Merge

    cities_df = merge_dataframes(dataframes)

    # Validate

    validate_dataset(cities_df)

    # Clean

    cities_df = clean_dataset(cities_df)

    # Feature Engineering

    cities_df = engineer_features(cities_df)

    # Export

    export_dataset(
        cities_df,
        OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()