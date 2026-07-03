from pathlib import Path
import json
import pandas as pd
import datetime

raw_folder = Path("data/raw")

# Creating dataframes for all 20 cities

all_dataframes = []

for file in raw_folder.glob("*.json"):

    print(f"Processing:", file)

    # Extract city name
    city = file.stem
    
    # Load JSON file
    with open(file, "r", encoding='utf-8') as f:
        data = json.load(f)

    # Create DataFrame
    hourly_df = pd.DataFrame(data["hourly"])

    # Add new column named 'city'
    hourly_df.insert(0, 'city', city)

    # Store df into all DataFrames
    all_dataframes.append(hourly_df)

print(f"\n Processed {len(all_dataframes)} cities.")

cities_df = pd.concat(all_dataframes, ignore_index=True)

# Validation Section

print("=" * 60)
print("DATASET SHAPE")
print(cities_df.shape)

print("=" * 60)
print("SAMPLE DATA")
print(cities_df.head())

print("=" * 60)
print("DATA TYPES")
print(cities_df.dtypes)

print("=" * 60)
print("MISSING VALUES")
print(cities_df.isnull().sum())

print("=" * 60)
print("DUPLICATE VALUES")
print(cities_df.duplicated().sum())

print("=" * 60)
print("DATAFRAME DESCRIPTION")
print(cities_df.describe())

print("=" * 60)
print("UNIQUE CITIES")
print(cities_df["city"].unique())

print("=" * 60)
print("RECORDS PER CITIES")
print(cities_df["city"].value_counts())

print("=" * 60)
print("UNIQUE ENTRIES IN is_day COLUMN")
print(cities_df["is_day"].unique())

print("=" * 60)
print("FIRST 5 TIMEFRAMES")
print(cities_df["time"].head())

print("=" * 60)
print("TIME RANGE")
print(cities_df["time"].min())
print(cities_df["time"].max())


# Data Cleaning Process

# Converting dtype of "time" from object type to datetime type
cities_df["time"] = pd.to_datetime(cities_df["time"])
print(cities_df["time"].dtype)


# Feature Engineering

# Extracting Date, Hour, Day_of_week, Month, Is_weekend
cities_df.insert(2, "date", cities_df["time"].dt.date)

cities_df.insert(3, "hour", cities_df["time"].dt.hour)

cities_df.insert(4, "day_of_week", cities_df["time"].dt.day_name())

cities_df.insert(5, "month", cities_df["time"].dt.month)

cities_df.insert(6, "is_weekend", cities_df["day_of_week"].isin(['Saturday', 'Sunday']))

print(cities_df.head())
print("Data is ready to be exported!")


# Exporting Data into a final CSV file 
cities_df.to_csv("data/processed/weather_processed.csv", index=False)