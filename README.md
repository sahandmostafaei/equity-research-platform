# Equity Research & Fundamental Valuation Platform

A modular equity-research platform for fundamental analysis, financial modelling, valuation, peer analysis, scenario analysis, and investment decision support.

The project follows a professional equity-research workflow:

**Financial Statements → Fundamental Analysis → Market Analysis → Forecasting → DCF → Comparable Companies → Scenario Analysis → Investment Assessment**

---

## Research Target

The default research universe contains one target company and four comparable companies.

| Role | Company | Ticker |
|---|---|---|
| Target | Microsoft | MSFT |
| Peer | Alphabet | GOOGL |
| Peer | Meta Platforms | META |
| Peer | Apple | AAPL |
| Peer | Amazon | AMZN |

The research universe is configurable through:

`data/research_config.csv`

---

## Key Capabilities

### Fundamental Analysis

- Revenue
- EBITDA
- EBIT
- Net income
- Operating cash flow
- Capital expenditure
- Free cash flow
- NOPAT
- Invested capital
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

### Market Analysis

- Current share price
- Market capitalization
- Enterprise value
- Shares outstanding
- Beta
- Debt
- Cash

### Valuation

- Discounted Cash Flow
- Terminal value
- Enterprise value
- Equity value
- Implied value per share
- Margin of safety
- Upside / downside
- P/E valuation
- Price / Sales valuation
- EV / Sales valuation
- EV / EBITDA valuation
- Peer median valuation

### Comparable Company Analysis

The platform evaluates:

- P/E
- EV / Sales
- EV / EBITDA
- Price / Sales
- FCF yield
- Peer median multiples
- Target premium / discount
- Implied valuation

Enterprise-value multiples are correctly bridged from enterprise value to equity value.

### Scenario Analysis

The valuation framework supports:

- Bear case
- Base case
- Bull case

Each scenario can specify:

- Revenue growth
- EBITDA margin
- WACC
- Terminal growth
- Forecast horizon
- FCF conversion

### Investment Assessment

The investment framework incorporates:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

These inputs are combined into a structured investment score and classification.

---

## Architecture

The project separates data ingestion, financial analysis, valuation, peer analysis, scenario analysis, research orchestration, and output generation.

**Data → Analysis → Valuation → Investment Assessment → Research Outputs**

Main components:

- `data_loader.py` — market and financial-data retrieval
- `financial_statements.py` — statement normalization and accounting calculations
- `financial_data.py` — standardized historical financial dataset
- `financial_analysis.py` — fundamental metrics
- `market_data.py` — market and capital-structure data
- `forecasting.py` — financial forecasting
- `capital_cost.py` — cost-of-capital calculations
- `valuation.py` — core valuation functions
- `dcf_model.py` — DCF modelling
- `peer_valuation.py` — comparable-company valuation
- `comparables.py` — valuation multiples
- `scenarios.py` — scenario definitions and forecasts
- `scenario_valuation.py` — scenario-based valuation
- `investment_thesis.py` — investment scoring
- `investment_decision.py` — investment classification
- `research_engine.py` — integrated research workflow
- `research_outputs.py` — output generation
- `research_report.py` — research reporting
- `data_quality.py` — validation and data-quality checks

---

## Research Workflow

1. Load research configuration
2. Identify target and peer companies
3. Retrieve financial statements
4. Normalize accounting line items
5. Calculate historical financial metrics
6. Retrieve market data
7. Calculate enterprise value and market metrics
8. Estimate cost of capital
9. Forecast operating performance
10. Run DCF valuation
11. Calculate comparable-company multiples
12. Calculate peer median multiples
13. Estimate implied peer-based valuation
14. Run bear, base, and bull scenarios
15. Consolidate valuation outputs
16. Calculate investment assessment
17. Save structured research outputs

---

## Financial Modelling

Free cash flow is standardized as:

**FCF = Operating Cash Flow − |Capital Expenditure|**

This handles differences in capital-expenditure sign conventions across data sources.

The DCF framework calculates:

- Present value of forecast cash flows
- Terminal value
- Present value of terminal value
- Enterprise value
- Equity value
- Implied value per share

The valuation framework validates the relationship between WACC and terminal growth before calculating terminal value.

---

## Cost of Capital

The model estimates cost of equity using CAPM:

**Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium**

After-tax cost of debt is calculated as:

**After-Tax Cost of Debt = Pre-Tax Cost of Debt × (1 − Tax Rate)**

WACC is then calculated using market-value weights of equity and debt.

The resulting WACC is also exposed as a research output for interpretation and validation.

---

## Comparable Companies

The comparable-company framework separates equity-value and enterprise-value methodologies.

### Equity-value multiples

Examples:

- P/E
- Price / Sales

### Enterprise-value multiples

Examples:

- EV / EBITDA
- EV / Sales

Enterprise-value approaches are subsequently bridged to equity value using:

**Equity Value = Enterprise Value − Debt + Cash**

This distinction is important for avoiding incorrect application of valuation multiples.

---

## Scenario Framework

The model uses three scenarios.

### Bear

- Lower revenue growth
- Lower EBITDA margin
- Higher WACC
- Lower terminal growth

### Base

- Central operating assumptions
- Central WACC
- Central terminal growth

### Bull

- Higher revenue growth
- Higher EBITDA margin
- Lower WACC
- Higher terminal growth

All scenario assumptions are stored in:

`data/research_config.csv`

---

## Configuration

Research assumptions are centralized rather than scattered throughout the source code.

Configuration includes:

- Target company
- Peer companies
- Tax rate
- Risk-free rate
- Equity risk premium
- Pre-tax cost of debt
- Forecast horizon
- FCF conversion
- Bear assumptions
- Base assumptions
- Bull assumptions

This makes the research workflow easier to reproduce and modify.

---

## Running the Project

Install dependencies:

`pip install -r requirements.txt`

Run the complete research pipeline:

`python run_research.py`

The pipeline retrieves current market and financial information and generates structured outputs under:

`data/processed/`

---

## Generated Outputs

The research pipeline can generate:

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

Generated market data and processed outputs are excluded from Git tracking.

---

## Testing

The project uses `pytest`.

Run:

`pytest`

The test suite covers key components including:

- Financial statement normalization
- Free cash flow calculation
- Financial validation
- DCF valuation
- Equity valuation
- Peer valuation
- Comparable-company multiples
- Scenario calculations
- Research output generation
- Research configuration

Continuous integration is configured through:

`.github/workflows/tests.yml`

---

## Project Structure

    equity-research-platform/
    │
    ├── .github/
    │   └── workflows/
    │       └── tests.yml
    │
    ├── data/
    │   ├── processed/
    │   ├── research_config.csv
    │   └── research_universe.csv
    │
    ├── figures/
    │
    ├── notebooks/
    │   └── 01_empirical_research.py
    │
    ├── src/
    │   ├── assumptions.py
    │   ├── capital_cost.py
    │   ├── comparables.py
    │   ├── config.py
    │   ├── data_loader.py
    │   ├── data_processing.py
    │   ├── data_quality.py
    │   ├── dcf_model.py
    │   ├── empirical_pipeline.py
    │   ├── financial_analysis.py
    │   ├── financial_data.py
    │   ├── financial_statements.py
    │   ├── forecasting.py
    │   ├── forecast_sensitivity.py
    │   ├── investment_decision.py
    │   ├── investment_thesis.py
    │   ├── market_data.py
    │   ├── peer_valuation.py
    │   ├── pipeline.py
    │   ├── reporting.py
    │   ├── research_engine.py
    │   ├── research_metrics.py
    │   ├── research_outputs.py
    │   ├── research_report.py
    │   ├── scenario_valuation.py
    │   ├── scenarios.py
    │   ├── screening.py
    │   └── valuation.py
    │
    ├── tests/
    │   ├── test_empirical_pipeline.py
    │   ├── test_financial_statements.py
    │   ├── test_peer_valuation.py
    │   ├── test_research_outputs.py
    │   ├── test_scenarios.py
    │   └── test_valuation.py
    │
    ├── .gitignore
    ├── LICENSE
    ├── PROJECT.md
    ├── README.md
    ├── RESULTS.md
    ├── pytest.ini
    ├── requirements.txt
    └── run_research.py

---

## Data and Research Integrity

The project retrieves financial and market information dynamically.

Therefore, valuation outputs can change depending on:

- Market prices
- Financial-statement updates
- Data availability
- Accounting classifications
- Peer selection
- Forecast assumptions
- WACC
- Terminal growth

No numerical research findings are manually fabricated in the repository.

Any numerical result used in an application, presentation, or research discussion should be generated from an actual execution of the pipeline and checked against the underlying data.

---

## Limitations

The platform is a research and modelling framework rather than a production investment system.

Important limitations include:

- External data-source limitations
- Missing financial observations
- Accounting-definition differences
- Simplified forecasting assumptions
- Peer-selection effects
- DCF sensitivity to WACC and terminal growth
- Market-price volatility
- Simplified investment scoring

The resulting valuation should therefore be interpreted as a model estimate rather than an objective measure of fair value.

---

## Academic and Professional Relevance

This project demonstrates applied skills in:

- Corporate finance
- Equity research
- Financial statement analysis
- Financial modelling
- Valuation
- Quantitative finance
- Investment analysis
- Financial data analysis
- Python
- Pandas
- NumPy
- Statistical reasoning
- Financial data engineering
- Research reproducibility

Relevant areas include:

- Equity Research
- Investment Banking
- Private Equity
- Hedge Funds
- Asset Management
- Quantitative Finance
- Financial Risk Management
- Financial Data Analytics

---

## Relationship to the Broader Portfolio

This project is designed as a company-level investment-analysis project.

It complements projects covering:

- Investment banking and M&A
- Portfolio optimization
- Credit risk
- Banking customer analytics
- Financial data warehousing

It also complements a separate empirical finance research project focused on portfolio construction and risk-adjusted performance rather than duplicating that research.

---

## Author

**Sahand Mostafaei**

BSc Electrical Engineering

Finance | Quantitative Finance | Risk Analytics | Financial Data

GitHub:

https://github.com/sahandmostafaei

---

## Disclaimer

This repository is intended for educational, research, and portfolio purposes only.

It does not constitute investment advice, an offer, or a recommendation to buy or sell any security.
