import pandas as pd
import requests
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from datetime import timezone, datetime
from pathlib import Path
from src.logger import get_logger
from src.config import AWS_REGION, S3_BUCKET_NAME, S3_UPLOAD_ENABLED

logger = get_logger(__name__)

s3_client = boto3.client("s3", region_name=AWS_REGION) if S3_UPLOAD_ENABLED else None


def upload_to_s3(local_path: Path, city: str, run_date: str) -> None:
    """
    Upload a raw JSON file to S3, partitioned by ingestion date.
    Failures here are logged but never break the local pipeline —
    S3 is a durability layer on top of local storage, not a
    replacement for it.
    """
    if not S3_UPLOAD_ENABLED:
        return

    s3_key = f"raw/{run_date}/{local_path.name}"

    try:
        s3_client.upload_file(
            str(local_path),
            S3_BUCKET_NAME,
            s3_key,
        )
        logger.info(f"Uploaded {local_path.name} to s3://{S3_BUCKET_NAME}/{s3_key}")

    except (BotoCoreError, ClientError) as e:
        logger.error(f"S3 upload failed for {city}: {e}")

# Load city list
cities = pd.read_csv("data/input/cities.csv")

raw_path = Path("data/raw")
raw_path.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://api.open-meteo.com/v1/forecast"

HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "cloud_cover",
    "pressure_msl",
    "wind_speed_10m",
    "wind_direction_10m",
    "weather_code",
    "is_day"
]

logger.info("Starting weather data extraction.")

for _, row in cities.iterrows():

    city = row["City"]

    logger.info(f"Fetching weather data for {city}")

    params = {
        "latitude": row["Latitude"],
        "longitude": row["Longitude"],
        "hourly": ",".join(HOURLY_VARIABLES),
        "forecast_days": 7,
        "timezone": "auto"
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        output_file = (
            raw_path /
            f"{city.lower().replace(' ', '_')}.json"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, indent=4)

        logger.info(f"Saved {output_file.name}")

        run_date = datetime.now(timezone.utc).date().isoformat()
        upload_to_s3(output_file, city, run_date)

    except requests.RequestException as e:
        logger.error(
            f"Failed to fetch weather for {city}. "
            f"Status Code: {getattr(e.response, 'status_code', 'N/A')}"
        )
        logger.exception(
            f"Unexpected error while fetching weather for {city}"
        )

logger.info(
    f"Weather data extraction completed successfully. "
    f"Processed {len(cities)} cities."
)