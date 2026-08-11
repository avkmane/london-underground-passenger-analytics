CREATE TABLE IF NOT EXISTS dim_station (station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS dim_time (hour_order INTEGER PRIMARY KEY, hour_code TEXT UNIQUE NOT NULL, time_band TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS fact_station_hourly_flow (station_name TEXT NOT NULL, hour_code TEXT NOT NULL, hour_order INTEGER NOT NULL, time_band TEXT NOT NULL, entries INTEGER NOT NULL, exits INTEGER NOT NULL, total_flow INTEGER NOT NULL, net_arrivals INTEGER NOT NULL);
