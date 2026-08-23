import pandas as pd
from pathlib import Path

# Mumbai Local Train - Timetable Data Cleaning

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "central_vih_kjm_timetable.csv"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_FILE)
print("Original shape:", df.shape)

# Clean up column names
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(".", "_", regex=False)
    .str.replace(" ", "_")
)
print("\n========== COLUMNS ==========")
print(df.columns.tolist())

# Strip whitespace from all text columns
text_columns = df.select_dtypes(include="object").columns
for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Clean numeric columns
df["cars"] = pd.to_numeric(df["cars"], errors="coerce")
df["train_no"] = df["train_no"].astype("string")

# Build departure/arrival time columns from the station stop times
df["departure_time"] = pd.to_datetime(
    df["stops_vidyavihar"], format="%H:%M", errors="coerce"
).dt.time

df["arrival_time"] = pd.to_datetime(
    df["stops_kanjur_marg"], format="%H:%M", errors="coerce"
).dt.time

# Calculate travel time between the two stops
departure = pd.to_datetime(df["stops_vidyavihar"], format="%H:%M", errors="coerce")
arrival = pd.to_datetime(df["stops_kanjur_marg"], format="%H:%M", errors="coerce")
df["travel_time_minutes"] = (arrival - departure).dt.total_seconds() / 60

# Build route
df["route"] = df["origin"] + " → " + df["destination"]

print("\n========== TRAIN TYPES ==========")
print(df["train_type"].value_counts())

print("\n========== OPERATING DAYS ==========")
print(df["days_of_week"].value_counts())

print("\n========== TRAVEL TIME ==========")
print(df["travel_time_minutes"].describe())

print("\n========== DUPLICATES ==========")
print("Duplicates:", df.duplicated().sum())

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== FIRST 10 TRAINS ==========")
print(
    df[
        [
            "train_no",
            "train_type",
            "origin",
            "destination",
            "stops_vidyavihar",
            "stops_kanjur_marg",
            "travel_time_minutes",
        ]
    ].head(10)
)

# Save the cleaned dataset
output_file = CLEANED_DIR / "timetable_cleaned.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\n==============================================")
print("TIMETABLE CLEANING COMPLETED")
print("==============================================")
print("Final shape:", df.shape)
print("Saved to:")
print(output_file)
print("==============================================")
