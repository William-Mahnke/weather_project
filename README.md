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
