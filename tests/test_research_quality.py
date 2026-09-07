import pandas as pd

from src.research_quality import (
    check_non_empty,
    check_positive_values,
    check_required_columns,
    check_unique_index,
    quality_checks_pass,
    run_research_quality_checks,
)


def test_check_non_empty():
    result = check_non_empty(
        pd.DataFrame({"value": [1, 2]}),
        "Test",
    )

    assert result.passed is True


def test_check_required_columns():
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0],
            "ebitda": [20.0],
        }
    )

    result = check_required_columns(
        dataframe,
        ["revenue", "ebitda"],
        "Financials",
    )

    assert result.passed is True


def test_missing_required_columns():
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0],
        }
    )

    result = check_required_columns(
        dataframe,
        [
            "revenue",
            "ebitda",
        ],
        "Financials",
    )

    assert result.passed is False


def test_positive_values():
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0, 120.0],
            "ebitda": [20.0, 25.0],
        }
    )

    result = check_positive_values(
        dataframe,
        [
            "revenue",
            "ebitda",
        ],
        "Financials",
    )

    assert result.passed is True


def test_unique_index():
    dataframe = pd.DataFrame(
        {
            "value": [1, 2, 3],
        },
        index=[
            "A",
            "B",
            "C",
        ],
    )

    result = check_unique_index(
        dataframe,
        "Test",
    )

    assert result.passed is True


def test_quality_checks_pass():
    dataframe = pd.DataFrame(
        {
            "passed": [
                True,
                True,
            ]
        }
    )

    assert quality_checks_pass(
        dataframe
    ) is True


def test_quality_checks_fail():
    dataframe = pd.DataFrame(
        {
            "passed": [
                True,
                False,
            ]
        }
    )

    assert quality_checks_pass(
        dataframe
    ) is False


def test_integrated_quality_checks():
    historical = pd.DataFrame(
        {
            "revenue": [100.0],
            "ebitda": [20.0],
            "net_income": [10.0],
            "free_cash_flow": [8.0],
        },
        index=["2025"],
    )

    scenarios = pd.DataFrame(
        {
            "scenario": [
                "Bear",
                "Base",
                "Bull",
            ],
            "per_share_value": [
                80.0,
                100.0,
                120.0,
            ],
        }
    )

    peer_multiples = pd.DataFrame(
        {
            "pe": [20.0, 22.0],
            "ev_ebitda": [15.0, 16.0],
            "ev_sales": [5.0, 5.5],
        }
    )

    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF - Base",
            ],
            "valuation_type": [
                "DCF",
            ],
            "implied_per_share": [
                100.0,
            ],
        }
    )

    checks = run_research_quality_checks(
        historical_financials=historical,
        scenario_valuations=scenarios,
        peer_multiples=peer_multiples,
        valuation_summary=valuation_summary,
    )

    assert not checks.empty
    assert quality_checks_pass(
        checks
    ) is True
