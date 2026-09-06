from __future__ import annotations

import pandas as pd

from src.dcf_model import calculate_dcf
from src.forecasting import build_dcf_forecast


def revenue_growth_sensitivity(
    historical_revenue: pd.Series,
    growth_rates: list[float],
    ebitda_margin: float,
    fcf_conversion: float,
    wacc: float,
    terminal_growth: float,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    years: int = 5,
) -> pd.DataFrame:
    results = []

    for growth_rate in growth_rates:
        forecast = build_dcf_forecast(
            historical_revenue=historical_revenue,
            growth_rate=growth_rate,
            ebitda_margin=ebitda_margin,
            fcf_conversion=fcf_conversion,
            years=years,
        )

        valuation = calculate_dcf(
            free_cash_flows=forecast["forecast_fcf"],
            wacc=wacc,
            terminal_growth=terminal_growth,
            total_debt=total_debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
        )

        results.append(
            {
                "revenue_growth": growth_rate,
                "per_share_value": (
                    valuation.per_share_value
                ),
            }
        )

    return pd.DataFrame(results)


def margin_sensitivity(
    historical_revenue: pd.Series,
    growth_rate: float,
    ebitda_margins: list[float],
    fcf_conversion: float,
    wacc: float,
    terminal_growth: float,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    years: int = 5,
) -> pd.DataFrame:
    results = []

    for margin in ebitda_margins:
        forecast = build_dcf_forecast(
            historical_revenue=historical_revenue,
            growth_rate=growth_rate,
            ebitda_margin=margin,
            fcf_conversion=fcf_conversion,
            years=years,
        )

        valuation = calculate_dcf(
            free_cash_flows=forecast["forecast_fcf"],
            wacc=wacc,
            terminal_growth=terminal_growth,
            total_debt=total_debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
        )

        results.append(
            {
                "ebitda_margin": margin,
                "per_share_value": (
                    valuation.per_share_value
                ),
            }
        )

    return pd.DataFrame(results)
