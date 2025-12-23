import numpy as np
import pandas as pd
from typing import Tuple

from tigramite.data_processing import DataFrame as TigramiteDataFrame
from tigramite.pcmci import PCMCI

# Robust import across tigramite versions
try:
    from tigramite.independence_tests.parcorr import ParCorr
except ImportError:
    from tigramite.independence_tests import ParCorr


def run_pcmci(
    df: pd.DataFrame,
    tau_max: int = 5,
    alpha: float = 0.05,
    verbosity: int = 0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Run PCMCI causal discovery on multivariate time series.

    Parameters
    ----------
    df : pd.DataFrame
        Stationary time series (T x N).
    tau_max : int
        Maximum time lag.
    alpha : float
        Significance level.
    verbosity : int
        Tigramite verbosity.

    Returns
    -------
    pvals_df : pd.DataFrame
        Minimum p-values over lags for each (cause, effect).
    adj_df : pd.DataFrame
        Boolean adjacency matrix.
    """
    data = TigramiteDataFrame(
        df.values,
        var_names=list(df.columns)
    )

    ci_test = ParCorr()

    pcmci = PCMCI(
        dataframe=data,
        cond_ind_test=ci_test,
        verbosity=verbosity
    )

    results = pcmci.run_pcmci(
        tau_max=tau_max,
        pc_alpha=alpha
    )

    p_matrix = results["p_matrix"]  # shape: [N, N, tau_max+1]
    n_vars = p_matrix.shape[0]
    var_names = df.columns

    pvals = np.full((n_vars, n_vars), np.nan)

    for i in range(n_vars):       # cause
        for j in range(n_vars):   # effect
            if i == j:
                continue
            lag_pvals = p_matrix[i, j, 1:]  # exclude tau=0
            pvals[i, j] = np.nanmin(lag_pvals)

    pvals_df = pd.DataFrame(pvals, index=var_names, columns=var_names)
    adj_df = pvals_df < alpha

    return pvals_df, adj_df