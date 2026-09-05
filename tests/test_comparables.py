import pandas as pd
import pytest

from src.comparables import (
    calculate_implied_value_from_multiple,
    calculate_relative_discount,
)


def test_implied_value():
    result = calculate_implied_value_from_multiple(
        metric=100.0,
        peer_multiple=10.0,
    )

    assert result == 1000.0


def test_relative_discount():
    result = calculate_relative_discount(
        company_multiple=8.0,
        peer_multiple=10.0,
    )

    assert result == pytest.approx(0.20)


def test_invalid_multiple():
    with pytest.raises(ValueError):
        calculate_implied_value_from_multiple(
            metric=100.0,
            peer_multiple=0.0,
        )
