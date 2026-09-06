# Research Results
## Equity Research & Fundamental Valuation Platform

## 1. Status

**Analytical framework:** Implemented

**Software architecture:** Implemented

**Unit-test framework:** Implemented

**Integrated research engine:** Implemented

**Centralized configuration:** Implemented

**Empirical market-data results:** Pending actual execution

No unexecuted model output is presented as an empirical finding.

## 2. Research Target

**Target:** Microsoft (MSFT)

## 3. Peer Universe

- Alphabet (GOOGL)
- Meta Platforms (META)
- Apple (AAPL)
- Amazon (AMZN)

## 4. Fundamental Analysis

The platform supports analysis of:

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

### Financial Strength

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage

### Cash Generation

- Operating cash flow
- Capital expenditure
- Free cash flow
- FCF margin
- FCF yield

## 5. Financial Statement Analysis

The platform standardizes:

- Income statement information
- Balance-sheet information
- Cash-flow information

The standardized analytical dataset includes:

- Revenue
- EBIT
- EBITDA
- Net income
- Operating cash flow
- Capital expenditure
- Free cash flow
- Debt
- Cash
- Equity
- NOPAT
- Invested capital

## 6. Market Valuation

Supported market metrics include:

- Market capitalization
- Enterprise value
- EPS
- P/E
- EV/Sales
- EV/EBITDA
- FCF yield

Actual values remain pending final data retrieval and execution.

## 7. Forecasting

The platform produces a configurable five-year operating forecast.

Forecast variables:

- Revenue
- EBITDA
- Free cash flow

## 8. Cost of Capital

The framework supports:

- Risk-free rate
- Beta
- Equity risk premium
- Cost of equity
- Cost of debt
- After-tax cost of debt
- Capital structure
- WACC

Actual company-specific WACC results remain pending empirical execution.

## 9. DCF Valuation

The DCF framework calculates:

- Present value of forecast FCF
- Terminal value
- Present value of terminal value
- Enterprise value
- Equity value
- Intrinsic value per share

The implementation validates:

**WACC > terminal growth**

## 10. Scenario Analysis

### Bear Case

| Assumption | Value |
|---|---:|
| Revenue Growth | 3.0% |
| EBITDA Margin | 18.0% |
| FCF Conversion | 50.0% |
| WACC | 11.0% |
| Terminal Growth | 2.0% |

### Base Case

| Assumption | Value |
|---|---:|
| Revenue Growth | 7.0% |
| EBITDA Margin | 22.0% |
| FCF Conversion | 50.0% |
| WACC | 9.0% |
| Terminal Growth | 2.5% |

### Bull Case

| Assumption | Value |
|---|---:|
| Revenue Growth | 12.0% |
| EBITDA Margin | 26.0% |
| FCF Conversion | 50.0% |
| WACC | 8.0% |
| Terminal Growth | 3.0% |

These assumptions are modelling inputs rather than empirical findings.

## 11. Relative Valuation

The platform supports:

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

Final peer valuation results remain pending actual execution.

## 12. Sensitivity Analysis

The platform supports:

- WACC / terminal-growth sensitivity
- Revenue-growth sensitivity
- EBITDA-margin sensitivity

The purpose is to identify valuation ranges and key valuation drivers.

## 13. Fundamental Screening

The screening framework evaluates:

- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA
- Interest coverage

Actual screening results remain pending execution.

## 14. Investment Scoring

The investment scoring framework incorporates:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The resulting score is normalized between zero and one.

## 15. Investment Decision

The investment decision framework combines:

- Fundamental score
- Valuation upside

Potential classifications include:

- Strong Buy Candidate
- Buy Candidate
- Watchlist
- Low Conviction

No final investment classification is claimed until the empirical pipeline is executed.

## 16. Investment Thesis

The final investment thesis is intended to contain:

### Thesis

Core investment rationale supported by fundamental evidence.

### Catalysts

Potential events or developments that could improve operating performance or valuation.

### Risks

Fundamental, valuation, balance-sheet, competitive, and macroeconomic risks.

### Valuation View

Comparison between intrinsic value estimates and market price.

### Conclusion

Evidence-based investment assessment.

The final thesis remains pending empirical execution.

## 17. Integrated Research Engine

The project now includes a high-level research engine.

The engine orchestrates:

1. Configuration loading
2. Financial-data retrieval
3. Financial statement normalization
4. Historical fundamental analysis
5. Market-metric calculation
6. Scenario construction
7. Scenario valuation
8. Consensus valuation
9. Investment scoring
10. Investment assessment

This provides a coherent end-to-end research architecture.

## 18. Centralized Configuration

Research assumptions are stored in:

`data/research_config.csv`

The configuration layer separates:

- Research universe
- Valuation assumptions
- Forecast assumptions
- Scenario assumptions

from the Python implementation.

## 19. Data Quality

The project includes:

- Required-column validation
- Missing-data reporting
- Duplicate detection
- Numeric conversion
- Positive-value validation
- Configuration validation
- Duplicate-parameter detection

## 20. Testing

Automated tests cover:

- Financial analysis
- Financial statements
- Financial data
- Data quality
- Configuration
- Forecasting
- DCF valuation
- Capital cost
- Comparable-company valuation
- Peer valuation
- Scenario valuation
- Sensitivity analysis
- Market metrics
- Screening
- Investment scoring
- Investment decision logic
- Research reporting
- Research engine orchestration

## 21. Analytical Architecture

The current analytical architecture is:

**Configuration**

↓

**Financial Data**

↓

**Financial Statement Normalization**

↓

**Fundamental Analysis**

↓

**Market Metrics**

↓

**Forecasting**

↓

**Cost of Capital**

↓

**DCF / Relative Valuation**

↓

**Scenario Analysis**

↓

**Sensitivity Analysis**

↓

**Investment Score**

↓

**Investment Decision**

## 22. Research Integrity

The repository explicitly distinguishes:

- Historical observations
- Derived metrics
- Analyst assumptions
- Forecasts
- Valuation outputs
- Investment conclusions

No fabricated empirical results are included.

## 23. Current Completion State

### Completed

- Modular financial analysis
- Financial statement processing
- Market metrics
- Forecasting
- CAPM/WACC framework
- DCF framework
- Comparable-company framework
- Peer valuation
- Scenario valuation
- Sensitivity analysis
- Fundamental screening
- Investment scoring
- Investment decision framework
- Research reporting
- Data-quality framework
- Centralized configuration
- Integrated research engine
- Unit-test framework
- GitHub Actions testing

### Remaining

The main remaining stage is empirical execution using actual financial and market data.

That stage should generate:

- Historical financial tables
- Current market metrics
- Peer valuation tables
- Forecast tables
- DCF valuation
- Scenario valuations
- Sensitivity tables
- Fundamental rankings
- Investment score
- Investment conclusion
- Research figures

## 24. Limitations

Important limitations include:

- Public-data availability
- Data-provider methodology
- Financial-statement classification
- Forecast uncertainty
- WACC uncertainty
- Terminal-value sensitivity
- Peer-selection bias
- Market-price volatility
- Model specification risk
- Assumption uncertainty

## 25. Final Research Standard

The completed research output should satisfy the following standard:

**Data → Calculation → Evidence → Valuation → Interpretation → Conclusion**

Every empirical claim should be traceable to data or a documented modelling assumption.

Every valuation output should be reproducible from the stated inputs.

Every investment conclusion should be supported by fundamental and valuation evidence.

## 26. Intended Academic Use

The project is suitable as a portfolio demonstration of:

- Corporate finance
- Equity valuation
- Financial modelling
- Quantitative finance
- Python
- Financial data analytics
- Investment research
- Research software engineering

## 27. Portfolio Role

This project complements the broader finance portfolio by adding company-level fundamental investment research to existing work in:

- Credit risk
- Portfolio optimization
- Banking analytics
- Financial data engineering
- Investment banking

Together, the projects demonstrate both quantitative and fundamental finance capabilities.

## 28. Author

**Sahand Mostafaei**

BSc Electrical Engineering
