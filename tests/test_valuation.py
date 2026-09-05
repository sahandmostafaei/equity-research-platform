import pytest

from src.valuation import (
    calculate_dcf_value,
    calculate_equity_value,
    calculate_per_share_value,
    calculate_upside,
)


def test_dcf_value_is_positive():
    value = calculate_dcf_value(
        free_cash_flows=[
            100.0,
            110.0,
            121.0,
            133.1,
            146.41,
        ],
        wacc=0.09,
        terminal_growth=0.025,
    )

    assert value > 0


def test_dcf_rejects_invalid_discount_rate():
    with pytest.raises(ValueError):
        calculate_dcf_value(
            free_cash_flows=[100.0],
            wacc=0.02,
            terminal_growth=0.03,
        )


def test_equity_value():
    result = calculate_equity_value(
        enterprise_value=1000.0,
        total_debt=200.0,
        cash=100.0,
    )

    assert result == 900.0


def test_per_share_value():
    result = calculate_per_share_value(
        equity_value=900.0,
        shares_outstanding=100.0,
    )

    assert result == 9.0


def test_upside():
    result = calculate_upside(
        intrinsic_value=120.0,
        market_price=100.0,
    )

    assert result == pytest.approx(0.20)
