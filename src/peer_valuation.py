from __future__ import annotations

import pandas as pd


def calculate_peer_median_multiples(
    multiples: pd.DataFrame,
) -> pd.Series:
    """
    Calculate median valuation multiples across peers.
    """
    if multiples.empty:
        raise ValueError(
            "Peer multiples cannot be empty."
        )

    return multiples.median(
        numeric_only=True
    )


def calculate_peer_implied_values(
    target_metrics: pd.Series,
    peer_medians: pd.Series,
) -> pd.Series:
    """
    Apply peer median multiples to target financial metrics.
    """
    mapping = {
        "pe": "eps",
        "ev_sales": "revenue",
        "ev_ebitda": "ebitda",
        "price_sales": "revenue",
        "fcf_yield": "free_cash_flow",
    }

    implied_values = {}

    for multiple, metric in mapping.items():
        if multiple not in peer_medians:
            continue

        if metric not in target_metrics:
            continue

        multiple_value = peer_medians[multiple]
        metric_value = target_metrics[metric]

        if pd.isna(multiple_value):
            continue

        implied_values[multiple] = (
            metric_value * multiple_value
        )

    return pd.Series(implied_values)


def compare_target_to_peers(
    target_multiples: pd.Series,
    peer_medians: pd.Series,
) -> pd.DataFrame:
    """
    Compare target valuation multiples with peer medians.
    """
    result = pd.DataFrame(
        {
            "target": target_multiples,
            "peer_median": peer_medians,
        }
    )

    result["premium_discount"] = (
        result["target"]
        / result["peer_median"]
        - 1
    )

    return result
