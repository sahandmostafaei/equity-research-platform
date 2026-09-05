import pandas as pd
import pytest

from src.peer_valuation import (
    calculate_peer_implied_values,
    calculate_peer_median_multiples,
    compare_target_to_peers,
)


def test_peer_median():
    multiples = pd.DataFrame(
        {
            "pe": [20.0, 25.0, 30.0],
            "ev_ebitda": [15.0, 17.0, 19.0],
        }
    )

    result = calculate_peer_median_multiples(
        multiples
    )

    assert result["pe"] == 25.0
    assert result["ev_ebitda"] == 17.0


def test_peer_implied_values():
    target = pd.Series(
        {
            "eps": 5.0,
            "ebitda": 100.0,
            "revenue": 500.0,
            "free_cash_flow": 50.0,
        }
    )

    peer_medians = pd.Series(
        {
            "pe": 20.0,
            "ev_ebitda": 15.0,
            "ev_sales": 5.0,
        }
    )

    result = calculate_peer_implied_values(
        target,
        peer_medians,
    )

    assert result["pe"] == 100.0
    assert result["ev_ebitda"] == 1500.0
    assert result["ev_sales"] == 2500.0


def test_target_peer_comparison():
    target = pd.Series(
        {
            "pe": 20.0,
            "ev_ebitda": 15.0,
        }
    )

    peers = pd.Series(
        {
            "pe": 25.0,
            "ev_ebitda": 20.0,
        }
    )

    result = compare_target_to_peers(
        target,
        peers,
    )

    assert result.loc[
        "pe",
        "premium_discount",
    ] == pytest.approx(-0.20)
