import pandas as pd
from pathlib import Path

# Mumbai Local Train - Station Data Cleaning

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "Mumbai Local Train Dataset.csv"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW_FILE, encoding="cp1252")
print("Original shape:", df.shape)

# Clean up column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("\n========== COLUMNS ==========")
print(df.columns.tolist())

# Strip whitespace from all text columns
text_columns = df.select_dtypes(include="object").columns
for column in text_columns:
    df[column] = df[column].astype("string").str.strip()

# Clean distance column - pull out the numeric part and convert
df["distance_from_previous_of_the_line"] = (
    df["distance_from_previous_of_the_line"]
    .astype("string")
    .str.extract(r"([\d.]+)", expand=False)
)
df["distance_from_previous_of_the_line"] = pd.to_numeric(
    df["distance_from_previous_of_the_line"], errors="coerce"
)

# Clean travel time column the same way
df["time_taken_from_previous_of_the_line"] = (
    df["time_taken_from_previous_of_the_line"]
    .astype("string")
    .str.extract(r"([\d.]+)", expand=False)
)
df["time_taken_from_previous_of_the_line"] = pd.to_numeric(
    df["time_taken_from_previous_of_the_line"], errors="coerce"
)

# Clean remaining numeric columns
numeric_columns = ["platforms", "tracks", "year_of_opening"]
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Clean passenger data - this column has mixed formats (annual/daily/million etc.)
print("\n========== ORIGINAL PASSENGER VALUES ==========")
print(df["number_of_passengers"].dropna().unique())

passenger_text = df["number_of_passengers"].astype("string").str.lower().str.strip()

is_annual = passenger_text.str.contains("annual", na=False)
is_daily = passenger_text.str.contains(r"daily|/day", regex=True, na=False)

# Pull out the numeric value from the text
number = passenger_text.str.replace(",", "", regex=False).str.extract(
    r"([\d.]+)", expand=False
)
number = pd.to_numeric(number, errors="coerce")

# Convert "million" values to their actual number
is_million = passenger_text.str.contains("million", na=False)
number.loc[is_million] = number.loc[is_million] * 1_000_000

# Build a standardized daily passenger estimate
df["passenger_daily_estimate"] = pd.NA
df.loc[is_daily, "passenger_daily_estimate"] = number.loc[is_daily]
df.loc[is_annual, "passenger_daily_estimate"] = number.loc[is_annual] / 365
df["passenger_daily_estimate"] = pd.to_numeric(
    df["passenger_daily_estimate"], errors="coerce"
)

# Some source values are unclear (e.g. "69 eut") - keep the original but flag for review
df["passenger_data_quality"] = "Valid"
df.loc[passenger_text.str.contains("eut", na=False), "passenger_data_quality"] = (
    "Review"
)

# Clean up empty-looking values
df["number_of_passengers"] = df["number_of_passengers"].replace(
    ["nan", "NaN", ""], pd.NA
)
df["previous_names"] = df["previous_names"].replace(["nan", "NaN", ""], pd.NA)

# Build station ID
df["station_id"] = df["station_code"].astype("string").str.upper().str.strip()

# Remove exact duplicates
duplicates_before = df.duplicated().sum()
df = df.drop_duplicates().reset_index(drop=True)
duplicates_after = df.duplicated().sum()

print("\n========== DUPLICATES ==========")
print("Duplicates found:", duplicates_before)
print("Duplicates remaining:", duplicates_after)

print("\n========== CLEANED DATA ==========")
print("\nShape:")
print(df.shape)
print("\nMissing values:")
print(df.isnull().sum())
print("\nData types:")
print(df.dtypes)

print("\n========== RAILWAY LINES ==========")
print(df["line"].value_counts())

print("\n========== PASSENGER DATA ==========")
print(
    df[
        [
            "station",
            "number_of_passengers",
            "passenger_daily_estimate",
            "passenger_data_quality",
        ]
    ]
    .dropna(subset=["number_of_passengers"])
    .to_string(index=False)
)

print("\n========== DAILY PASSENGER STATISTICS ==========")
print(df["passenger_daily_estimate"].describe())

print("\n========== VALUES REQUIRING REVIEW ==========")
review_data = df[df["passenger_data_quality"] == "Review"]
if len(review_data) > 0:
    print(
        review_data[["station", "station_code", "number_of_passengers"]].to_string(
            index=False
        )
    )
else:
    print("No questionable passenger values found.")

print("\n========== DISTANCE CHECK ==========")
print(df["distance_from_previous_of_the_line"].describe())

print("\n========== TRAVEL TIME CHECK ==========")
print(df["time_taken_from_previous_of_the_line"].describe())

# Save the cleaned dataset
output_file = CLEANED_DIR / "stations_cleaned.csv"
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("\n==============================================")
print("STATION DATA CLEANING COMPLETED SUCCESSFULLY")
print("==============================================")
print("\nOriginal rows:", 202)
print("Final rows:", len(df))
print("\nSaved file:")
print(output_file)
print("\n==============================================")
