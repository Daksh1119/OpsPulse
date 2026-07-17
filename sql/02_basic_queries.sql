-- ==========================================================
-- OpsPulse SQL Analytics
-- File: 02_basic_queries.sql
-- Description:
-- Basic SQL queries demonstrating filtering, sorting,
-- comparison operators, logical operators, and limiting
-- results using the weather_forecast dataset.
-- ==========================================================


-- ==========================================================
-- Query 1
-- Retrieve all weather records for Mumbai
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE city = 'mumbai';


-- ==========================================================
-- Query 2
-- Display forecasts where the temperature exceeds 30°C
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE temperature_2m > 30;


-- ==========================================================
-- Query 3
-- Retrieve all records where relative humidity is above 85%
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE relative_humidity_2m > 85;


-- ==========================================================
-- Query 4
-- Display forecasts with precipitation greater than 5 mm
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE precipitation > 5;


-- ==========================================================
-- Query 5
-- Retrieve forecasts where cloud cover exceeds 90%
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE cloud_cover > 90;


-- ==========================================================
-- Query 6
-- Display all daytime weather forecasts
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE is_day = TRUE;


-- ==========================================================
-- Query 7
-- Retrieve weekend forecasts where temperature exceeds 28°C
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE is_weekend = TRUE
  AND temperature_2m > 28;


-- ==========================================================
-- Query 8
-- Display the 10 hottest weather forecasts
-- ==========================================================

SELECT *
FROM weather_forecast
ORDER BY temperature_2m DESC
LIMIT 10;


-- ==========================================================
-- Query 9
-- Display the 10 forecasts with the highest wind speed
-- ==========================================================

SELECT *
FROM weather_forecast
ORDER BY wind_speed_10m DESC
LIMIT 10;


-- ==========================================================
-- Query 10
-- Retrieve weather forecasts for Mumbai and Pune,
-- ordered chronologically by forecast time
-- ==========================================================

SELECT *
FROM weather_forecast
WHERE city IN ('mumbai', 'pune')
ORDER BY forecast_time;