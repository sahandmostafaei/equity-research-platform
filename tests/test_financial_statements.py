import pandas as pd
import pytest

from src.financial_statements import (
    calculate_ebitda,
    calculate_fcf,
    calculate_invested_capital,
    calculate_nopat,
    find_statement_value,
)


def test_find_statement_value():
    statement = pd.DataFrame(
        {
            "2025": [100.0],
            "2024": [90.0],
        },
        index=["Revenue"],
    )

    result = find_statement_value(
        statement,
        ["revenue"],
    )

    assert result.iloc[0] == 100.0


def test_ebitda():
    ebit = pd.Series([100.0])
    da = pd.Series([20.0])

    result = calculate_ebitda(
        ebit,
        da,
    )

    assert result.iloc[0] == 120.0


def test_nopat():
    ebit = pd.Series([100.0])

    result = calculate_nopat(
        ebit,
        tax_rate=0.25,
    )

    assert result.iloc[0] == 75.0


def test_invested_capital():
    debt = pd.Series([100.0])
    equity = pd.Series([200.0])
    cash = pd.Series([50.0])

    result = calculate_invested_capital(
        debt,
        equity,
        cash,
    )

    assert result.iloc[0] == 250.0


def test_fcf():
    ocf = pd.Series([150.0])
    capex = pd.Series([50.0])

    result = calculate_fcf(
        ocf,
        capex,
    )

    assert result.iloc[0] == 100.0


def test_missing_statement_value():
    statement = pd.DataFrame(
        {"2025": [100.0]},
        index=["Revenue"],
    )

    with pytest.raises(KeyError):
        find_statement_value(
            statement,
            ["EBITDA"],
        )
