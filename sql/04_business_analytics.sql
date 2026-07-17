SELECT city, ROUND(AVG(temperature_2m):: numeric, 2) AS max_avg_temperature
FROM weather_forecast
GROUP BY city
ORDER BY AVG(temperature_2m) DESC
LIMIT 1;


SELECT city, ROUND(AVG(temperature_2m):: numeric, 2) AS min_avg_temperature
FROM weather_forecast
GROUP BY city
ORDER BY AVG(temperature_2m) ASC
LIMIT 1;


SELECT city, ROUND(AVG(relative_humidity_2m):: numeric, 2) AS max_avg_humidity
FROM weather_forecast
GROUP BY city
ORDER BY AVG(relative_humidity_2m) DESC
LIMIT 1;


SELECT city, ROUND(SUM(precipitation):: numeric, 2) AS max_total_precipitation
FROM weather_forecast
GROUP BY city
ORDER BY SUM(precipitation) DESC
LIMIT 1;


SELECT city, ROUND(AVG(wind_speed_10m):: numeric, 2) AS max_avg_wind_speed
FROM weather_forecast
GROUP BY city
ORDER BY AVG(wind_speed_10m) DESC
LIMIT 1;