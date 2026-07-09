BEGIN;

-- Clear existing data (including reseting SERIAL for city)
TRUNCATE weather.statistics;
TRUNCATE weather.city RESTART IDENTITY CASCADE;

-- Popualte database with processed CSVs
COPY weather.city(city_id, city_name, latitude, longitude, elevation, timezone)
FROM '/tmp/cities.csv'
WITH (FORMAT csv, HEADER true);

-- Sync city_id after load
SELECT setval(
    pg_get_serial_sequence('weather.city', 'city_id'),
    COALESCE((SELECT MAX(city_id) FROM weather.city), 1)
);

COPY weather.statistics(city_id, date, mean_temp_f, max_temp_f, min_temp_f, total_rain_in,
                        total_snow_in, max_wind_speed_mph, daylight_duration_s)
FROM '/tmp/weather.csv'
WITH (FORMAT csv, HEADER true);

COMMIT;