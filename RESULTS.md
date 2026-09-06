# Research Results

## Equity Research & Fundamental Valuation Platform

## Status

This repository contains a dynamic equity-research and valuation pipeline.

Numerical market, financial-statement, valuation, and investment outputs are generated from the research pipeline rather than manually inserted into this document.

No numerical research results are fabricated in this repository.

---

## Default Research Universe

### Target

Microsoft — MSFT

### Peers

Alphabet — GOOGL
Meta Platforms — META
Apple — AAPL
Amazon — AMZN

The research universe can be changed through:

`data/research_config.csv`

---

## Analytical Outputs

When the pipeline is executed, the following analytical layers are produced.

### 1. Historical Financial Analysis

The pipeline retrieves and standardizes:

- Revenue
- EBITDA
- EBIT
- Net income
- Operating cash flow
- Capital expenditure
- Free cash flow
- Debt
- Cash
- Assets
- Shareholders' equity
- NOPAT
- Invested capital

It then derives:

- Revenue growth
- EBITDA margin
- EBIT margin
- Net margin
- FCF margin
- ROIC
- ROA
- ROE
- Net debt
- Net debt / EBITDA

---

## 2. Market Analysis

The market layer produces:

- Current price
- Market capitalization
- Shares outstanding
- Beta
- Debt
- Enterprise value

and derives valuation-related market metrics.

---

## 3. DCF Analysis

The DCF layer evaluates the target under:

- Bear scenario
- Base scenario
- Bull scenario

The model produces:

- Forecast revenue
- Forecast EBITDA
- Forecast free cash flow
- Enterprise value
- Equity value
- Implied value per share

---

## 4. Comparable Company Analysis

The peer analysis produces:

- P/E
- EV / Sales
- EV / EBITDA
- Price / Sales
- FCF yield

Peer medians are then used to calculate implied target valuations.

---

## 5. Consolidated Valuation

The research engine combines:

- DCF valuation
- P/E valuation
- Price / Sales valuation
- EV / Sales valuation
- EV / EBITDA valuation

into a consolidated valuation table.

The model's consensus valuation is derived from the available valuation observations.

---

## 6. Investment Assessment

The investment assessment incorporates:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The result is converted into a structured investment classification.

---

## 7. Generated Output Files

Running:

`python run_research.py`

generates:

- `target_financials.csv`
- `market_snapshot.csv`
- `market_metrics.csv`
- `scenario_valuations.csv`
- `peer_market_data.csv`
- `peer_market_metrics.csv`
- `peer_multiples.csv`
- `peer_median_multiples.csv`
- `peer_comparison.csv`
- `peer_valuation.csv`
- `valuation_summary.csv`
- `investment_summary.csv`
- `research_snapshot.csv`

These files are intentionally excluded from Git tracking because they depend on dynamically retrieved financial and market data.

---

## 8. Interpretation Framework

The research should be interpreted across four dimensions.

### Business Quality

Evaluate:

- Growth
- Profitability
- Cash generation
- ROIC
- Balance-sheet strength

### Relative Valuation

Evaluate:

- Target versus peer multiples
- Premium / discount
- Peer median valuation

### Intrinsic Valuation

Evaluate:

- DCF value
- WACC
- Terminal growth
- Forecast assumptions
- Margin assumptions

### Investment Risk

Evaluate:

- Valuation sensitivity
- Leverage
- Growth assumptions
- Margin assumptions
- Peer-selection effects
- Data quality

---

## 9. Reproducibility

Results are reproducible from the source code and configuration.

The research assumptions are centralized in:

`data/research_config.csv`

The research workflow is executed through:

`run_research.py`

---

## 10. Important Research Integrity Statement

This document intentionally does not contain manually created numerical findings.

Any numerical result presented in an application, report, presentation, or research discussion should be generated from an actual execution of the pipeline and checked against the underlying source data.

This prevents unsupported claims and fabricated empirical evidence.

---

## 11. Recommended Interpretation

The platform should be treated as a structured research framework rather than an automated investment decision-maker.

The strongest use of the project is to demonstrate the complete analytical process:

Financial Statements
→ Fundamental Analysis
→ Forecasting
→ DCF
→ Peer Valuation
→ Scenario Analysis
→ Investment Assessment

The resulting valuation is a model estimate whose reliability depends on the quality of the underlying data and assumptions.
