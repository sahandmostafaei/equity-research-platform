from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DCFAssumptions:
    revenue_growth: float
    ebitda_margin: float
    fcf_conversion: float
    wacc: float
    terminal_growth: float
    forecast_years: int = 5

    def validate(self) -> None:
        if self.forecast_years <= 0:
            raise ValueError(
                "Forecast years must be positive."
            )

        if self.wacc <= self.terminal_growth:
            raise ValueError(
                "WACC must be greater than terminal growth."
            )

        if self.fcf_conversion <= 0:
            raise ValueError(
                "FCF conversion must be positive."
            )

        if self.ebitda_margin <= 0:
            raise ValueError(
                "EBITDA margin must be positive."
            )


def create_default_dcf_assumptions() -> DCFAssumptions:
    assumptions = DCFAssumptions(
        revenue_growth=0.07,
        ebitda_margin=0.22,
        fcf_conversion=0.50,
        wacc=0.09,
        terminal_growth=0.025,
        forecast_years=5,
    )

    assumptions.validate()

    return assumptions
