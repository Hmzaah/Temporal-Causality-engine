# Temporal Causality Engine

Temporal Causality Engine is a research-oriented Python project for **causal discovery in multivariate time series**.  
It was built with a simple philosophy: *prefer statistically correct answers over visually appealing ones*.

This project treats **uncertainty and null results as meaningful outcomes**, not failures to be hidden or corrected.

---

## Why this project exists

Causal discovery in time series is often presented with dense graphs and confident edges, even when the statistical evidence is weak.  
In practice, many pipelines silently relax assumptions or significance thresholds to “show something.”

Temporal Causality Engine takes the opposite stance:

- If the data does not support a causal claim, **no edge is shown**
- If multiple hypotheses are tested, **false discoveries are controlled explicitly**
- If assumptions are violated, **they are corrected or surfaced, not ignored**

The result is a system that may look conservative, but is methodologically defensible.

---

## Core Principles

- Statistical honesty over aesthetics
- Explicit control of false discoveries
- Reproducibility and benchmarking over anecdotes
- Empty causal graphs are valid scientific results
- No threshold hacking or post-hoc tuning

---

## What the system does

### Stationarity Enforcement
All time series are validated before causal analysis.

- Augmented Dickey–Fuller (ADF)
- KPSS test
- Automatic differencing when required
- Implemented in `utils.py`

Causal tests are only applied once assumptions are satisfied.

---

### Causal Discovery Methods

The framework currently supports:

- **Granger Causality (raw)**
- **Granger Causality with Benjamini–Hochberg FDR correction**
- **PCMCI** (via `tigramite`, using ParCorr conditional independence tests)

A key design decision is that **Granger + FDR is expected to produce empty graphs** in many real settings.  
This is not an error — it is the statistically correct outcome under multiple-hypothesis control.

No artificial relaxation of significance thresholds is performed anywhere in the pipeline.

---

### Statistical Rigor

- Explicit multiple-hypothesis correction
- No alpha inflation
- No forced sparsity or density
- Null results are preserved and reported

If a method returns no causal edges, the system accepts that outcome.

---

### Benchmarking with Ground Truth

To avoid subjective evaluation, the project includes a benchmarking pipeline using **synthetic VAR chain data** with known causal structure.

Metrics reported:
- Precision
- Recall
- F1 score
- Runtime

Implemented in:
- `benchmark.py`
- `examples/run_benchmark.py`

Results are saved as CSV files for reproducibility and comparison.

---

### Visualization (Interactive by design)

Visualization is intentionally separated from computation.

- Streamlit-based interactive dashboard
- Users can switch between:
  - Granger (raw)
  - Granger + FDR
  - PCMCI
- Interactive causal graphs and adjacency matrices
- Clear warnings when FDR-controlled graphs are empty

**Why no static plots?**  
Static plots tend to hide uncertainty and invite over-interpretation. Interactive inspection makes assumptions and outcomes explicit.


---

## Usage

Run the benchmarking pipeline:

```bash
python examples/run_benchmark.py
