import pandas as pd
from temporal_causality_engine.utils import make_synthetic_var, make_stationary
from temporal_causality_engine.granger_module import pairwise_granger_fdr
from temporal_causality_engine.pcmci_module import run_pcmci
from temporal_causality_engine.benchmark import (
    adjacency_from_chain,
    benchmark_method,
)

# Generate synthetic data
n_vars = 4
df_raw = make_synthetic_var(n_series=n_vars, n_samples=800, seed=0)
df = make_stationary(df_raw)

truth_adj = adjacency_from_chain(n_vars)

# Wrap methods to common API
def granger_method(data):
    return pairwise_granger_fdr(data, alpha=0.05)

def pcmci_method(data):
    return run_pcmci(data, tau_max=5, alpha=0.05)

results = []

results.append(
    benchmark_method(granger_method, df, truth_adj, "Granger+FDR")
)
results.append(
    benchmark_method(pcmci_method, df, truth_adj, "PCMCI")
)

df_results = pd.DataFrame(results)
print("\nBenchmark results:\n")
print(df_results)

df_results.to_csv("results/benchmark_results.csv", index=False)
