import pytest

from src.research_engine import (
    EquityResearchEngine,
    run_research,
)


def test_engine_initializes():

    engine = EquityResearchEngine(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
            "AAPL",
            "AMZN",
        ],
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
        "AAPL",
        "AMZN",
    ]

    assert engine.start_date == "2018-01-01"

    assert engine.end_date is None


def test_engine_normalizes_tickers():

    engine = EquityResearchEngine(
        target_ticker="msft",
        peer_tickers=[
            "googl",
            "meta",
        ],
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
    ]


def test_engine_removes_target_from_peers():

    engine = EquityResearchEngine(
        target_ticker="MSFT",
        peer_tickers=[
            "MSFT",
            "GOOGL",
            "META",
        ],
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
    ]


def test_empty_target_is_rejected():

    with pytest.raises(ValueError):

        EquityResearchEngine(
            target_ticker="",
            peer_tickers=[
                "GOOGL",
            ],
        )


def test_empty_peer_list_is_rejected():

    with pytest.raises(ValueError):

        EquityResearchEngine(
            target_ticker="MSFT",
            peer_tickers=[],
        )


def test_run_research_constructs_engine():

    engine = run_research(
        target_ticker="MSFT",
        peer_tickers=[
            "GOOGL",
            "META",
        ],
    )

    assert engine.target_ticker == "MSFT"

    assert engine.peer_tickers == [
        "GOOGL",
        "META",
    ]
