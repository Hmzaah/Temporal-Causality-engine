import numpy as np
import pandas as pd
from temporal_causality_engine.utils import make_stationary

def test_make_stationary_runs():
    rng = np.random.RandomState(0)
    non_stationary = pd.DataFrame({
        "x": np.cumsum(rng.normal(size=500)),
        "y": rng.normal(size=500)
    })
    out = make_stationary(non_stationary)
    assert not out.isnull().values.any()
    assert out.shape[0] < non_stationary.shape[0]
