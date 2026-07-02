import pandas as pd
import requests
import json
from pathlib import Path

# Load city list
cities = pd.read_csv("data/input/cities.csv")

raw_path = Path("data/raw")

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

for _, row in cities.iterrows():

    params = {
        "latitude": row["Latitude"],
        "longitude": row["Longitude"],
        "hourly": ",".join(HOURLY_VARIABLES),
        "forecast_days": 7,
        "timezone": "auto"
    }

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    output_file = raw_path / f"{row['City'].lower().replace(' ','_')}.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(response.json(), f, indent=4)