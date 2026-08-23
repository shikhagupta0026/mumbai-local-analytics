import sqlite3
import pandas as pd
from pathlib import Path

# Create SQLite Database From Cleaned Data

BASE_DIR = Path(__file__).resolve().parent.parent

CSV_FILE = BASE_DIR / "data" / "cleaned" / "timetables_cleaned.csv"
DB_FILE = BASE_DIR / "data" / "mumbai_local.db"

print("=" * 60)
print("CREATING MUMBAI LOCAL TRAIN SQL DATABASE")
print("=" * 60)

# Load cleaned dataset
df = pd.read_csv(CSV_FILE)

print("\nDataset shape:")
print(df.shape)
print("\nColumns:")
print(df.columns.tolist())

# Connect to SQLite and write the table
conn = sqlite3.connect(DB_FILE)
df.to_sql("train_timetable", conn, if_exists="replace", index=False)

# Verify the table was created correctly
result = pd.read_sql_query(
    "SELECT COUNT(*) AS total_records FROM train_timetable;", conn
)
print("\n========== SQL TEST ==========")
print(result)

# Check important columns
columns = pd.read_sql_query("PRAGMA table_info(train_timetable);", conn)
print("\n========== DATABASE COLUMNS ==========")
print(columns[["name", "type"]])

conn.close()

print("\n" + "=" * 60)
print("SQL DATABASE CREATED SUCCESSFULLY")
print("=" * 60)
print("\nDatabase:")
print(DB_FILE)
