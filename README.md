# Equity Research & Fundamental Valuation Platform

Python-based equity research platform for fundamental company analysis, financial statement analysis, financial modelling, valuation, peer comparison, scenario analysis, sensitivity analysis, and systematic investment screening.

## Objective

This project implements a modular equity research workflow that transforms financial statements and market information into structured fundamental analysis, valuation outputs, and an investment assessment.

The architecture is designed to resemble a simplified institutional equity research workflow:

**Configuration → Financial Data → Fundamental Analysis → Forecasting → Cost of Capital → DCF → Relative Valuation → Scenarios → Sensitivity → Investment Assessment**

The project emphasizes:

- Financial analysis
- Fundamental valuation
- Financial modelling
- Quantitative screening
- Reproducibility
- Data-quality controls
- Unit testing
- Modular software architecture

## Research Workflow

1. Define the research universe
2. Load centralized research configuration
3. Retrieve financial statements
4. Retrieve market information
5. Normalize financial statement data
6. Validate financial data
7. Calculate historical financial metrics
8. Analyze growth and profitability
9. Analyze capital efficiency
10. Analyze financial strength
11. Calculate market valuation metrics
12. Construct operating forecasts
13. Estimate cost of capital
14. Perform DCF valuation
15. Perform comparable-company valuation
16. Run Bear/Base/Bull scenarios
17. Perform valuation sensitivity analysis
18. Screen and rank companies
19. Calculate investment scores
20. Generate an investment assessment
21. Produce research tables and visualizations

## Research Universe

The initial research universe contains:

| Ticker | Company | Sector | Role |
|---|---|---|---|
| MSFT | Microsoft | Technology | Target |
| GOOGL | Alphabet | Technology | Peer |
| META | Meta Platforms | Technology | Peer |
| AAPL | Apple | Technology | Peer |
| AMZN | Amazon | Consumer Discretionary | Peer |

The universe is defined in:

`data/research_universe.csv`

Research assumptions and modelling parameters are maintained separately in:

`data/research_config.csv`

## Fundamental Analysis

The platform evaluates companies across several fundamental dimensions.

### Growth

- Revenue growth
- EBITDA growth
- Earnings growth
- Free cash flow growth

### Profitability

- EBITDA margin
- EBIT margin
- Net margin
- ROA
- ROE
- ROIC

### Capital Efficiency

- NOPAT
- Invested capital
- ROIC
- Free cash flow
- FCF margin

### Financial Strength

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage

## Financial Statement Processing

The platform processes:

- Income statements
- Balance sheets
- Cash-flow statements

Standardized analytical variables include:

- Revenue
- EBIT
- EBITDA
- Net income
- Depreciation and amortization
- Operating cash flow
- Capital expenditure
- Free cash flow
- Total debt
- Cash
- Shareholders' equity
- NOPAT
- Invested capital

Financial statement line-item aliases are mapped into standardized analytical variables.

## Market Analysis

Market data is used to calculate:

- Market capitalization
- Enterprise value
- Current share price
- Shares outstanding
- EPS
- P/E
- EV/Sales
- EV/EBITDA
- FCF yield

These metrics connect operating fundamentals with market valuation.

## Forecasting

The forecasting framework produces a five-year operating forecast using configurable assumptions for:

- Revenue growth
- EBITDA margin
- FCF conversion
- Forecast horizon

Forecast outputs include:

- Revenue
- EBITDA
- Free cash flow

The modelling assumptions are separated from the valuation implementation.

## Cost of Capital

The project includes a CAPM/WACC framework using:

- Risk-free rate
- Equity beta
- Equity risk premium
- Cost of equity
- Pre-tax cost of debt
- Tax rate
- After-tax cost of debt
- Market-value capital structure

The discount rate is therefore an explicit modelling input rather than an unexplained hard-coded value.

## DCF Valuation

The DCF framework calculates:

- Present value of forecast free cash flow
- Terminal value
- Present value of terminal value
- Enterprise value
- Equity value
- Intrinsic value per share

The model validates the fundamental terminal-value condition:

**WACC > terminal growth**

This prevents mathematically invalid Gordon-growth terminal values.

## Relative Valuation

Comparable-company analysis includes:

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

Peer valuation can be used alongside DCF analysis to provide a second valuation perspective.

## Scenario Analysis

The platform supports three scenarios:

| Scenario | Revenue Growth | EBITDA Margin | WACC | Terminal Growth |
|---|---:|---:|---:|---:|
| Bear | 3.0% | 18.0% | 11.0% | 2.0% |
| Base | 7.0% | 22.0% | 9.0% | 2.5% |
| Bull | 12.0% | 26.0% | 8.0% | 3.0% |

These are modelling assumptions and are not historical company results.

Each scenario generates a separate DCF valuation.

## Sensitivity Analysis

The project supports sensitivity analysis across:

- WACC
- Terminal growth
- Revenue growth
- EBITDA margin

The objective is to evaluate valuation ranges instead of relying exclusively on a single point estimate.

## Fundamental Screening

Companies can be screened using:

- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA
- Interest coverage

The framework can identify companies exhibiting combinations of:

- Strong profitability
- Attractive growth
- Strong cash generation
- Manageable leverage
- Strong debt-service capacity

## Investment Scoring

The investment scoring framework considers:

- Valuation attractiveness
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The resulting score is classified into:

- High Conviction
- Attractive
- Neutral
- Cautious
- Low Conviction

The score is a quantitative research framework and does not replace analyst judgment.

## Investment Decision

The platform combines:

1. Fundamental quality
2. Growth
3. Cash generation
4. Balance-sheet strength
5. Valuation

The resulting assessment can classify a company as:

- Strong Buy Candidate
- Buy Candidate
- Watchlist
- Low Conviction

These classifications are model outputs and must be interpreted with the underlying assumptions and evidence.

## Integrated Research Engine

The project contains a high-level `ResearchEngine` that orchestrates the major analytical components.

The integrated architecture is:

**Research Configuration**
↓
**Financial Statements**
↓
**Historical Fundamental Analysis**
↓
**Market Metrics**
↓
**Operating Forecasts**
↓
**Scenario DCF Valuation**
↓
**Consensus Valuation**
↓
**Investment Score**
↓
**Investment Assessment**

This separates individual analytical functions from the higher-level research workflow.

## Centralized Configuration

Research assumptions are maintained in:

`data/research_config.csv`

The configuration contains:

- Research target
- Peer universe
- Tax rate
- Risk-free rate
- Equity risk premium
- Cost of debt
- Forecast horizon
- FCF conversion
- Bear-case assumptions
- Base-case assumptions
- Bull-case assumptions

This makes the model easier to audit and reproduce.

## Data Quality

The project includes controls for:

- Required columns
- Missing observations
- Duplicate rows
- Numeric conversion
- Positive-value validation
- Configuration validation
- Duplicate configuration parameters

The objective is to prevent avoidable data-quality problems from propagating into valuation outputs.

## Research Reporting

The reporting layer supports:

- Company snapshots
- Peer comparison tables
- Valuation summaries
- Research tables
- CSV exports
- Revenue and EBITDA charts
- DCF sensitivity visualizations

## Testing

The repository contains unit tests covering:

- Financial analysis
- Financial statements
- Financial data
- Data quality
- Configuration
- Forecasting
- DCF valuation
- Capital cost
- Comparable-company analysis
- Peer valuation
- Scenario valuation
- Forecast sensitivity
- Research metrics
- Screening
- Investment scoring
- Investment decision logic
- Research reporting
- Valuation summaries
- Research engine orchestration

GitHub Actions is configured to run the test suite automatically for pushes and pull requests targeting `main`.

## Technology

- Python
- pandas
- NumPy
- SciPy
- scikit-learn
- Matplotlib
- yfinance
- openpyxl
- pytest
- GitHub Actions

## Project Structure

The repository is organized into:

- `data/` — research universe and modelling configuration
- `figures/` — generated research visualizations
- `notebooks/` — research notebooks
- `src/` — analytical and valuation modules
- `tests/` — automated unit tests
- `.github/workflows/` — continuous integration

Key modules include:

- `config.py`
- `data_loader.py`
- `data_processing.py`
- `data_quality.py`
- `financial_data.py`
- `financial_analysis.py`
- `financial_statements.py`
- `market_data.py`
- `research_metrics.py`
- `forecasting.py`
- `capital_cost.py`
- `valuation.py`
- `dcf_model.py`
- `comparables.py`
- `peer_valuation.py`
- `scenarios.py`
- `scenario_valuation.py`
- `forecast_sensitivity.py`
- `screening.py`
- `investment_thesis.py`
- `investment_decision.py`
- `research_report.py`
- `valuation_summary.py`
- `reporting.py`
- `pipeline.py`
- `research_engine.py`

## Reproducibility

The project separates:

- Retrieved financial data
- Processed financial data
- Research configuration
- Analyst assumptions
- Forecast values
- Valuation calculations
- Investment conclusions

This makes the analytical chain easier to inspect and reproduce.

## Research Integrity

The project maintains a distinction between:

### Historical observations

Data retrieved from financial and market-data sources.

### Derived metrics

Metrics calculated from historical observations.

### Analyst assumptions

Explicit modelling parameters.

### Forecasts

Values generated from analyst assumptions.

### Valuation outputs

Values generated by valuation models.

### Investment assessment

Interpretation of the resulting evidence.

The repository does not present unexecuted analytical outputs as empirical findings.

## Portfolio Context

This project forms part of a broader finance and quantitative-finance portfolio.

It demonstrates:

- Equity research
- Financial statement analysis
- Financial modelling
- DCF valuation
- Comparable-company valuation
- Fundamental screening
- Scenario analysis
- Sensitivity analysis
- Python financial analytics
- Data-quality controls
- Automated testing
- Research workflow architecture

## Intended Applications

The framework is relevant to:

- Equity research
- Investment analysis
- Asset management
- Hedge funds
- Private equity
- Investment banking
- Financial modelling
- Quantitative finance
- Financial data analytics

## Limitations

This project is intended for educational and research purposes.

Important limitations include:

- Public-data availability
- Financial-statement classification differences
- Data-provider limitations
- Forecast uncertainty
- WACC estimation uncertainty
- Terminal-value sensitivity
- Peer-selection bias
- Market-price volatility
- Model specification risk
- Assumption uncertainty

The platform does not constitute investment advice.

## Author

**Sahand Mostafaei**

BSc Electrical Engineering

Areas of interest:

- Quantitative Finance
- Investment Analysis
- Financial Risk Management
- Banking
- Financial Modelling
- Investment Banking
- Private Equity
- Hedge Funds
- Financial Data Analytics
