import pytest

from src.assumptions import (
    DCFAssumptions,
    create_default_dcf_assumptions,
)


def test_default_assumptions():
    assumptions = create_default_dcf_assumptions()

    assert assumptions.forecast_years == 5
    assert assumptions.wacc > assumptions.terminal_growth


def test_invalid_assumptions():
    assumptions = DCFAssumptions(
        revenue_growth=0.07,
        ebitda_margin=0.22,
        fcf_conversion=0.50,
        wacc=0.02,
        terminal_growth=0.03,
    )

    with pytest.raises(ValueError):
        assumptions.validate()
