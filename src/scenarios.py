from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Scenario:
    """
    Operating assumptions for an investment scenario.
    """

    name: str
    revenue_growth: float
    ebitda_margin: float
    wacc: float
    terminal_growth: float


def create_default_scenarios() -> dict[str, Scenario]:
    """
    Create standardized bear, base, and bull scenarios.
    """
    return {
        "bear": Scenario(
            name="Bear",
            revenue_growth=0.03,
            ebitda_margin=0.18,
            wacc=0.11,
            terminal_growth=0.02,
        ),
        "base": Scenario(
            name="Base",
            revenue_growth=0.07,
            ebitda_margin=0.22,
            wacc=0.09,
            terminal_growth=0.025,
        ),
        "bull": Scenario(
            name="Bull",
            revenue_growth=0.12,
            ebitda_margin=0.26,
            wacc=0.08,
            terminal_growth=0.03,
        ),
    }


def project_revenue(
    starting_revenue: float,
    growth_rate: float,
    years: int,
) -> list[float]:
    """
    Project revenue over multiple years.
    """
    if starting_revenue <= 0:
        raise ValueError("Starting revenue must be positive.")

    if years <= 0:
        raise ValueError("Years must be positive.")

    return [
        starting_revenue * ((1 + growth_rate) ** year)
        for year in range(1, years + 1)
    ]


def project_ebitda(
    projected_revenue: list[float],
    ebitda_margin: float,
) -> list[float]:
    """
    Project EBITDA from revenue and an EBITDA margin.
    """
    return [
        revenue * ebitda_margin
        for revenue in projected_revenue
    ]
