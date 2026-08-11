import sqlite3
from pathlib import Path
import pandas as pd


def build_sqlite_database(hourly: pd.DataFrame, stations: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    with sqlite3.connect(path) as conn:
        hourly.to_sql('fact_station_hourly_flow', conn, index=False, if_exists='replace')
        stations.to_sql('mart_station_metrics', conn, index=False, if_exists='replace')
        conn.execute('CREATE INDEX idx_hourly_station ON fact_station_hourly_flow(Station)')
        conn.execute('CREATE INDEX idx_hourly_hour ON fact_station_hourly_flow(hour_code)')
        conn.execute('CREATE INDEX idx_metrics_segment ON mart_station_metrics(segment)')
        conn.execute('''CREATE VIEW vw_network_hourly AS SELECT hour_code, hour_order, SUM(entries) AS entries, SUM(exits) AS exits, SUM(total_flow) AS total_flow, SUM(net_arrivals) AS net_arrivals FROM fact_station_hourly_flow GROUP BY hour_code, hour_order ORDER BY hour_order''')
        conn.execute('''CREATE VIEW vw_top_stations AS SELECT Station, total_footfall, segment, employment_score FROM mart_station_metrics ORDER BY total_footfall DESC''')
