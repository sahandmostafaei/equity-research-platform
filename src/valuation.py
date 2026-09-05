from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_dcf_value(
    free_cash_flows: list[float],
    wacc: float,
    terminal_growth: float,
) -> float:
    """
    Calculate enterprise value using a standard DCF model.
    """

    if not free_cash_flows:
        raise ValueError("At least one forecast FCF is required.")

    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth.")

    if wacc <= -1:
        raise ValueError("WACC must be greater than -100%.")

    forecast_pv = sum(
        fcf / ((1 + wacc) ** year)
        for year, fcf in enumerate(free_cash_flows, start=1)
    )

    terminal_fcf = free_cash_flows[-1] * (1 + terminal_growth)

    terminal_value = terminal_fcf / (wacc - terminal_growth)

    terminal_pv = terminal_value / (
        (1 + wacc) ** len(free_cash_flows)
    )

    return float(forecast_pv + terminal_pv)


def calculate_terminal_value(
    final_fcf: float,
    wacc: float,
    terminal_growth: float,
) -> float:
    """
    Calculate terminal value using the Gordon Growth Model.
    """

    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth.")

    return (
        final_fcf * (1 + terminal_growth)
    ) / (wacc - terminal_growth)


def calculate_equity_value(
    enterprise_value: float,
    total_debt: float,
    cash: float,
) -> float:
    """
    Convert enterprise value into equity value.
    """

    return enterprise_value - total_debt + cash


def calculate_per_share_value(
    equity_value: float,
    shares_outstanding: float,
) -> float:
    """
    Calculate intrinsic value per share.
    """

    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be positive.")

    return equity_value / shares_outstanding


def calculate_upside(
    intrinsic_value: float,
    market_price: float,
) -> float:
    """
    Calculate implied upside/downside relative to market price.
    """

    if market_price <= 0:
        raise ValueError("Market price must be positive.")

    return intrinsic_value / market_price - 1


def calculate_pe_value(
    eps: float,
    peer_pe: float,
) -> float:
    """
    Estimate value per share using a P/E multiple.
    """

    return eps * peer_pe


def calculate_ev_ebitda_value(
    ebitda: float,
    peer_ev_ebitda: float,
    net_debt: float,
    shares_outstanding: float,
) -> float:
    """
    Estimate equity value per share using EV/EBITDA.
    """

    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be positive.")

    enterprise_value = ebitda * peer_ev_ebitda

    equity_value = enterprise_value - net_debt

    return equity_value / shares_outstanding


def valuation_sensitivity(
    free_cash_flows: list[float],
    wacc_values: list[float],
    terminal_growth_values: list[float],
) -> pd.DataFrame:
    """
    Produce a DCF enterprise-value sensitivity table.
    """

    results = []

    for wacc in wacc_values:
        row = {}

        for growth in terminal_growth_values:
            try:
                row[growth] = calculate_dcf_value(
                    free_cash_flows,
                    wacc,
                    growth,
                )
            except ValueError:
                row[growth] = np.nan

        results.append(pd.Series(row, name=wacc))

    table = pd.DataFrame(results)

    table.index.name = "WACC"

    return table


def calculate_margin_of_safety(
    intrinsic_value: float,
    market_price: float,
) -> float:
    """
    Calculate margin of safety.

    Margin of safety represents the discount between
    estimated intrinsic value and the current market price.
    """

    if intrinsic_value <= 0:
        raise ValueError("Intrinsic value must be positive.")

    if market_price <= 0:
        raise ValueError("Market price must be positive.")

    return 1 - (market_price / intrinsic_value)
