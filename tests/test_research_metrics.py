import pytest

from src.research_metrics import (
    calculate_enterprise_value,
    calculate_eps,
    calculate_ev_to_ebitda,
    calculate_ev_to_sales,
    calculate_fcf_yield,
)


def test_eps():
    assert calculate_eps(500.0, 100.0) == 5.0


def test_enterprise_value():
    assert calculate_enterprise_value(
        market_cap=1000.0,
        total_debt=200.0,
        cash=100.0,
    ) == 1100.0


def test_ev_to_sales():
    assert calculate_ev_to_sales(
        enterprise_value=1000.0,
        revenue=500.0,
    ) == 2.0


def test_ev_to_ebitda():
    assert calculate_ev_to_ebitda(
        enterprise_value=1000.0,
        ebitda=100.0,
    ) == 10.0


def test_fcf_yield():
    assert calculate_fcf_yield(
        free_cash_flow=50.0,
        market_cap=1000.0,
    ) == pytest.approx(0.05)
