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

    result["pe"] = market_cap / earnings.replace(0, np.nan)
    result["ev_sales"] = enterprise_value / revenue.replace(0, np.nan)
    result["ev_ebitda"] = enterprise_value / ebitda.replace(0, np.nan)
    result["price_sales"] = market_cap / revenue.replace(0, np.nan)
    result["fcf_yield"] = free_cash_flow / market_cap.replace(0, np.nan)

    return result


def peer_summary(
    multiples: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate median, mean, minimum, and maximum peer multiples.
    """
    summary = pd.DataFrame(
        {
            "mean": multiples.mean(),
            "median": multiples.median(),
            "min": multiples.min(),
            "max": multiples.max(),
            "std": multiples.std(),
        }
    )

    return summary


def remove_invalid_multiples(
    multiples: pd.DataFrame,
) -> pd.DataFrame:
    """
    Replace infinite values with NaN and remove empty columns.
    """
    cleaned = multiples.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return cleaned.dropna(axis=1, how="all")
