import json
from pathlib import Path
import requests

# base api url
URL = "https://archive-api.open-meteo.com/v1/archive"

# coordinates for cities
CITIES = [
    {"name": "San Jose", "state": "California", "latitude": 37.33, "longitude": -121.88, "id": 1},
    {"name": "Santa Barbara", "state": "California", "latitude": 34.42, "longitude": -119.69, "id": 2},
    {"name": "Seattle", "state": "Washington", "latitude": 47.60, "longitude": -122.33, "id": 3},
]

# date range for project (all of 2025)
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# parameters shared by every request
BASE_PARAMS = {
    "daily": ",".join([
		"temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
		"rain_sum", "snowfall_sum", "wind_speed_10m_max", "daylight_duration",
	]),
	"timezone": "America/Los_Angeles",
	"temperature_unit": "fahrenheit",
	"wind_speed_unit": "mph",
	"precipitation_unit": "inch"
}

# path to save raw json files
RAW_DIR = Path("data/raw")

# request for daily weather data for city over date range
def get_city_data(city: dict) -> dict:
    params = {**BASE_PARAMS, "latitude": city["latitude"], "longitude": city["longitude"],
                "start_date": START_DATE, "end_date": END_DATE}
    response = requests.get(URL, params = params, timeout = 30)
    response.raise_for_status()
    return response.json()

# create string named for saved json files
def slugify_city(name: str) -> str:
    return name.lower().replace(" ", "_")

# wrapper for making and saving requests for data
def wrapper():
    RAW_DIR.mkdir(parents = True, exist_ok = True)
    for city in CITIES:
        data = get_city_data(city)
        data["city_name"] = city["name"]

        out_path = RAW_DIR / f"{slugify_city(city["name"])}_{START_DATE}_{END_DATE}.json"
        with out_path.open("w", encoding = "utf-8") as f:
            json.dump(data, f, indent = 4)
        print(f"Saved {city["name"]} -> {out_path}")

if __name__ == "__main__":
    wrapper()