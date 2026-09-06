from __future__ import annotations

import pandas as pd


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: set[str],
) -> None:
    missing = required_columns - set(dataframe.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )


def calculate_missing_data_report(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    report = pd.DataFrame(
        {
            "missing_count": dataframe.isna().sum(),
            "missing_percentage": (
                dataframe.isna().mean()
            ),
        }
    )

    return report.sort_values(
        "missing_percentage",
        ascending=False,
    )


def remove_duplicate_rows(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    return dataframe.drop_duplicates().copy()


def validate_positive_values(
    dataframe: pd.DataFrame,
    columns: list[str],
) -> None:
    for column in columns:
        if column not in dataframe.columns:
            raise ValueError(
                f"Column not found: {column}"
            )

        if (dataframe[column] <= 0).any():
            raise ValueError(
                f"Column contains non-positive values: {column}"
            )
