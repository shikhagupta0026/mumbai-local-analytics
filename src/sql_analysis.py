import sqlite3
from pathlib import Path
import pandas as pd

# Mumbai Local Train - SQL Analysis

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "mumbai_local.db"

conn = sqlite3.connect(DB_FILE)

print("=" * 60)
print("MUMBAI LOCAL TRAIN - SQL ANALYSIS")
print("=" * 60)

# Total train records
print("\n========== TOTAL TRAIN RECORDS ==========")
query = """
SELECT COUNT(*) AS total_records
FROM train_timetable;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Train count by railway line
print("\n========== TRAIN COUNT BY LINE ==========")
query = """
SELECT
    line,
    COUNT(*) AS train_records
FROM train_timetable
GROUP BY line
ORDER BY train_records DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Local vs AC
print("\n========== TRAIN TYPE ==========")
query = """
SELECT
    train_type,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY train_type
ORDER BY train_count DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Top destinations
print("\n========== TOP DESTINATIONS ==========")
query = """
SELECT
    destination,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY destination
ORDER BY train_count DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Busiest routes
print("\n========== BUSIEST ROUTES ==========")
query = """
SELECT
    from_station || ' -> ' || to_station AS route,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY from_station, to_station
ORDER BY train_count DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Average travel time by line
print("\n========== AVERAGE TRAVEL TIME BY LINE ==========")
query = """
SELECT
    line,
    ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time
FROM train_timetable
GROUP BY line
ORDER BY avg_travel_time DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Average distance by line
print("\n========== AVERAGE DISTANCE BY LINE ==========")
query = """
SELECT
    line,
    ROUND(AVG(distance_km), 2) AS avg_distance
FROM train_timetable
GROUP BY line
ORDER BY avg_distance DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Train frequency by time period
print("\n========== TRAIN FREQUENCY BY TIME PERIOD ==========")
query = """
SELECT
    time_period,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY time_period
ORDER BY train_count DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Slowest routes
print("\n========== SLOWEST ROUTES ==========")
query = """
SELECT
    from_station || ' -> ' || to_station AS route,
    ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time
FROM train_timetable
GROUP BY from_station, to_station
HAVING COUNT(*) >= 2
ORDER BY avg_travel_time DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Fastest routes
print("\n========== FASTEST ROUTES ==========")
query = """
SELECT
    from_station || ' -> ' || to_station AS route,
    ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time
FROM train_timetable
GROUP BY from_station, to_station
HAVING COUNT(*) >= 2
ORDER BY avg_travel_time ASC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Most frequent trains
print("\n========== MOST FREQUENT TRAINS ==========")
query = """
SELECT
    train_no,
    train_type,
    origin,
    destination,
    COUNT(*) AS route_records
FROM train_timetable
GROUP BY train_no, train_type, origin, destination
ORDER BY route_records DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Railway line vs train type
print("\n========== LINE VS TRAIN TYPE ==========")
query = """
SELECT
    line,
    train_type,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY line, train_type
ORDER BY line, train_count DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Top origins
print("\n========== TOP ORIGINS ==========")
query = """
SELECT
    origin,
    COUNT(*) AS train_count
FROM train_timetable
GROUP BY origin
ORDER BY train_count DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Average travel time by train type
print("\n========== TRAVEL TIME BY TRAIN TYPE ==========")
query = """
SELECT
    train_type,
    ROUND(AVG(travel_time_minutes), 2) AS avg_travel_time
FROM train_timetable
GROUP BY train_type
ORDER BY avg_travel_time DESC;
"""
result = pd.read_sql_query(query, conn)
print(result)

# Longest routes by distance
print("\n========== LONGEST ROUTES ==========")
query = """
SELECT
    from_station || ' -> ' || to_station AS route,
    ROUND(AVG(distance_km), 2) AS avg_distance
FROM train_timetable
GROUP BY from_station, to_station
ORDER BY avg_distance DESC
LIMIT 10;
"""
result = pd.read_sql_query(query, conn)
print(result)

conn.close()

print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)
