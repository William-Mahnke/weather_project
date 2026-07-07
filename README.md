# Weather Project

This project uses data from the Open-Meteo Historical Weather API for the cities San Jose (CA), Santa Barbara (CA), and Seattle (WA) from 1/1/23 to 12/31/25. Using `requests` for the given endpoint and query parameters based on the geographic coordinates of the cities provided by the API's documentation, parameters were included in the request to gather daily weather statistics including temperature, precipitation, windspeed, and daylight duration. The JSON responses were then combined, validated, and processed before being saved as two CSV files for populating the database, `cities.csv` containing information about the cities including elevation and time zone and `weather.csv` for the daily statistics.

Since the API is well-created, no issues were found when ingesting and processing the JSON responses. During the requests and ingestion phase, there was no issue accessing the API endpoint using the appropriate path parameters. Early on in project development I looked up approximate coordinates to use for each of the cities before realizing the API's documentation provided them when looking up cities. However I also learned the API automatically adjusted the coordinates in the response to the ones according to their documentation.

The only other issue I encountered was populating the database with the processed csv files. When creating the processed data I manually assigned cities a city_id value. However when creating the schema for the database I defined the city_id column in the primary table as SERIAL. To resolve this after inserting the records into `weather.city`, I manually synced the sequence for city_id in the table using a query to get the next value to be used if another city was added. This processed also could've been resolved not manually assigning cities id values before ingesting and processing the API responses, but the resolution to this decision would've been more complicated than the previous (it would require querying `weather.city` and then aligning rows in `weather.csv` to match accordingly).

## Project Setup and Use

### src (python scripts)

- `fetch_weather.py`: Uses cities, longitude, and latitude in `CITIES[list[dict]]` to iterate through and make requests. JSON responses are stored in a created directory `data/raw` (also in gitignore)
- `process_json.py`: Uses JSON files resulting from fetch_weather to combine into one dataframe, validate data for specific conditions, and process the data before being saved in a created directory `data/processed`. Also creates a separate city CSV file which is to be used as the primary data for database population
- `exceptions.py`: custom exceptions used in process_json for errors more specific to the data (invalid date range, missing cities defined in fetch_weather, missing records for a city, and improper numeric values)
- `load_data.py`: script which can be used to populate the database. database information necessary for connection should be stored in `.env`

### sql

- `ddl/schema.sql`: creates schema `weather` for database, creates tables `city` for city related data (corresponds to `cities.csv`) and `statistics` for daily weather data (corresponds to `weather.csv`)
- `dml/insert_data.sql`: sql file for sql option to populate data using CSV files in `data/processed`. commented code is an example of inserting a singular record but shouldn't be used
- `queries/`: contains analytical queries
  - `high_temp_days.sql`: days where max temp reached 90°F or above, per month by city
  - `highest_temperature.sql`: highest temperature for each city and date
  - `total_rain.sql`: total rainfall by month & year for each city
  - `weekly_daylight.sql`: average daylight duration by week for each city
  - `windiest_weeks.sql`: windiest week for each city in each year by average max wind speed

### Other Files

- `.gitignore`
- `instructions.md`
- `requirements.txt`: dependencies used for project
- `response_sample.json`: example of JSON response when using fetch_weather (San Jose, 2023-2025)

### Use

- `python -m src.fetch_weather` to make requests and save JSON responses to data/raw
- `python -m src.process_json` to ingest, validate, and process responses to data/processed (both cities.csv and weather.csv)
- `python -m src.load_data` to populate PostgreSQL database with processed CSV files

- `schema.sql` to create `weather` schema and tables `city` and `statistics`
- `insert_data.sql` can be used in place of `load_data.py` to populate the database, CSV path should be adjusted accordingly if processed data location or file names are changed
- `queries/` to answer analytical questions for database

## Project Structure

├── README.md
├── data
│   ├── old
│   │   ├── cities.csv
│   │   ├── san_jose_2025-01-01_2025-12-31.json
│   │   ├── santa_barbara_2025-01-01_2025-12-31.json
│   │   ├── seattle_2025-01-01_2025-12-31.json
│   │   └── weather.csv
│   ├── processed
│   │   ├── cities.csv
│   │   └── weather.csv
│   └── raw
│       ├── san_jose_2023-01-01_2025-12-31.json
│       ├── santa_barbara_2023-01-01_2025-12-31.json
│       └── seattle_2023-01-01_2025-12-31.json
├── instructions.md
├── requirements.txt
├── response_sample.json
├── sql
│   ├── ddl
│   │   └── schema.sql
│   ├── dml
│   │   └── insert_data.sql
│   └── queries
│       ├── high_temp_days.sql
│       ├── highest_temperature.sql
│       ├── total_rain.sql
│       ├── weekly_daylight.sql
│       └── windiest_weeks.sql
└── src
    ├── __init__.py
    ├── exceptions.py
    ├── fetch_weather.py
    ├── load_data.py
    └── process_json.py

## Data Profiling Output

=== Weather Data Profile ===
Shape: 3288 rows x 9 columns
Cities: ['San Jose', 'Santa Barbara', 'Seattle']
Date range: 2023-01-01 00:00:00 to 2025-12-31 00:00:00
<class 'pandas.DataFrame'>
RangeIndex: 3288 entries, 0 to 3287
Data columns (total 9 columns):

     Column               Non-Null Count  Dtype
---  ------               --------------  -----
 0   time                 3288 non-null   datetime64[us]
 1   temperature_2m_mean  3288 non-null   float64
 2   temperature_2m_max   3288 non-null   float64
 3   temperature_2m_min   3288 non-null   float64
 4   rain_sum             3288 non-null   float64
 5   snowfall_sum         3288 non-null   float64
 6   wind_speed_10m_max   3288 non-null   float64
 7   daylight_duration    3288 non-null   float64
 8   city_name            3288 non-null   str
dtypes: datetime64[us](1), float64(7), str(1)
memory usage: 231.3 KB
       temperature_2m_mean  temperature_2m_max  temperature_2m_min  ...  snowfall_sum  wind_speed_10m_max  daylight_duration
count              3288.00             3288.00             3288.00  ...       3288.00             3288.00            3288.00
mean                 57.31               67.01               48.95  ...          0.01               10.15           43933.64
std                  11.44               14.12                9.81  ...          0.14                3.85            7314.08
min                  17.60               24.40               12.60  ...          0.00                2.30           30311.85
25%                  48.50               56.00               41.40  ...          0.00                7.40           37335.61
50%                  56.50               66.40               48.80  ...          0.00                9.50           43996.20
75%                  65.50               77.60               56.10  ...          0.00               12.40           50473.67
max                  94.10              107.90               81.70  ...          4.77               32.30           57560.40

[8 rows x 7 columns]
No missing values
