from pathlib import Path
from temporal_causality_engine.utils import make_synthetic_var, make_stationary
from temporal_causality_engine.pcmci_module import run_pcmci
from temporal_causality_engine.viz import build_graph_from_adjacency, plot_graph

Path("results").mkdir(exist_ok=True)

df_raw = make_synthetic_var(n_series=4, n_samples=600, seed=42)
df = make_stationary(df_raw)

pvals, adj = run_pcmci(df, tau_max=5, alpha=0.05)

print("\nPCMCI adjacency:\n", adj.astype(int))

pvals.to_csv("results/pcmci_pvalues.csv")
adj.astype(int).to_csv("results/pcmci_adj.csv")

G = build_graph_from_adjacency(adj)
plot_graph(G, "PCMCI Causal Graph", "results/pcmci_graph.png")
