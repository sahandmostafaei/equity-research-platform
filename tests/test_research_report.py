import pandas as pd

from src.research_report import (
    build_company_snapshot,
    build_peer_comparison_table,
)


def test_company_snapshot():
    metrics = pd.Series(
        {
            "roic": 0.20,
            "fcf_margin": 0.15,
        }
    )

    result = build_company_snapshot(
        company="Microsoft",
        ticker="MSFT",
        sector="Technology",
        metrics=metrics,
    )

    assert result["company"] == "Microsoft"
    assert result["ticker"] == "MSFT"
    assert result["roic"] == 0.20


def test_peer_comparison():
    target = pd.Series(
        {
            "roic": 0.20,
            "fcf_margin": 0.15,
        }
    )

    peers = pd.DataFrame(
        {
            "roic": [0.18, 0.22],
            "fcf_margin": [0.12, 0.17],
        },
        index=["Peer A", "Peer B"],
    )

    result = build_peer_comparison_table(
        "Microsoft",
        target,
        peers,
    )

    assert len(result) == 3
    assert "Microsoft" in result.index
