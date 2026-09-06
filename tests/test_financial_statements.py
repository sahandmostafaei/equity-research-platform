import pandas as pd
import pytest

from src.financial_statements import (
    calculate_fcf,
    find_statement_value,
    normalize_line_item_name,
)


def test_normalize_line_item_name():
    assert (
        normalize_line_item_name(
            "Total Revenue"
        )
        == "totalrevenue"
    )

    assert (
        normalize_line_item_name(
            "Capital_Expenditure"
        )
        == "capitalexpenditure"
    )


def test_find_statement_value_ignores_formatting():
    statement = pd.DataFrame(
        {
            "2025": [100.0],
            "2024": [90.0],
        },
        index=[
            "Total Revenue"
        ],
    )

    result = find_statement_value(
        statement,
        [
            "total_revenue"
        ],
    )

    assert result["2025"] == 100.0
    assert result["2024"] == 90.0


def test_fcf_standardizes_negative_capex():
    operating_cash_flow = pd.Series(
        [150.0]
    )

    capital_expenditure = pd.Series(
        [-50.0]
    )

    result = calculate_fcf(
        operating_cash_flow,
        capital_expenditure,
    )

    assert result.iloc[0] == 100.0


def test_empty_statement_rejected():
    statement = pd.DataFrame()

    with pytest.raises(
        ValueError
    ):
        find_statement_value(
            statement,
            ["Revenue"],
        )
