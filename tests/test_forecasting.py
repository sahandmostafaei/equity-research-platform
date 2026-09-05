import pandas as pd
import pytest

from src.forecasting import (
    build_dcf_forecast,
    forecast_ebitda,
    forecast_revenue,
)


def test_forecast_revenue():
    historical = pd.Series(
        [100.0, 110.0, 120.0]
    )

    result = forecast_revenue(
        historical,
        growth_rate=0.10,
        years=3,
    )

    assert len(result) == 3
    assert result.iloc[0] == pytest.approx(132.0)


def test_forecast_ebitda():
    revenue = pd.Series(
        [100.0, 110.0]
    )

    result = forecast_ebitda(
        revenue,
        ebitda_margin=0.20,
    )

    assert result.iloc[0] == 20.0
    assert result.iloc[1] == 22.0


def test_dcf_forecast():
    historical = pd.Series(
        [100.0, 110.0, 120.0]
    )

    result = build_dcf_forecast(
        historical_revenue=historical,
        growth_rate=0.08,
        ebitda_margin=0.25,
        fcf_conversion=0.50,
        years=5,
    )

    assert list(result.columns) == [
        "forecast_revenue",
        "forecast_ebitda",
        "forecast_fcf",
    ]

    assert len(result) == 5


def test_invalid_margin():
    revenue = pd.Series(
        [100.0]
    )

    with pytest.raises(ValueError):
        forecast_ebitda(
            revenue,
            ebitda_margin=1.5,
        )
