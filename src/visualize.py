import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Mumbai Local Train - Visualization

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "timetables_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("MUMBAI LOCAL TRAIN - VISUALIZATION")
print("=" * 60)
print("\nDataset shape:", df.shape)

# Train count by railway line
line_count = df["line"].value_counts()

plt.figure(figsize=(8, 5))
line_count.plot(kind="bar")
plt.title("Train Records by Railway Line")
plt.xlabel("Railway Line")
plt.ylabel("Number of Train Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "train_count_by_line.png", dpi=150)
plt.close()

# Train type distribution
train_type = df["train_type"].value_counts()

plt.figure(figsize=(7, 5))
train_type.plot(kind="bar")
plt.title("Local vs AC Trains")
plt.xlabel("Train Type")
plt.ylabel("Number of Train Records")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "train_type_distribution.png", dpi=150)
plt.close()

# Top 10 routes
top_routes = df["route"].value_counts().head(10).sort_values()

plt.figure(figsize=(10, 6))
top_routes.plot(kind="barh")
plt.title("Top 10 Most Frequent Routes")
plt.xlabel("Number of Train Records")
plt.ylabel("Route")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_10_routes.png", dpi=150)
plt.close()

# Average travel time by line
avg_time_line = df.groupby("line")["travel_time_minutes"].mean().sort_values()

plt.figure(figsize=(8, 5))
avg_time_line.plot(kind="bar")
plt.title("Average Travel Time by Railway Line")
plt.xlabel("Railway Line")
plt.ylabel("Average Travel Time (minutes)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_travel_time_by_line.png", dpi=150)
plt.close()

# Distance vs travel time
plt.figure(figsize=(8, 6))
plt.scatter(df["distance_km"], df["travel_time_minutes"], alpha=0.6)
plt.title("Distance vs Travel Time")
plt.xlabel("Distance (km)")
plt.ylabel("Travel Time (minutes)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "distance_vs_travel_time.png", dpi=150)
plt.close()

# Train frequency by hour
hourly = df["departure_hour"].value_counts().sort_index()

plt.figure(figsize=(10, 5))
hourly.plot(kind="line", marker="o")
plt.title("Train Frequency by Departure Hour")
plt.xlabel("Departure Hour")
plt.ylabel("Number of Train Records")
plt.xticks(range(0, 24))
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "train_frequency_by_hour.png", dpi=150)
plt.close()

# Top destinations
destinations = df["destination"].value_counts().head(10).sort_values()

plt.figure(figsize=(9, 6))
destinations.plot(kind="barh")
plt.title("Top 10 Train Destinations")
plt.xlabel("Number of Train Records")
plt.ylabel("Destination")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "top_destinations.png", dpi=150)
plt.close()

# Average distance by line
avg_distance = df.groupby("line")["distance_km"].mean().sort_values()

plt.figure(figsize=(8, 5))
avg_distance.plot(kind="bar")
plt.title("Average Distance Between Stations by Line")
plt.xlabel("Railway Line")
plt.ylabel("Average Distance (km)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "average_distance_by_line.png", dpi=150)
plt.close()

# Top 10 slowest routes
slow_routes = (
    df.groupby("route")["travel_time_minutes"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
slow_routes.plot(kind="barh")
plt.title("Top 10 Slowest Routes")
plt.xlabel("Average Travel Time (minutes)")
plt.ylabel("Route")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "slowest_routes.png", dpi=150)
plt.close()

# Top 10 longest routes
long_routes = (
    df.groupby("route")["distance_km"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
long_routes.plot(kind="barh")
plt.title("Top 10 Longest Routes")
plt.xlabel("Distance (km)")
plt.ylabel("Route")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "longest_routes.png", dpi=150)
plt.close()

print("\n" + "=" * 60)
print("VISUALIZATION COMPLETED")
print("=" * 60)
print("\nCharts saved to:")
print(OUTPUT_DIR)
print("\nGenerated charts:")

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print("-", file.name)

print("\n" + "=" * 60)
