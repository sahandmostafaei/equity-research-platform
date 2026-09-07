from __future__ import annotations

from pathlib import Path

from src.research_engine import (
    create_default_research_engine,
)
from src.research_outputs import (
    save_research_outputs,
)
from src.investment_thesis import (
    build_thesis,
)
from src.reporting import (
    plot_peer_multiples,
    plot_scenario_valuation,
    plot_revenue_and_ebitda,
    save_investment_thesis,
    save_research_report,
)


def build_catalysts(result) -> list[str]:
    """
    Build research catalysts from quantitative outputs.
    """

    catalysts: list[str] = []

    summary = result.investment_summary

    valuation_upside = summary.get(
        "valuation_upside"
    )

    if (
        valuation_upside is not None
        and valuation_upside > 0
    ):
        catalysts.append(
            "Potential valuation re-rating if "
            "fundamental performance supports the "
            "current valuation assumptions."
        )

    latest = (
        result.historical_financials.iloc[-1]
    )

    revenue_growth = latest.get(
        "revenue_growth"
    )

    if (
        revenue_growth is not None
        and revenue_growth > 0
    ):
        catalysts.append(
            "Positive historical revenue growth "
            "provides support for forward operating "
            "growth assumptions."
        )

    roic = latest.get(
        "roic"
    )

    if (
        roic is not None
        and roic > 0
    ):
        catalysts.append(
            "Positive returns on invested capital "
            "support the underlying business-quality "
            "case."
        )

    if not catalysts:
        catalysts.append(
            "Improvement in operating fundamentals "
            "could support a stronger valuation outcome."
        )

    return catalysts


def build_risks(result) -> list[str]:
    """
    Build research risks from quantitative outputs.
    """

    risks: list[str] = []

    summary = result.investment_summary

    valuation_upside = summary.get(
        "valuation_upside"
    )

    if (
        valuation_upside is not None
        and valuation_upside < 0
    ):
        risks.append(
            "Current valuation assumptions may not "
            "support sufficient upside relative to "
            "the market price."
        )

    latest = (
        result.historical_financials.iloc[-1]
    )

    net_debt_to_ebitda = latest.get(
        "net_debt_to_ebitda"
    )

    if (
        net_debt_to_ebitda is not None
        and net_debt_to_ebitda > 2
    ):
        risks.append(
            "Elevated leverage increases financial "
            "risk and can reduce valuation flexibility."
        )

    revenue_growth = latest.get(
        "revenue_growth"
    )

    if (
        revenue_growth is not None
        and revenue_growth < 0
    ):
        risks.append(
            "Negative historical revenue growth "
            "creates execution risk for forward "
            "growth assumptions."
        )

    risks.append(
        "DCF valuation remains sensitive to WACC, "
        "terminal growth, operating assumptions, "
        "and forecast free cash flow."
    )

    return risks


def main() -> None:
    engine = (
        create_default_research_engine()
    )

    result = engine.run()

    output_dir = Path(
        "data/processed"
    )

    paths = save_research_outputs(
        result,
        output_dir=output_dir,
    )

    summary = result.investment_summary

    market_price = summary.get(
        "market_price"
    )

    consensus_value = summary.get(
        "consensus_value"
    )

    valuation_upside = summary.get(
        "valuation_upside"
    )

    fundamental_score = summary.get(
        "fundamental_score"
    )

    catalysts = build_catalysts(
        result
    )

    risks = build_risks(
        result
    )

    thesis = build_thesis(
        company=result.target_ticker,
        valuation_upside=float(
            valuation_upside
        ),
        fundamental_score=float(
            fundamental_score
        ),
        catalysts=catalysts,
        risks=risks,
    )

    thesis_path = (
        output_dir
        / "investment_thesis.csv"
    )

    save_investment_thesis(
        thesis.to_dict(),
        thesis_path,
    )

    report_path = (
        output_dir
        / "research_report.md"
    )

    save_research_report(
        target_ticker=(
            result.target_ticker
        ),
        investment_summary=(
            result.investment_summary
        ),
        valuation_summary=(
            result.valuation_summary
        ),
        peer_comparison=(
            result.peer_comparison
        ),
        output_path=report_path,
    )

    historical = (
        result.historical_financials
    )

    revenue_plot = (
        output_dir
        / "historical_revenue_ebitda.png"
    )

    plot_revenue_and_ebitda(
        revenue=historical[
            "revenue"
        ],
        ebitda=historical[
            "ebitda"
        ],
        output_path=revenue_plot,
    )

    peer_plot = (
        output_dir
        / "peer_valuation_multiples.png"
    )

    plot_peer_multiples(
        multiples=result.peer_multiples,
        output_path=peer_plot,
    )

    scenario_plot = (
        output_dir
        / "scenario_valuation.png"
    )

    plot_scenario_valuation(
        scenario_valuations=(
            result.scenario_valuations
        ),
        output_path=scenario_plot,
    )

    print(
        f"Research completed for "
        f"{result.target_ticker}."
    )

    print(
        f"Estimated WACC: "
        f"{result.estimated_wacc:.2%}"
    )

    if market_price is not None:
        print(
            f"Market price: "
            f"{float(market_price):.2f}"
        )

    if consensus_value is not None:
        print(
            f"Consensus valuation: "
            f"{float(consensus_value):.2f}"
        )

    if valuation_upside is not None:
        print(
            f"Valuation upside: "
            f"{float(valuation_upside):.2%}"
        )

    if fundamental_score is not None:
        print(
            f"Fundamental score: "
            f"{float(fundamental_score):.2f}"
        )

    print(
        f"Investment view: "
        f"{summary.get('investment_view')}"
    )

    print(
        f"Saved {len(paths)} core output files "
        f"to {output_dir}."
    )

    print(
        "Saved investment thesis, research report, "
        "and analytical charts."
    )


if __name__ == "__main__":
    main()
