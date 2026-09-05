# Equity Research & Fundamental Valuation Platform

A Python-based equity research platform for fundamental company analysis, financial statement analysis, valuation, peer comparison, scenario analysis, and systematic investment screening.

## Objective

This project develops a reproducible buy-side style framework for analyzing publicly traded companies.

The platform combines:

- Financial statement analysis
- Fundamental ratio analysis
- Growth and profitability analysis
- ROIC and capital-efficiency analysis
- Free cash flow analysis
- Financial forecasting
- Discounted Cash Flow valuation
- Comparable-company valuation
- Trading multiple analysis
- Bull/base/bear scenarios
- DCF sensitivity analysis
- Fundamental screening
- Company ranking
- Investment scoring
- Investment thesis organization

## Research Workflow

Financial Data
→ Financial Statements
→ Fundamental Analysis
→ Operating Forecast
→ DCF Valuation
→ Comparable Valuation
→ Scenario Analysis
→ Sensitivity Analysis
→ Investment Score
→ Investment Thesis

## Core Questions

The framework is designed to answer:

1. Is the company financially healthy?
2. Is the company generating attractive returns on capital?
3. Is growth translating into profitability?
4. How efficiently does the company convert earnings into free cash flow?
5. How much financial leverage does the company use?
6. How does the company compare with its peers?
7. What is the estimated intrinsic value?
8. What does the current market price imply?
9. How sensitive is valuation to key assumptions?
10. Does the investment case remain attractive under adverse scenarios?

## Fundamental Metrics

### Growth

- Revenue growth
- EBITDA growth
- EBIT growth
- EPS growth
- Free cash flow growth

### Profitability

- EBITDA margin
- EBIT margin
- Net margin
- ROA
- ROE
- ROIC

### Balance Sheet

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage

### Cash Flow

- Operating cash flow
- Capital expenditure
- Free cash flow
- FCF margin
- Cash conversion

## Valuation

### Discounted Cash Flow

The DCF framework separates:

- Operating forecasts
- Free cash flow
- Explicit forecast period
- Terminal value
- Discounting
- Enterprise value
- Equity value
- Per-share intrinsic value

### Comparable Companies

Relative valuation includes:

- P/E
- EV/EBITDA
- EV/Sales
- Price/Sales
- FCF yield

Peer statistics include:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation

## Scenario Analysis

The framework evaluates:

- Bear case
- Base case
- Bull case

Assumptions can vary across:

- Revenue growth
- EBITDA margin
- WACC
- Terminal growth
- FCF conversion

## Sensitivity Analysis

DCF valuation is tested across combinations of:

- WACC
- Terminal growth

This provides a valuation range rather than relying on a single point estimate.

## Fundamental Screening

The platform can identify companies meeting configurable criteria such as:

- ROIC ≥ 15%
- Revenue growth ≥ 10%
- Net debt / EBITDA ≤ 2.0x
- FCF margin ≥ 8%

## Investment Scoring

A research-prioritization score incorporates:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Balance-sheet leverage

The score is intended to prioritize further research rather than serve as a standalone trading signal.

## Technology

- Python
- pandas
- NumPy
- SciPy
- scikit-learn
- Matplotlib
- yfinance
- pytest

## Project Structure

equity-research-platform/
│
├── data/
│   └── research_universe.csv
│
├── figures/
│
├── notebooks/
│
├── src/
│   ├── __init__.py
│   ├── comparables.py
│   ├── data_loader.py
│   ├── data_processing.py
│   ├── financial_analysis.py
│   ├── financial_statements.py
│   ├── forecasting.py
│   ├── investment_thesis.py
│   ├── market_data.py
│   ├── pipeline.py
│   ├── reporting.py
│   ├── scenarios.py
│   ├── screening.py
│   └── valuation.py
│
├── tests/
│   ├── test_comparables.py
│   ├── test_financial_analysis.py
│   ├── test_financial_statements.py
│   ├── test_forecasting.py
│   ├── test_investment_thesis.py
│   ├── test_screening.py
│   └── test_valuation.py
│
├── .gitignore
├── LICENSE
├── PROJECT.md
├── README.md
├── RESULTS.md
├── pytest.ini
└── requirements.txt

## Reproducibility

The system is modular so that:

1. Data can be acquired independently.
2. Financial statements can be processed independently.
3. Fundamental metrics can be calculated independently.
4. Forecasts can be tested independently.
5. Valuation models can be tested independently.
6. Screening and ranking can be tested independently.
7. Reporting can be reproduced from the same inputs.

## Limitations

The analysis depends on the quality of financial data and the assumptions used in forecasting and valuation.

DCF estimates are particularly sensitive to:

- Revenue growth
- Operating margins
- Free cash flow conversion
- WACC
- Terminal growth
- Capital requirements

Peer valuation is also sensitive to the choice of comparable companies.

The framework is therefore intended for research and analytical purposes rather than as a definitive investment recommendation.

## Portfolio Context

This project forms part of a broader finance portfolio covering:

- Investment banking
- Equity valuation
- Portfolio optimization
- Credit risk
- Financial data engineering
- Machine learning in finance

## Author

**Sahand Mostafaei**

BSc Electrical Engineering

Focus areas:

- Private Equity
- Hedge Funds
- Quantitative Finance
- Investment Analysis
- Financial Modelling
- Financial Risk
- Data Analytics
