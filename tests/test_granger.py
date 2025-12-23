from temporal_causality_engine.utils import make_synthetic_var
from temporal_causality_engine.granger_module import pairwise_granger

def test_granger_runs():
    df = make_synthetic_var(n_series=3, n_samples=300)
    pvals, adj = pairwise_granger(df)
    assert pvals.shape == (3, 3)
    assert adj.shape == (3, 3)
