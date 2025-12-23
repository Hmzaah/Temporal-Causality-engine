from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import warnings
from statsmodels.tsa.stattools import grangercausalitytests

def _safe_granger_test(x: pd.Series, y: pd.Series, maxlag: int) -> Dict[int, Dict[str, Any]]:
    arr = pd.concat([y, x], axis=1).dropna().values
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        return grangercausalitytests(arr, maxlag=maxlag, verbose=False)

def select_best_lag(results: Dict[int, Dict[str, Any]], test: str) -> Tuple[int, float]:
    best_lag, best_p = 0, 1.0
    for lag, res in results.items():
        if test in res:
            p = res[test][1]
            if p < best_p:
                best_p, best_lag = p, lag
    return best_lag, best_p

def pairwise_granger(
    df: pd.DataFrame,
    maxlag: int = 5,
    alpha: float = 0.05,
    test: str = "ssr_chi2test"
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    vars_ = df.columns
    pvals = pd.DataFrame(1.0, index=vars_, columns=vars_)
    adj = pd.DataFrame(False, index=vars_, columns=vars_)

    for cause in vars_:
        for effect in vars_:
            if cause == effect:
                pvals.loc[cause, effect] = np.nan
                continue
            try:
                res = _safe_granger_test(df[cause], df[effect], maxlag)
                _, p = select_best_lag(res, test)
                pvals.loc[cause, effect] = p
                adj.loc[cause, effect] = p < alpha
            except Exception:
                pvals.loc[cause, effect] = np.nan

    return pvals, adj
