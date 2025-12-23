import pandas as pd
from temporal_causality_engine.utils import make_synthetic_var, make_stationary
from temporal_causality_engine.pcmci_module import run_pcmci


def test_pcmci_runs():
    df = make_synthetic_var(n_series=3, n_samples=300, seed=0)
    df = make_stationary(df)

    pvals, adj = run_pcmci(df, tau_max=3)

    assert isinstance(pvals, pd.DataFrame)
    assert isinstance(adj, pd.DataFrame)
    assert pvals.shape == (3, 3)
    assert adj.shape == (3, 3)
