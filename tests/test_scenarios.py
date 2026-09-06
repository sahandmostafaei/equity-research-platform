import pytest

from src.scenarios import (
    create_default_scenarios,
    project_ebitda,
    project_revenue,
)


def test_default_scenarios_exist():
    scenarios = create_default_scenarios()

    assert set(scenarios) == {
        "bear",
        "base",
        "bull",
    }


def test_project_revenue():
    result = project_revenue(
        starting_revenue=100.0,
        growth_rate=0.10,
        years=3,
    )

    assert len(result) == 3
    assert result[0] == pytest.approx(110.0)
    assert result[1] == pytest.approx(121.0)
    assert result[2] == pytest.approx(133.1)


def test_project_revenue_rejects_invalid_years():
    with pytest.raises(ValueError):
        project_revenue(
            starting_revenue=100.0,
            growth_rate=0.10,
            years=0,
        )


def test_project_ebitda():
    result = project_ebitda(
        projected_revenue=[
            100.0,
            110.0,
        ],
        ebitda_margin=0.20,
    )

    assert result == [
        pytest.approx(20.0),
        pytest.approx(22.0),
    ]
