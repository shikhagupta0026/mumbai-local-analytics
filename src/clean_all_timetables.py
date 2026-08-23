import pandas as pd
from pathlib import Path

# Mumbai Local Train - Timetable Cleaning

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "all_timetables.csv"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = CLEANED_DIR / "timetables_cleaned.csv"

df = pd.read_csv(RAW_FILE)

print("=" * 60)
print("MUMBAI LOCAL TRAIN - TIMETABLE CLEANING")
print("=" * 60)
print("\nOriginal shape:")
print(df.shape)

# Clean up column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("\nColumns:")
print(df.columns.tolist())

# Strip whitespace from all text columns
text_columns = df.select_dtypes(include=["object", "str"]).columns
for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Convert numeric columns, coercing anything invalid to NaN
numeric_columns = ["distance_km", "train_no", "cars"]
for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Clean up time columns
df["departure_time"] = df["departure_time"].astype("string").str.strip()
df["arrival_time"] = df["arrival_time"].astype("string").str.strip()

# Split departure time into hour and minute
df["departure_hour"] = pd.to_numeric(
    df["departure_time"].str.split(":").str[0], errors="coerce"
)
df["departure_minute"] = pd.to_numeric(
    df["departure_time"].str.split(":").str[1], errors="coerce"
)

# Convert departure and arrival times to minutes for travel time calc
departure_minutes = df["departure_hour"] * 60 + df["departure_minute"]

arrival_hour = pd.to_numeric(df["arrival_time"].str.split(":").str[0], errors="coerce")
arrival_minute = pd.to_numeric(
    df["arrival_time"].str.split(":").str[1], errors="coerce"
)
arrival_minutes = arrival_hour * 60 + arrival_minute

df["travel_time_minutes"] = arrival_minutes - departure_minutes

# Handle trains that cross midnight (negative travel time)
df.loc[df["travel_time_minutes"] < 0, "travel_time_minutes"] += 1440

# Build route and train ID
df["route"] = df["from_station"] + " -> " + df["to_station"]
df["train_id"] = df["train_no"].astype("Int64").astype("string")

# Standardize train category
df["train_category"] = df["train_type"].str.upper().str.strip()
df["train_category"] = df["train_category"].replace({"LOCAL": "LOCAL", "AC": "AC"})


def get_time_period(hour):
    if pd.isna(hour):
        return "Unknown"
    if 5 <= hour < 9:
        return "Morning Peak"
    elif 9 <= hour < 12:
        return "Late Morning"
    elif 12 <= hour < 16:
        return "Afternoon"
    elif 16 <= hour < 20:
        return "Evening Peak"
    elif 20 <= hour < 24:
        return "Night"
    else:
        return "Late Night"


df["time_period"] = df["departure_hour"].apply(get_time_period)

# Fill missing speed values
df["speed"] = df["speed"].fillna("Unknown")

# Drop exact duplicate rows
before = len(df)
df = df.drop_duplicates()
after = len(df)
print("\nDuplicates removed:")
print(before - after)

print("\n========== TRAVEL TIME ==========")
print(df["travel_time_minutes"].describe())

# Flag suspicious travel times (negative/zero or unusually long)
invalid_travel = df[
    (df["travel_time_minutes"] <= 0) | (df["travel_time_minutes"] > 120)
]
print("\nInvalid travel time records:")
print(len(invalid_travel))

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== RAILWAY LINES ==========")
print(df["line"].value_counts())

print("\n========== TRAIN TYPES ==========")
print(df["train_type"].value_counts())

print("\n========== TIME PERIOD ==========")
print(df["time_period"].value_counts())

print("\n========== TOP ROUTES ==========")
print(df["route"].value_counts().head(20))

print("\n========== TRAIN SUMMARY ==========")
print(df["train_id"].nunique(), "unique trains")

print("\n========== FINAL DATASET ==========")
print("Shape:")
print(df.shape)

# Save the cleaned dataset
df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 60)
print("TIMETABLE CLEANING COMPLETED")
print("=" * 60)
print("\nSaved to:")
print(OUTPUT_FILE)
print("=" * 60)
