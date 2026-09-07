import pandas as pd
import pytest

from src.reporting import (
    build_research_report,
    plot_peer_multiples,
    plot_revenue_and_ebitda,
    plot_scenario_valuation,
    plot_valuation_sensitivity,
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

    path = tmp_path / "data.csv"

    save_dataframe(
        dataframe,
        path,
    )

    assert path.exists()


def test_save_text(tmp_path):
    path = tmp_path / "report.md"

    save_text(
        "# Research Report",
        path,
    )

    assert path.exists()
    assert path.read_text(
        encoding="utf-8"
    ) == "# Research Report"


def test_save_investment_thesis(tmp_path):
    path = (
        tmp_path
        / "investment_thesis.csv"
    )

    save_investment_thesis(
        {
            "company": "Microsoft",
            "valuation_view": (
                "Moderately Undervalued"
            ),
        },
        path,
    )

    assert path.exists()


def test_plot_revenue_and_ebitda(tmp_path):
    revenue = pd.Series(
        [100.0, 110.0, 121.0],
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

    plot_revenue_and_ebitda(
        revenue,
        ebitda,
        path,
    )

    assert path.exists()


def test_plot_valuation_sensitivity(tmp_path):
    sensitivity = pd.DataFrame(
        {
            0.02: [
                1000.0,
                900.0,
                800.0,
            ],
            0.03: [
                1100.0,
                1000.0,
                900.0,
            ],
        },
        index=[
            0.08,
            0.10,
            0.12,
        ],
    )

    path = (
        tmp_path
        / "sensitivity.png"
    )

    plot_valuation_sensitivity(
        sensitivity,
        path,
    )

    assert path.exists()


def test_plot_valuation_sensitivity_rejects_empty_data(
    tmp_path,
):
    with pytest.raises(ValueError):
        plot_valuation_sensitivity(
            pd.DataFrame(),
            tmp_path / "empty.png",
        )


def test_plot_peer_multiples(tmp_path):
    multiples = pd.DataFrame(
        {
            "pe": [
                20.0,
                25.0,
                30.0,
            ],
            "ev_ebitda": [
                15.0,
                18.0,
                20.0,
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

    plot_peer_multiples(
        multiples,
        path,
    )

    assert path.exists()


def test_plot_scenario_valuation(tmp_path):
    scenarios = pd.DataFrame(
        {
            "scenario": [
                "Bear",
                "Base",
                "Bull",
            ],
            "dcf_value": [
                80.0,
                110.0,
                140.0,
            ],
        }
    )

    path = (
        tmp_path
        / "scenarios.png"
    )

    plot_scenario_valuation(
        scenarios,
        path,
    )

    assert path.exists()


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

    assert "# Equity Research Report — MSFT" in report
    assert "Investment Summary" in report
    assert "DCF" in report
    assert "20.0%" in report


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

    save_research_report(
        target_ticker="MSFT",
        investment_summary={
            "market_price": 100.0,
            "consensus_value": 120.0,
            "valuation_upside": 0.20,
        },
        valuation_summary=valuation_summary,
        output_path=path,
    )

    assert path.exists()
    assert "MSFT" in path.read_text(
        encoding="utf-8"
    )
