import json
from .config import DATA_RAW, DATA_PROCESSED, FIGURES, DASHBOARD, HOUR_COLUMNS
from .io import load_wide
from .validation import validate_inputs
from .features import build_hourly_flow, build_station_metrics
from .statistics import compute_statistics
from .segmentation import segment_stations
from .anomalies import detect_anomalies
from .sql_layer import build_sqlite_database
from .visualize import save_static_figures, build_interactive_dashboard


def run_pipeline() -> dict:
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    entries = load_wide(DATA_RAW / 'hourly_entries.csv'); exits = load_wide(DATA_RAW / 'hourly_exits.csv')
    quality = validate_inputs(entries, exits)
    hourly = build_hourly_flow(entries, exits); metrics = build_station_metrics(entries, exits); stats = compute_statistics(metrics)
    segmented, clustering = segment_stations(metrics, selected_k=3); final = detect_anomalies(segmented)
    hourly.to_csv(DATA_PROCESSED / 'hourly_station_flow.csv', index=False); final.to_csv(DATA_PROCESSED / 'station_metrics.csv', index=False)
    network_summary = {'stations': int(len(entries)), 'hour_periods': int(len(HOUR_COLUMNS)), 'station_hour_rows': int(len(hourly)), 'hourly_entry_exit_measurements': int(len(hourly) * 2), 'network_entries': int(entries[HOUR_COLUMNS].to_numpy().sum()), 'network_exits': int(exits[HOUR_COLUMNS].to_numpy().sum()), 'combined_flow': int(entries[HOUR_COLUMNS].to_numpy().sum() + exits[HOUR_COLUMNS].to_numpy().sum()), 'anomalies_flagged': int(final['is_anomaly'].sum())}
    for name, payload in [('data_quality_report.json', quality), ('statistical_results.json', stats), ('clustering_results.json', clustering), ('network_summary.json', network_summary)]: (DATA_PROCESSED / name).write_text(json.dumps(payload, indent=2), encoding='utf-8')
    build_sqlite_database(hourly, final, DATA_PROCESSED / 'tube_analytics.sqlite'); save_static_figures(hourly, final, FIGURES); build_interactive_dashboard(hourly, final, DASHBOARD / 'interactive_dashboard.html')
    return {'quality': quality, 'statistics': stats, 'clustering': clustering, 'network': network_summary}


if __name__ == '__main__':
    print(json.dumps(run_pipeline(), indent=2))
