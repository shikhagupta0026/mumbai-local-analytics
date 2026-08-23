import requests
import pandas as pd
import json
import time
from pathlib import Path

# Mumbai Local Train - Full Timetable Collector

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = RAW_DIR / "all_timetables.csv"
STATION_FILE = RAW_DIR / "all_line_stations.json"

BASE_URL = "https://www.mumbailifeline.com/api"

session = requests.Session()

DELAY = 3
MAX_RETRIES = 5

# Fetch different time periods
TIME_WINDOWS = [
    "00:00",
    "04:00",
    "08:00",
    "12:00",
    "16:00",
    "20:00",
]


def get_data(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(url, params=params, timeout=30)
            print("Status:", response.status_code)

            if response.status_code == 429:
                wait_time = 15 * (attempt + 1)
                print(f"429 RATE LIMIT - waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            if response.status_code == 400:
                print("No direct trains for this route.")
                return None

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print("Request error:", e)
            wait_time = 10 * (attempt + 1)
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)

    print("Failed after maximum retries.")
    return None


# Load any existing timetable data so we can resume instead of starting over
existing_records = []

if OUTPUT_FILE.exists():
    print("\nExisting timetable file found.")
    try:
        existing_df = pd.read_csv(OUTPUT_FILE)
        existing_records = existing_df.to_dict(orient="records")
        print("Existing records:", len(existing_df))
    except Exception as e:
        print("Could not read existing file:", e)
else:
    print("\nNo existing timetable file found.")

# Build a set of routes we've already collected, so we can skip them
completed_routes = set()

for record in existing_records:
    route_key = (
        record.get("line"),
        record.get("from_station"),
        record.get("to_station"),
    )
    completed_routes.add(route_key)

print("Existing routes:", len(completed_routes))

# Step 1 - get railway lines
print("\n" + "=" * 60)
print("FETCHING MUMBAI LOCAL TRAIN DATA")
print("=" * 60)

lines_data = get_data("lines")

if not lines_data:
    print("Could not fetch railway lines.")
    raise SystemExit

print("\nDetected lines:")
for line in lines_data:
    print(line.get("code"), "-", line.get("name"))

# Step 2 - get stations for each line
all_stations = {}

print("\n" + "=" * 60)
print("FETCHING STATIONS")
print("=" * 60)

for line in lines_data:
    line_code = line["code"]
    print(f"\nFetching stations for {line_code}...")

    data = get_data(f"lines/{line_code}/stations")

    if not data:
        print("No station data.")
        continue

    all_stations[line_code] = data
    print("Stations received:", len(data))
    time.sleep(DELAY)

# Save station data
with open(STATION_FILE, "w", encoding="utf-8") as f:
    json.dump(all_stations, f, indent=4, ensure_ascii=False)

print("\nStation data saved:")
print(STATION_FILE)

# Step 3 - timetable collection
print("\n" + "=" * 60)
print("FETCHING TIMETABLE DATA")
print("=" * 60)

all_records = existing_records.copy()

# Process each line
for line_code, stations in all_stations.items():
    print("\n")
    print("-" * 60)
    print(f"PROCESSING LINE: {line_code}")
    print("-" * 60)

    # Extract station names, handling both dict and plain string formats
    station_names = []

    for station in stations:
        if isinstance(station, dict):
            name = station.get("name")
            if name:
                station_names.append(name)
        elif isinstance(station, str):
            station_names.append(station)

    print(f"{line_code}: {len(station_names)} stations found")
    print("First stations:", station_names[:10])

    # Go through each consecutive station pair
    for i in range(len(station_names) - 1):
        from_station = station_names[i]
        to_station = station_names[i + 1]
        route_key = (line_code, from_station, to_station)

        # Skip routes we've already collected
        if route_key in completed_routes:
            print(f"SKIPPING: {from_station} -> {to_station}")
            continue

        print("\n" + "-" * 50)
        print(f"ROUTE: {line_code} | {from_station} -> {to_station}")

        route_records = []

        # Fetch trains across the different time windows
        for time_window in TIME_WINDOWS:
            print(f"\nFetching after {time_window}")

            params = {
                "line": line_code,
                "from": from_station,
                "to": to_station,
                "after": time_window,
            }

            data = get_data("timetable", params=params)

            if not data:
                time.sleep(DELAY)
                continue

            trains = data.get("trains", [])
            print("Trains:", len(trains))

            # Store each train record
            for train in trains:
                stops = train.get("stops", {})
                departure_time = stops.get(from_station)
                arrival_time = stops.get(to_station)

                record = {
                    "line": line_code,
                    "from_station": from_station,
                    "to_station": to_station,
                    "distance_km": data.get("distance_km"),
                    "direction": data.get("direction"),
                    "train_no": train.get("train_no"),
                    "train_code": train.get("train_code"),
                    "cars": train.get("cars"),
                    "speed": train.get("speed"),
                    "train_type": train.get("train_type"),
                    "days_of_week": train.get("days_of_week"),
                    "origin": train.get("origin"),
                    "destination": train.get("destination"),
                    "departure_time": departure_time,
                    "arrival_time": arrival_time,
                }

                route_records.append(record)

            time.sleep(DELAY)

        # Save progress after each route
        if route_records:
            all_records.extend(route_records)

            temp_df = pd.DataFrame(all_records)
            temp_df = temp_df.drop_duplicates()
            temp_df.to_csv(OUTPUT_FILE, index=False)

            print("\nProgress saved:", len(temp_df), "records")

            completed_routes.add(route_key)
        else:
            print("No timetable records found for this route.")

        # Wait before next route
        time.sleep(DELAY)

# Final dataset
print("\n")
print("=" * 60)
print("DATA COLLECTION COMPLETED")
print("=" * 60)

if all_records:
    df = pd.DataFrame(all_records)
    df = df.drop_duplicates()
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTOTAL RECORDS:", len(df))
    print(
        "\nTOTAL ROUTES:",
        df[["line", "from_station", "to_station"]].drop_duplicates().shape[0],
    )
    print("\nLINES:")
    print(df["line"].value_counts())
    print("\nTRAIN TYPES:")
    print(df["train_type"].value_counts())
    print("\nUNIQUE TRAINS:")
    print(df["train_no"].nunique())
    print("\nSAVED TO:")
    print(OUTPUT_FILE)
else:
    print("\nNo timetable data collected.")

print("\n" + "=" * 60)
