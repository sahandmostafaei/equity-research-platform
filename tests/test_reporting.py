from pathlib import Path

import pandas as pd

from src.reporting import (
    build_research_report,
    plot_peer_multiples,
    plot_revenue_and_ebitda,
    plot_scenario_valuation,
    save_dataframe,
    save_investment_thesis,
    save_research_report,
    save_text,
)


def test_save_dataframe(tmp_path):

    dataframe = pd.DataFrame(
        {
            "metric": [
                "revenue",
                "ebitda",
            ],
            "value": [
                100.0,
                25.0,
            ],
        }
    )

    path = save_dataframe(
        dataframe=dataframe,
        filename="data.csv",
        output_dir=tmp_path,
    )

    assert path.exists()

    assert path.name == "data.csv"

    loaded = pd.read_csv(path)

    assert list(loaded.columns) == [
        "metric",
        "value",
    ]


def test_save_text(tmp_path):

    path = save_text(
        text="# Research Report",
        filename="report.md",
        output_dir=tmp_path,
    )

    assert path.exists()

    assert path.name == "report.md"

    assert path.read_text(
        encoding="utf-8"
    ) == "# Research Report"


def test_save_investment_thesis(tmp_path):

    thesis = {
        "company": "Microsoft",
        "thesis": (
            "Strong fundamental profile."
        ),
        "catalysts": [
            "Revenue growth",
            "Margin expansion",
        ],
        "risks": [
            "Valuation",
            "Competition",
        ],
        "valuation_view": (
            "Moderately Undervalued"
        ),
        "conclusion": (
            "Further diligence required."
        ),
    }

    path = (
        tmp_path
        / "investment_thesis.csv"
    )

    result = save_investment_thesis(
        thesis,
        path,
    )

    assert result.exists()

    assert result == path


def test_build_research_report():

    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF",
                "EV/EBITDA",
            ],
            "value": [
                120.0,
                115.0,
            ],
        }
    )

    report = build_research_report(
        target_ticker="MSFT",
        investment_summary={
            "market_price": 100.0,
            "consensus_value": 120.0,
            "valuation_upside": 0.20,
            "fundamental_score": 0.75,
            "valuation_classification": (
                "Moderately Undervalued"
            ),
            "investment_view": (
                "Buy Candidate"
            ),
        },
        valuation_summary=valuation_summary,
    )

    assert isinstance(
        report,
        str,
    )

    assert "MSFT" in report

    assert "120.0" in report

    assert "Buy Candidate" in report


def test_save_research_report(tmp_path):

    valuation_summary = pd.DataFrame(
        {
            "method": [
                "DCF",
            ],
            "value": [
                120.0,
            ],
        }
    )

    path = (
        tmp_path
        / "research_report.md"
    )

    result = save_research_report(
        target_ticker="MSFT",
        investment_summary={
            "market_price": 100.0,
            "consensus_value": 120.0,
            "valuation_upside": 0.20,
        },
        valuation_summary=valuation_summary,
        output_path=path,
    )

    assert result.exists()

    assert result == path

    text = path.read_text(
        encoding="utf-8"
    )

    assert "MSFT" in text


def test_plot_revenue_and_ebitda(
    tmp_path,
):

    revenue = pd.Series(
        [100.0, 120.0, 140.0],
        index=[
            "2023",
            "2024",
            "2025",
        ],
    )

    ebitda = pd.Series(
        [20.0, 25.0, 30.0],
        index=[
            "2023",
            "2024",
            "2025",
        ],
    )

    path = (
        tmp_path
        / "revenue_ebitda.png"
    )

    result = plot_revenue_and_ebitda(
        revenue,
        ebitda,
        path,
    )

    assert result.exists()


def test_plot_peer_multiples(
    tmp_path,
):

    multiples = pd.DataFrame(
        {
            "pe": [
                20.0,
                22.0,
                24.0,
            ],
            "ev_ebitda": [
                12.0,
                14.0,
                16.0,
            ],
        },
        index=[
            "GOOGL",
            "META",
            "AAPL",
        ],
    )

    path = (
        tmp_path
        / "peer_multiples.png"
    )

    result = plot_peer_multiples(
        multiples,
        path,
    )

    assert result.exists()


def test_plot_scenario_valuation(
    tmp_path,
):

    scenarios = pd.DataFrame(
        {
            "scenario": [
                "Bear",
                "Base",
                "Bull",
            ],
            "implied_per_share": [
                80.0,
                110.0,
                140.0,
            ],
        }
    )

    path = (
        tmp_path
        / "scenario_valuation.png"
    )

    result = plot_scenario_valuation(
        scenarios,
        path,
    )

    assert result.exists()
