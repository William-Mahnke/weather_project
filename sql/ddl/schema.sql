-- schema
DROP SCHEMA IF EXISTS weather CASCADE;

CREATE SCHEMA weather;

-- city table 
CREATE TABLE weather.city (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(30) NOT NULL,
    latitude NUMERIC CHECK (latitude BETWEEN -90 AND 90) NOT NULL,
    longitude NUMERIC CHECK (longitude BETWEEN -180 AND 180) NOT NULL,
    elevation NUMERIC NOT NULL,
    timezone VARCHAR(40) NOT NULL,
    UNIQUE (latitude, longitude),
    UNIQUE (city_name)
);

-- weather statistics table
CREATE TABLE weather.statistics (
    city_id INTEGER NOT NULL REFERENCES weather.city(city_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    mean_temp_f NUMERIC,
    max_temp_f NUMERIC,
    min_temp_f NUMERIC,
    total_rain_in NUMERIC,
    total_snow_in NUMERIC,
    max_wind_speed_mph NUMERIC,
    daylight_duration_s NUMERIC,
    PRIMARY KEY (city_id, date),
    CHECK (total_rain_in >= 0),
    CHECK (total_snow_in >= 0),
    CHECK (max_wind_speed_mph >= 0)
);