import pandas as pd

from src.scenario_valuation import (
    run_all_scenarios,
)
from src.scenarios import create_default_scenarios


def test_all_scenarios():
    historical_revenue = pd.Series(
        [100.0, 110.0, 120.0, 130.0]
    )

    scenarios = create_default_scenarios()

    result = run_all_scenarios(
        historical_revenue=historical_revenue,
        scenarios=scenarios,
        total_debt=100.0,
        cash=50.0,
        shares_outstanding=100.0,
    )

    assert len(result) == 3
    assert set(result["scenario"]) == {
        "Bear",
        "Base",
        "Bull",
    }
    assert (
        result["per_share_value"]
        .notna()
        .all()
    )
