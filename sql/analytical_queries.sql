-- Top stations by combined passenger flow
SELECT Station, total_footfall, segment, employment_score FROM mart_station_metrics ORDER BY total_footfall DESC LIMIT 15;

-- Network flow by hour
SELECT hour_code, SUM(entries) AS entries, SUM(exits) AS exits, SUM(total_flow) AS total_flow, SUM(net_arrivals) AS net_arrivals FROM fact_station_hourly_flow GROUP BY hour_code, hour_order ORDER BY hour_order;

-- Segment-level operational profile
SELECT segment, COUNT(*) AS stations, ROUND(AVG(total_footfall),1) AS avg_footfall, ROUND(AVG(employment_score),3) AS avg_employment_score, ROUND(AVG(am_entry_share),3) AS avg_am_entry_share, ROUND(AVG(am_exit_share),3) AS avg_am_exit_share, ROUND(AVG(pm_entry_share),3) AS avg_pm_entry_share, ROUND(AVG(pm_exit_share),3) AS avg_pm_exit_share FROM mart_station_metrics GROUP BY segment ORDER BY avg_employment_score;

-- High-volume anomalous patterns
SELECT Station, total_footfall, segment, employment_score, anomaly_score FROM mart_station_metrics WHERE is_anomaly = 1 ORDER BY total_footfall DESC;

-- Employment-oriented stations
SELECT Station, total_footfall, employment_score, am_entries, am_exits, pm_entries, pm_exits FROM mart_station_metrics WHERE segment = 'Employment-destination' ORDER BY employment_score DESC, total_footfall DESC;
