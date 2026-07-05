# OpsPulse

A modular end-to-end ETL pipeline that collects, transforms, validates, and prepares weather forecast data for multiple Indian cities using the Open-Meteo API. The project demonstrates data engineering and data analysis best practices with Python, Pandas, Pytest, and Jupyter Notebook.

---

## Project Overview

OpsPulse automates the process of collecting hourly weather forecast data for multiple Indian cities and transforming it into an analytics-ready dataset.

The project follows a production-style ETL (Extract → Transform → Load) workflow:

- Extract hourly weather forecast data from the Open-Meteo API
- Store raw API responses as JSON files
- Transform nested JSON into structured Pandas DataFrames
- Validate and clean the dataset
- Engineer analytical features
- Export an analytics-ready CSV dataset
- Upsert processed records into Supabase
- Automate testing using Pytest
- Schedule automated ETL execution using GitHub Actions

---

## Project Architecture

```text
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
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
 Validation      Data Cleaning   Feature Engineering
                       │
                       ▼
             Analytics-ready Dataset
                  │             │
                  ▼             ▼
          Processed CSV     Supabase Database
                  │
                  ▼
        Power BI Dashboard (Upcoming)

             ▲
             │
      GitHub Actions
     (Daily Automation)
```

---

## Features

- Modular ETL pipeline
- Automated weather data collection from Open-Meteo API
- Hourly forecast collection for 20 Indian cities
- Raw JSON data storage
- Data transformation using Pandas
- Dataset validation and quality checks
- Datetime parsing and cleaning
- Feature engineering
- Production-style logging
- Automated testing with Pytest
- Exploratory Data Analysis (EDA)
- Statistical analysis and visualizations
- Analytics-ready processed dataset
- Cloud database integration with Supabase
- Automated daily ETL using GitHub Actions
- Environment-based configuration using .env
- Batch upsert into PostgreSQL (Supabase)

---

## Tech Stack

- Python 3.10+
- Pandas
- Requests
- Supabase
- PostgreSQL
- python-dotenv
- Pytest
- GitHub Actions
- Jupyter Notebook
- Open-Meteo API
- Git & GitHub

---

## Project Structure

```text
OpsPulse/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── daily-etl.yml
│
├── data/
│   ├── raw/
│   └── processed/
│
├── logs/
│
├── notebooks/
│   └── eda.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── fetch_weather.py
│   ├── logger.py
│   ├── main.py
│   └── transform.py
│
├── tests/
│   └── test_transform.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── pytest.ini
├── requirements.txt
└── README.md
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

The processed dataset is loaded into two destinations:

- Local analytics-ready CSV
  - `data/processed/weather_processed.csv`

- Supabase PostgreSQL database
  - Batch upsert using a composite unique key (`city`, `forecast_time`)

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

## Cloud Database Integration

OpsPulse stores processed weather forecasts in a Supabase PostgreSQL database.

Features:

- Secure environment variable configuration
- Batch upload for improved performance
- Upsert strategy to prevent duplicate records
- Composite unique constraint on (`city`, `forecast_time`)
- Production-ready logging and error handling

---

## Automation

The ETL pipeline is fully automated using GitHub Actions.

### Continuous Integration

- Runs automatically on every push and pull request
- Installs dependencies
- Executes automated Pytest suite

### Daily ETL Pipeline

Runs every day at **08:00 AM IST**.

Workflow:

1. Fetch latest weather forecast
2. Transform and validate data
3. Engineer analytical features
4. Export processed CSV
5. Upsert records into Supabase

---

## Exploratory Data Analysis

The processed dataset has been analyzed using Jupyter Notebook, Pandas, Matplotlib, and Seaborn.

The EDA includes:

- City-wise temperature comparison
- Humidity analysis
- Wind speed analysis
- Atmospheric pressure analysis
- Precipitation analysis
- Hourly temperature trends
- Temperature variation analysis
- Weekday vs Weekend comparison
- Weather condition frequency analysis
- Correlation analysis
- Distribution analysis

Each visualization is accompanied by statistical insights and business observations.

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

### Completed

- Open-Meteo API Integration
- Modular ETL Pipeline
- Data Validation
- Data Cleaning
- Feature Engineering
- Production Logging
- Automated Testing (Pytest)
- Exploratory Data Analysis
- Statistical Visualizations
- Project Documentation
- ETL Pipeline Automation
- GitHub Repository Enhancements


### In Progress

- Interactive Power BI Dashboard

---

## Future Improvements

- Docker Containerization
- Historical Weather Trend Analysis
- Power BI Dashboard Deployment
- Data Quality Monitoring
- Alerting & Notifications
- REST API for Weather Analytics

---

## Learning Outcomes

This project demonstrates practical experience with:

- REST API Integration
- End-to-End ETL Pipeline Development
- Data Wrangling with Pandas
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Statistical Data Analysis
- Data Visualization
- Production Logging
- Automated Testing with Pytest
- Modular Python Project Architecture
- Git & GitHub Version Control

---

## Author

**Daksh Patel**

B.Tech Computer Engineering

GitHub: https://github.com/Daksh1119

LinkedIn: https://www.linkedin.com/in/dakshpatel11/

---

## License

This project is licensed under the MIT License.