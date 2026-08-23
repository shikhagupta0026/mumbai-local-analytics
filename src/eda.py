import pandas as pd
from pathlib import Path

# Mumbai Local Train - Exploratory Data Analysis

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "cleaned" / "timetables_cleaned.csv"

print("=" * 60)
print("MUMBAI LOCAL TRAIN - EDA")
print("=" * 60)

df = pd.read_csv(INPUT_FILE)
print("\nDataset loaded successfully!")
print("Shape:", df.shape)

print("\n========== BASIC INFORMATION ==========")
print("\nRows:", len(df))
print("Columns:", len(df.columns))
print("\nRailway Lines:")
print(df["line"].value_counts())

# Train frequency by line
print("\n========== TRAIN FREQUENCY BY LINE ==========")
line_frequency = df.groupby("line").size().sort_values(ascending=False)
print(line_frequency)

# Train type distribution
print("\n========== TRAIN TYPE DISTRIBUTION ==========")
train_types = df["train_type"].value_counts()
print(train_types)

# Operating days
print("\n========== OPERATING DAYS ==========")
days = df["days_of_week"].value_counts()
print(days)

# Top routes
print("\n========== TOP 20 ROUTES ==========")
top_routes = df["route"].value_counts().head(20)
print(top_routes)

# Average travel time by line
print("\n========== AVERAGE TRAVEL TIME BY LINE ==========")
avg_travel_line = (
    df.groupby("line")["travel_time_minutes"].mean().sort_values(ascending=False)
)
print(avg_travel_line)

# Average travel time by route
print("\n========== AVERAGE TRAVEL TIME BY ROUTE ==========")
avg_travel_route = (
    df.groupby("route")["travel_time_minutes"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
)
print(avg_travel_route)

# Distance vs travel time
print("\n========== DISTANCE VS TRAVEL TIME ==========")
distance_analysis = (
    df.groupby("route")
    .agg(
        distance_km=("distance_km", "mean"),
        travel_time_minutes=("travel_time_minutes", "mean"),
        train_count=("train_id", "count"),
    )
    .sort_values("travel_time_minutes", ascending=False)
)
print(distance_analysis.head(20))

# Busiest from-stations
print("\n========== BUSIEST FROM-STATIONS ==========")
busy_from = df["from_station"].value_counts().head(20)
print(busy_from)

# Busiest to-stations
print("\n========== BUSIEST TO-STATIONS ==========")
busy_to = df["to_station"].value_counts().head(20)
print(busy_to)

# Train frequency by hour
print("\n========== TRAIN FREQUENCY BY HOUR ==========")
hourly_frequency = df["departure_hour"].value_counts().sort_index()
print(hourly_frequency)

# Train frequency by time period
print("\n========== TRAIN FREQUENCY BY TIME PERIOD ==========")
period_frequency = df["time_period"].value_counts()
print(period_frequency)

# AC vs local by line
print("\n========== AC VS LOCAL BY LINE ==========")
line_train_type = pd.crosstab(df["line"], df["train_type"])
print(line_train_type)

# Average distance by line
print("\n========== AVERAGE DISTANCE BY LINE ==========")
avg_distance = df.groupby("line")["distance_km"].mean().sort_values(ascending=False)
print(avg_distance)

# Longest routes
print("\n========== LONGEST ROUTES ==========")
longest_routes = (
    df.groupby("route")["distance_km"].mean().sort_values(ascending=False).head(20)
)
print(longest_routes)

# Fastest routes
print("\n========== FASTEST ROUTES ==========")
fastest_routes = (
    df.groupby("route")["travel_time_minutes"].mean().sort_values().head(20)
)
print(fastest_routes)

# Slowest routes
print("\n========== SLOWEST ROUTES ==========")
slowest_routes = (
    df.groupby("route")["travel_time_minutes"]
    .mean()
    .sort_values(ascending=False)
    .head(20)
)
print(slowest_routes)

# Train count by destination
print("\n========== TOP DESTINATIONS ==========")
destinations = df["destination"].value_counts().head(20)
print(destinations)

# Train count by origin
print("\n========== TOP ORIGINS ==========")
origins = df["origin"].value_counts().head(20)
print(origins)

# Correlation between distance, travel time, and cars
print("\n========== CORRELATION ==========")
correlation = df[["distance_km", "travel_time_minutes", "cars"]].corr()
print(correlation)

# Key project insights
print("\n")
print("=" * 60)
print("KEY PROJECT INSIGHTS")
print("=" * 60)

print("\nMost active railway line:")
print(df["line"].value_counts().idxmax())

print("\nMost common train type:")
print(df["train_type"].value_counts().idxmax())

print("\nMost common route:")
print(df["route"].value_counts().idxmax())

print("\nAverage travel time:")
print(round(df["travel_time_minutes"].mean(), 2), "minutes")

print("\nAverage distance:")
print(round(df["distance_km"].mean(), 2), "km")

print("\nNumber of unique trains:")
print(df["train_id"].nunique())

print("\nNumber of unique routes:")
print(df["route"].nunique())

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)
