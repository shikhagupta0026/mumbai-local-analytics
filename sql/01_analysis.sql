CREATE DATABASE mumbai_local_analytics;

USE mumbai_local_analytics;
CREATE TABLE train_timetable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    line VARCHAR(10),
    from_station VARCHAR(100),
    to_station VARCHAR(100),
    distance_km DECIMAL(10,2),
    direction VARCHAR(20),
    train_no INT,
    train_code VARCHAR(20),
    cars INT,
    speed VARCHAR(20),
    train_type VARCHAR(20),
    days_of_week VARCHAR(20),
    origin VARCHAR(100),
    destination VARCHAR(100),
    departure_time TIME,
    arrival_time TIME,
    departure_hour INT,
    departure_minute INT,
    travel_time_minutes DECIMAL(10,2),
    route VARCHAR(200),
    train_id VARCHAR(20),
    train_category VARCHAR(20),
    time_period VARCHAR(30)
);