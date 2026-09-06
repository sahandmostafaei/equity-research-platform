from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_growth(
    series: pd.Series,
) -> pd.Series:
    """
    Calculate period-over-period growth.
    """
    return series.pct_change()


def calculate_margin(
    numerator: pd.Series,
    denominator: pd.Series,
) -> pd.Series:
    """
    Calculate a financial margin.
    """
    denominator = denominator.replace(
        0,
        np.nan,
    )

    return numerator / denominator


def calculate_roic(
    nopat: pd.Series,
    invested_capital: pd.Series,
) -> pd.Series:
    """
    Calculate return on invested capital.
    """
    invested_capital = invested_capital.replace(
        0,
        np.nan,
    )

    return nopat / invested_capital


def calculate_roa(
    net_income: pd.Series,
    total_assets: pd.Series,
) -> pd.Series:
    """
    Calculate return on assets.
    """
    total_assets = total_assets.replace(
        0,
        np.nan,
    )

    return net_income / total_assets


def calculate_roe(
    net_income: pd.Series,
    shareholders_equity: pd.Series,
) -> pd.Series:
    """
    Calculate return on equity.
    """
    shareholders_equity = (
        shareholders_equity.replace(
            0,
            np.nan,
        )
    )

    return (
        net_income
        / shareholders_equity
    )


def calculate_net_debt(
    total_debt: pd.Series,
    cash: pd.Series,
) -> pd.Series:
    """
    Calculate net debt.
    """
    return total_debt - cash


def calculate_net_debt_to_ebitda(
    net_debt: pd.Series,
    ebitda: pd.Series,
) -> pd.Series:
    """
    Calculate net debt / EBITDA.
    """
    ebitda = ebitda.replace(
        0,
        np.nan,
    )

    return net_debt / ebitda


def calculate_interest_coverage(
    ebit: pd.Series,
    interest_expense: pd.Series,
) -> pd.Series:
    """
    Calculate EBIT / absolute interest expense.
    """
    denominator = (
        interest_expense.abs()
        .replace(
            0,
            np.nan,
        )
    )

    return ebit / denominator


def calculate_free_cash_flow(
    operating_cash_flow: pd.Series,
    capital_expenditure: pd.Series,
) -> pd.Series:
    """
    Calculate free cash flow.

    CapEx is standardized using its absolute value
    because cash-flow statements may report CapEx
    as a negative cash outflow.

        FCF = OCF - |CapEx|
    """
    return (
        operating_cash_flow
        - capital_expenditure.abs()
    )


def calculate_fcf_margin(
    free_cash_flow: pd.Series,
    revenue: pd.Series,
) -> pd.Series:
    """
    Calculate free-cash-flow margin.
    """
    revenue = revenue.replace(
        0,
        np.nan,
    )

    return (
        free_cash_flow
        / revenue
    )


def build_fundamental_metrics(
    revenue: pd.Series,
    ebitda: pd.Series,
    ebit: pd.Series,
    net_income: pd.Series,
    operating_cash_flow: pd.Series,
    capital_expenditure: pd.Series,
    total_debt: pd.Series,
    cash: pd.Series,
    total_assets: pd.Series,
    shareholders_equity: pd.Series,
    invested_capital: pd.Series,
    interest_expense: pd.Series,
) -> pd.DataFrame:
    """
    Build a standardized fundamental-analysis dataset.
    """

    free_cash_flow = (
        calculate_free_cash_flow(
            operating_cash_flow,
            capital_expenditure,
        )
    )

    net_debt = calculate_net_debt(
        total_debt,
        cash,
    )

    metrics = pd.DataFrame(
        {
            "revenue_growth": calculate_growth(
                revenue
            ),
            "ebitda_growth": calculate_growth(
                ebitda
            ),
            "ebitda_margin": calculate_margin(
                ebitda,
                revenue,
            ),
            "ebit_margin": calculate_margin(
                ebit,
                revenue,
            ),
            "net_margin": calculate_margin(
                net_income,
                revenue,
            ),
            "roa": calculate_roa(
                net_income,
                total_assets,
            ),
            "roe": calculate_roe(
                net_income,
                shareholders_equity,
            ),
            "roic": calculate_roic(
                nopat_from_ebit(ebit),
                invested_capital,
            ),
            "free_cash_flow": free_cash_flow,
            "fcf_margin": calculate_fcf_margin(
                free_cash_flow,
                revenue,
            ),
            "net_debt": net_debt,
            "net_debt_to_ebitda": (
                calculate_net_debt_to_ebitda(
                    net_debt,
                    ebitda,
                )
            ),
            "interest_coverage": (
                calculate_interest_coverage(
                    ebit,
                    interest_expense,
                )
            ),
        }
    )

    return metrics


def nopat_from_ebit(
    ebit: pd.Series,
    tax_rate: float = 0.25,
) -> pd.Series:
    """
    Calculate NOPAT from EBIT.
    """
    if not 0 <= tax_rate <= 1:
        raise ValueError(
            "Tax rate must be between 0 and 1."
        )

    return ebit * (
        1 - tax_rate
    )
