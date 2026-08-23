import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "data" / "raw" / "Mumbai Local Train Dataset.csv"

df = pd.read_csv(file_path, encoding="cp1252")

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== COLUMNS ==========")
print(df.columns.tolist())

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== DUPLICATES ==========")
print(df.duplicated().sum())

print("\n========== UNIQUE LINES ==========")
print(df["Line"].value_counts())

print("\n========== BASIC STATISTICS ==========")
print(df.describe(include="all"))
