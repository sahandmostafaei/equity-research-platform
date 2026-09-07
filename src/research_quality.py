from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class QualityCheck:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "check": self.name,
            "passed": self.passed,
            "message": self.message,
        }


def check_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
    name: str,
) -> QualityCheck:
    missing = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing:
        return QualityCheck(
            name=f"{name} required columns",
            passed=False,
            message=(
                "Missing required columns: "
                + ", ".join(missing)
            ),
        )

    return QualityCheck(
        name=f"{name} required columns",
        passed=True,
        message="All required columns are present.",
    )


def check_non_empty(
    dataframe: pd.DataFrame,
    name: str,
) -> QualityCheck:
    if dataframe.empty:
        return QualityCheck(
            name=f"{name} non-empty",
            passed=False,
            message=f"{name} is empty.",
        )

    return QualityCheck(
        name=f"{name} non-empty",
        passed=True,
        message=f"{name} contains observations.",
    )


def check_numeric_finite(
    dataframe: pd.DataFrame,
    columns: list[str],
    name: str,
) -> QualityCheck:
    missing = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing:
        return QualityCheck(
            name=f"{name} numeric validity",
            passed=False,
            message=(
                "Missing columns: "
                + ", ".join(missing)
            ),
        )

    numeric = dataframe[columns]

    if not all(
        pd.api.types.is_numeric_dtype(
            numeric[column]
        )
        for column in columns
    ):
        return QualityCheck(
            name=f"{name} numeric validity",
            passed=False,
            message="At least one required column is not numeric.",
        )

    if not numeric.apply(
        lambda column: column.map(
            lambda value: pd.notna(value)
            and pd.notna(float(value))
        ).all()
    ).all():
        return QualityCheck(
            name=f"{name} numeric validity",
            passed=False,
            message="Non-finite or missing numeric values were detected.",
        )

    return QualityCheck(
        name=f"{name} numeric validity",
        passed=True,
        message="Required numeric values are finite.",
    )


def check_positive_values(
    dataframe: pd.DataFrame,
    columns: list[str],
    name: str,
) -> QualityCheck:
    missing = [
        column
        for column in columns
        if column not in dataframe.columns
    ]

    if missing:
        return QualityCheck(
            name=f"{name} positive values",
            passed=False,
            message=(
                "Missing columns: "
                + ", ".join(missing)
            ),
        )

    for column in columns:
        values = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        if values.isna().any():
            return QualityCheck(
                name=f"{name} positive values",
                passed=False,
                message=(
                    f"Column '{column}' contains "
                    "missing or non-numeric values."
                ),
            )

        if (values <= 0).any():
            return QualityCheck(
                name=f"{name} positive values",
                passed=False,
                message=(
                    f"Column '{column}' contains "
                    "non-positive values."
                ),
            )

    return QualityCheck(
        name=f"{name} positive values",
        passed=True,
        message="Required values are positive.",
    )


def check_unique_index(
    dataframe: pd.DataFrame,
    name: str,
) -> QualityCheck:
    if not dataframe.index.is_unique:
        return QualityCheck(
            name=f"{name} unique index",
            passed=False,
            message=f"{name} contains duplicate index values.",
        )

    return QualityCheck(
        name=f"{name} unique index",
        passed=True,
        message="Index values are unique.",
    )


def run_research_quality_checks(
    historical_financials: pd.DataFrame,
    scenario_valuations: pd.DataFrame,
    peer_multiples: pd.DataFrame,
    valuation_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Run deterministic quality checks on core research outputs.

    The function reports validation results without modifying
    the underlying research data.
    """

    checks: list[QualityCheck] = []

    checks.append(
        check_non_empty(
            historical_financials,
            "Historical financials",
        )
    )

    checks.append(
        check_required_columns(
            historical_financials,
            [
                "revenue",
                "ebitda",
                "net_income",
                "free_cash_flow",
            ],
            "Historical financials",
        )
    )

    checks.append(
        check_non_empty(
            scenario_valuations,
            "Scenario valuations",
        )
    )

    checks.append(
        check_required_columns(
            scenario_valuations,
            [
                "scenario",
                "per_share_value",
            ],
            "Scenario valuations",
        )
    )

    checks.append(
        check_non_empty(
            peer_multiples,
            "Peer multiples",
        )
    )

    checks.append(
        check_required_columns(
            peer_multiples,
            [
                "pe",
                "ev_ebitda",
                "ev_sales",
            ],
            "Peer multiples",
        )
    )

    checks.append(
        check_non_empty(
            valuation_summary,
            "Valuation summary",
        )
    )

    checks.append(
        check_required_columns(
            valuation_summary,
            [
                "method",
                "valuation_type",
                "implied_per_share",
            ],
            "Valuation summary",
        )
    )

    checks.append(
        check_unique_index(
            historical_financials,
            "Historical financials",
        )
    )

    if "per_share_value" in scenario_valuations.columns:
        checks.append(
            check_numeric_finite(
                scenario_valuations,
                ["per_share_value"],
                "Scenario valuations",
            )
        )

    if "implied_per_share" in valuation_summary.columns:
        checks.append(
            check_numeric_finite(
                valuation_summary,
                ["implied_per_share"],
                "Valuation summary",
            )
        )

    return pd.DataFrame(
        [
            check.to_dict()
            for check in checks
        ]
    )


def quality_checks_pass(
    checks: pd.DataFrame,
) -> bool:
    """
    Return True only when every quality check passes.
    """

    if checks.empty:
        return False

    if "passed" not in checks.columns:
        return False

    return bool(
        checks["passed"].all()
    )
