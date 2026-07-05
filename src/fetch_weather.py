import pandas as pd
import requests
import json
from pathlib import Path
from src.logger import get_logger

logger = get_logger(__name__)

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