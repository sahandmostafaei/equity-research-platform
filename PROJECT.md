# Project Specification

# Equity Research & Fundamental Valuation Platform

## 1. Objective

The objective of this project is to develop a modular equity research and fundamental valuation platform using Python.

The platform transforms financial statements and market information into:

- Fundamental financial analysis
- Operating forecasts
- Cost-of-capital estimates
- DCF valuation
- Comparable-company valuation
- Scenario analysis
- Sensitivity analysis
- Fundamental screening
- Investment scoring
- Investment decision support

The project is designed to resemble a simplified institutional equity research workflow while maintaining reproducibility and transparent assumptions.

---

## 2. Research Workflow

The complete workflow is:

1. Define research universe
2. Acquire financial and market data
3. Normalize financial statement data
4. Validate data quality
5. Calculate historical fundamentals
6. Calculate market valuation metrics
7. Construct operating forecasts
8. Estimate cost of capital
9. Perform DCF valuation
10. Perform comparable-company valuation
11. Run scenario analysis
12. Run sensitivity analysis
13. Screen and rank companies
14. Generate investment score
15. Generate investment decision
16. Produce research outputs

---

## 3. Research Universe

Initial target:

**Microsoft (MSFT)**

Initial peers:

- Alphabet (GOOGL)
- Meta Platforms (META)
- Apple (AAPL)
- Amazon (AMZN)

The universe is stored in:

`data/research_universe.csv`

The architecture allows additional companies to be added without changing the core analytical modules.

---

## 4. Financial Analysis

The platform evaluates historical company fundamentals.

### 4.1 Growth

Metrics include:

- Revenue growth
- EBITDA growth
- EBIT growth
- Net income growth
- Free cash flow growth

### 4.2 Profitability

Metrics include:

- EBITDA margin
- EBIT margin
- Net margin
- ROA
- ROE
- ROIC

### 4.3 Capital Efficiency

Metrics include:

- Invested capital
- NOPAT
- ROIC
- Free cash flow
- FCF margin

### 4.4 Financial Strength

Metrics include:

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage

The purpose is to evaluate the company's ability to generate returns while maintaining financial resilience.

---

## 5. Financial Statement Processing

The platform processes:

### Income Statement

- Revenue
- EBIT
- EBITDA
- Net income
- Depreciation and amortization

### Balance Sheet

- Total debt
- Cash
- Total assets
- Shareholders' equity
- Invested capital

### Cash Flow Statement

- Operating cash flow
- Capital expenditure
- Free cash flow

Financial-statement line items are mapped into standardized analytical variables.

This allows differences in source naming conventions to be handled through aliases.

---

## 6. Data Quality

The platform includes validation for:

- Missing required columns
- Missing observations
- Duplicate rows
- Numeric conversion
- Positive-value requirements

Data-quality validation occurs before analytical outputs are interpreted.

The objective is to prevent basic data problems from propagating into financial analysis and valuation.

---

## 7. Market Data

Market analysis includes:

- Current share price
- Market capitalization
- Enterprise value
- Shares outstanding
- EPS
- P/E
- EV/Sales
- EV/EBITDA
- FCF yield

Enterprise value is calculated using:

Market Capitalization + Debt - Cash

These metrics connect operating fundamentals to market valuation.

---

## 8. Forecasting

The initial forecast horizon is five years.

The operating forecast uses assumptions for:

- Revenue growth
- EBITDA margin
- FCF conversion

The forecast produces:

- Revenue
- EBITDA
- Free cash flow

The forecast assumptions are explicitly separated from historical financial observations.

---

## 9. Cost of Capital

The capital-cost module supports:

- Risk-free rate
- Equity beta
- Equity risk premium
- Cost of equity
- Pre-tax cost of debt
- Tax rate
- After-tax cost of debt
- Market value of equity
- Market value of debt
- WACC

The cost of equity follows the CAPM framework:

Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

WACC combines the weighted cost of equity and after-tax debt.

The model requires WACC to exceed terminal growth when calculating terminal value.

---

## 10. DCF Valuation

The DCF framework calculates:

1. Forecast free cash flow
2. Present value of forecast free cash flow
3. Terminal value
4. Present value of terminal value
5. Enterprise value
6. Equity value
7. Intrinsic value per share

The terminal value uses the perpetual-growth approach.

The valuation framework explicitly separates:

- Forecast assumptions
- Discount rate
- Terminal growth
- Capital structure
- Equity value calculation

---

## 11. Relative Valuation

Comparable-company analysis uses:

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

Peer median multiples can be applied to target-company financial metrics to derive implied valuation estimates.

---

## 12. Peer Analysis

The peer framework compares the target company against selected comparable companies.

Comparison dimensions include:

- Growth
- Profitability
- Capital efficiency
- Leverage
- Cash generation
- Market valuation

The peer-selection process should be interpreted carefully because companies within the same broad sector may still have materially different:

- Business models
- Growth profiles
- Capital intensity
- Margin structures
- Risk profiles
- Capital structures

---

## 13. Scenario Analysis

Three scenarios are currently defined.

### Bear

- Revenue growth: 3.0%
- EBITDA margin: 18.0%
- WACC: 11.0%
- Terminal growth: 2.0%

### Base

- Revenue growth: 7.0%
- EBITDA margin: 22.0%
- WACC: 9.0%
- Terminal growth: 2.5%

### Bull

- Revenue growth: 12.0%
- EBITDA margin: 26.0%
- WACC: 8.0%
- Terminal growth: 3.0%

These are model assumptions.

They are not historical company observations.

Each scenario produces an independent valuation.

---

## 14. Sensitivity Analysis

The platform supports sensitivity analysis across:

### DCF Variables

- WACC
- Terminal growth

### Operating Variables

- Revenue growth
- EBITDA margin

The purpose is to identify how sensitive intrinsic value is to major assumptions.

Sensitivity analysis should be interpreted as a valuation-range analysis rather than as a prediction of a single precise share price.

---

## 15. Fundamental Screening

Companies can be screened using:

- Minimum ROIC
- Minimum revenue growth
- Maximum net debt / EBITDA
- Minimum FCF margin

The framework can identify companies exhibiting combinations of:

- Strong profitability
- Attractive growth
- Strong cash generation
- Moderate leverage

---

## 16. Investment Scoring

The investment scoring framework considers:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The current weighted structure gives greater importance to valuation and business quality while incorporating growth, cash generation, and leverage.

Scores are normalized to a 0–1 scale.

Classification categories include:

- High Conviction
- Attractive
- Neutral
- Cautious
- Low Conviction

The score is a structured analytical aid and should not replace qualitative research.

---

## 17. Investment Decision

The investment decision framework combines:

- Fundamental score
- Valuation upside

Possible classifications include:

- Strong Buy Candidate
- Buy Candidate
- Watchlist
- Low Conviction

The decision output should always be evaluated together with:

- Underlying financial metrics
- Valuation assumptions
- Peer positioning
- Scenario analysis
- Key risks
- Catalysts

---

## 18. Investment Thesis

The final research output should contain:

### Thesis

The central fundamental argument.

### Catalysts

Potential developments that could cause market expectations to change.

### Risks

Potential operating, financial, competitive, valuation, and market risks.

### Valuation

Comparison between:

- Current market price
- DCF value
- Relative valuation
- Scenario valuations
- Peer-implied values

### Conclusion

An evidence-based investment assessment.

---

## 19. Research Reporting

The reporting framework supports:

- Company snapshots
- Peer comparison tables
- Valuation summaries
- Exportable research tables
- Revenue/EBITDA visualizations
- DCF sensitivity visualizations

The final research output should make the analytical chain traceable from source data to conclusion.

---

## 20. Reproducibility

The project separates:

1. Retrieved financial data
2. Processed financial data
3. Historical metrics
4. Analyst assumptions
5. Forecast values
6. Valuation calculations
7. Investment conclusions

This separation is important because an analyst assumption must not be presented as an observed historical result.

---

## 21. Analytical Architecture

The platform follows the following modular architecture:

**Data Acquisition → Financial Statements → Data Quality → Fundamentals → Market Metrics → Forecasting → WACC → DCF → Peer Valuation → Scenarios → Sensitivity → Screening → Investment Decision → Reporting**

Each stage is implemented through dedicated Python modules.

This architecture improves:

- Transparency
- Maintainability
- Testability
- Reproducibility
- Extensibility

---

## 22. Testing

The project uses automated unit testing for the principal analytical modules.

Testing covers:

- Financial analysis
- Financial statements
- Data quality
- Forecasting
- DCF
- Capital cost
- Comparable valuation
- Peer valuation
- Scenario valuation
- Sensitivity analysis
- Market metrics
- Screening
- Investment scoring
- Investment decision
- Research reporting
- Valuation summaries
- Assumption validation

GitHub Actions is configured to execute the test suite automatically.

---

## 23. Software Structure

### Data Layer

Responsible for:

- Market data
- Financial statements
- Research universe
- Data normalization
- Data validation

### Analysis Layer

Responsible for:

- Fundamental metrics
- Financial ratios
- Market metrics
- Screening
- Ranking

### Forecasting Layer

Responsible for:

- Revenue forecasts
- EBITDA forecasts
- FCF forecasts
- Scenario assumptions

### Valuation Layer

Responsible for:

- WACC
- DCF
- Terminal value
- Relative valuation
- Peer valuation
- Sensitivity analysis

### Decision Layer

Responsible for:

- Investment score
- Valuation classification
- Investment view
- Investment thesis framework

### Reporting Layer

Responsible for:

- Research tables
- Company snapshots
- Peer comparisons
- Valuation summaries
- Visual outputs

---

## 24. Limitations

Important limitations include:

- Public-data availability
- Financial statement classification differences
- Data-provider limitations
- Forecast uncertainty
- WACC estimation uncertainty
- Terminal-value sensitivity
- Peer-selection bias
- Market-price volatility
- Model specification risk
- Assumption uncertainty

The project is intended for educational and research purposes and does not constitute investment advice.

---

## 25. Intended Application

The platform is designed to demonstrate skills relevant to:

- Equity research
- Investment analysis
- Asset management
- Hedge funds
- Private equity
- Investment banking
- Financial modelling
- Quantitative finance
- Financial data analytics

The project emphasizes the intersection of financial analysis, valuation, quantitative methods, and software-based research workflows.
