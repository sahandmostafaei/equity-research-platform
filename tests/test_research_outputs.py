import pandas as pd

from src.research_outputs import (
    build_research_snapshot,
    save_dataframe,
    save_investment_summary,
)


def test_save_dataframe(tmp_path):
    dataframe = pd.DataFrame(
        {
            "metric": ["revenue"],
            "value": [100.0],
        }
    )

    path = save_dataframe(
        dataframe,
        "test.csv",
        tmp_path,
    )

    assert path.exists()
    assert path.name == "test.csv"


def test_save_investment_summary(tmp_path):
    summary = {
        "market_price": 100.0,
        "consensus_value": 120.0,
        "valuation_upside": 0.20,
    }

    path = save_investment_summary(
        summary,
        tmp_path,
    )

    assert path.exists()
    assert (
        path.name
        == "investment_summary.csv"
    )


def test_research_snapshot():
    class MockResult:
        target_ticker = "MSFT"
        peer_financials = {
            "GOOGL": pd.DataFrame(),
            "META": pd.DataFrame(),
        }
        valuation_summary = pd.DataFrame(
            {
                "method": [
                    "DCF",
                    "EV/EBITDA",
                ]
            }
        )
        estimated_wacc = 0.08
        investment_summary = {
            "market_price": 100.0,
            "consensus_value": 120.0,
            "valuation_upside": 0.20,
            "score": 0.80,
            "score_classification": "Strong",
        }

    snapshot = build_research_snapshot(
        MockResult()
    )

    assert (
        snapshot.iloc[0][
            "target_ticker"
        ]
        == "MSFT"
    )

    assert (
        snapshot.iloc[0][
            "peer_count"
        ]
        == 2
    )

    assert (
        snapshot.iloc[0][
            "valuation_method_count"
        ]
        == 2
    )
