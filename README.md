# OpsPulse

A modular end-to-end ETL pipeline that collects, transforms, validates, and prepares weather forecast data for multiple Indian cities using the Open-Meteo API. The project demonstrates data engineering and data analysis best practices with Python, Pandas, Pytest, and Jupyter Notebook.

---

## Project Overview

OpsPulse automates the process of collecting hourly weather forecast data for multiple Indian cities and transforming it into an analytics-ready dataset.

The project follows a complete ETL (Extract → Transform → Load) workflow:

- Extract weather forecast data from the Open-Meteo API
- Store raw API responses as JSON files
- Transform nested JSON into structured Pandas DataFrames
- Validate and clean the dataset
- Engineer additional analytical features
- Export a processed dataset for further analysis
- Verify pipeline correctness using Pytest

---

## Project Architecture

```
                Open-Meteo API
                       │
                       ▼
            Fetch Weather Data
                       │
                       ▼
          Store Raw JSON Files
                       │
                       ▼
         ETL Transformation Pipeline
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Validation     Data Cleaning   Feature Engineering
        │
        ▼
   Processed CSV Dataset
        │
        ▼
 Exploratory Data Analysis (Upcoming)
```

---

## Features

- Modular ETL pipeline
- Weather data collection for 20 Indian cities
- Raw JSON data storage
- Automatic DataFrame generation
- Dataset validation
- Datetime conversion
- Feature engineering
- Automated testing using Pytest
- Analytics-ready processed dataset

---

## Tech Stack

- Python 3.10+
- Pandas
- Requests
- Pytest
- Jupyter Notebook
- Open-Meteo API
- Git & GitHub

---

## Project Structure

```
OpsPulse/
│
├── data/
│   ├── input/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── eda.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── fetch_weather.py
│   ├── transform.py
│   └── main.py
│
├── tests/
│   └── test_transform.py
│
├── pyproject.toml
├── pytest.ini
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ETL Workflow

### 1. Extract

- Read city list
- Fetch hourly weather forecast from Open-Meteo API
- Save raw API response as JSON

### 2. Transform

- Parse nested JSON
- Convert to DataFrame
- Merge all cities
- Validate dataset
- Clean timestamp column
- Engineer analytical features

### 3. Load

Export the final processed dataset as:

```
data/processed/weather_processed.csv
```

---

## Engineered Features

The ETL pipeline creates the following additional columns:

| Feature | Description |
|----------|-------------|
| date | Calendar date |
| hour | Hour of the day |
| day_of_week | Weekday name |
| month | Month number |
| is_weekend | Weekend indicator |

---

## Dataset Information

Current dataset includes:

- 20 Indian Cities
- 7-Day Forecast
- Hourly Weather Data
- 3,360 Records
- Weather Parameters:
  - Temperature
  - Humidity
  - Wind Speed
  - Wind Direction
  - Cloud Cover
  - Atmospheric Pressure
  - Precipitation
  - Weather Code
  - Day/Night Indicator

---

## Validation Checks

The transformation pipeline validates:

- Dataset shape
- Missing values
- Duplicate records
- Data types
- Summary statistics
- Time range
- Records per city
- Unique city count

---

## Testing

The project includes automated tests using Pytest.

Current tests verify:

- Dataset is not empty
- Required columns exist
- No duplicate rows
- Datetime conversion
- Expected number of cities

Run tests:

```bash
pytest -v
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Daksh1119/OpsPulse.git
```

Navigate into the project

```bash
cd OpsPulse
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Execute the ETL pipeline

```bash
python -m src.main
```

---

## Current Status

Completed

- API Integration
- ETL Pipeline
- Data Validation
- Data Cleaning
- Feature Engineering
- Automated Testing

In Progress

- Exploratory Data Analysis
- Data Visualization
- Dashboard
- Documentation Enhancements

---

## Future Improvements

- Interactive Power BI Dashboard
- Historical Weather Analysis
- Scheduled Data Collection
- Database Integration
- Data Quality Reports
- Docker Support
- CI/CD Pipeline
- Logging Framework

---

## Learning Outcomes

This project demonstrates practical experience with:

- REST API Integration
- ETL Pipeline Design
- Data Wrangling
- Data Validation
- Feature Engineering
- Software Testing
- Python Project Structuring
- Git Version Control

---

## Author

**Daksh Patel**

B.Tech Computer Engineering

GitHub: https://github.com/Daksh1119

LinkedIn: https://www.linkedin.com/in/dakshpatel11/

---

## License

This project is licensed under the MIT License.