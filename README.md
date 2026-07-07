# Weather Project

This project uses data from the Open-Meteo Historical Weather API for the cities San Jose (CA), Santa Barbara (CA), and Seattle (WA) from 1/1/23 to 12/31/25. Using `requests` for with the given endpoint and query parameters based on the geographic coordinates of the cities provided by the API's documentation, parameters were included in the request to gather daily weather statistics including temperature, precipitation, windspeed, and daylight duration. The JSON responses were then combined, validated, and processed before being saved as two CSV files for populating the database, `cities.csv` containing information about the cities including elevation and timezine and `weather.csv` for the daily statistics.

Since the API is well-created, no issues were found when ingesting and processing the JSON responses. During the requests and ingestion phase, there was no issue accessing the API endpoint using the appropriate path parameters. Early on in project development I looked up approximate coordinates to use for each of the cities before realizing the API's documenation provided them when looking up cities. However I also learned the API automatically adjusted the coordinates in the response to the ones according to their documentation.

The only other issue I encountered was populating the database with the processed csv files. When creating the processed data I manually assigned cities a city_id value. However when creating the schema for the database I defined the city_id column in the primary table as SERIAL. To resolve this after inserting the records into `weather.city`, I manually synced the sequence for city_id in the table using a query to get the next value to be used if another city was added. This processed also could've been resolved not manually assigning cities id values before ingesting and processing the API responses, but the resolution to this decision would've been more complicated than the previous (it would require querying `weather.city` and then aligning rows in `weather.csv` to match accordingly).

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
    ├── __pycache__
    │   ├── __init__.cpython-312.pyc
    │   ├── exceptions.cpython-312.pyc
    │   ├── fetch_weather.cpython-312.pyc
    │   ├── load_data.cpython-312.pyc
    │   └── process_json.cpython-312.pyc
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
