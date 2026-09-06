import pandas as pd

from src.forecast_sensitivity import (
    margin_sensitivity,
    revenue_growth_sensitivity,
)


def test_growth_sensitivity():
    historical = pd.Series(
        [100.0, 110.0, 120.0]
    )

    result = revenue_growth_sensitivity(
        historical_revenue=historical,
        growth_rates=[0.05, 0.08, 0.10],
        ebitda_margin=0.25,
        fcf_conversion=0.50,
        wacc=0.09,
        terminal_growth=0.025,
        total_debt=100.0,
        cash=50.0,
        shares_outstanding=100.0,
    )

    assert len(result) == 3
    assert (
        result["per_share_value"].notna().all()
    )


def test_margin_sensitivity():
    historical = pd.Series(
        [100.0, 110.0, 120.0]
    )

    result = margin_sensitivity(
        historical_revenue=historical,
        growth_rate=0.08,
        ebitda_margins=[0.20, 0.25, 0.30],
        fcf_conversion=0.50,
        wacc=0.09,
        terminal_growth=0.025,
        total_debt=100.0,
        cash=50.0,
        shares_outstanding=100.0,
    )

    assert len(result) == 3
    assert (
        result["per_share_value"].notna().all()
    )
