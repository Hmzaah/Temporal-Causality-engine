import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from temporal_causality_engine.utils import (
    make_synthetic_var,
    make_stationary,
)
from temporal_causality_engine.granger_module import (
    pairwise_granger,
    pairwise_granger_fdr,
)
from temporal_causality_engine.pcmci_module import run_pcmci
from temporal_causality_engine.viz import build_graph_from_adjacency


# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Temporal Causality Engine",
    layout="centered"
)

st.title("🧠 Temporal Causality Engine")
st.markdown(
    """
Interactive causal discovery for multivariate time series.

This demo compares:
- **Granger causality (raw)**
- **Granger causality with FDR correction**
- **PCMCI (state-of-the-art multivariate method)**

Empty graphs for Granger+FDR are **statistically expected** under conservative testing.
"""
)

# ---------------------------
# Sidebar controls
# ---------------------------
st.sidebar.header("Configuration")

method = st.sidebar.selectbox(
    "Causal discovery method",
    [
        "Granger (raw)",
        "Granger + FDR",
        "PCMCI"
    ]
)

n_vars = st.sidebar.slider(
    "Number of variables",
    min_value=3,
    max_value=6,
    value=4
)

n_samples = st.sidebar.slider(
    "Number of samples",
    min_value=300,
    max_value=1500,
    value=800
)

alpha = st.sidebar.slider(
    "Significance level (alpha)",
    min_value=0.01,
    max_value=0.2,
    value=0.05,
    step=0.01
)

st.sidebar.markdown("---")
st.sidebar.caption("Synthetic VAR chain data")

# ---------------------------
# Data generation
# ---------------------------
df_raw = make_synthetic_var(
    n_series=n_vars,
    n_samples=n_samples,
    seed=42
)

df = make_stationary(df_raw)

st.subheader("📈 Time-Series Data (preview)")
st.dataframe(df.head())

# ---------------------------
# Run causal discovery
# ---------------------------
with st.spinner("Running causal discovery..."):

    if method == "Granger (raw)":
        pvals, adj = pairwise_granger(
            df,
            alpha=alpha
        )

    elif method == "Granger + FDR":
        pvals, adj = pairwise_granger_fdr(
            df,
            alpha=alpha
        )

    else:  # PCMCI
        pvals, adj = run_pcmci(
            df,
            tau_max=5,
            alpha=alpha
        )

# ---------------------------
# Show adjacency matrix
# ---------------------------
st.subheader("🧮 Causal Adjacency Matrix")
st.dataframe(adj.astype(int))

# ---------------------------
# Empty-graph explanation
# ---------------------------
if adj.values.sum() == 0:
    st.warning(
        """
No significant causal edges detected.

This is **expected behavior** for conservative methods such as
**Granger causality with FDR correction**, especially when signal
strength is moderate.

Try:
- Granger (raw) to see uncorrected edges
- PCMCI for multivariate causal discovery
"""
    )

# ---------------------------
# Plot causal graph
# ---------------------------
st.subheader("🕸️ Causal Graph")

G = build_graph_from_adjacency(adj)

fig, ax = plt.subplots(figsize=(6, 6))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    with_labels=True,
    node_size=900,
    node_color="#A7C7E7",
    arrowsize=18,
    ax=ax
)

st.pyplot(fig)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption(
    "Temporal Causality Engine • "
    "Granger vs PCMCI • Research-grade causal discovery"
)
