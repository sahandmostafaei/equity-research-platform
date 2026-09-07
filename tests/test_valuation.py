import pytest

from src.valuation import (
    calculate_dcf_value,
    calculate_equity_value,
    calculate_margin_of_safety,
    calculate_per_share_value,
    calculate_upside,
)


def test_dcf_requires_valid_wacc_spread():
    with pytest.raises(ValueError):
        calculate_dcf_value(
            free_cash_flows=[100.0, 110.0],
            wacc=0.08,
            terminal_growth=0.08,
        )


def test_dcf_returns_positive_value():
    value = calculate_dcf_value(
        free_cash_flows=[
            100.0,
            110.0,
            120.0,
        ],
        wacc=0.10,
        terminal_growth=0.02,
    )

    assert value > 0


def test_equity_value_bridge():
    result = calculate_equity_value(
        enterprise_value=1000.0,
        total_debt=250.0,
        cash=100.0,
    )

    assert result == 850.0


def test_per_share_value():
    result = calculate_per_share_value(
        equity_value=1000.0,
        shares_outstanding=100.0,
    )

    assert result == 10.0


def test_per_share_requires_positive_shares():
    with pytest.raises(ValueError):
        calculate_per_share_value(
            equity_value=1000.0,
            shares_outstanding=0.0,
        )


def test_upside():
    result = calculate_upside(
        intrinsic_value=120.0,
        market_price=100.0,
    )

    assert result == pytest.approx(0.20)


def test_margin_of_safety():
    result = calculate_margin_of_safety(
        intrinsic_value=120.0,
        market_price=90.0,
    )

    assert result == pytest.approx(0.25)
