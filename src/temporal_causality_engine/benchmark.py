import time
import numpy as np
import pandas as pd
from typing import Dict


def adjacency_from_chain(n_vars: int) -> pd.DataFrame:
    """
    Ground-truth adjacency for synthetic VAR:
    x0 -> x1 -> x2 -> ...
    """
    adj = np.zeros((n_vars, n_vars), dtype=bool)
    for i in range(n_vars - 1):
        adj[i, i + 1] = True
    cols = [f"x{i}" for i in range(n_vars)]
    return pd.DataFrame(adj, index=cols, columns=cols)


def evaluate_adjacency(
    pred: pd.DataFrame,
    truth: pd.DataFrame
) -> Dict[str, float]:
    """
    Compute precision, recall, F1 for predicted adjacency.
    """
    pred_vals = pred.values.astype(bool)
    truth_vals = truth.values.astype(bool)

    tp = np.sum(pred_vals & truth_vals)
    fp = np.sum(pred_vals & ~truth_vals)
    fn = np.sum(~pred_vals & truth_vals)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0 else 0.0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
    }


def benchmark_method(
    method_fn,
    df: pd.DataFrame,
    truth_adj: pd.DataFrame,
    name: str
) -> Dict[str, float]:
    """
    Benchmark a causal discovery method.
    """
    start = time.time()
    _, adj = method_fn(df)
    runtime = time.time() - start

    metrics = evaluate_adjacency(adj, truth_adj)
    metrics["runtime_sec"] = runtime
    metrics["method"] = name
    return metrics
