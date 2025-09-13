# ANES Time Series (CDF) Workspace

This repository is a working space for exploring the ANES (American National Election Studies) Time Series Cumulative Data File (CDF) and its accompanying documentation.

## Repository Structure

- `raw/anes_timeseries_cdf_csv_20220916.csv` – The Cumulative Data File (CSV) released 2022-09-16.
- `raw/anes_timeseries_2024_csv_20250808.csv` – A newer (2024) time series data release.
- `raw/anes_timeseries_cdf_codebook_var_20220916.pdf` → converted to `raw/anes_timeseries_cdf_codebook_var_20220916.txt`.
- `raw/anes_timeseries_cdf_codebook_app_20220916.pdf` → converted to `raw/anes_timeseries_cdf_codebook_app_20220916.txt`.
- `raw/anes_timeseries_2024_userguidecodebook_20250808.pdf` → converted to `raw/anes_timeseries_2024_userguidecodebook_20250808.txt`.
- `dev_notebook.ipynb` – Scratch / exploratory notebook (includes PDF→text extraction snippet using PyMuPDF).
- `socsci_venv/` – Local Python virtual environment (not intended for distribution).

## Relationship Between the Two Codebook Text Files

| File | Primary Content Focus | Typical Sections | How to Use It Programmatically |
|------|-----------------------|------------------|--------------------------------|
| `anes_timeseries_cdf_codebook_var_20220916.txt` | Variable-level documentation | Variable name, label, question text, universe, coding categories / value labels, notes, sometimes weighting or comparability notes inline | Parse to build a structured data dictionary (variables, types, value labels). Anchor on consistent variable header patterns (e.g., variable name followed by label). |
| `anes_timeseries_cdf_codebook_app_20220916.txt` | Appendices and methodological reference material | Study design, sampling, weighting schemes, derived scale construction, panel composition, response rates, longitudinal notes, possibly index construction tables | Use as narrative reference; limited structured extraction value except for targeted sections (e.g., weight construction). |

In short: the `_var_` file is the operational codebook for programmatic parsing; the `_app_` file supplies contextual and methodological appendices that explain how certain variables, weights, or composite indices came to be.

## Why Keep Both?
- Reproducibility: Methodological notes (appendix) justify analysis choices (e.g., which weight to apply).
- Data Integrity: Variable-level metadata alone can be ambiguous without appendix definitions (e.g., construction of feeling thermometers or ideology scales).
- Traceability: When publishing results, you can cite specific appendix sections that clarify transformations or sampling adjustments.

## When to Consult the Appendix (`*_app_*.txt`)
- Selecting the correct weight variable(s) (e.g., post-stratification vs. panel weights).
- Understanding changes in question wording across waves.
- Interpreting composite scales or index construction steps.
- Clarifying sampling frames or subsample restrictions that explain missingness patterns.

## 2024 Stand-Alone Release vs. Cumulative (Through 2020)

Two distinct data assets exist in this workspace:

| File | Coverage | Status Relative to CDF | Notes |
|------|----------|------------------------|-------|
| `raw/anes_timeseries_cdf_csv_20220916.csv` | 1948–2020 (per CDF release vintage 2022-09-16) | Canonical cumulative (integration already performed by ANES) | Variable names / codes standardized up through 2020. |
| `raw/anes_timeseries_2024_csv_20250808.csv` | 2024 wave (and only 2024) | NOT yet merged into cumulative file | Naming / coding may differ; new variables; potential reworded or retired items. |

Goal: Harmonize the 2024 release with the cumulative data so analyses can span 1948–2024 pending an official updated CDF.

## 2024 User Guide & Codebook

`raw/anes_timeseries_2024_userguidecodebook_20250808.txt` is a text extraction of the 2024 release's combined user guide + codebook PDF. It blends:

1. Study-level documentation (design, sampling, weighting, methodological 2024 updates).
2. Variable-level descriptions (new or modified items vs. 2020 and earlier waves).
3. Analyst guidance (recommended weights, handling break-offs, derived constructs).

Unlike the historical split (variable vs appendix) for the CDF, 2024 co-locates both layers. For harmonization we conceptually partition it into:
- Variable metadata blocks (feed a parser akin to the CDF variable codebook)
- Methodological sections (justify mapping and transformation decisions)