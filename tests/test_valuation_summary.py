import pandas as pd
import pytest

from src.valuation_summary import (
    build_valuation_summary,
    calculate_consensus_value,
)


def test_valuation_summary():
    result = build_valuation_summary(
        dcf_value=120.0,
        pe_value=110.0,
        ev_ebitda_value=115.0,
        market_price=100.0,
    )

    assert len(result) == 3
    assert result["implied_value"].max() == 120.0
    assert result["upside_downside"].iloc[0] == pytest.approx(0.20)


def test_consensus_value():
    values = pd.Series(
        [100.0, 120.0, 110.0]
    )

    result = calculate_consensus_value(values)

    assert result == 110.0
