# Project Specification

## Equity Research & Fundamental Valuation Platform

## 1. Objective

The objective of this project is to build a modular equity-research framework capable of transforming financial and market data into a structured investment-analysis workflow.

The system integrates:

1. Financial statement processing
2. Fundamental analysis
3. Market analysis
4. Forecasting
5. Cost-of-capital estimation
6. DCF valuation
7. Comparable-company valuation
8. Scenario analysis
9. Investment scoring
10. Research output generation

The project is designed to demonstrate the ability to combine financial theory, quantitative methods, programming, and financial data engineering.

---

## 2. Research Question

The central analytical question is:

How can historical financial performance, market information, peer valuation, and scenario-based discounted cash-flow analysis be combined into a structured framework for evaluating the intrinsic value and investment characteristics of a publicly traded company?

---

## 3. Research Universe

The default universe contains one target company and four peers.

Target:

Microsoft — MSFT

Peers:

Alphabet — GOOGL
Meta Platforms — META
Apple — AAPL
Amazon — AMZN

The universe is configurable and can be changed without modifying the core research engine.

---

## 4. Financial Statement Framework

The system retrieves:

### Income Statement

- Revenue
- EBIT
- Net income
- Depreciation and amortization

### Balance Sheet

- Total debt
- Cash
- Total assets
- Shareholders' equity

### Cash Flow Statement

- Operating cash flow
- Capital expenditure

These raw accounting line items are normalized into a common research schema.

---

## 5. Fundamental Analysis

The platform calculates:

### Growth

Revenue growth.

### Profitability

EBITDA margin
EBIT margin
Net margin
FCF margin

### Capital Efficiency

ROIC
ROA
ROE

### Leverage

Net debt
Net debt / EBITDA

### Cash Generation

Free cash flow

Free cash flow is standardized as:

FCF = Operating Cash Flow - |Capital Expenditure|

This avoids sign-convention inconsistencies across data providers.

---

## 6. Market Analysis

Market information includes:

- Current share price
- Market capitalization
- Shares outstanding
- Beta
- Debt
- Enterprise value

Enterprise value is constructed consistently from equity value, debt, and cash.

---

## 7. Cost of Capital

The framework estimates cost of equity using CAPM:

Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

After-tax cost of debt is:

After-Tax Cost of Debt = Pre-Tax Cost of Debt × (1 - Tax Rate)

WACC is then constructed using market-value capital weights.

The model's scenario assumptions remain configurable independently from the estimated WACC.

---

## 8. DCF Valuation

The DCF framework forecasts free cash flow and discounts forecast cash flows using WACC.

Terminal value is calculated using the Gordon Growth approach:

Terminal Value = FCF_(n+1) / (WACC - g)

Enterprise value equals:

Present Value of Forecast FCF + Present Value of Terminal Value

Equity value is:

Enterprise Value - Debt + Cash

Per-share value is:

Equity Value / Shares Outstanding

---

## 9. Comparable Company Valuation

The platform calculates:

- P/E
- EV / Sales
- EV / EBITDA
- Price / Sales
- FCF yield

Peer median multiples are used as the central relative-valuation reference.

Equity-value multiples are applied to equity metrics.

Enterprise-value multiples are applied to enterprise metrics and subsequently bridged to equity value.

This distinction prevents a common valuation modelling error in which EV-based multiples are incorrectly applied directly to equity-value metrics.

---

## 10. Scenario Analysis

Three scenarios are supported:

### Bear

Lower growth
Lower margin
Higher WACC
Lower terminal growth

### Base

Central assumptions.

### Bull

Higher growth
Higher margin
Lower WACC
Higher terminal growth

All assumptions are externally configurable.

---

## 11. Investment Assessment

The investment assessment combines:

- Valuation upside
- ROIC
- Revenue growth
- FCF margin
- Net debt / EBITDA

The resulting score is classified into an investment category.

The score is a structured analytical framework and not a substitute for independent investment judgement.

---

## 12. Data Quality

The architecture includes validation of:

- Missing financial statements
- Missing required metrics
- Invalid denominators
- Invalid valuation assumptions
- Invalid share counts
- Invalid market prices
- Invalid WACC / terminal-growth relationships
- Empty datasets

The objective is to fail explicitly rather than silently generate misleading valuation results.

---

## 13. Reproducibility

The project centralizes research assumptions in:

`data/research_config.csv`

The research engine reads configuration values rather than embedding the assumptions directly into individual analysis modules.

The complete workflow can therefore be reconstructed from:

- Configuration
- Source code
- Data retrieval logic
- Research engine
- Output layer

---

## 14. Output Architecture

The research engine returns a structured result containing:

- Target historical financials
- Target market data
- Target market metrics
- Scenario valuations
- Peer financials
- Peer market data
- Peer market metrics
- Peer multiples
- Peer median multiples
- Target-peer comparison
- Peer implied valuations
- Consolidated valuation summary
- Investment assessment
- Estimated WACC

The output layer converts these objects into machine-readable CSV research files.

---

## 15. Software Engineering Design

The project uses a modular architecture.

Responsibilities are separated across:

- Data ingestion
- Financial statement normalization
- Financial analysis
- Market analysis
- Forecasting
- Valuation
- Peer analysis
- Scenario analysis
- Research orchestration
- Output generation
- Testing

This avoids placing the entire analysis inside one notebook or script.

---

## 16. Testing

The project includes unit tests for key financial and software components.

Testing focuses on:

- Financial formulas
- Data normalization
- Error handling
- Peer valuation
- Output generation
- Research configuration

The project uses pytest.

---

## 17. Academic Value

The project demonstrates applied understanding of:

- Corporate finance
- Financial statement analysis
- Equity valuation
- Capital markets
- Portfolio and investment analysis
- Quantitative finance
- Financial data processing
- Python-based modelling
- Research reproducibility

It is designed to complement a separate empirical portfolio-optimization research paper rather than duplicate it.

---

## 18. Intended Professional Applications

The framework is relevant to:

- Equity Research
- Investment Banking
- Private Equity
- Hedge Funds
- Asset Management
- Quantitative Finance
- Financial Risk
- Investment Analysis
- Financial Data Analytics

---

## 19. Limitations

The model is not intended to represent a full institutional investment platform.

Limitations include:

- External data-source limitations
- Accounting-definition differences
- Simplified forecasts
- Peer-selection risk
- DCF parameter sensitivity
- Market-data timing
- Potential missing observations
- Simplified investment scoring

Results should therefore be interpreted as model-based estimates.

---

## 20. Final Deliverable

The completed project provides an end-to-end equity-research workflow:

Data
→ Financial Statements
→ Fundamental Analysis
→ Market Analysis
→ Forecasting
→ DCF
→ Comparable Companies
→ Scenario Analysis
→ Investment Assessment
→ Research Outputs

The final implementation is intended to be suitable as a technical finance portfolio project and as supporting evidence of quantitative and financial modelling ability in graduate-school applications.
