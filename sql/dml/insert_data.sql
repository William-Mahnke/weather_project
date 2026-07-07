\set ON_ERROR_STOP on

-- Clear existing data (including reseting SERIAL for city)
TRUNCATE weather.statistics;
TRUNCATE weather.city RESTART IDENTITY CASCADE;

-- Popualte database with processed CSVs
\copy weather.city(city_id, city_name, latitude, longitude, elevation, timezone)
FROM 'data/processed/cities.csv'
WITH (FORMAT csv, HEADER true);

-- Sync city_id after load
SELECT setval(
    pg_get_serial_sequence('weather.city', 'city_id'),
    COALESCE((SELECT MAX(city_id) FROM weather.city), 1)
);

\copy weather.statistics(city_id, date, mean_temp_f, max_temp_f, min_temp_f, total_rain_in,
                        total_snow_in, max_wind_speed_mph, daylight_duration_s)
FROM 'data/processed/weather.csv'
WITH (FORMAT csv, HEADER true);

-- Example insert pattern (one city row):
/*
INSERT INTO weather.city
    (city_id, city_name, latitude, longitude, elevation, timezone)
VALUES
     (1, 'San Jose', 37.293495, -121.870026, 73.0, 'America/Los_Angeles');

Example DML pattern (one weather row):
INSERT INTO weather.statistics
     (city_id, date, mean_temp_f, max_temp_f, min_temp_f,
      total_rain_in, total_snow_in, max_wind_speed_mph, daylight_duration_s)
 VALUES
     (1, '2023-01-01', 49.2, 57.4, 42.4, 0.0, 0.0, 12.7, 34732.49);
*/