import pandas as pd
import pytest

from src.comparables import (
    calculate_implied_value_from_multiple,
    calculate_multiples,
    calculate_relative_discount,
    remove_invalid_multiples,
)


def test_calculate_multiples():
    index = ["A", "B"]

    result = calculate_multiples(
        market_cap=pd.Series(
            [1000.0, 2000.0],
            index=index,
        ),
        enterprise_value=pd.Series(
            [1100.0, 2100.0],
            index=index,
        ),
        revenue=pd.Series(
            [500.0, 1000.0],
            index=index,
        ),
        ebitda=pd.Series(
            [100.0, 200.0],
            index=index,
        ),
        earnings=pd.Series(
            [50.0, 100.0],
            index=index,
        ),
        free_cash_flow=pd.Series(
            [80.0, 160.0],
            index=index,
        ),
    )

    assert result.loc["A", "pe"] == pytest.approx(20.0)
    assert result.loc["A", "ev_sales"] == pytest.approx(2.2)
    assert result.loc["A", "ev_ebitda"] == pytest.approx(11.0)
    assert result.loc["A", "price_sales"] == pytest.approx(2.0)
    assert result.loc["A", "fcf_yield"] == pytest.approx(0.08)


def test_invalid_multiples_are_cleaned():
    multiples = pd.DataFrame(
        {
            "pe": [
                20.0,
                float("inf"),
            ],
            "ev_ebitda": [
                10.0,
                float("-inf"),
            ],
        }
    )

    result = remove_invalid_multiples(
        multiples
    )

    assert pd.isna(
        result.iloc[1]["pe"]
    )

    assert pd.isna(
        result.iloc[1]["ev_ebitda"]
    )


def test_implied_value_from_multiple():
    result = calculate_implied_value_from_multiple(
        metric=5.0,
        peer_multiple=20.0,
    )

    assert result == 100.0


def test_implied_value_requires_positive_inputs():
    with pytest.raises(ValueError):
        calculate_implied_value_from_multiple(
            metric=0.0,
            peer_multiple=20.0,
        )


def test_relative_discount():
    result = calculate_relative_discount(
        company_multiple=15.0,
        peer_multiple=20.0,
    )

    assert result == pytest.approx(0.25)


def test_relative_discount_requires_positive_peer_multiple():
    with pytest.raises(ValueError):
        calculate_relative_discount(
            company_multiple=15.0,
            peer_multiple=0.0,
        )
