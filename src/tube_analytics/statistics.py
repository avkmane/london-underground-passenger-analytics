import pandas as pd
from scipy.stats import pearsonr, spearmanr, ttest_rel, wilcoxon


def compute_statistics(metrics: pd.DataFrame) -> dict:
    am = metrics['am_exit_share']
    pm = metrics['pm_exit_share']
    diff = pm - am
    pearson = pearsonr(am, pm)
    spearman = spearmanr(am, pm)
    paired_t = ttest_rel(am, pm)
    paired_w = wilcoxon(am, pm)
    return {
        'mean_am_exit_share': float(am.mean()),
        'median_am_exit_share': float(am.median()),
        'mean_pm_exit_share': float(pm.mean()),
        'median_pm_exit_share': float(pm.median()),
        'mean_pm_minus_am_percentage_points': float(diff.mean() * 100),
        'pearson_r_am_vs_pm_exit_share': float(pearson.statistic),
        'pearson_p_value': float(pearson.pvalue),
        'spearman_rho_am_vs_pm_exit_share': float(spearman.statistic),
        'spearman_p_value': float(spearman.pvalue),
        'paired_t_statistic': float(paired_t.statistic),
        'paired_t_p_value': float(paired_t.pvalue),
        'wilcoxon_statistic': float(paired_w.statistic),
        'wilcoxon_p_value': float(paired_w.pvalue),
        'cohen_dz_pm_minus_am': float(diff.mean() / diff.std(ddof=1)),
    }
