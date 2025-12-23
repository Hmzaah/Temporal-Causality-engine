from pathlib import Path
from temporal_causality_engine.utils import make_synthetic_var, make_stationary
from temporal_causality_engine.granger_module import pairwise_granger_fdr
from temporal_causality_engine.viz import build_graph_from_adjacency, plot_graph

Path("results").mkdir(exist_ok=True)

df_raw = make_synthetic_var(n_series=4, n_samples=600, seed=42)
df = make_stationary(df_raw)

pvals, adj_fdr = pairwise_granger_fdr(df, alpha=0.05)

print("\nFDR-corrected adjacency:\n", adj_fdr.astype(int))

pvals.to_csv("results/granger_pvalues.csv")
adj_fdr.astype(int).to_csv("results/granger_adj_fdr.csv")

G = build_graph_from_adjacency(adj_fdr)
plot_graph(G, "Granger Causality (FDR-corrected)", "results/granger_graph_fdr.png")
