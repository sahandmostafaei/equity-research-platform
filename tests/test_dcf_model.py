import pandas as pd
import pytest

from src.dcf_model import calculate_dcf


def test_complete_dcf():
    free_cash_flows = pd.Series(
        [
            100.0,
            110.0,
            121.0,
            133.1,
            146.41,
        ]
    )

    result = calculate_dcf(
        free_cash_flows=free_cash_flows,
        wacc=0.09,
        terminal_growth=0.025,
        total_debt=200.0,
        cash=100.0,
        shares_outstanding=100.0,
    )

    assert result.enterprise_value > 0
    assert result.terminal_value > 0
    assert result.equity_value > 0
    assert result.per_share_value > 0


def test_dcf_rejects_invalid_wacc():
    with pytest.raises(ValueError):
        calculate_dcf(
            free_cash_flows=pd.Series([100.0]),
            wacc=0.02,
            terminal_growth=0.03,
            total_debt=100.0,
            cash=50.0,
            shares_outstanding=100.0,
        )
