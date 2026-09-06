from __future__ import annotations

from pathlib import Path

from src.research_engine import (
    create_default_research_engine,
)
from src.research_outputs import (
    save_research_outputs,
)


def main() -> None:
    engine = (
        create_default_research_engine()
    )

    result = engine.run()

    paths = save_research_outputs(
        result,
        output_dir=Path(
            "data/processed"
        ),
    )

    print(
        f"Research completed for "
        f"{result.target_ticker}."
    )

    print(
        f"Estimated WACC: "
        f"{result.estimated_wacc:.2%}"
    )

    summary = (
        result.investment_summary
    )

    if (
        summary.get(
            "market_price"
        )
        is not None
    ):
        print(
            f"Market price: "
            f"{summary['market_price']:.2f}"
        )

    if (
        summary.get(
            "consensus_value"
        )
        is not None
    ):
        print(
            f"Consensus valuation: "
            f"{summary['consensus_value']:.2f}"
        )

    if (
        summary.get(
            "valuation_upside"
        )
        is not None
    ):
        print(
            f"Valuation upside: "
            f"{summary['valuation_upside']:.2%}"
        )

    print(
        f"Saved {len(paths)} output files "
        "to data/processed/."
    )


if __name__ == "__main__":
    main()
