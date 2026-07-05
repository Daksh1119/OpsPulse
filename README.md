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
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Validation      Data Cleaning   Feature Engineering
                      │
                      ▼
          Processed CSV Dataset
                │          │
                ▼          ▼
        Automated Tests   EDA Notebook
                             │
                             ▼
                  Power BI Dashboard (Upcoming)
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

### In Progress

- Interactive Power BI Dashboard
- ETL Pipeline Automation
- GitHub Repository Enhancements

---

## Future Improvements

- Interactive Power BI Dashboard
- Automated ETL Scheduling
- GitHub Actions CI/CD
- Database Integration (PostgreSQL/Supabase)
- Docker Containerization
- Historical Weather Trend Analysis
- Data Quality Reporting
- Cloud Deployment

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