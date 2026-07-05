"""
Database utilities for OpsPulse.

Handles:
- Connecting to Supabase
- Uploading processed weather data
- Connection testing
"""

from typing import List

import pandas as pd
from supabase import Client, create_client

from src.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)

from src.logger import get_logger

logger = get_logger(__name__)


TABLE_NAME = "weather_forecast"


def get_supabase_client() -> Client:
    """
    Creates and returns a Supabase client.
    """

    if not SUPABASE_URL:
        raise ValueError(
            "SUPABASE_URL not found in environment variables."
        )

    if not SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError(
            "SUPABASE_SERVICE_ROLE_KEY not found in environment variables."
        )

    logger.info("Connecting to Supabase...")

    client = create_client(
        SUPABASE_URL,
        SUPABASE_SERVICE_ROLE_KEY
    )

    logger.info("Successfully connected to Supabase.")

    return client


def dataframe_to_records(df: pd.DataFrame) -> List[dict]:
    """
    Converts a pandas DataFrame into JSON-serializable records
    suitable for Supabase insertion.
    """

    upload_df = df.copy()

    # Rename time column to match database schema
    upload_df.rename(
        columns={"time": "forecast_time"},
        inplace=True
    )

    # Convert timestamp to ISO-8601 string
    upload_df["forecast_time"] = (
        pd.to_datetime(upload_df["forecast_time"])
        .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    # Drop columns that are NOT stored in Supabase
    upload_df.drop(
        columns=[
            "date",
            "hour",
            "day_of_week",
        ],
        errors="ignore",
        inplace=True,
    )

    # Convert is_day to boolean
    upload_df["is_day"] = upload_df["is_day"].astype(bool)

    # Convert any remaining date/datetime objects to strings
    for column in upload_df.columns:
        if upload_df[column].dtype == "object":
            upload_df[column] = upload_df[column].apply(
                lambda x: x.isoformat() if hasattr(x, "isoformat") else x
            )

    return upload_df.to_dict(orient="records")


def upload_weather_data(
    df: pd.DataFrame,
    batch_size: int = 500
) -> None:
    """
    Uploads processed weather data to Supabase.

    Parameters
    ----------
    df : pd.DataFrame
        Processed weather dataframe.

    batch_size : int
        Number of rows uploaded per request.
    """

    if df.empty:
        logger.warning("DataFrame is empty. Nothing to upload.")
        return

    client = get_supabase_client()

    records = dataframe_to_records(df)

    total_records = len(records)

    logger.info(
        f"Preparing to upload {total_records} records..."
    )

    try:

        for start in range(
            0,
            total_records,
            batch_size
        ):

            end = start + batch_size

            batch = records[start:end]

            (
                client.table(TABLE_NAME)\
                .upsert(
                    batch,
                    on_conflict="city,forecast_time"
                )\
                .execute()
            )

            logger.info(
                f"Uploaded records "
                f"{start + 1}-{min(end, total_records)}"
            )

        logger.info(
            f"Successfully uploaded "
            f"{total_records} records to Supabase."
        )

    except Exception as e:

        logger.exception(
            "Supabase upload failed."
        )

        raise RuntimeError(
            f"Upload failed: {e}"
        )


def test_connection() -> None:
    """
    Tests whether the Supabase connection is working.
    """

    try:

        client = get_supabase_client()

        (
            client.table(TABLE_NAME)
            .select("id")
            .limit(1)
            .execute()
        )

        logger.info(
            "Supabase connection test passed."
        )

    except Exception as e:

        logger.exception(
            "Supabase connection test failed."
        )

        raise RuntimeError(
            f"Unable to connect to Supabase: {e}"
        )