from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class InvestmentThesis:
    """
    Structured investment thesis for an equity research report.
    """

    company: str
    thesis: str
    catalysts: list[str]
    risks: list[str]
    valuation_view: str
    conclusion: str

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the thesis into a serializable dictionary.
        """
        return asdict(self)

    def validate(self) -> None:
        """
        Validate the structure of the investment thesis.
        """
        if not self.company.strip():
            raise ValueError(
                "Company name cannot be empty."
            )

        if not self.thesis.strip():
            raise ValueError(
                "Investment thesis cannot be empty."
            )

        if not self.catalysts:
            raise ValueError(
                "At least one catalyst is required."
            )

        if not self.risks:
            raise ValueError(
                "At least one risk is required."
            )

        if not self.valuation_view.strip():
            raise ValueError(
                "Valuation view cannot be empty."
            )

        if not self.conclusion.strip():
            raise ValueError(
                "Conclusion cannot be empty."
            )


def calculate_investment_score(
    valuation_upside: float,
    roic: float,
    revenue_growth: float,
    fcf_margin: float,
    net_debt_to_ebitda: float,
) -> float:
    """
    Calculate a research-prioritization score.

    The score combines valuation, business quality,
    growth, cash-flow generation, and leverage.

    This is an analytical framework rather than
    a trading signal.
    """

    valuation_score = max(
        0.0,
        min(
            1.0,
            (valuation_upside + 0.20) / 0.70,
        ),
    )

    quality_score = max(
        0.0,
        min(
            1.0,
            roic / 0.25,
        ),
    )

    growth_score = max(
        0.0,
        min(
            1.0,
            revenue_growth / 0.20,
        ),
    )

    cash_flow_score = max(
        0.0,
        min(
            1.0,
            fcf_margin / 0.20,
        ),
    )

    leverage_score = 1 - max(
        0.0,
        min(
            1.0,
            net_debt_to_ebitda / 4.0,
        ),
    )

    score = (
        0.30 * valuation_score
        + 0.25 * quality_score
        + 0.15 * growth_score
        + 0.15 * cash_flow_score
        + 0.15 * leverage_score
    )

    return float(
        max(
            0.0,
            min(1.0, score),
        )
    )


def classify_score(
    score: float,
) -> str:
    """
    Convert an investment score into a research classification.
    """

    if not 0 <= score <= 1:
        raise ValueError(
            "Score must be between 0 and 1."
        )

    if score >= 0.80:
        return "High Conviction"

    if score >= 0.65:
        return "Attractive"

    if score >= 0.50:
        return "Neutral"

    if score >= 0.35:
        return "Cautious"

    return "Low Conviction"


def classify_valuation_view(
    valuation_upside: float,
) -> str:
    """
    Classify valuation relative to the current market price.
    """

    if valuation_upside >= 0.25:
        return "Significantly Undervalued"

    if valuation_upside >= 0.10:
        return "Moderately Undervalued"

    if valuation_upside > -0.10:
        return "Fairly Valued"

    if valuation_upside > -0.25:
        return "Moderately Overvalued"

    return "Significantly Overvalued"


def build_investment_assessment(
    valuation_upside: float,
    roic: float,
    revenue_growth: float,
    fcf_margin: float,
    net_debt_to_ebitda: float,
) -> dict[str, Any]:
    """
    Build a complete investment assessment.

    Returns both the numerical score and qualitative
    classifications used by downstream reporting.
    """

    score = calculate_investment_score(
        valuation_upside=valuation_upside,
        roic=roic,
        revenue_growth=revenue_growth,
        fcf_margin=fcf_margin,
        net_debt_to_ebitda=net_debt_to_ebitda,
    )

    return {
        "fundamental_score": score,
        "score_classification": classify_score(
            score
        ),
        "valuation_upside": valuation_upside,
        "valuation_classification": classify_valuation_view(
            valuation_upside
        ),
    }


def build_thesis(
    company: str,
    valuation_upside: float,
    fundamental_score: float,
    catalysts: list[str],
    risks: list[str],
) -> InvestmentThesis:
    """
    Construct a structured investment thesis from
    quantitative assessment outputs.
    """

    valuation_view = classify_valuation_view(
        valuation_upside
    )

    score_view = classify_score(
        fundamental_score
    )

    thesis = (
        f"{company} presents a "
        f"{score_view.lower()} fundamental profile "
        f"with a valuation assessment of "
        f"{valuation_view.lower()}."
    )

    conclusion = (
        f"The investment view is driven by a "
        f"{fundamental_score:.2f} fundamental score "
        f"and estimated valuation upside of "
        f"{valuation_upside:.1%}. "
        f"Further diligence should focus on the "
        f"identified catalysts and key risks."
    )

    result = InvestmentThesis(
        company=company,
        thesis=thesis,
        catalysts=catalysts,
        risks=risks,
        valuation_view=valuation_view,
        conclusion=conclusion,
    )

    result.validate()

    return result
