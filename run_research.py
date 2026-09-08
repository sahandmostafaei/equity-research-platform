from pathlib import Path

from src.analytical_summary import (
    build_research_dashboard,
    save_research_dashboard,
)
from src.investment_thesis import (
    build_thesis,
)
from src.research_engine import (
    EquityResearchEngine,
)
from src.research_outputs import (
    save_research_outputs,
)
from src.research_quality import (
    run_research_quality_checks,
    quality_checks_pass,
)
from src.reporting import (
    build_research_report,
    plot_peer_multiples,
    plot_revenue_and_ebitda,
    plot_scenario_valuation,
    save_investment_thesis,
    save_research_report,
)


PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR = PROJECT_ROOT / "figures"


def main() -> None:
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    engine = EquityResearchEngine()

    result = engine.run()

    save_research_outputs(
        result,
        OUTPUT_DIR,
    )

    dashboard = build_research_dashboard(
        result
    )

    save_research_dashboard(
        dashboard,
        OUTPUT_DIR,
    )

    latest_financials = (
        result.historical_financials.iloc[-1]
    )

    roic = float(
        latest_financials.get(
            "roic",
            0.0,
        )
    )

    revenue_growth = float(
        latest_financials.get(
            "revenue_growth",
            0.0,
        )
    )

    free_cash_flow = float(
        latest_financials.get(
            "free_cash_flow",
            0.0,
        )
    )

    revenue = float(
        latest_financials.get(
            "revenue",
            0.0,
        )
    )

    fcf_margin = (
        free_cash_flow / revenue
        if revenue != 0
        else 0.0
    )

    net_debt_to_ebitda = float(
        latest_financials.get(
            "net_debt_to_ebitda",
            0.0,
        )
    )

    valuation_upside = float(
        result.investment_summary.get(
            "valuation_upside",
            0.0,
        )
    )

    fundamental_score = float(
        result.investment_summary.get(
            "fundamental_score",
            0.0,
        )
    )

    catalysts = [
        "Revenue growth and operating performance",
        "Margin expansion and cash-flow generation",
        "Valuation relative to fundamental value",
    ]

    risks = [
        "Changes in revenue growth assumptions",
        "Margin compression",
        "Higher discount rates and valuation sensitivity",
        "Competitive and macroeconomic risks",
    ]

    thesis = build_thesis(
        company=result.target_ticker,
        valuation_upside=valuation_upside,
        fundamental_score=fundamental_score,
        catalysts=catalysts,
        risks=risks,
    )

    save_investment_thesis(
        thesis.to_dict(),
        OUTPUT_DIR / "investment_thesis.csv",
    )

    report = build_research_report(
        result=result,
        dashboard=dashboard,
        thesis=thesis.to_dict(),
    )

    save_research_report(
        report,
        OUTPUT_DIR / "research_report.md",
    )

    plot_revenue_and_ebitda(
        result.historical_financials[
            "revenue"
        ],
        result.historical_financials[
            "ebitda"
        ],
        FIGURES_DIR / "revenue_ebitda_history.png",
    )

    plot_peer_multiples(
        result.peer_multiples,
        FIGURES_DIR / "peer_multiples.png",
    )

    plot_scenario_valuation(
        result.scenario_valuations,
        FIGURES_DIR / "scenario_valuation.png",
    )

    quality_checks = (
        run_research_quality_checks(
            historical_financials=(
                result.historical_financials
            ),
            scenario_valuations=(
                result.scenario_valuations
            ),
            peer_multiples=(
                result.peer_multiples
            ),
            valuation_summary=(
                result.valuation_summary
            ),
        )
    )

    if not quality_checks_pass(
        quality_checks
    ):
        failed_checks = [
            check.name
            for check in quality_checks
            if not check.passed
        ]

        raise RuntimeError(
            "Research quality checks failed: "
            + ", ".join(failed_checks)
        )

    summary = result.investment_summary

    print(
        "\n"
        "Equity Research Platform\n"
        "========================\n"
    )

    print(
        f"Target: {result.target_ticker}"
    )

    print(
        f"Estimated WACC: "
        f"{result.estimated_wacc:.2%}"
    )

    print(
        f"Market Price: "
        f"{summary.get('market_price', float('nan')):.2f}"
    )

    print(
        f"Median Valuation Reference: "
        f"{summary.get('consensus_value', float('nan')):.2f}"
    )

    print(
        f"Valuation Upside: "
        f"{summary.get('valuation_upside', float('nan')):.2%}"
    )

    print(
        f"Fundamental Score: "
        f"{summary.get('fundamental_score', float('nan')):.2f}"
    )

    print(
        f"Valuation Classification: "
        f"{summary.get('valuation_classification', 'N/A')}"
    )

    print(
        f"Investment View: "
        f"{summary.get('investment_view', 'N/A')}"
    )

    print(
        "\nQuality Checks: PASSED"
    )

    print(
        f"ROIC: {roic:.2%}"
    )

    print(
        f"Revenue Growth: {revenue_growth:.2%}"
    )

    print(
        f"FCF Margin: {fcf_margin:.2%}"
    )

    print(
        f"Net Debt / EBITDA: "
        f"{net_debt_to_ebitda:.2f}"
    )

    print(
        "\nOutputs saved to:"
    )

    print(
        f"  {OUTPUT_DIR}"
    )

    print(
        f"  {FIGURES_DIR}"
    )


if __name__ == "__main__":
    main()
