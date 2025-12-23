from pathlib import Path
from temporal_causality_engine.utils import make_synthetic_var, make_stationary
from temporal_causality_engine.granger_module import pairwise_granger
from temporal_causality_engine.viz import build_graph_from_adjacency, plot_graph

Path("results").mkdir(exist_ok=True)

df_raw = make_synthetic_var(n_series=4, n_samples=600, seed=42)
df = make_stationary(df_raw)

pvals, adj = pairwise_granger(df)

print("\nAdjacency:\n", adj.astype(int))

pvals.to_csv("results/granger_pvalues.csv")
adj.astype(int).to_csv("results/granger_adj.csv")

G = build_graph_from_adjacency(adj)
plot_graph(G, "Granger Causality (Stationary)", "results/granger_graph.png")
