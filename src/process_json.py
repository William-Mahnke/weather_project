import json
import pandas as pd
from pathlib import Path
from exceptions import CityMismatchError, DateMissingError, IncompleteSeriesError
from fetch_weather import START_DATE, END_DATE, CITIES
import logging # TODO implement a logger for information

# convert jsons to combined dataframe
def convert_jsons() -> pd.DataFrame:
    frames = []
    for path in Path("data/raw").glob("*.json"):
        data = json.load(open(path))
        # cheap structural guard per file, with the filename for good error messages
        assert "daily" in data and "city_name" in data, f"Bad structure: {path.name}"
        frames.append(pd.DataFrame(data["daily"]).assign(city_name = data["city_name"]))
    return pd.concat(frames, ignore_index = True)

# validate data
def validate_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    # coerce numeric columns to pd numeric type
    numeric_cols = ["temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
            "rain_sum", "snowfall_sum", "wind_speed_10m_max", "daylight_duration"]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors = "coerce")
    
    # dates to pd datetime   
    df["time"] = pd.to_datetime(df["time"], errors = "coerce")

    # check for duplicates
    duplicates = df.duplicated(["city_name", "time"]).sum()
    if duplicates:
        print(f"Dropped {duplicates} duplicate (city_name, date) row(s)")
        df = df.drop_duplicates(subset = ["city_name", "time"])
        
    
    # check all cities are present
    df_cities = set(df["city_name"])
    exp_cities = {city["name"] for city in CITIES}
    if df_cities != exp_cities:
        missing = exp_cities - df_cities
        extra = df_cities - exp_cities
        raise CityMismatchError(f"Cities mismatch - missing: {missing or 'None'}, unexpected: {extra or 'None'}")

    # each city has expected number of days
    expected_days = len(pd.date_range(START_DATE, END_DATE))
    counts = df.groupby("city_name").size()
    bad_counts = counts.loc[counts != expected_days]
    if len(bad_counts):
        raise IncompleteSeriesError(f"Incomplete series (expected {expected_days} rows/city):\n{bad_counts.to_string()}")


    # check full date range for each city
    for city, group in df.groupby("city_name"):
        missing = pd.date_range(START_DATE, END_DATE).difference(group["time"])
        if len(missing): # missing date in range
            raise DateMissingError(f"{city} missing {len(missing)} date(s).")

    # missing values
    na_values = df.isna().sum().to_dict()
    cols_with_na = [col for col, n in na_values.items() if n > 0]
    if cols_with_na:
        print(f"Columns with missing values: {cols_with_na}")
        

    # range checks for numeric values
    # temperature - not impossible temperatures + min <= mean <= max
    temp_cols = ["temperature_2m_min", "temperature_2m_mean", "temperature_2m_max"]
    bad_temps = 0
    for temp_col in temp_cols:
        out_of_range = df[temp_col].notna() & (~df[temp_col].between(-459.67, 134.1))
        bad_temps += out_of_range.sum()
    if bad_temps:
        print(f"WARNING: {bad_temps} temperature value(s) outside [-459.67, 134.1]°F")

    # check min <= mean <= max for everyday
    complete = df[temp_cols].notna().all(axis = 1)
    violates = (~(df["temperature_2m_min"] <= df["temperature_2m_mean"]) |
            ~(df["temperature_2m_mean"] <= df["temperature_2m_max"]))
    improper_temps = (complete & violates).sum()
    if improper_temps:
        offenders = df.loc[complete & violates, ["city_name", "time",
                        "temperature_2m_min", "temperature_2m_mean", "temperature_2m_max"]]
        print(f"WARNING: {improper_temps} row(s) violate min<=mean<=max:\n{offenders.to_string(index=False)}")

    # check rain, snow, wind, daylight duration all non-negative
    cols = ["rain_sum", "snowfall_sum", "wind_speed_10m_max", "daylight_duration"]
    negative_values = (df[cols] < 0).any(axis = 1).sum()
    if negative_values:
        neg_per_col = (df[cols] < 0).sum()
        print(f"WARNING: {negative_values} row(s) with negative values:\n{neg_per_col[neg_per_col > 0].to_string()}")

    # additional check daylight duration less than total seconds in the day 
    improper_duration = (df["daylight_duration"] > 86400).sum()
    if improper_duration:
        print(f"WARNING: {improper_duration} row(s) with daylight > 86400s")

    return df

# process data before saving
def process_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    # with all validation complete, rename columns before saving 
    df = df.rename(columns = {"time": "date", "temperature_2m_mean": "mean_temp_f",
                                "temperature_2m_min": "min_temp_f", "temperature_2m_max": "max_temp_f",
                                "rain_sum": "total_rain_in", "snowfall_sum": "total_snow_in",
                                "wind_speed_10m_max": "max_wind_speed_mph", "daylight_duration": "daylight_duration_s"})

    # map city names to id column
    city_id_map = {city["name"]: city["id"] for city in CITIES}
    df["city_id"] = df["city_name"].map(city_id_map)  # pyright: ignore[reportArgumentType]

    # sort by city then date for organized processed file
    df = df.sort_values(by = ["city_name", "date"], ascending = [True, True]).reset_index(drop = True)
    df = df.drop(columns = "city_name")
    return df

# save city information to separate table
def build_city_df() -> pd.DataFrame:
    city_meta = {c["name"]: c for c in CITIES}
    rows = []
    for path in Path("data/raw").glob("*.json"):
        data = json.load(open(path))
        rows.append({
            "city_id": city_meta[data["city_name"]]["id"],
            "city_name": data["city_name"],
            "state": city_meta[data["city_name"]]["state"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "elevation": data["elevation"],
            "timezone": data["timezone"]
        })
    return pd.DataFrame(rows).sort_values("city_id").reset_index(drop = True)

# save processed data to folder
def save_processed_data(weather_df: pd.DataFrame, cities_df: pd.DataFrame, path: str = "data/processed"):
    Path(path).mkdir(parents = True, exist_ok = True)
    weather_df.to_csv(Path(path) / "weather.csv", index = False)
    print(f"Processed weather statistics saved to {Path(path) / 'weather.csv'}")
    cities_df.to_csv(Path(path) / "cities.csv", index = False)
    print(f"City data saved to {Path(path) / 'cities.csv'}")

# wrapper function
def process_json():
    weather_df = convert_jsons()
    cities_df = build_city_df()
    validated_weather_df = validate_weather_data(weather_df)  # pyright: ignore[reportArgumentType]
    processed_weather_df = process_weather_data(validated_weather_df)
    save_processed_data(processed_weather_df, cities_df)

if __name__ == "__main__":
    process_json()