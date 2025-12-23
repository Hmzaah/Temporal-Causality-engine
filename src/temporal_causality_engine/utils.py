import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss


def make_synthetic_var(
    n_series: int = 3,
    n_samples: int = 500,
    seed: int = 0
) -> pd.DataFrame:
    """
    Create a stable VAR(1) synthetic dataset with known causal structure.
    """
    rng = np.random.RandomState(seed)

    A = np.eye(n_series) * 0.5
    for i in range(n_series - 1):
        A[i + 1, i] = 0.6  # x_i → x_{i+1}

    data = np.zeros((n_samples, n_series))
    noise = rng.normal(scale=1.0, size=(n_samples, n_series))

    for t in range(1, n_samples):
        data[t] = data[t - 1] @ A.T + noise[t]

    return pd.DataFrame(data, columns=[f"x{i}" for i in range(n_series)])


def adf_test(series: pd.Series, alpha: float = 0.05) -> bool:
    """
    Augmented Dickey-Fuller test.
    Returns True if series is stationary.
    """
    series = series.dropna()
    pvalue = adfuller(series, autolag="AIC")[1]
    return pvalue < alpha


def kpss_test(series: pd.Series, alpha: float = 0.05) -> bool:
    """
    KPSS test.
    Returns True if series is stationary.
    """
    series = series.dropna()
    try:
        pvalue = kpss(series, nlags="auto")[1]
        return pvalue > alpha
    except ValueError:
        # Happens for very short or constant series
        return False


def difference(series: pd.Series, order: int = 1) -> pd.Series:
    """
    Apply differencing of given order.
    """
    return series.diff(order)


def make_stationary(
    df: pd.DataFrame,
    max_diff: int = 2,
    strategy: str = "auto"
) -> pd.DataFrame:
    """
    Ensure all columns in df are stationary.

    Parameters
    ----------
    strategy:
        - "adf"   : use ADF only
        - "kpss"  : use KPSS only
        - "auto"  : require BOTH ADF and KPSS to indicate stationarity
    """
    out = df.copy()

    for col in out.columns:
        s = out[col]

        for _ in range(max_diff + 1):
            adf_ok = adf_test(s)
            kpss_ok = kpss_test(s)

            if strategy == "adf" and adf_ok:
                break
            if strategy == "kpss" and kpss_ok:
                break
            if strategy == "auto" and adf_ok and kpss_ok:
                break

            s = difference(s)

        out[col] = s

    return out.dropna()
