from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = PROJECT_ROOT / 'data' / 'raw'
DATA_PROCESSED = PROJECT_ROOT / 'data' / 'processed'
REPORTS = PROJECT_ROOT / 'reports'
FIGURES = REPORTS / 'figures'
DASHBOARD = PROJECT_ROOT / 'dashboard'

HOUR_COLUMNS = [
    'H05','H06','H07','H08','H09','H10','H11','H12','H13','H14','H15',
    'H16','H17','H18','H19','H20','H21','H22','H23','H00','H01'
]
TIME_BANDS = {
    'early': ['H05','H06'],
    'am_peak': ['H07','H08','H09'],
    'interpeak': ['H10','H11','H12','H13','H14','H15'],
    'pm_peak': ['H16','H17','H18'],
    'evening': ['H19','H20','H21'],
    'late': ['H22','H23','H00','H01'],
}
AM_PEAK = TIME_BANDS['am_peak']
PM_PEAK = TIME_BANDS['pm_peak']
RANDOM_STATE = 42
