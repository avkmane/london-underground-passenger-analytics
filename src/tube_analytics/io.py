from pathlib import Path
import pandas as pd
from .config import HOUR_COLUMNS


def load_wide(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = ['Station', *HOUR_COLUMNS]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns in {path.name}: {missing}')
    return df[required].copy()
