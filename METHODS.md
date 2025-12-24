# Methodological Notes

This document summarizes the methodological guarantees and design choices
behind Temporal Causality Engine.

---

## Stationarity

All time series are validated using:
- Augmented Dickey–Fuller (ADF)
- KPSS tests

Automatic differencing is applied where required.
Causal inference is never performed on non-stationary series.

---

## Granger causality

Granger causality is implemented without heuristic thresholding.
Raw p-values are exposed directly.

---

## Multiple hypothesis testing

False discovery rate is controlled using the Benjamini–Hochberg procedure.

Empty causal graphs under FDR correction are expected and preserved.
No alpha inflation or edge forcing is performed.

---

## PCMCI

PCMCI is implemented via the tigramite framework using ParCorr
conditional independence tests.

PCMCI results may differ from Granger due to conditioning effects
and different statistical assumptions.

---

## Interpretation

- Absence of edges indicates insufficient statistical evidence
- Presence of edges does not imply mechanistic causation
- Results are hypothesis-generating, not confirmatory

---

## Non-goals

This project intentionally avoids:
- causal strength ranking
- effect size exaggeration
- visual-first causal graphs
- automated causal explanations without uncertainty
