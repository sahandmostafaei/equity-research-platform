import pytest

from src.capital_cost import (
    calculate_after_tax_cost_of_debt,
    calculate_cost_of_equity,
    calculate_wacc,
)


def test_cost_of_equity():
    result = calculate_cost_of_equity(
        risk_free_rate=0.04,
        beta=1.2,
        equity_risk_premium=0.05,
    )
    assert result == pytest.approx(0.10)


def test_after_tax_cost_of_debt():
    result = calculate_after_tax_cost_of_debt(
        pre_tax_cost_of_debt=0.06,
        tax_rate=0.25,
    )
    assert result == pytest.approx(0.045)


def test_wacc():
    result = calculate_wacc(
        market_value_equity=800.0,
        market_value_debt=200.0,
        cost_of_equity=0.10,
        after_tax_cost_of_debt=0.045,
    )
    assert result == pytest.approx(0.089)


def test_wacc_rejects_invalid_capital():
    with pytest.raises(ValueError):
        calculate_wacc(
            market_value_equity=0.0,
            market_value_debt=0.0,
            cost_of_equity=0.10,
            after_tax_cost_of_debt=0.05,
        )
