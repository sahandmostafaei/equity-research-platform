from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analytical_summary import (
    build_research_dashboard,
    save_research_dashboard,
)
from src.investment_thesis import build_thesis
from src.research_engine import create_default_research_engine
from src.research_outputs import save_research_outputs
from src.research_quality import (
    quality_checks_pass,
    run_research_quality_checks,
)
from src.reporting import (
    plot_peer_multiples,
    plot_revenue_and_ebitda,
    plot_scenario_valuation,
    save_investment_thesis,
    save_research_report,
)


ROOT_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = (
    ROOT_DIR
    / "data"
    / "processed"
)

FIGURES_DIR = (
    ROOT_DIR
    / "figures"
)


def main() -> None:
    """
    Run the complete equity research workflow.

    Workflow:
    1. Load research configuration.
    2. Download target and peer financial data.
    3. Calculate fundamental and market metrics.
    4. Estimate WACC.
    5. Run scenario valuation.
    6. Run peer valuation.
    7. Build investment assessment.
    8. Build analytical dashboard.
    9. Build structured investment thesis.
    10. Generate research report and figures.
    11. Run data-quality checks.
    12. Save all outputs.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Starting equity research workflow..."
    )

    # ---------------------------------------------------------
    # 1. Create research engine
    # ---------------------------------------------------------

    engine = (
        create_default_research_engine()
    )

    print(
        f"Target company: "
        f"{engine.config.target_ticker}"
    )

    print(
        "Peer companies: "
        + ", ".join(
            engine.config.peer_tickers
        )
    )

    # ---------------------------------------------------------
    # 2. Run integrated research engine
    # ---------------------------------------------------------

    result = engine.run()

    print(
        "Research engine completed."
    )

    # ---------------------------------------------------------
    # 3. Save core analytical outputs
    # ---------------------------------------------------------

    output_paths = save_research_outputs(
        result,
        OUTPUT_DIR,
    )

    print(
        f"Saved {len(output_paths)} "
        "core analytical outputs."
    )

    # ---------------------------------------------------------
    # 4. Build analytical dashboard
    # ---------------------------------------------------------

    dashboard = (
        build_research_dashboard(
            result
        )
    )

    dashboard_paths = (
        save_research_dashboard(
            dashboard,
            OUTPUT_DIR,
        )
    )

    print(
        f"Saved {len(dashboard_paths)} "
        "dashboard outputs."
    )

    # ---------------------------------------------------------
    # 5. Extract investment assessment
    # ---------------------------------------------------------

    investment_summary = (
        result.investment_summary
    )

    valuation_upside = float(
        investment_summary.get(
            "valuation_upside",
            0.0,
        )
    )

    fundamental_score = float(
        investment_summary.get(
            "fundamental_score",
            0.0,
        )
    )

    # ---------------------------------------------------------
    # 6. Build catalysts and risks
    # ---------------------------------------------------------

    catalysts = [
        (
            "Revenue growth and operating "
            "margin expansion can increase "
            "intrinsic value."
        ),
        (
            "Strong cash-flow generation can "
            "support reinvestment and shareholder "
            "returns."
        ),
        (
            "Relative valuation versus selected "
            "technology peers provides a market "
            "reference point."
        ),
    ]

    risks = [
        (
            "Valuation is sensitive to WACC, "
            "terminal growth, and forecast "
            "assumptions."
        ),
        (
            "Peer multiples may be affected by "
            "differences in growth, margins, "
            "capital intensity, and risk."
        ),
        (
            "Market data and financial-statement "
            "inputs are sourced dynamically and "
            "should be independently verified "
            "before investment use."
        ),
    ]

    # ---------------------------------------------------------
    # 7. Determine company name
    # ---------------------------------------------------------

    company = result.market_data.get(
        "company"
    )

    if not company:
        company = result.target_ticker

    company = str(company)

    # ---------------------------------------------------------
    # 8. Build structured investment thesis
    # ---------------------------------------------------------

    thesis = build_thesis(
        company=company,
        valuation_upside=valuation_upside,
        fundamental_score=fundamental_score,
        catalysts=catalysts,
        risks=risks,
    )

    thesis_path = (
        OUTPUT_DIR
        / "investment_thesis.csv"
    )

    save_investment_thesis(
        thesis.to_dict(),
        thesis_path,
    )

    print(
        "Saved investment thesis."
    )

    # ---------------------------------------------------------
    # 9. Generate research report
    # ---------------------------------------------------------

    report_path = (
        OUTPUT_DIR
        / "research_report.md"
    )

    save_research_report(
        target_ticker=result.target_ticker,
        investment_summary=(
            result.investment_summary
        ),
        valuation_summary=(
            result.valuation_summary
        ),
        output_path=report_path,
        peer_comparison=(
            result.peer_comparison
        ),
    )

    print(
        "Saved research report."
    )

    # ---------------------------------------------------------
    # 10. Generate revenue / EBITDA figure
    # ---------------------------------------------------------

    revenue_ebitda_path = (
        FIGURES_DIR
        / "revenue_ebitda_history.png"
    )

    plot_revenue_and_ebitda(
        result.historical_financials[
            "revenue"
        ],
        result.historical_financials[
            "ebitda"
        ],
        revenue_ebitda_path,
    )

    print(
        "Saved revenue and EBITDA figure."
    )

    # ---------------------------------------------------------
    # 11. Generate peer multiples figure
    # ---------------------------------------------------------

    peer_multiples_path = (
        FIGURES_DIR
        / "peer_multiples.png"
    )

    plot_peer_multiples(
        result.peer_multiples,
        peer_multiples_path,
    )

    print(
        "Saved peer multiples figure."
    )

    # ---------------------------------------------------------
    # 12. Generate scenario valuation figure
    # ---------------------------------------------------------

    scenario_valuation_path = (
        FIGURES_DIR
        / "scenario_valuation.png"
    )

    plot_scenario_valuation(
        result.scenario_valuations,
        scenario_valuation_path,
    )

    print(
        "Saved scenario valuation figure."
    )

    # ---------------------------------------------------------
    # 13. Run research-quality checks
    # ---------------------------------------------------------

    quality_checks = (
        run_research_quality_checks(
            result
        )
    )

    quality_path = (
        OUTPUT_DIR
        / "research_quality_checks.csv"
    )

    quality_checks.to_csv(
        quality_path,
        index=False,
    )

    print(
        "Saved research-quality checks."
    )

    # ---------------------------------------------------------
    # 14. Stop if quality checks fail
    # ---------------------------------------------------------

    if not quality_checks_pass(
        quality_checks
    ):
        print(
            "Research-quality checks failed."
        )
        raise RuntimeError(
            "Research-quality checks failed. "
            "Review data/processed/"
            "research_quality_checks.csv."
        )

    print(
        "Research-quality checks passed."
    )

    # ---------------------------------------------------------
    # 15. Final summary
    # ---------------------------------------------------------

    market_price = investment_summary.get(
        "market_price"
    )

    median_valuation = investment_summary.get(
        "consensus_value"
    )

    valuation_classification = (
        investment_summary.get(
            "valuation_classification"
        )
    )

    investment_view = (
        investment_summary.get(
            "investment_view"
        )
    )

    print()
    print(
        "========================================"
    )
    print(
        "EQUITY RESEARCH SUMMARY"
    )
    print(
        "========================================"
    )

    print(
        f"Target: "
        f"{result.target_ticker}"
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

    if median_valuation is not None:
        print(
            "Median valuation reference: "
            f"{float(median_valuation):.2f}"
        )

    print(
        f"Valuation upside: "
        f"{valuation_upside:.2%}"
    )

    print(
        f"Fundamental score: "
        f"{fundamental_score:.2f}"
    )

    print(
        f"Valuation classification: "
        f"{valuation_classification}"
    )

    print(
        f"Investment view: "
        f"{investment_view}"
    )

    print(
        "========================================"
    )

    print(
        "Research workflow completed successfully."
    )


if __name__ == "__main__":
    main()
