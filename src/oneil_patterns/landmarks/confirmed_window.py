from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from .model import Landmark, LandmarkType


@dataclass(frozen=True, slots=True)
class ConfirmedWindowParams:
    confirm_sessions: int = 3
    min_excursion_pct: float = 0.03

    def __post_init__(self) -> None:
        if self.confirm_sessions < 1:
            raise ValueError("confirm_sessions must be >= 1")
        if not 0 <= self.min_excursion_pct < 1:
            raise ValueError("min_excursion_pct must be in [0, 1)")


def _to_date(value) -> date:
    return pd.Timestamp(value).date()


def extract_confirmed_window_landmarks(
    frame: pd.DataFrame,
    params: ConfirmedWindowParams | None = None,
) -> list[Landmark]:
    """Confirm extrema only after `confirm_sessions` later bars have elapsed.

    This deliberately records the original extremum date separately from the
    first date on which the detector could know that no more extreme price
    occurred during the confirmation window.
    """
    params = params or ConfirmedWindowParams()
    required = {"date", "high", "low"}
    if not required.issubset(frame.columns):
        raise ValueError(f"frame missing required columns: {sorted(required - set(frame.columns))}")
    if frame.empty:
        return []

    data = frame.sort_values("date").reset_index(drop=True)
    if data["date"].duplicated().any():
        raise ValueError("duplicate dates are not allowed")

    out: list[Landmark] = []
    c = params.confirm_sessions
    for i in range(c, len(data) - c):
        left = data.iloc[i - c : i]
        right = data.iloc[i + 1 : i + c + 1]
        high = float(data.loc[i, "high"])
        low = float(data.loc[i, "low"])

        max_neighbor_high = max(float(left["high"].max()), float(right["high"].max()))
        min_neighbor_low = min(float(left["low"].min()), float(right["low"].min()))

        if high > max_neighbor_high:
            prominence = (high - max_neighbor_high) / high
            if prominence >= params.min_excursion_pct:
                out.append(
                    Landmark(
                        type=LandmarkType.SWING_HIGH,
                        price=high,
                        price_date=_to_date(data.loc[i, "date"]),
                        confirmed_date=_to_date(data.loc[i + c, "date"]),
                        method="confirmed_window",
                        evidence={
                            "confirm_sessions": c,
                            "min_excursion_pct": params.min_excursion_pct,
                            "prominence_pct": prominence,
                        },
                    )
                )

        if low < min_neighbor_low:
            prominence = (min_neighbor_low - low) / min_neighbor_low
            if prominence >= params.min_excursion_pct:
                out.append(
                    Landmark(
                        type=LandmarkType.SWING_LOW,
                        price=low,
                        price_date=_to_date(data.loc[i, "date"]),
                        confirmed_date=_to_date(data.loc[i + c, "date"]),
                        method="confirmed_window",
                        evidence={
                            "confirm_sessions": c,
                            "min_excursion_pct": params.min_excursion_pct,
                            "prominence_pct": prominence,
                        },
                    )
                )

    return sorted(out, key=lambda x: (x.confirmed_date, x.price_date, x.type.value))
