import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from .config import RANDOM_STATE

FEATURES = ['am_entry_share', 'am_exit_share', 'pm_entry_share', 'pm_exit_share', 'employment_score']


def segment_stations(metrics: pd.DataFrame, selected_k: int = 3) -> tuple[pd.DataFrame, dict]:
    X = StandardScaler().fit_transform(metrics[FEATURES])
    silhouette_by_k, labels_by_k = {}, {}
    for k in range(2, 7):
        model = KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=50)
        labels = model.fit_predict(X)
        silhouette_by_k[k] = float(silhouette_score(X, labels))
        labels_by_k[k] = labels
    if selected_k not in labels_by_k:
        raise ValueError('selected_k must be between 2 and 6.')
    out = metrics.copy()
    out['cluster_id'] = labels_by_k[selected_k]
    cluster_order = out.groupby('cluster_id')['employment_score'].mean().sort_values().index.tolist()
    if selected_k == 3:
        label_map = {cluster_order[0]: 'Residential-origin', cluster_order[1]: 'Mixed-use/interchange', cluster_order[2]: 'Employment-destination'}
    else:
        label_map = {cluster: f'Segment-{i+1}' for i, cluster in enumerate(cluster_order)}
    out['segment'] = out['cluster_id'].map(label_map)
    summary = {
        'selected_k': selected_k,
        'selected_silhouette': silhouette_by_k[selected_k],
        'best_k_by_silhouette': max(silhouette_by_k, key=silhouette_by_k.get),
        'best_silhouette': max(silhouette_by_k.values()),
        'silhouette_by_k': {str(k): v for k, v in silhouette_by_k.items()},
        'segment_counts': {k: int(v) for k, v in out['segment'].value_counts().to_dict().items()},
    }
    return out, summary
