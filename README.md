# Equity Research & Fundamental Valuation Platform

Python-based equity research platform for fundamental company analysis, financial statement analysis, valuation, peer comparison, scenario analysis, sensitivity analysis, and systematic investment screening.

## Objective

This project develops a modular equity research workflow that transforms company financial statements and market data into structured fundamental analysis and valuation outputs.

The workflow is designed to resemble a simplified institutional equity research process:

**Financial Data → Fundamental Analysis → Forecasting → Cost of Capital → DCF → Comparable Valuation → Scenarios → Sensitivity → Screening → Investment Decision**

The platform emphasizes transparency, reproducibility, testing, and separation between observed data and analyst assumptions.

## Research Workflow

1. Define the research universe
2. Retrieve financial and market data
3. Normalize financial statement information
4. Validate data quality
5. Calculate historical financial metrics
6. Analyze profitability and capital efficiency
7. Analyze financial strength
8. Calculate market valuation metrics
9. Construct operating forecasts
10. Estimate cost of capital
11. Perform DCF valuation
12. Perform comparable-company valuation
13. Run Bear/Base/Bull scenarios
14. Perform valuation sensitivity analysis
15. Screen and rank companies
16. Generate an investment assessment
17. Produce research tables and visual outputs

## Research Target

The initial research universe contains:

| Ticker | Company | Sector | Role |
|---|---|---|---|
| MSFT | Microsoft | Technology | Target |
| GOOGL | Alphabet | Technology | Peer |
| META | Meta Platforms | Technology | Peer |
| AAPL | Apple | Technology | Peer |
| AMZN | Amazon | Consumer Discretionary | Peer |

The universe can be expanded through `data/research_universe.csv`.

## Fundamental Analysis

The platform evaluates company fundamentals across four major areas.

### Growth

- Revenue growth
- EBITDA growth
- EBIT growth
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

- Invested capital
- ROIC
- Free cash flow generation
- FCF margin

### Financial Strength

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage
- Liquidity and balance-sheet indicators

## Financial Statement Processing

The platform provides standardized processing for:

- Income statements
- Balance sheets
- Cash-flow statements
- Revenue
- EBIT
- EBITDA
- Net income
- Depreciation and amortization
- Operating cash flow
- Capital expenditure
- Debt
- Cash
- Shareholders' equity
- Invested capital
- NOPAT
- Free cash flow

Different financial-statement line-item names can be mapped into standardized analytical variables.

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

These metrics connect company fundamentals with market valuation.

## Forecasting

The forecasting framework produces a five-year operating forecast using configurable assumptions for:

- Revenue growth
- EBITDA margin
- FCF conversion
- Forecast horizon

The forecast produces:

- Revenue
- EBITDA
- Free cash flow

The framework is designed so that assumptions can be changed without rewriting the valuation model.

## Cost of Capital

The project includes a capital-cost framework based on:

- Risk-free rate
- Equity beta
- Equity risk premium
- Cost of equity
- Pre-tax cost of debt
- Tax rate
- After-tax cost of debt
- Capital structure
- WACC

The objective is to make the DCF discount rate an explicit modelling assumption rather than an unexplained hard-coded number.

## DCF Valuation

The DCF framework calculates:

- Present value of forecast free cash flow
- Terminal value
- Present value of terminal value
- Enterprise value
- Equity value
- Intrinsic value per share

The model explicitly checks that:

**WACC > terminal growth**

This prevents mathematically invalid terminal-value assumptions.

## Relative Valuation

Comparable-company analysis evaluates:

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

Peer median multiples can then be applied to target-company financial metrics to produce implied valuation estimates.

## Scenario Analysis

The platform supports three operating and valuation scenarios:

| Scenario | Revenue Growth | EBITDA Margin | WACC | Terminal Growth |
|---|---:|---:|---:|---:|
| Bear | 3.0% | 18.0% | 11.0% | 2.0% |
| Base | 7.0% | 22.0% | 9.0% | 2.5% |
| Bull | 12.0% | 26.0% | 8.0% | 3.0% |

These figures are modelling assumptions and should not be interpreted as historical company results.

Each scenario produces a separate valuation.

## Sensitivity Analysis

The platform supports sensitivity analysis across:

- WACC
- Terminal growth
- Revenue growth
- EBITDA margin

This allows the research to evaluate valuation ranges rather than relying on a single point estimate.

## Fundamental Screening

Companies can be screened using thresholds for:

- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA
- Interest coverage

The screening framework can identify companies exhibiting combinations of:

- Strong profitability
- Attractive growth
- Strong cash generation
- Manageable leverage
- Strong debt-service capacity

## Investment Scoring

The platform combines several fundamental characteristics into a normalized investment score.

The current framework considers:

- Valuation attractiveness
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The score can then be classified into categories such as:

- High Conviction
- Attractive
- Neutral
- Cautious
- Low Conviction

The score is a research framework rather than a substitute for analyst judgment.

## Investment Decision Framework

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

These labels are analytical outputs from the model and require interpretation alongside the underlying evidence.

## Research Reporting

The reporting layer supports:

- Company snapshots
- Peer comparison tables
- Valuation summaries
- Research tables
- Exportable CSV outputs
- Revenue and EBITDA charts
- DCF sensitivity visualizations

## Data Quality

The project includes explicit data-quality controls for:

- Required columns
- Missing observations
- Duplicate rows
- Numeric conversion
- Positive-value validation

This is intended to reduce errors propagating from raw financial data into analytical outputs.

## Testing

The project includes unit tests covering:

- Financial analysis
- Financial statements
- Financial data quality
- Forecasting
- DCF valuation
- Capital cost calculations
- Comparable-company analysis
- Peer valuation
- Scenario valuation
- Sensitivity analysis
- Market metrics
- Screening
- Investment scoring
- Investment decision logic
- Research reporting
- Valuation summaries
- Assumption validation

GitHub Actions is configured to automatically execute the test suite when changes are pushed or pull requests are opened.

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

## Analytical Framework

The platform contains modular components for:

- Financial statement normalization
- Fundamental ratio analysis
- Profitability analysis
- Capital efficiency analysis
- Financial strength analysis
- Market valuation metrics
- CAPM and WACC
- DCF valuation
- Terminal value analysis
- P/E valuation
- EV/EBITDA valuation
- Comparable-company analysis
- Peer valuation
- Bear/Base/Bull scenarios
- Revenue-growth sensitivity
- EBITDA-margin sensitivity
- WACC/terminal-growth sensitivity
- Fundamental screening
- Investment scoring
- Investment decision classification
- Research reporting
- Data quality validation

## Quality Controls

The project includes:

- Unit tests
- Input validation
- Financial data quality checks
- Reproducible assumptions
- Automated GitHub Actions testing
- Explicit separation between assumptions and observed data

## Project Structure

The repository is organized into:

- `data/` — research universe and financial data
- `figures/` — generated research visualizations
- `notebooks/` — research notebooks
- `src/` — analytical and valuation modules
- `tests/` — automated unit tests
- `.github/workflows/` — continuous integration

Key analytical modules include:

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

## Reproducibility

The project separates:

- Raw or retrieved financial data
- Processed financial data
- Analyst assumptions
- Forecast values
- Valuation calculations
- Research conclusions

This structure makes it possible to trace valuation outputs back to the underlying assumptions and financial inputs.

## Research Integrity

The project follows a strict distinction between:

- Historical observations
- Derived financial metrics
- Analyst assumptions
- Forecast values
- Valuation outputs
- Investment conclusions

Historical financial results should originate from financial data.

Forecast results should originate from explicit assumptions.

Valuation results should originate from reproducible model calculations.

Investment conclusions should be supported by the resulting evidence.

## Limitations

This project is intended for educational and research purposes.

Important limitations include:

- Public-data availability
- Differences in financial-statement classifications
- Data-provider limitations
- Forecast uncertainty
- WACC estimation uncertainty
- Terminal-value sensitivity
- Peer-selection bias
- Market-price volatility
- Model specification risk
- Assumption uncertainty

The platform does not represent investment advice.

## Portfolio Context

This project is part of a broader finance and quantitative-finance portfolio.

It demonstrates:

- Fundamental equity research
- Financial statement analysis
- Financial modelling
- DCF valuation
- Comparable-company valuation
- Quantitative screening
- Scenario analysis
- Sensitivity analysis
- Python-based financial analytics
- Data-quality controls
- Automated testing

## Intended Application

The analytical framework is relevant to:

- Equity research
- Investment analysis
- Asset management
- Hedge funds
- Private equity
- Investment banking
- Financial modelling
- Quantitative finance
- Financial data analytics

## Author

**Sahand Mostafaei**

BSc Electrical Engineering

Areas of interest:

- Quantitative Finance
- Investment Analysis
- Financial Risk Management
- Banking
- Financial Modelling
- Private Equity
- Hedge Funds
- Financial Data Analytics
