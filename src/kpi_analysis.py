import pandas as pd
from pathlib import Path

# Mumbai Local Train - KPI & Analytics

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "cleaned" / "timetables_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("MUMBAI LOCAL TRAIN - KPI ANALYSIS")
print("=" * 60)
print("\nDataset:", df.shape)

# Basic KPIs
total_records = len(df)
unique_trains = df["train_id"].nunique()
unique_routes = df["route"].nunique()
railway_lines = df["line"].nunique()
avg_travel_time = df["travel_time_minutes"].mean()
avg_distance = df["distance_km"].mean()
total_stations = len(set(df["from_station"].dropna()) | set(df["to_station"].dropna()))

# Busiest route
busiest_route = df["route"].value_counts().idxmax()
busiest_route_count = df["route"].value_counts().max()

# Most active line
most_active_line = df["line"].value_counts().idxmax()
most_active_line_count = df["line"].value_counts().max()

# Most common train type
most_common_train_type = df["train_type"].value_counts().idxmax()

# Longest route
longest_route = df.groupby("route")["distance_km"].mean().idxmax()
longest_route_distance = df.groupby("route")["distance_km"].mean().max()

# Slowest route
slowest_route = df.groupby("route")["travel_time_minutes"].mean().idxmax()
slowest_route_time = df.groupby("route")["travel_time_minutes"].mean().max()

# Fastest route
fastest_route = df.groupby("route")["travel_time_minutes"].mean().idxmin()
fastest_route_time = df.groupby("route")["travel_time_minutes"].mean().min()

# Train type counts
local_trains = df[df["train_type"] == "LOCAL"]["train_id"].nunique()
ac_trains = df[df["train_type"] == "AC"]["train_id"].nunique()

# Line summary
line_summary = (
    df.groupby("line")
    .agg(
        train_records=("train_id", "count"),
        unique_trains=("train_id", "nunique"),
        avg_distance_km=("distance_km", "mean"),
        avg_travel_time=("travel_time_minutes", "mean"),
    )
    .reset_index()
)
line_summary = line_summary.sort_values("train_records", ascending=False)

# Route summary
route_summary = (
    df.groupby("route")
    .agg(
        train_count=("train_id", "count"),
        distance_km=("distance_km", "mean"),
        avg_travel_time=("travel_time_minutes", "mean"),
    )
    .reset_index()
)
route_summary = route_summary.sort_values("train_count", ascending=False)

# Display KPIs
print("\n" + "=" * 60)
print("DASHBOARD KPIs")
print("=" * 60)

print(f"\nTotal Train Records       : {total_records}")
print(f"Unique Trains             : {unique_trains}")
print(f"Unique Routes             : {unique_routes}")
print(f"Railway Lines             : {railway_lines}")
print(f"Stations Covered          : {total_stations}")
print(f"Average Travel Time       : {avg_travel_time:.2f} minutes")
print(f"Average Distance          : {avg_distance:.2f} km")
print(f"Busiest Route             : {busiest_route} ({busiest_route_count} trains)")
print(
    f"Most Active Line          : {most_active_line} ({most_active_line_count} records)"
)
print(f"Most Common Train Type    : {most_common_train_type}")
print(f"Longest Route             : {longest_route} ({longest_route_distance:.2f} km)")
print(f"Slowest Route             : {slowest_route} ({slowest_route_time:.2f} min)")
print(f"Fastest Route             : {fastest_route} ({fastest_route_time:.2f} min)")
print(f"Local Trains              : {local_trains}")
print(f"AC Trains                 : {ac_trains}")

# Save KPI data
kpi_data = pd.DataFrame(
    {
        "metric": [
            "Total Train Records",
            "Unique Trains",
            "Unique Routes",
            "Railway Lines",
            "Stations Covered",
            "Average Travel Time",
            "Average Distance",
            "Busiest Route",
            "Most Active Line",
            "Most Common Train Type",
            "Longest Route",
            "Slowest Route",
            "Fastest Route",
            "Local Trains",
            "AC Trains",
        ],
        "value": [
            total_records,
            unique_trains,
            unique_routes,
            railway_lines,
            total_stations,
            round(avg_travel_time, 2),
            round(avg_distance, 2),
            busiest_route,
            most_active_line,
            most_common_train_type,
            longest_route,
            slowest_route,
            fastest_route,
            local_trains,
            ac_trains,
        ],
    }
)

kpi_file = OUTPUT_DIR / "dashboard_kpis.csv"
kpi_data.to_csv(kpi_file, index=False)

# Save summaries
line_summary.to_csv(OUTPUT_DIR / "line_summary.csv", index=False)
route_summary.to_csv(OUTPUT_DIR / "route_summary.csv", index=False)

print("\n" + "=" * 60)
print("KPI ANALYSIS COMPLETED")
print("=" * 60)

print("\nFiles created:")
print("1.", kpi_file)
print("2.", OUTPUT_DIR / "line_summary.csv")
print("3.", OUTPUT_DIR / "route_summary.csv")
print("\n" + "=" * 60)
