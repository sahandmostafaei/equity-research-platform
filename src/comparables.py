from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_multiples(
    market_cap: pd.Series,
    enterprise_value: pd.Series,
    revenue: pd.Series,
    ebitda: pd.Series,
    earnings: pd.Series,
    free_cash_flow: pd.Series,
) -> pd.DataFrame:
    """
    Calculate common trading multiples.
    """

    result = pd.DataFrame(index=market_cap.index)

    result["pe"] = (
        market_cap / earnings.replace(0, np.nan)
    )

    result["ev_sales"] = (
        enterprise_value / revenue.replace(0, np.nan)
    )

    result["ev_ebitda"] = (
        enterprise_value / ebitda.replace(0, np.nan)
    )

    result["price_sales"] = (
        market_cap / revenue.replace(0, np.nan)
    )

    result["fcf_yield"] = (
        free_cash_flow / market_cap.replace(0, np.nan)
    )

    return result


def peer_summary(
    multiples: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate descriptive statistics for peer multiples.
    """

    return pd.DataFrame(
        {
            "mean": multiples.mean(),
            "median": multiples.median(),
            "min": multiples.min(),
            "max": multiples.max(),
            "std": multiples.std(),
        }
    )


def remove_invalid_multiples(
    multiples: pd.DataFrame,
) -> pd.DataFrame:
    """
    Replace infinite values with NaN.
    """

    cleaned = multiples.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return cleaned


def calculate_implied_value_from_multiple(
    metric: float,
    peer_multiple: float,
) -> float:
    """
    Calculate implied enterprise or equity value
    from a selected peer multiple.
    """

    if metric <= 0:
        raise ValueError("Metric must be positive.")

    if peer_multiple <= 0:
        raise ValueError("Peer multiple must be positive.")

    return metric * peer_multiple


def calculate_relative_discount(
    company_multiple: float,
    peer_multiple: float,
) -> float:
    """
    Calculate the discount/premium of a company multiple
    relative to the peer multiple.

    Positive value = company trades at a discount.
    Negative value = company trades at a premium.
    """

    if peer_multiple <= 0:
        raise ValueError("Peer multiple must be positive.")

    return 1 - (company_multiple / peer_multiple)
