from __future__ import annotations

import numpy as np
import pandas as pd


EQUITY_MULTIPLES = {
    "pe",
    "price_sales",
    "fcf_yield",
}

ENTERPRISE_MULTIPLES = {
    "ev_sales",
    "ev_ebitda",
}


def calculate_peer_median_multiples(
    multiples: pd.DataFrame,
) -> pd.Series:
    """
    Calculate median valuation multiples across peers.
    """

    if multiples.empty:
        raise ValueError(
            "Peer multiples cannot be empty."
        )

    cleaned = (
        multiples
        .replace(
            [np.inf, -np.inf],
            np.nan,
        )
    )

    return cleaned.median(
        numeric_only=True
    )


def calculate_equity_implied_values(
    target_metrics: pd.Series,
    peer_medians: pd.Series,
    shares_outstanding: float,
) -> pd.Series:
    """
    Calculate equity-based implied per-share values.

    Supported methods:

    - P/E
    - Price/Sales
    - FCF Yield
    """

    if shares_outstanding <= 0:
        raise ValueError(
            "Shares outstanding must be positive."
        )

    values = {}

    if (
        "pe" in peer_medians
        and "eps" in target_metrics
    ):
        multiple = peer_medians["pe"]
        eps = target_metrics["eps"]

        if (
            pd.notna(multiple)
            and pd.notna(eps)
            and multiple > 0
            and eps > 0
        ):
            values["pe"] = (
                eps
                * multiple
            )

    if (
        "price_sales" in peer_medians
        and "revenue_per_share"
        in target_metrics
    ):
        multiple = peer_medians[
            "price_sales"
        ]
        revenue_per_share = (
            target_metrics[
                "revenue_per_share"
            ]
        )

        if (
            pd.notna(multiple)
            and pd.notna(
                revenue_per_share
            )
            and multiple > 0
            and revenue_per_share > 0
        ):
            values["price_sales"] = (
                revenue_per_share
                * multiple
            )

    if (
        "fcf_yield" in peer_medians
        and "free_cash_flow"
        in target_metrics
    ):
        multiple = peer_medians[
            "fcf_yield"
        ]
        free_cash_flow = (
            target_metrics[
                "free_cash_flow"
            ]
        )

        if (
            pd.notna(multiple)
            and pd.notna(
                free_cash_flow
            )
            and multiple > 0
            and free_cash_flow > 0
        ):
            market_cap = (
                free_cash_flow
                / multiple
            )

            values["fcf_yield"] = (
                market_cap
                / shares_outstanding
            )

    return pd.Series(
        values,
        dtype="float64",
    )


def calculate_enterprise_implied_values(
    target_metrics: pd.Series,
    peer_medians: pd.Series,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
) -> pd.Series:
    """
    Calculate enterprise-value-based implied
    per-share equity values.

    Supported methods:

    - EV/Sales
    - EV/EBITDA

    Enterprise-value methods are bridged to equity value:

        Equity Value
        = Enterprise Value
        - Net Debt

    Net Debt = Debt - Cash
    """

    if shares_outstanding <= 0:
        raise ValueError(
            "Shares outstanding must be positive."
        )

    net_debt = (
        total_debt
        - cash
    )

    values = {}

    if (
        "ev_sales" in peer_medians
        and "revenue" in target_metrics
    ):
        multiple = peer_medians[
            "ev_sales"
        ]
        revenue = target_metrics[
            "revenue"
        ]

        if (
            pd.notna(multiple)
            and pd.notna(revenue)
            and multiple > 0
            and revenue > 0
        ):
            enterprise_value = (
                revenue
                * multiple
            )

            equity_value = (
                enterprise_value
                - net_debt
            )

            values["ev_sales"] = (
                equity_value
                / shares_outstanding
            )

    if (
        "ev_ebitda" in peer_medians
        and "ebitda" in target_metrics
    ):
        multiple = peer_medians[
            "ev_ebitda"
        ]
        ebitda = target_metrics[
            "ebitda"
        ]

        if (
            pd.notna(multiple)
            and pd.notna(ebitda)
            and multiple > 0
            and ebitda > 0
        ):
            enterprise_value = (
                ebitda
                * multiple
            )

            equity_value = (
                enterprise_value
                - net_debt
            )

            values["ev_ebitda"] = (
                equity_value
                / shares_outstanding
            )

    return pd.Series(
        values,
        dtype="float64",
    )


def calculate_peer_implied_values(
    target_metrics: pd.Series,
    peer_medians: pd.Series,
    total_debt: float = 0.0,
    cash: float = 0.0,
    shares_outstanding: float = 1.0,
) -> pd.Series:
    """
    Calculate peer-based implied per-share values
    across equity and enterprise valuation methods.
    """

    equity_values = (
        calculate_equity_implied_values(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            shares_outstanding=shares_outstanding,
        )
    )

    enterprise_values = (
        calculate_enterprise_implied_values(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            total_debt=total_debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
        )
    )

    return pd.concat(
        [
            equity_values,
            enterprise_values,
        ]
    )


def compare_target_to_peers(
    target_multiples: pd.Series,
    peer_medians: pd.Series,
) -> pd.DataFrame:
    """
    Compare target valuation multiples with
    peer median multiples.
    """

    result = pd.DataFrame(
        {
            "target": target_multiples,
            "peer_median": peer_medians,
        }
    )

    result["premium_discount"] = np.where(
        result["peer_median"].abs() > 0,
        (
            result["target"]
            / result["peer_median"]
            - 1
        ),
        np.nan,
    )

    return result


def build_peer_valuation_summary(
    target_metrics: pd.Series,
    peer_medians: pd.Series,
    total_debt: float,
    cash: float,
    shares_outstanding: float,
) -> pd.DataFrame:
    """
    Build a structured peer-valuation summary.
    """

    implied_values = (
        calculate_peer_implied_values(
            target_metrics=target_metrics,
            peer_medians=peer_medians,
            total_debt=total_debt,
            cash=cash,
            shares_outstanding=shares_outstanding,
        )
    )

    rows = []

    for method, value in (
        implied_values.items()
    ):
        if pd.isna(value):
            continue

        valuation_type = (
            "Enterprise Value"
            if method
            in ENTERPRISE_MULTIPLES
            else "Equity Value"
        )

        rows.append(
            {
                "method": method,
                "valuation_type": (
                    valuation_type
                ),
                "implied_per_share": (
                    float(value)
                ),
            }
        )

    return pd.DataFrame(rows)
