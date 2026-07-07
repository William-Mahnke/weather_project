# Weather Project

Cities: San Jose, Santa Barbara, Seattle
Coordinates: San Jose (37.33, 121.88), Santa Barbara (34.42, 119.69), Seattle (47.60, 122.33)

## Project Structure

weather_project/
├── README.md                     # overview, setup, how to run the pipeline
├── requirements.txt              # requests, pandas, psycopg2-binary, python-dotenv
├── .gitignore                    # venv, __pycache__, .env, processed data
├── .env.example                  # DB creds + config template (no secrets)
├── config/
│   └── config.py                 # cities list, date range, API base URL, DB settings
├── src/
│   ├── extract/
│   │   └── fetch_weather.py      # parameterized requests to Open-Meteo (3+ cities)
│   ├── profile/
│   │   └── profile_data.py       # nulls, type checks, value ranges, duplicates
│   ├── transform/
│   │   └── clean_data.py         # flatten JSON + clean into tabular form (pandas)
│   ├── load/
│   │   └── load_to_postgres.py   # connect + bulk insert cleaned records
│   └── pipeline.py               # orchestrates Extract→Profile→Clean→Load
├── sql/
│   ├── ddl/
│   │   └── schema.sql            # CREATE TABLE cities + weather_records (PK/FK)
│   ├── dml/
│   │   └── insert_data.sql       # sample/generated INSERTs
│   └── analysis/                 # 5+ analytical queries, one file each
│       ├── 01_highest_temp_per_city.sql
│       ├── 02_total_monthly_precipitation.sql
│       ├── 03_windiest_week.sql
│       ├── 04_avg_rainfall_by_city.sql
│       └── 05_extreme_temp_day_frequency.sql
├── data/
│   ├── raw/
│   │   └── sample_response.json  # committed sample of raw API JSON (deliverable)
│   └── processed/                # cleaned CSVs (gitignored except maybe a sample)
├── docs/
│   └── summary.md                # the half-to-one-page written summary (deliverable)
└── project1_Instructions.md

## Data Profiling Output

=== Weather Data Profile ===
Shape: 3288 rows x 9 columns
Cities: ['San Jose', 'Santa Barbara', 'Seattle']
Date range: 2023-01-01 00:00:00 to 2025-12-31 00:00:00
<class 'pandas.DataFrame'>
RangeIndex: 3288 entries, 0 to 3287
Data columns (total 9 columns):
 #   Column               Non-Null Count  Dtype
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
