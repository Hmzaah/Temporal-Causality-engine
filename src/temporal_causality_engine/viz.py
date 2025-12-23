import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def build_graph_from_adjacency(adj: pd.DataFrame) -> nx.DiGraph:
    G = nx.DiGraph()
    for src in adj.index:
        for dst in adj.columns:
            if adj.loc[src, dst]:
                G.add_edge(src, dst)
    return G

def plot_graph(G: nx.DiGraph, title: str, savepath: str = None):
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=800, arrowsize=16)
    plt.title(title)
    plt.axis("off")
    if savepath:
        plt.savefig(savepath, dpi=150, bbox_inches="tight")
    else:
        plt.show()
