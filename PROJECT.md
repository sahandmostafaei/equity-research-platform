# Project Specification

## Equity Research & Fundamental Valuation Platform

### 1. Research Objective

The objective of this project is to develop a reproducible quantitative framework for fundamental equity research.

The system evaluates companies from four primary perspectives:

1. Financial quality
2. Operating performance
3. Valuation
4. Investment attractiveness

---

## 2. Research Framework

The project follows a buy-side equity research workflow:

Financial statements
→ fundamental metrics
→ business quality
→ valuation
→ peer comparison
→ scenarios
→ sensitivity analysis
→ investment conclusion

---

## 3. Fundamental Analysis

The analysis evaluates:

### Growth

- Revenue growth
- EBITDA growth
- EBIT growth
- EPS growth
- FCF growth

### Profitability

- Gross margin
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
- Liquidity

### Cash Flow

- Operating cash flow
- Capital expenditure
- Free cash flow
- FCF margin
- Cash conversion

---

## 4. Valuation

The project uses multiple valuation approaches.

### DCF

Enterprise value is estimated from projected free cash flow and terminal value.

The framework explicitly separates:

- Forecast period
- Terminal period
- Discounting
- Enterprise value
- Net debt adjustment
- Equity value
- Per-share value

### Relative Valuation

Peer multiples include:

- P/E
- EV/EBITDA
- EV/Sales
- Price/Sales
- FCF yield

---

## 5. Scenario Analysis

Three scenarios are used:

- Bear
- Base
- Bull

Each scenario can vary:

- Revenue growth
- EBITDA margin
- WACC
- Terminal growth

The objective is to determine whether an investment thesis remains attractive under different operating assumptions.

---

## 6. Sensitivity Analysis

The DCF framework evaluates valuation across multiple WACC and terminal-growth combinations.

This identifies:

- Base valuation
- Upside case
- Downside case
- Valuation sensitivity
- Margin of safety

---

## 7. Screening Framework

A fundamental screening model identifies companies meeting minimum quality requirements.

Example criteria:

- ROIC ≥ 15%
- Revenue growth ≥ 10%
- Net debt / EBITDA ≤ 2.0x
- FCF margin ≥ 8%

The thresholds are configurable.

---

## 8. Company Ranking

Companies can also be ranked using a weighted fundamental score.

The ranking can incorporate:

- ROIC
- Revenue growth
- FCF margin
- EBITDA margin
- Interest coverage

This creates a systematic method for prioritizing investment research.

---

## 9. Reproducibility

The project separates:

- Data acquisition
- Financial analysis
- Valuation
- Scenario modelling
- Screening
- Testing

This modular architecture allows individual components to be validated independently.

---

## 10. Limitations

Fundamental valuation is inherently sensitive to assumptions.

The largest sources of uncertainty include:

- Revenue growth
- Operating margins
- Capital expenditure
- Working capital
- WACC
- Terminal growth
- Peer selection
- Market conditions

Therefore, valuation should be interpreted as a range rather than a precise point estimate.

---

## 11. Intended Application

The framework is designed to demonstrate practical capabilities relevant to:

- Equity research
- Hedge fund research
- Private equity
- Investment banking
- Asset management
- Quantitative finance

The emphasis is on combining financial reasoning with reproducible quantitative analysis.
