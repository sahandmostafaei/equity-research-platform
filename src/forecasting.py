from __future__ import annotations

import pandas as pd


def forecast_revenue(
    historical_revenue: pd.Series,
    growth_rate: float,
    years: int = 5,
) -> pd.Series:
    """
    Forecast revenue using a constant growth assumption.
    """

    if historical_revenue.empty:
        raise ValueError(
            "Historical revenue cannot be empty."
        )

    if years <= 0:
        raise ValueError(
            "Forecast horizon must be positive."
        )

    starting_revenue = float(
        historical_revenue.dropna().iloc[-1]
    )

    if starting_revenue <= 0:
        raise ValueError(
            "Starting revenue must be positive."
        )

    values = []

    current = starting_revenue

    for _ in range(years):
        current *= 1 + growth_rate
        values.append(current)

    return pd.Series(
        values,
        index=range(
            1,
            years + 1,
        ),
        name="forecast_revenue",
    )


def forecast_ebitda(
    revenue_forecast: pd.Series,
    ebitda_margin: float,
) -> pd.Series:
    """
    Forecast EBITDA from projected revenue.
    """

    if not 0 < ebitda_margin < 1:
        raise ValueError(
            "EBITDA margin must be between 0 and 1."
        )

    return (
        revenue_forecast
        * ebitda_margin
    ).rename("forecast_ebitda")


def forecast_fcf(
    ebitda_forecast: pd.Series,
    fcf_conversion: float,
) -> pd.Series:
    """
    Forecast free cash flow from EBITDA.
    """

    if not 0 < fcf_conversion <= 1:
        raise ValueError(
            "FCF conversion must be between 0 and 1."
        )

    return (
        ebitda_forecast
        * fcf_conversion
    ).rename("forecast_fcf")


def build_dcf_forecast(
    historical_revenue: pd.Series,
    growth_rate: float,
    ebitda_margin: float,
    fcf_conversion: float,
    years: int = 5,
) -> pd.DataFrame:
    """
    Build a simple operating forecast for DCF analysis.
    """

    revenue = forecast_revenue(
        historical_revenue,
        growth_rate,
        years,
    )

    ebitda = forecast_ebitda(
        revenue,
        ebitda_margin,
    )

    fcf = forecast_fcf(
        ebitda,
        fcf_conversion,
    )

    return pd.concat(
        [
            revenue,
            ebitda,
            fcf,
        ],
        axis=1,
    )
