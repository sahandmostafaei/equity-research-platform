from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.valuation import (
    calculate_equity_value,
    calculate_per_share_value,
    calculate_terminal_value,
)


@dataclass
class DCFResult:
    enterprise_value: float
    terminal_value: float
    present_value_of_forecast: float
    present_value_of_terminal_value: float
    equity_value: float
    per_share_value: float


def calculate_dcf(
    free_cash_flows: pd.Series,
    wacc: float,
    terminal_growth: float,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
) -> DCFResult:
    """
    Calculate a complete discounted cash flow valuation.
    """
    if free_cash_flows.empty:
        raise ValueError(
            "Free cash flow forecast cannot be empty."
        )

    if wacc <= terminal_growth:
        raise ValueError(
            "WACC must be greater than terminal growth."
        )

    if shares_outstanding <= 0:
        raise ValueError(
            "Shares outstanding must be positive."
        )

    forecast_pv = 0.0

    for year, fcf in enumerate(
        free_cash_flows,
        start=1,
    ):
        forecast_pv += (
            float(fcf)
            / ((1 + wacc) ** year)
        )

    final_fcf = float(free_cash_flows.iloc[-1])

    terminal_value = calculate_terminal_value(
        final_fcf=final_fcf,
        wacc=wacc,
        terminal_growth=terminal_growth,
    )

    terminal_pv = terminal_value / (
        (1 + wacc) ** len(free_cash_flows)
    )

    enterprise_value = (
        forecast_pv + terminal_pv
    )

    equity_value = calculate_equity_value(
        enterprise_value=enterprise_value,
        total_debt=total_debt,
        cash=cash,
    )

    per_share_value = calculate_per_share_value(
        equity_value=equity_value,
        shares_outstanding=shares_outstanding,
    )

    return DCFResult(
        enterprise_value=float(enterprise_value),
        terminal_value=float(terminal_value),
        present_value_of_forecast=float(forecast_pv),
        present_value_of_terminal_value=float(
            terminal_pv
        ),
        equity_value=float(equity_value),
        per_share_value=float(per_share_value),
    )
