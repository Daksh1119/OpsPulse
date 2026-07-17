-- ==========================================================
-- OpsPulse SQL Analytics
-- File: 01_database_exploration.sql
-- Description:
-- Initial exploration of the weather_forecast table.
-- ==========================================================


-- ==========================================================
-- Query 1
-- Display the first 5 records
-- ==========================================================

SELECT *
FROM weather_forecast
LIMIT 5;


-- ==========================================================
-- Query 2
-- Count total number of records
-- ==========================================================

SELECT COUNT(*) AS total_records
FROM weather_forecast;


-- ==========================================================
-- Query 3
-- Display table schema
-- ==========================================================

SELECT
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'weather_forecast';


-- ==========================================================
-- Query 4
-- Count distinct cities
-- ==========================================================

SELECT COUNT(DISTINCT city) AS total_cities
FROM weather_forecast;


-- ==========================================================
-- Query 5
-- List all cities alphabetically
-- ==========================================================

SELECT DISTINCT city
FROM weather_forecast
ORDER BY city;


-- ==========================================================
-- Query 6
-- Find the earliest forecast timestamp
-- ==========================================================

SELECT city, MIN(forecast_time) AS earliest_timestamp
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 7
-- Find the latest forecast timestamp
-- ==========================================================

SELECT city, MAX(forecast_time) AS latest_timestamp
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 8
-- Count how many records exist for each city
-- ==========================================================

SELECT city, COUNT(*) AS total_records
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 9
-- Count how many records are daytime vs nighttime
-- ==========================================================

SELECT
    CASE
        WHEN is_day THEN 'Daytime'
        ELSE 'Nighttime'
    END AS period,
    COUNT(*) AS total_records
FROM weather_forecast
GROUP BY period;


-- ==========================================================
-- Query 10
-- Find the number of weekend and weekday records
-- ==========================================================

SELECT
    CASE
        WHEN is_weekend THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(*) AS total_records
FROM weather_forecast
GROUP BY day_type;