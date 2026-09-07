import pandas as pd
import pytest

from src.analytical_summary import (
    build_fundamental_kpi_summary,
    build_valuation_range,
    calculate_valuation_statistics,
)


def test_build_fundamental_kpi_summary():

    financials = pd.DataFrame(
        {
            "revenue": [100.0, 120.0],
            "ebitda": [20.0, 30.0],
            "free_cash_flow": [10.0, 15.0],
            "roic": [0.10, 0.12],
        }
    )

    result = build_fundamental_kpi_summary(
        financials
    )

    assert not result.empty

    revenue = result.loc[
        result["metric"] == "revenue",
        "latest_value",
    ].iloc[0]

    assert revenue == 120.0


def test_build_valuation_range():

    valuation = pd.DataFrame(
        {
            "method": [
                "DCF",
                "PE",
                "EV/EBITDA",
            ],
            "implied_per_share": [
                100.0,
                120.0,
                110.0,
            ],
        }
    )

    result = build_valuation_range(
        valuation
    )

    assert result.iloc[0][
        "implied_per_share"
    ] == 100.0

    assert result.iloc[-1][
        "implied_per_share"
    ] == 120.0


def test_calculate_valuation_statistics():

    valuation = pd.DataFrame(
        {
            "method": [
                "DCF",
                "PE",
                "EV/EBITDA",
            ],
            "implied_per_share": [
                100.0,
                120.0,
                110.0,
            ],
        }
    )

    result = calculate_valuation_statistics(
        valuation
    )

    assert result["minimum"] == 100.0
    assert result["maximum"] == 120.0
    assert result["median"] == 110.0


def test_empty_valuation_rejected():

    valuation = pd.DataFrame()

    with pytest.raises(ValueError):
        build_valuation_range(
            valuation
        )
