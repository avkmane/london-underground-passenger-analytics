from pathlib import Path
import pytest
from tube_analytics.config import DATA_RAW, HOUR_COLUMNS
from tube_analytics.io import load_wide
from tube_analytics.validation import validate_inputs
from tube_analytics.features import build_hourly_flow, build_station_metrics
from tube_analytics.statistics import compute_statistics
from tube_analytics.segmentation import segment_stations


def _inputs():
    entry_path, exit_path = DATA_RAW / 'hourly_entries.csv', DATA_RAW / 'hourly_exits.csv'
    if not entry_path.exists() or not exit_path.exists():
        pytest.skip('Raw coursework datasets are not redistributed in the public repository.')
    return load_wide(entry_path), load_wide(exit_path)


def test_raw_data_quality():
    entries, exits = _inputs(); report = validate_inputs(entries, exits)
    assert report['passed'] is True and len(entries) == 268 and len(exits) == 268 and len(HOUR_COLUMNS) == 21


def test_hourly_fact_shape_and_non_negative():
    entries, exits = _inputs(); hourly = build_hourly_flow(entries, exits)
    assert len(hourly) == 268 * 21 and (hourly[['entries','exits','total_flow']] >= 0).all().all()


def test_station_metrics_bounds():
    entries, exits = _inputs(); metrics = build_station_metrics(entries, exits)
    for col in ['am_entry_share','am_exit_share','pm_entry_share','pm_exit_share','peak_concentration']: assert metrics[col].between(0,1).all()
    assert metrics['employment_score'].between(-1,1).all()


def test_key_statistical_result_is_reproducible():
    entries, exits = _inputs(); stats = compute_statistics(build_station_metrics(entries, exits))
    assert stats['pearson_r_am_vs_pm_exit_share'] < -0.88 and stats['pearson_p_value'] < 1e-50


def test_three_segment_solution_is_interpretable():
    entries, exits = _inputs(); segmented, summary = segment_stations(build_station_metrics(entries, exits), selected_k=3)
    assert segmented['segment'].nunique() == 3 and summary['selected_silhouette'] > 0.45
