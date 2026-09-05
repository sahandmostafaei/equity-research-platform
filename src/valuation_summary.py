from __future__ import annotations

import pandas as pd


def build_valuation_summary(
    dcf_value: float,
    pe_value: float,
    ev_ebitda_value: float,
    market_price: float,
) -> pd.DataFrame:
    """
    Compare valuation methods against the current market price.
    """
    methods = [
        "DCF",
        "P/E",
        "EV/EBITDA",
    ]

    values = [
        dcf_value,
        pe_value,
        ev_ebitda_value,
    ]

    summary = pd.DataFrame(
        {
            "method": methods,
            "implied_value": values,
        }
    )

    summary["market_price"] = market_price

    summary["upside_downside"] = (
        summary["implied_value"]
        / market_price
        - 1
    )

    summary["premium_discount"] = (
        summary["implied_value"]
        / market_price
        - 1
    )

    return summary


def calculate_consensus_value(
    valuation_values: pd.Series,
) -> float:
    """
    Calculate the median implied value across
    valuation methodologies.
    """
    cleaned = pd.to_numeric(
        valuation_values,
        errors="coerce",
    ).dropna()

    if cleaned.empty:
        raise ValueError(
            "At least one valid valuation is required."
        )

    return float(cleaned.median())
