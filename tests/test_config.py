import pandas as pd
import pytest

from src.config import (
    get_config_value,
    get_float_config,
    get_int_config,
    load_research_config,
)


def test_load_research_config():
    config = load_research_config(
        "data/research_config.csv"
    )

    assert not config.empty
    assert "parameter" in config.columns
    assert "value" in config.columns


def test_get_config_value():
    config = pd.DataFrame(
        {
            "parameter": [
                "target_ticker"
            ],
            "value": [
                "MSFT"
            ],
            "unit": [
                "text"
            ],
            "category": [
                "universe"
            ],
            "description": [
                "Target"
            ],
        }
    )

    assert (
        get_config_value(
            config,
            "target_ticker",
        )
        == "MSFT"
    )


def test_get_float_config():
    config = pd.DataFrame(
        {
            "parameter": [
                "tax_rate"
            ],
            "value": [
                "0.25"
            ],
            "unit": [
                "decimal"
            ],
            "category": [
                "valuation"
            ],
            "description": [
                "Tax"
            ],
        }
    )

    assert (
        get_float_config(
            config,
            "tax_rate",
        )
        == 0.25
    )


def test_get_int_config():
    config = pd.DataFrame(
        {
            "parameter": [
                "forecast_years"
            ],
            "value": [
                "5"
            ],
            "unit": [
                "years"
            ],
            "category": [
                "forecast"
            ],
            "description": [
                "Forecast"
            ],
        }
    )

    assert (
        get_int_config(
            config,
            "forecast_years",
        )
        == 5
    )


def test_missing_parameter():
    config = pd.DataFrame(
        {
            "parameter": [
                "tax_rate"
            ],
            "value": [
                "0.25"
            ],
            "unit": [
                "decimal"
            ],
            "category": [
                "valuation"
            ],
            "description": [
                "Tax"
            ],
        }
    )

    with pytest.raises(KeyError):
        get_config_value(
            config,
            "missing_parameter",
        )


def test_duplicate_parameters_are_rejected():
    config = pd.DataFrame(
        {
            "parameter": [
                "tax_rate",
                "tax_rate",
            ],
            "value": [
                "0.25",
                "0.30",
            ],
            "unit": [
                "decimal",
                "decimal",
            ],
            "category": [
                "valuation",
                "valuation",
            ],
            "description": [
                "Tax",
                "Tax",
            ],
        }
    )

    path = "tests/temp_duplicate_config.csv"

    config.to_csv(
        path,
        index=False,
    )

    try:
        with pytest.raises(ValueError):
            load_research_config(path)
    finally:
        import os

        if os.path.exists(path):
            os.remove(path)
