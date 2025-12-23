import numpy as np
import pandas as pd


def benjamini_hochberg(
    pvals: pd.DataFrame,
    alpha: float = 0.05
) -> pd.DataFrame:
    """
    Apply Benjamini–Hochberg FDR correction.

    Parameters
    ----------
    pvals : pd.DataFrame
        Raw p-values, indexed by cause, columns by effect.
    alpha : float
        Desired false discovery rate.

    Returns
    -------
    pd.DataFrame
        Boolean adjacency matrix after FDR correction.
    """
    pval_array = pvals.values.flatten()
    valid_mask = ~np.isnan(pval_array)

    p = pval_array[valid_mask]
    m = len(p)

    if m == 0:
        return pd.DataFrame(False, index=pvals.index, columns=pvals.columns)

    order = np.argsort(p)
    sorted_p = p[order]

    thresholds = alpha * np.arange(1, m + 1) / m
    passed = sorted_p <= thresholds

    if not passed.any():
        cutoff = 0.0
    else:
        cutoff = sorted_p[passed].max()

    adj = (pvals <= cutoff)
    adj = adj.fillna(False)

    return adj
