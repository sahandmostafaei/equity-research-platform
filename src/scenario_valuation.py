from __future__ import annotations

import pandas as pd

from src.dcf_model import calculate_dcf
from src.forecasting import build_dcf_forecast
from src.scenarios import Scenario


def run_scenario_valuation(
    historical_revenue: pd.Series,
    scenario: Scenario,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    fcf_conversion: float = 0.50,
    years: int = 5,
) -> dict[str, float]:
    """
    Forecast operating performance and calculate
    scenario-specific DCF valuation.
    """
    forecast = build_dcf_forecast(
        historical_revenue=historical_revenue,
        growth_rate=scenario.revenue_growth,
        ebitda_margin=scenario.ebitda_margin,
        fcf_conversion=fcf_conversion,
        years=years,
    )

    dcf_result = calculate_dcf(
        free_cash_flows=forecast["forecast_fcf"],
        wacc=scenario.wacc,
        terminal_growth=scenario.terminal_growth,
        total_debt=total_debt,
        cash=cash,
        shares_outstanding=shares_outstanding,
    )

    return {
        "scenario": scenario.name,
        "enterprise_value": dcf_result.enterprise_value,
        "equity_value": dcf_result.equity_value,
        "per_share_value": dcf_result.per_share_value,
        "terminal_value": dcf_result.terminal_value,
    }


def run_all_scenarios(
    historical_revenue: pd.Series,
    scenarios: dict[str, Scenario],
    total_debt: float,
    cash: float,
    shares_outstanding: float,
    fcf_conversion: float = 0.50,
    years: int = 5,
) -> pd.DataFrame:
    """
    Run Bear, Base, and Bull valuations.
    """
    results = []

    for scenario in scenarios.values():
        results.append(
            run_scenario_valuation(
                historical_revenue=historical_revenue,
                scenario=scenario,
                total_debt=total_debt,
                cash=cash,
                shares_outstanding=shares_outstanding,
                fcf_conversion=fcf_conversion,
                years=years,
            )
        )

    return pd.DataFrame(results)
