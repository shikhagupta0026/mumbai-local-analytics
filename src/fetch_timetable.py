import requests
import pandas as pd
from pathlib import Path

# Mumbai Local Train - Real Timetable Data

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# API configuration
url = "https://www.mumbailifeline.com/api/timetable"
params = {"line": "CR", "from": "vidyavihar", "to": "kanjur_marg", "after": "15:00"}

print("Fetching real timetable data...")

response = requests.get(url, params=params, timeout=30)
print("Status:", response.status_code)

response.raise_for_status()
data = response.json()

print("\nLine:", data.get("line"))
print("From:", data.get("from"))
print("To:", data.get("to"))
print("Direction:", data.get("direction"))
print("Distance:", data.get("distance_km"), "km")

trains = data.get("trains", [])
print("\nNumber of trains:", len(trains))
print("\nFirst train:")
print(trains[0] if trains else "No train data found")

if trains:
    trains_df = pd.json_normalize(trains)

    print("\nColumns:")
    print(trains_df.columns.tolist())

    print("\nFirst 5 records:")
    print(trains_df.head())

    output_file = RAW_DIR / "central_vih_kjm_timetable.csv"
    trains_df.to_csv(output_file, index=False)

    print("\nSaved to:")
    print(output_file)
else:
    print("No timetable records returned.")
