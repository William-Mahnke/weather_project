import pandas as pd
import psycopg
from pathlib import Path
import os
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent

load_dotenv(ROOT / ".env") 

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "port": int(os.environ["DB_PORT"]),
    "dbname": os.environ["DB_NAME"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"]
}

CITIES_CSV = ROOT / "data/processed/cities.csv"
WEATHER_CSV = ROOT / "data/processed/weather.csv"

def load_cities(conn: psycopg.Connection) -> None:
    df = pd.read_csv(CITIES_CSV)
    sql = """
        INSERT INTO weather.city
            (city_id, city_name, latitude, longitude, elevation, timezone)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cursor:
        cursor.executemany(sql, df.itertuples(index = False, name = None))

        # sync SERIAL with explicitly given ids from CSV
        cursor.execute("""
            SELECT setval(
                pg_get_serial_sequence('weather.city', 'city_id'),
                COALESCE((SELECT MAX(city_id) FROM weather.city), 1)
            )
        """)

def load_weather(conn: psycopg.Connection) -> None:
    df = pd.read_csv(WEATHER_CSV)
    sql = """
        INSERT INTO weather.statistics
            (city_id, date, mean_temp_f, max_temp_f, min_temp_f,
             total_rain_in, total_snow_in, max_wind_speed_mph, daylight_duration_s)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with conn.cursor() as cur:
        cur.executemany(sql, df.itertuples(index = False, name = None))

def truncate_tables(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE weather.statistics")
        cur.execute("TRUNCATE weather.city RESTART IDENTITY CASCADE")
def verify_load(conn) -> None:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM weather.city")
        print(f"Cities loaded: {cur.fetchone()[0]}")  # expect 3
        cur.execute("SELECT COUNT(*) FROM weather.statistics")
        print(f"Weather rows loaded: {cur.fetchone()[0]}")  # expect 3288
        cur.execute("""
            SELECT c.city_name, COUNT(*) AS days
            FROM weather.statistics s
            JOIN weather.city c USING (city_id)
            GROUP BY c.city_name
            ORDER BY c.city_name
        """)
        for row in cur.fetchall():
            print(row)
def main() -> None:
    with psycopg.connect(**DB_CONFIG) as conn:
        truncate_tables(conn)      # safe re-run
        load_cities(conn)
        load_weather(conn)
        conn.commit()
        verify_load(conn)
if __name__ == "__main__":
    main()