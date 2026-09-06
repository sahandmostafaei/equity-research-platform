import pandas as pd
import pytest

from src.peer_valuation import (
    calculate_enterprise_implied_values,
    calculate_equity_implied_values,
    calculate_peer_median_multiples,
)


def test_peer_median_multiples():
    multiples = pd.DataFrame(
        {
            "pe": [20.0, 24.0, 22.0],
            "ev_ebitda": [15.0, 17.0, 16.0],
        }
    )

    result = (
        calculate_peer_median_multiples(
            multiples
        )
    )

    assert result["pe"] == 22.0
    assert result["ev_ebitda"] == 16.0


def test_equity_valuation():
    target_metrics = pd.Series(
        {
            "eps": 5.0,
            "revenue_per_share": 20.0,
        }
    )

    peer_medians = pd.Series(
        {
            "pe": 20.0,
            "price_sales": 4.0,
        }
    )

    result = (
        calculate_equity_implied_values(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            shares_outstanding=100.0,
        )
    )

    assert result["pe"] == 100.0
    assert result["price_sales"] == 80.0


def test_enterprise_valuation_bridges_to_equity():
    target_metrics = pd.Series(
        {
            "revenue": 1000.0,
            "ebitda": 200.0,
        }
    )

    peer_medians = pd.Series(
        {
            "ev_sales": 3.0,
            "ev_ebitda": 10.0,
        }
    )

    result = (
        calculate_enterprise_implied_values(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            total_debt=200.0,
            cash=100.0,
            shares_outstanding=100.0,
        )
    )

    # EV/Sales:
    # 1000 * 3 = 3000 EV
    # 3000 - 100 net debt = 2900 equity
    # 2900 / 100 shares = 29
    assert result["ev_sales"] == pytest.approx(
        29.0
    )

    # EV/EBITDA:
    # 200 * 10 = 2000 EV
    # 2000 - 100 net debt = 1900 equity
    # 1900 / 100 shares = 19
    assert result["ev_ebitda"] == pytest.approx(
        19.0
    )
