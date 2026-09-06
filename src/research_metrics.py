from __future__ import annotations

import pandas as pd


def calculate_eps(
    net_income: float,
    shares_outstanding: float,
) -> float:
    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be positive.")
    return net_income / shares_outstanding


def calculate_fcf_yield(
    free_cash_flow: float,
    market_cap: float,
) -> float:
    if market_cap <= 0:
        raise ValueError("Market capitalization must be positive.")
    return free_cash_flow / market_cap


def calculate_enterprise_value(
    market_cap: float,
    total_debt: float,
    cash: float,
) -> float:
    return market_cap + total_debt - cash


def calculate_ev_to_sales(
    enterprise_value: float,
    revenue: float,
) -> float:
    if revenue <= 0:
        raise ValueError("Revenue must be positive.")
    return enterprise_value / revenue


def calculate_ev_to_ebitda(
    enterprise_value: float,
    ebitda: float,
) -> float:
    if ebitda <= 0:
        raise ValueError("EBITDA must be positive.")
    return enterprise_value / ebitda


def build_market_metrics(
    market_cap: float,
    total_debt: float,
    cash: float,
    revenue: float,
    ebitda: float,
    net_income: float,
    free_cash_flow: float,
    shares_outstanding: float,
) -> pd.Series:
    enterprise_value = calculate_enterprise_value(
        market_cap,
        total_debt,
        cash,
    )

    return pd.Series(
        {
            "market_cap": market_cap,
            "enterprise_value": enterprise_value,
            "eps": calculate_eps(
                net_income,
                shares_outstanding,
            ),
            "ev_sales": calculate_ev_to_sales(
                enterprise_value,
                revenue,
            ),
            "ev_ebitda": calculate_ev_to_ebitda(
                enterprise_value,
                ebitda,
            ),
            "fcf_yield": calculate_fcf_yield(
                free_cash_flow,
                market_cap,
            ),
        }
    )
