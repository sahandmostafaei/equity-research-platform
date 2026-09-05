from __future__ import annotations


def calculate_cost_of_equity(
    risk_free_rate: float,
    beta: float,
    equity_risk_premium: float,
) -> float:
    """
    CAPM cost of equity.
    """
    return risk_free_rate + beta * equity_risk_premium


def calculate_after_tax_cost_of_debt(
    pre_tax_cost_of_debt: float,
    tax_rate: float,
) -> float:
    """
    After-tax cost of debt.
    """
    if not 0 <= tax_rate <= 1:
        raise ValueError("Tax rate must be between 0 and 1.")

    return pre_tax_cost_of_debt * (1 - tax_rate)


def calculate_wacc(
    market_value_equity: float,
    market_value_debt: float,
    cost_of_equity: float,
    after_tax_cost_of_debt: float,
) -> float:
    """
    Calculate weighted average cost of capital.
    """
    total_capital = (
        market_value_equity + market_value_debt
    )

    if total_capital <= 0:
        raise ValueError(
            "Total capital must be positive."
        )

    equity_weight = (
        market_value_equity / total_capital
    )

    debt_weight = (
        market_value_debt / total_capital
    )

    return (
        equity_weight * cost_of_equity
        + debt_weight * after_tax_cost_of_debt
    )
