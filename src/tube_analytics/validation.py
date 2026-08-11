import pandas as pd
from .config import HOUR_COLUMNS


def validate_inputs(entries: pd.DataFrame, exits: pd.DataFrame) -> dict:
    checks = {
        'entries_rows': int(len(entries)), 'exits_rows': int(len(exits)), 'hour_columns': int(len(HOUR_COLUMNS)),
        'entries_missing_values': int(entries.isna().sum().sum()), 'exits_missing_values': int(exits.isna().sum().sum()),
        'entries_duplicate_stations': int(entries['Station'].duplicated().sum()), 'exits_duplicate_stations': int(exits['Station'].duplicated().sum()),
        'station_sets_match': bool(set(entries['Station']) == set(exits['Station'])),
        'negative_entry_values': int((entries[HOUR_COLUMNS] < 0).sum().sum()), 'negative_exit_values': int((exits[HOUR_COLUMNS] < 0).sum().sum()),
    }
    checks['passed'] = bool(checks['entries_rows'] == checks['exits_rows'] and checks['entries_missing_values'] == 0 and checks['exits_missing_values'] == 0 and checks['entries_duplicate_stations'] == 0 and checks['exits_duplicate_stations'] == 0 and checks['station_sets_match'] and checks['negative_entry_values'] == 0 and checks['negative_exit_values'] == 0)
    if not checks['passed']:
        raise ValueError(f'Data-quality validation failed: {checks}')
    return checks
