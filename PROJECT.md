# Project Specification

## Equity Research & Fundamental Valuation Platform

## 1. Objective

The objective is to develop a reproducible equity research framework combining financial statement analysis, fundamental screening, financial forecasting, valuation, peer analysis, scenario analysis, and investment-thesis construction.

The framework is designed around a practical buy-side research workflow.

---

## 2. Research Workflow

The analytical process is:

Financial Data
→ Financial Statements
→ Fundamental Metrics
→ Historical Performance
→ Operating Forecast
→ DCF Valuation
→ Comparable Valuation
→ Scenario Analysis
→ Sensitivity Analysis
→ Investment Score
→ Investment Thesis

---

## 3. Financial Analysis

The framework evaluates:

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

### Capital Efficiency

- Invested capital
- ROIC
- Cash conversion
- FCF margin

### Financial Strength

- Total debt
- Cash
- Net debt
- Net debt / EBITDA
- Interest coverage
- Liquidity

---

## 4. Forecasting

The operating forecast projects:

- Revenue
- EBITDA
- Free cash flow

The forecast is driven by explicit assumptions rather than opaque model outputs.

Key assumptions include:

- Revenue growth
- EBITDA margin
- FCF conversion
- Forecast horizon

---

## 5. DCF Valuation

The DCF framework consists of:

1. Operating forecast
2. Free cash flow forecast
3. Explicit-period discounting
4. Terminal value
5. Enterprise value
6. Net debt adjustment
7. Equity value
8. Per-share value

---

## 6. Relative Valuation

The framework evaluates:

- P/E
- EV/EBITDA
- EV/Sales
- Price/Sales
- FCF yield

Peer analysis uses descriptive statistics including:

- Mean
- Median
- Minimum
- Maximum
- Standard deviation

---

## 7. Scenario Analysis

The framework uses three scenarios:

### Bear

Conservative growth and profitability assumptions with a higher discount rate.

### Base

Central operating and valuation assumptions.

### Bull

Higher growth and profitability assumptions with a lower discount rate.

---

## 8. Sensitivity Analysis

DCF valuation is evaluated across:

- WACC
- Terminal growth

The purpose is to identify the valuation range and assess the robustness of the investment thesis.

---

## 9. Fundamental Screening

Companies can be screened according to:

- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA
- Interest coverage

Thresholds are configurable.

---

## 10. Investment Scoring

The platform produces a research-prioritization score using:

- Valuation attractiveness
- ROIC
- Revenue growth
- FCF margin
- Balance-sheet leverage

The score is not intended to function as a standalone trading signal.

---

## 11. Investment Thesis

The final research output is designed to organize:

### Thesis

Why the company may be attractive.

### Catalysts

Events or developments that could change market expectations.

### Risks

Factors that could impair the investment thesis.

### Valuation

Comparison between intrinsic value and market price.

### Conclusion

Overall assessment based on fundamental evidence.

---

## 12. Reproducibility

The system separates:

- Data acquisition
- Data processing
- Financial analysis
- Forecasting
- Valuation
- Comparable analysis
- Screening
- Investment scoring
- Reporting

Automated tests validate core calculations.

---

## 13. Limitations

The framework depends on:

- Data quality
- Accounting classifications
- Forecast assumptions
- Peer selection
- Discount rates
- Terminal growth assumptions
- Market conditions

Valuation should therefore be interpreted as a range rather than a precise estimate.

---

## 14. Intended Application

The project is intended to demonstrate skills relevant to:

- Private equity
- Hedge funds
- Equity research
- Investment banking
- Asset management
- Fundamental investing
- Financial modelling

The primary emphasis is fundamental investment analysis combined with reproducible quantitative methods.
