-- ==========================================================
-- OpsPulse SQL Analytics
-- File: 03_aggregation_queries.sql
-- Description:
-- Aggregation queries demonstrating the use of aggregate
-- functions, GROUP BY, HAVING, and ORDER BY to generate
-- business insights from the weather_forecast dataset.
-- ==========================================================


-- ==========================================================
-- Query 1
-- Calculate the average temperature for each city
-- ==========================================================

SELECT
    city,
    ROUND(AVG(temperature_2m)::NUMERIC, 2) AS avg_temperature
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 2
-- Calculate the average relative humidity for each city
-- ==========================================================

SELECT
    city,
    ROUND(AVG(relative_humidity_2m)::NUMERIC, 2) AS avg_relative_humidity
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 3
-- Find the maximum wind speed recorded in each city
-- ==========================================================

SELECT
    city,
    MAX(wind_speed_10m) AS max_wind_speed
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 4
-- Calculate the total precipitation received by each city
-- ==========================================================

SELECT
    city,
    SUM(precipitation) AS total_precipitation
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 5
-- Count the total number of weather forecast records
-- available for each city
-- ==========================================================

SELECT
    city,
    COUNT(*) AS total_records
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 6
-- Find the highest temperature recorded in each city
-- ==========================================================

SELECT
    city,
    MAX(temperature_2m) AS max_temperature
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 7
-- Find the lowest temperature recorded in each city
-- ==========================================================

SELECT
    city,
    MIN(temperature_2m) AS min_temperature
FROM weather_forecast
GROUP BY city;


-- ==========================================================
-- Query 8
-- Display cities whose average temperature exceeds 30°C
-- ==========================================================

SELECT
    city,
    ROUND(AVG(temperature_2m)::NUMERIC, 2) AS avg_temperature
FROM weather_forecast
GROUP BY city
HAVING AVG(temperature_2m) > 30;


-- ==========================================================
-- Query 9
-- Display cities whose total precipitation exceeds 100 mm
-- ==========================================================

SELECT
    city,
    SUM(precipitation) AS total_precipitation
FROM weather_forecast
GROUP BY city
HAVING SUM(precipitation) > 100;


-- ==========================================================
-- Query 10
-- Rank cities by average temperature in descending order
-- ==========================================================

SELECT
    city,
    ROUND(AVG(temperature_2m)::NUMERIC, 2) AS avg_temperature
FROM weather_forecast
GROUP BY city
ORDER BY avg_temperature DESC;