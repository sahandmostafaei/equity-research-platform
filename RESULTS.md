# Research Results

## Status

The analytical framework is implemented and tested.

Final empirical valuation results should be generated only after the
research pipeline retrieves the selected company's financial statements,
market data, peer data, and model assumptions.

No valuation figures are fabricated in this repository.

## Research Target

**Target Company:** Microsoft (MSFT)

## Initial Peer Universe

- Alphabet (GOOGL)
- Meta Platforms (META)
- Apple (AAPL)
- Amazon (AMZN)

## Fundamental Analysis

The platform evaluates:

- Revenue growth
- EBITDA growth
- EBITDA margin
- EBIT margin
- Net margin
- ROA
- ROE
- ROIC
- Free cash flow
- FCF margin
- Net debt
- Net debt / EBITDA
- Interest coverage
- Financial strength

Final values will be generated from retrieved financial statements.

## Forecasting

The base forecasting framework uses:

- Revenue growth
- EBITDA margin
- FCF conversion
- Five-year forecast horizon

The scenario framework contains:

| Scenario | Revenue Growth | EBITDA Margin | WACC | Terminal Growth |
|---|---:|---:|---:|---:|
| Bear | 3.0% | 18.0% | 11.0% | 2.0% |
| Base | 7.0% | 22.0% | 9.0% | 2.5% |
| Bull | 12.0% | 26.0% | 8.0% | 3.0% |

These are model assumptions, not observed company results.

## DCF Valuation

The DCF framework produces:

- Present value of forecast free cash flow
- Terminal value
- Present value of terminal value
- Enterprise value
- Equity value
- Intrinsic value per share

## Relative Valuation

The platform evaluates:

- P/E
- EV/EBITDA
- EV/Sales
- Price/Sales
- FCF yield

Peer median multiples are used as reference valuation benchmarks.

## Valuation Comparison

The final research output will compare:

1. DCF valuation
2. P/E-based valuation
3. EV/EBITDA valuation
4. Peer-based valuation
5. Current market price
6. Consensus implied value
7. Upside/downside
8. Margin of safety

## Sensitivity Analysis

DCF valuation will be evaluated across combinations of:

- WACC
- Terminal growth

This is intended to identify the valuation range rather than rely on a
single point estimate.

## Investment Screening

The screening framework evaluates companies using:

- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA
- Interest coverage

Companies can then be ranked using a weighted fundamental score.

## Investment Thesis

The final research output will contain:

### Thesis

The central fundamental investment argument.

### Catalysts

Potential events or developments that could change market expectations.

### Risks

Key operating, financial, valuation, competitive, and market risks.

### Valuation

Comparison of intrinsic value with the current market price.

### Conclusion

A final evidence-based investment assessment.

## Testing

The project includes automated tests covering:

- Financial analysis
- Financial statement processing
- Forecasting
- DCF valuation
- Relative valuation
- Peer analysis
- Scenario analysis
- Investment scoring
- Capital cost calculations
- Screening

GitHub Actions is configured to execute the test suite automatically.

## Data Integrity

The project deliberately separates:

- Model assumptions
- Retrieved financial data
- Derived financial metrics
- Valuation outputs
- Investment conclusions

Observed financial results should not be confused with analyst assumptions.

## Limitations

The platform is intended for educational and research purposes.

Important limitations include:

- Public-data availability
- Financial statement line-item differences
- Model assumptions
- WACC estimation uncertainty
- Terminal-value sensitivity
- Peer-selection bias
- Market-price volatility
- Forecast uncertainty

## Final Research Standard

The completed research should report actual calculated results,
supporting tables, sensitivity analysis, valuation comparisons, and an
evidence-based investment thesis.

No unsupported investment conclusions should be presented as empirical
findings.
