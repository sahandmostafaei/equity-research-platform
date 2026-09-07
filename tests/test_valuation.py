import pandas as pd
import pytest

from src.valuation import (
    calculate_dcf_value,
    calculate_equity_value,
    calculate_ev_ebitda_value,
    calculate_margin_of_safety,
    calculate_pe_value,
    calculate_per_share_value,
    calculate_terminal_value,
    calculate_upside,
    valuation_sensitivity,
)


def test_dcf_value():
    free_cash_flows = [
        100.0,
        110.0,
        121.0,
        133.1,
        146.41,
    ]

    result = calculate_dcf_value(
        free_cash_flows=free_cash_flows,
        wacc=0.10,
        terminal_growth=0.03,
    )

    assert result > 0


def test_dcf_rejects_invalid_wacc():
    with pytest.raises(ValueError):
        calculate_dcf_value(
            free_cash_flows=[100.0, 110.0],
            wacc=0.03,
            terminal_growth=0.03,
        )


def test_dcf_rejects_empty_forecast():
    with pytest.raises(ValueError):
        calculate_dcf_value(
            free_cash_flows=[],
            wacc=0.10,
            terminal_growth=0.03,
        )


def test_terminal_value():
    result = calculate_terminal_value(
        final_fcf=100.0,
        wacc=0.10,
        terminal_growth=0.03,
    )

    expected = (
        100.0 * 1.03
    ) / (
        0.10 - 0.03
    )

    assert result == pytest.approx(
        expected
    )


def test_equity_value_bridge():
    result = calculate_equity_value(
        enterprise_value=1000.0,
        total_debt=200.0,
        cash=100.0,
    )

    assert result == pytest.approx(
        900.0
    )


def test_per_share_value():
    result = calculate_per_share_value(
        equity_value=900.0,
        shares_outstanding=100.0,
    )

    assert result == pytest.approx(
        9.0
    )


def test_per_share_rejects_zero_shares():
    with pytest.raises(ValueError):
        calculate_per_share_value(
            equity_value=900.0,
            shares_outstanding=0.0,
        )


def test_upside():
    result = calculate_upside(
        intrinsic_value=120.0,
        market_price=100.0,
    )

    assert result == pytest.approx(
        0.20
    )


def test_upside_rejects_invalid_price():
    with pytest.raises(ValueError):
        calculate_upside(
            intrinsic_value=120.0,
            market_price=0.0,
        )


def test_pe_valuation():
    result = calculate_pe_value(
        eps=5.0,
        peer_pe=20.0,
    )

    assert result == pytest.approx(
        100.0
    )


def test_ev_ebitda_valuation():
    result = calculate_ev_ebitda_value(
        ebitda=200.0,
        peer_ev_ebitda=10.0,
        net_debt=500.0,
        shares_outstanding=100.0,
    )

    expected = (
        2000.0 - 500.0
    ) / 100.0

    assert result == pytest.approx(
        expected
    )


def test_ev_ebitda_rejects_invalid_shares():
    with pytest.raises(ValueError):
        calculate_ev_ebitda_value(
            ebitda=200.0,
            peer_ev_ebitda=10.0,
            net_debt=500.0,
            shares_outstanding=0.0,
        )


def test_valuation_sensitivity():
    result = valuation_sensitivity(
        free_cash_flows=[
            100.0,
            110.0,
            121.0,
        ],
        wacc_values=[
            0.08,
            0.10,
            0.12,
        ],
        terminal_growth_values=[
            0.02,
            0.03,
            0.04,
        ],
    )

    assert isinstance(
        result,
        pd.DataFrame
    )

    assert result.shape == (
        3,
        3
    )

    assert result.index.name == "WACC"


def test_sensitivity_higher_wacc_reduces_value():
    result = valuation_sensitivity(
        free_cash_flows=[
            100.0,
            110.0,
            121.0,
        ],
        wacc_values=[
            0.08,
            0.10,
            0.12,
        ],
        terminal_growth_values=[
            0.03,
        ],
    )

    assert (
        result.loc[0.08, 0.03]
        >
        result.loc[0.10, 0.03]
        >
        result.loc[0.12, 0.03]
    )


def test_sensitivity_higher_terminal_growth_increases_value():
    result = valuation_sensitivity(
        free_cash_flows=[
            100.0,
            110.0,
            121.0,
        ],
        wacc_values=[
            0.10,
        ],
        terminal_growth_values=[
            0.02,
            0.03,
            0.04,
        ],
    )

    assert (
        result.loc[0.10, 0.02]
        <
        result.loc[0.10, 0.03]
        <
        result.loc[0.10, 0.04]
    )


def test_margin_of_safety():
    result = calculate_margin_of_safety(
        intrinsic_value=125.0,
        market_price=100.0,
    )

    assert result == pytest.approx(
        0.20
    )


def test_margin_of_safety_rejects_invalid_intrinsic_value():
    with pytest.raises(ValueError):
        calculate_margin_of_safety(
            intrinsic_value=0.0,
            market_price=100.0,
        )


def test_margin_of_safety_rejects_invalid_market_price():
    with pytest.raises(ValueError):
        calculate_margin_of_safety(
            intrinsic_value=125.0,
            market_price=0.0,
        )
