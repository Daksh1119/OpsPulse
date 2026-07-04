import pytest
import pandas as pd

from src.config import RAW_FOLDER

from src.transform import (
    load_weather_data,
    merge_dataframes,
    clean_dataset,
    engineer_features,
)

@pytest.fixture(scope="module")
def processed_df():
    """
    Creates a processed DataFrame once for all tests.
    """

    dataframes = load_weather_data(RAW_FOLDER)

    df = merge_dataframes(dataframes)

    df = clean_dataset(df)

    df = engineer_features(df)

    return df


# TEST 1 - DataFrame is not empty

def test_dataframe_is_not_empty(processed_df):

    assert not processed_df.empty


# TEST 2 - Expected columns exist


def test_expected_columns_exist(processed_df):

    expected_columns = {
        "city",
        "time",
        "date",
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "cloud_cover",
        "pressure_msl",
        "wind_speed_10m",
        "wind_direction_10m",
        "weather_code",
        "is_day",
    }

    assert expected_columns.issubset(processed_df.columns)


# TEST 3 - No duplicate rows


def test_no_duplicate_rows(processed_df):

    assert processed_df.duplicated().sum() == 0


# TEST 4 - Datetime conversion


def test_time_column_is_datetime(processed_df):

    assert pd.api.types.is_datetime64_any_dtype(
        processed_df["time"]
    )


# TEST 5 - Exactly 20 Cities


def test_twenty_unique_cities(processed_df):

    assert processed_df["city"].nunique() == 20