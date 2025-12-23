import numpy as np
import pandas as pd
from temporal_causality_engine.fdr import benjamini_hochberg


def test_bh_fdr_basic():
    pvals = pd.DataFrame(
        [[np.nan, 0.001, 0.2],
         [0.04, np.nan, 0.6],
         [0.02, 0.03, np.nan]],
        columns=["x", "y", "z"],
        index=["x", "y", "z"]
    )

    adj = benjamini_hochberg(pvals, alpha=0.05)

    # Only the smallest p-value survives BH
    assert adj.loc["x", "y"] == True
    assert adj.loc["z", "x"] == False
    assert adj.loc["z", "y"] == False
    assert adj.loc["y", "x"] == False
