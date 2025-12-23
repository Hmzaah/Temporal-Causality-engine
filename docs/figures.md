# Visualizations & Figures

This project intentionally avoids committing static figures.

Instead, **all causal graphs and matrices are generated dynamically**
via the Streamlit dashboard.

## Why no static plots?
- Graphs depend on method (Granger / FDR / PCMCI)
- Results vary with sample size, alpha, and preprocessing
- Static plots would be misleading

## How to view figures
Run the Streamlit app locally:

```bash
streamlit run streamlit_app/app.py

