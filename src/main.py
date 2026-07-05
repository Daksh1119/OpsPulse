"""
Main entry point for the OpsPulse ETL pipeline.
"""

from src.config import (
    RAW_FOLDER,
    OUTPUT_FILE,
)

from src.logger import get_logger

from src.transform import (
    load_weather_data,
    merge_dataframes,
    validate_dataset,
    clean_dataset,
    engineer_features,
    export_dataset,
)

logger = get_logger(__name__)


def main() -> None:
    """
    Executes the complete ETL pipeline.
    """

    logger.info("=" * 60)
    logger.info("OpsPulse ETL Pipeline Started.")

    try:

        # ===================================================
        # Extract
        # ===================================================

        logger.info("Starting data extraction.")

        dataframes = load_weather_data(RAW_FOLDER)

        logger.info("Data extraction completed.")

        # ===================================================
        # Merge
        # ===================================================

        logger.info("Merging city datasets.")

        cities_df = merge_dataframes(dataframes)

        logger.info("Dataset merge completed.")

        # ===================================================
        # Validate
        # ===================================================

        logger.info("Validating dataset.")

        validate_dataset(cities_df)

        logger.info("Dataset validation completed.")

        # ===================================================
        # Clean
        # ===================================================

        logger.info("Cleaning dataset.")

        cities_df = clean_dataset(cities_df)

        logger.info("Dataset cleaning completed.")

        # ===================================================
        # Feature Engineering
        # ===================================================

        logger.info("Starting feature engineering.")

        cities_df = engineer_features(cities_df)

        logger.info("Feature engineering completed.")

        # ===================================================
        # Export
        # ===================================================

        logger.info("Exporting processed dataset.")

        export_dataset(
            cities_df,
            OUTPUT_FILE,
        )

        logger.info("Dataset export completed successfully.")

        logger.info("OpsPulse ETL Pipeline Finished Successfully.")
        logger.info("=" * 60)

    except Exception:

        logger.exception(
            "OpsPulse ETL Pipeline Failed."
        )

        raise


if __name__ == "__main__":
    main()