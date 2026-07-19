# OpsPulse

A modular, cloud-integrated end-to-end ETL pipeline that collects, transforms, validates, and prepares weather forecast data for multiple Indian cities using the Open-Meteo API. The project demonstrates production-style data engineering practices — durable cloud storage, centralized observability, automated alerting, and CI/CD — built with Python, Pandas, AWS, Supabase, and GitHub Actions.

---

## Project Overview

OpsPulse automates the process of collecting hourly weather forecast data for multiple Indian cities and transforming it into an analytics-ready dataset, while persisting raw data durably in the cloud and monitoring the pipeline's health automatically.

The project follows a production-style ETL (Extract → Transform → Load) workflow, backed by cloud infrastructure rather than local-only storage:

- Extract hourly weather forecast data from the Open-Meteo API
- Persist raw API responses locally and in an **AWS S3 data lake**, partitioned by ingestion date
- Transform nested JSON into structured Pandas DataFrames
- Validate and clean the dataset
- Engineer analytical features
- Export an analytics-ready CSV dataset
- Upsert processed records into Supabase
- Stream pipeline logs to **AWS CloudWatch** for centralized observability
- Automatically alert via **AWS SNS** when pipeline errors occur
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
              ┌───────────┴───────────┐
              ▼                       ▼
     Store Raw JSON Files     AWS S3 (Raw Data Lake)
     (local staging area)     date-partitioned, 30-day
                              lifecycle expiry
              │
              ▼
        ETL Transformation Pipeline
              │
 ┌────────────┼────────────┐
 ▼            ▼            ▼
Validation  Cleaning  Feature Engineering
              │
              ▼
     Analytics-ready Dataset
       │               │
       ▼               ▼
 Processed CSV   Supabase Database
                        │
                        ▼
             Power BI Dashboard (Upcoming)

     ─────────────────────────────────
     Cross-cutting Cloud Infrastructure
     ─────────────────────────────────

  Application Logs
        │
        ▼
  AWS CloudWatch Logs (/opspulse/etl)
        │
        ▼
  Metric Filter → ErrorCount metric
        │
        ▼
  CloudWatch Alarm (threshold ≥ 1/day)
        │
        ▼
  AWS SNS Topic → Email Notification

              ▲
              │
       GitHub Actions
      (Daily Automation,
   least-privilege IAM user)
```

---

## Features

- Modular ETL pipeline
- Automated weather data collection from Open-Meteo API
- Hourly forecast collection for 20 Indian cities
- Raw JSON data storage — local and cloud (AWS S3)
- **AWS S3 data lake** for raw data, partitioned by ingestion date (`raw/YYYY-MM-DD/`)
- **S3 lifecycle policy** to auto-expire raw data after 30 days, keeping storage cost bounded
- **Least-privilege IAM** — dedicated CI user scoped to only the specific S3 actions and CloudWatch log group it needs
- Data transformation using Pandas
- Dataset validation and quality checks
- Datetime parsing and cleaning
- Feature engineering
- Production-style logging — local file, console, and **AWS CloudWatch Logs**
- **Automated failure alerting** via CloudWatch Metric Filters, Alarms, and Amazon SNS
- Automated testing with Pytest
- Exploratory Data Analysis (EDA)
- Statistical analysis and visualizations
- Analytics-ready processed dataset
- Cloud database integration with Supabase
- Automated daily ETL using GitHub Actions
- Environment-based configuration using .env, with feature flags for optional cloud integrations
- Batch upsert into PostgreSQL (Supabase)

---

## Tech Stack

- Python 3.10+
- Pandas
- Requests
- **AWS S3** (raw data lake)
- **AWS CloudWatch** (centralized logging & metrics)
- **AWS SNS** (alerting/notifications)
- **AWS IAM** (least-privilege access control)
- boto3 / watchtower
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
│   ├── raw/            # local staging (git-ignored, mirrored to S3)
│   └── processed/      # local staging (git-ignored)
│
├── logs/
│
├── notebooks/
│   └── eda.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py        # env config, incl. AWS/S3/CloudWatch settings
│   ├── database.py
│   ├── fetch_weather.py # extraction + S3 upload
│   ├── logger.py         # local + CloudWatch logging handler
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
- Save raw API response as JSON locally
- Upload raw JSON to **AWS S3**, partitioned by ingestion date (`raw/YYYY-MM-DD/{city}.json`)
- Upload failures are logged but never break the pipeline — S3 is a durability layer on top of local storage, not a hard dependency

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

## Cloud Infrastructure

### AWS S3 — Raw Data Lake

Raw weather API responses are persisted in a dedicated S3 bucket (`opspulse-raw-weather-data`), organized as an immutable, date-partitioned raw/bronze layer:

```
s3://opspulse-raw-weather-data/raw/2026-07-19/mumbai.json
s3://opspulse-raw-weather-data/raw/2026-07-19/delhi.json
...
```

This separates the **raw, replayable** data layer from the **queryable, processed** layer in Supabase — each storage system used for what it's good at, rather than defaulting to one tool for everything. A **lifecycle rule** automatically expires objects after 30 days, keeping storage cost effectively flat regardless of how long the pipeline runs.

### AWS CloudWatch — Centralized Logging

Application logs (`src/logger.py`) are streamed to a dedicated CloudWatch Log Group (`/opspulse/etl`) in addition to local file and console output, so pipeline runs — including scheduled GitHub Actions runs — are visible centrally rather than locked inside ephemeral CI logs.

### AWS SNS — Automated Alerting

A CloudWatch Metric Filter scans the log group for `ERROR`-level entries and publishes a custom metric (`OpsPulse/ErrorCount`). A CloudWatch Alarm evaluates this metric daily and, when triggered, publishes to an SNS topic (`opspulse-alerts`), sending an immediate email notification — closing the loop on pipeline failure detection without manual log-checking.

### IAM — Least-Privilege Access

The CI/CD credentials used by GitHub Actions belong to a dedicated IAM user (`opspulse-ci-deploy`), scoped by inline policy to only:
- `s3:PutObject` on the `raw/*` prefix of the specific bucket
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`, `logs:DescribeLogStreams` on the specific log group

No broader permissions, no root credentials in any automation path.

### Feature Flags for Optional Cloud Dependencies

All AWS integrations are gated behind environment variable flags (`S3_UPLOAD_ENABLED`, `CLOUDWATCH_ENABLED`), so the pipeline degrades gracefully to local-only operation if cloud credentials aren't configured — useful for local development, testing, or onboarding without requiring AWS access.

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

The ETL pipeline is fully automated using GitHub Actions, secured with least-privilege IAM credentials stored as encrypted repository secrets.

### Continuous Integration

- Runs automatically on every push and pull request
- Installs dependencies
- Executes automated Pytest suite

### Daily ETL Pipeline

Runs every day at **08:00 AM IST**.

Workflow:

1. Fetch latest weather forecast
2. Upload raw data to AWS S3
3. Transform and validate data
4. Engineer analytical features
5. Export processed CSV
6. Upsert records into Supabase
7. Stream logs to CloudWatch; trigger SNS alert on failure

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

Configure environment variables

```bash
cp .env.example .env
```

Populate `.env` with your Supabase credentials and, optionally, AWS credentials to enable the S3 and CloudWatch integrations (`S3_UPLOAD_ENABLED=true`, `CLOUDWATCH_ENABLED=true`). The pipeline runs normally without these if left disabled.

---

## Running the Project

Fetch raw weather data (extract + optional S3 upload)

```bash
python -m src.fetch_weather
```

Execute the full ETL pipeline (transform, validate, load)

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
- Production Logging (local, console, and AWS CloudWatch)
- AWS S3 Raw Data Lake with date-partitioning and lifecycle expiry
- AWS SNS Alerting on pipeline failures via CloudWatch Alarms
- Least-Privilege IAM Configuration
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
- Migrate scheduled extraction from GitHub Actions to AWS Lambda + EventBridge
- AWS Secrets Manager for credential management
- REST API for Weather Analytics

---

## Learning Outcomes

This project demonstrates practical experience with:

- REST API Integration
- End-to-End ETL Pipeline Development
- Cloud Data Lake Design (AWS S3)
- Cloud Observability & Alerting (AWS CloudWatch, SNS)
- Least-Privilege IAM & Cloud Security Practices
- Data Wrangling with Pandas
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Statistical Data Analysis
- Data Visualization
- Production Logging
- Automated Testing with Pytest
- Modular Python Project Architecture
- Git & GitHub Version Control
- CI/CD with GitHub Actions

---

## Author

**Daksh Patel**

B.Tech Computer Engineering

GitHub: https://github.com/Daksh1119

LinkedIn: https://www.linkedin.com/in/dakshpatel11/

---

## License

This project is licensed under the MIT License.