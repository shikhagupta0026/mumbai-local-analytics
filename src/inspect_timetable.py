import pandas as pd
from pathlib import Path

# Inspect Mumbai Local Timetable Data

BASE_DIR = Path(__file__).resolve().parent.parent
FILE = BASE_DIR / "data" / "raw" / "all_timetables.csv"

print("=" * 60)
print("MUMBAI LOCAL TRAIN - TIMETABLE INSPECTION")
print("=" * 60)

df = pd.read_csv(FILE)

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== FIRST 10 RECORDS ==========")
print(df.head(10).to_string())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())

print("\n========== RAILWAY LINES ==========")
print(df["line"].value_counts())

print("\n========== TRAIN TYPES ==========")
print(df["train_type"].value_counts())

print("\n========== OPERATING DAYS ==========")
print(df["days_of_week"].value_counts())

print("\n========== ROUTE COUNT ==========")
df["route"] = df["from_station"] + " -> " + df["to_station"]
print("Unique routes:", df["route"].nunique())
print("\nTop routes:")
print(df["route"].value_counts().head(20))

print("\n========== TRAIN COUNT ==========")
print("Unique trains:", df["train_no"].nunique())

print("\n========== TRAIN TYPE SUMMARY ==========")
print(df.groupby("train_type")["train_no"].nunique())

print("\n" + "=" * 60)
print("INSPECTION COMPLETED")
print("=" * 60)
