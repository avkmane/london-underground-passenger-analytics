import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from .config import RANDOM_STATE

ANOMALY_FEATURES = [
    'log_total_footfall', 'am_entry_share', 'am_exit_share',
    'pm_entry_share', 'pm_exit_share', 'employment_score',
    'peak_concentration', 'flow_balance'
]


def detect_anomalies(metrics: pd.DataFrame, contamination: float = 0.05) -> pd.DataFrame:
    out = metrics.copy()
    X = StandardScaler().fit_transform(out[ANOMALY_FEATURES])
    model = IsolationForest(n_estimators=500, contamination=contamination, random_state=RANDOM_STATE)
    pred = model.fit_predict(X)
    out['anomaly_score'] = model.decision_function(X)
    out['is_anomaly'] = pred == -1
    return out
