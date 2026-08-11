import numpy as np
import pandas as pd
from .config import HOUR_COLUMNS, AM_PEAK, PM_PEAK, TIME_BANDS


def build_hourly_flow(entries: pd.DataFrame, exits: pd.DataFrame) -> pd.DataFrame:
    entry_long = entries.melt(id_vars='Station', value_vars=HOUR_COLUMNS,
                               var_name='hour_code', value_name='entries')
    exit_long = exits.melt(id_vars='Station', value_vars=HOUR_COLUMNS,
                           var_name='hour_code', value_name='exits')
    hourly = entry_long.merge(exit_long, on=['Station', 'hour_code'], validate='one_to_one')
    order = {h: i for i, h in enumerate(HOUR_COLUMNS)}
    hourly['hour_order'] = hourly['hour_code'].map(order).astype(int)
    band_lookup = {h: band for band, cols in TIME_BANDS.items() for h in cols}
    hourly['time_band'] = hourly['hour_code'].map(band_lookup)
    hourly['total_flow'] = hourly['entries'] + hourly['exits']
    hourly['net_arrivals'] = hourly['exits'] - hourly['entries']
    return hourly.sort_values(['Station', 'hour_order']).reset_index(drop=True)


def _sum(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    return df[cols].sum(axis=1)


def build_station_metrics(entries: pd.DataFrame, exits: pd.DataFrame) -> pd.DataFrame:
    e = entries.set_index('Station').sort_index()
    x = exits.set_index('Station').sort_index()
    if not e.index.equals(x.index):
        raise ValueError('Entry/exit station order could not be aligned.')

    m = pd.DataFrame(index=e.index)
    m['total_entries'] = _sum(e, HOUR_COLUMNS)
    m['total_exits'] = _sum(x, HOUR_COLUMNS)
    m['total_footfall'] = m['total_entries'] + m['total_exits']
    m['am_entries'] = _sum(e, AM_PEAK)
    m['am_exits'] = _sum(x, AM_PEAK)
    m['pm_entries'] = _sum(e, PM_PEAK)
    m['pm_exits'] = _sum(x, PM_PEAK)
    m['am_entry_share'] = m['am_entries'] / m['total_entries']
    m['am_exit_share'] = m['am_exits'] / m['total_exits']
    m['pm_entry_share'] = m['pm_entries'] / m['total_entries']
    m['pm_exit_share'] = m['pm_exits'] / m['total_exits']
    peak_total = m[['am_entries','am_exits','pm_entries','pm_exits']].sum(axis=1)
    m['employment_score'] = ((m['am_exits'] - m['am_entries']) + (m['pm_entries'] - m['pm_exits'])) / peak_total.replace(0, np.nan)
    m['peak_concentration'] = peak_total / m['total_footfall']
    m['flow_balance'] = (m['total_entries'] - m['total_exits']) / m['total_footfall']
    m['entry_exit_ratio'] = m['total_entries'] / m['total_exits'].replace(0, np.nan)
    m['log_total_footfall'] = np.log1p(m['total_footfall'])
    for band, cols in TIME_BANDS.items():
        m[f'{band}_entries'] = _sum(e, cols)
        m[f'{band}_exits'] = _sum(x, cols)
    return m.reset_index()
