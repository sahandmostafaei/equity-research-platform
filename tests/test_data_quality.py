import pandas as pd
import pytest

from src.data_quality import (
    calculate_missing_data_report,
    remove_duplicate_rows,
    validate_positive_values,
    validate_required_columns,
)


def test_required_columns():
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0],
            "ebitda": [20.0],
        }
    )

    validate_required_columns(
        dataframe,
        {"revenue", "ebitda"},
    )


def test_missing_columns():
    dataframe = pd.DataFrame(
        {"revenue": [100.0]}
    )

    with pytest.raises(ValueError):
        validate_required_columns(
            dataframe,
            {"revenue", "ebitda"},
        )


def test_missing_data_report():
    dataframe = pd.DataFrame(
        {
            "revenue": [100.0, None],
            "ebitda": [20.0, 30.0],
        }
    )

    result = calculate_missing_data_report(
        dataframe
    )

    assert result.loc[
        "revenue",
        "missing_count",
    ] == 1


def test_duplicate_removal():
    dataframe = pd.DataFrame(
        {
            "ticker": ["MSFT", "MSFT"],
            "value": [100.0, 100.0],
        }
    )

    result = remove_duplicate_rows(
        dataframe
    )

    assert len(result) == 1


def test_positive_values():
    dataframe = pd.DataFrame(
        {"revenue": [100.0, 200.0]}
    )

    validate_positive_values(
        dataframe,
        ["revenue"],
    )
