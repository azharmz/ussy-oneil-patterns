from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from .model import Landmark, LandmarkType


@dataclass(frozen=True, slots=True)
class ExcursionParams:
    reversal_pct: float = 0.08
    min_separation_sessions: int = 3

    def __post_init__(self) -> None:
        if not 0 < self.reversal_pct < 1:
            raise ValueError("reversal_pct must be between 0 and 1")
        if self.min_separation_sessions < 1:
            raise ValueError("min_separation_sessions must be >= 1")


def _to_date(value) -> date:
    return pd.Timestamp(value).date()


def extract_excursion_landmarks(frame: pd.DataFrame, params: ExcursionParams | None = None) -> list[Landmark]:
    """Extract alternating structural extrema using causal percentage reversals."""
    params = params or ExcursionParams()
    required = {"date", "high", "low"}
    if not required.issubset(frame.columns):
        raise ValueError(f"frame missing required columns: {sorted(required - set(frame.columns))}")
    if frame.empty:
        return []

    data = frame.sort_values("date").reset_index(drop=True)
    if data["date"].duplicated().any():
        raise ValueError("duplicate dates are not allowed")

    landmarks: list[Landmark] = []
    mode = "seeking_peak"
    peak_idx = trough_idx = 0
    peak_price = float(data.loc[0, "high"])
    trough_price = float(data.loc[0, "low"])

    for i in range(1, len(data)):
        high = float(data.loc[i, "high"])
        low = float(data.loc[i, "low"])

        if mode == "seeking_peak":
            if high >= peak_price:
                peak_price, peak_idx = high, i
            decline = (peak_price - low) / peak_price
            if decline >= params.reversal_pct and i - peak_idx >= params.min_separation_sessions:
                landmarks.append(
                    Landmark(
                        type=LandmarkType.SWING_HIGH,
                        price=peak_price,
                        price_date=_to_date(data.loc[peak_idx, "date"]),
                        confirmed_date=_to_date(data.loc[i, "date"]),
                        method="percentage_excursion",
                        evidence={"reversal_pct": params.reversal_pct, "confirmation_index": i},
                    )
                )
                mode = "seeking_trough"
                trough_price, trough_idx = low, i
        else:
            if low <= trough_price:
                trough_price, trough_idx = low, i
            advance = (high - trough_price) / trough_price
            if advance >= params.reversal_pct and i - trough_idx >= params.min_separation_sessions:
                landmarks.append(
                    Landmark(
                        type=LandmarkType.SWING_LOW,
                        price=trough_price,
                        price_date=_to_date(data.loc[trough_idx, "date"]),
                        confirmed_date=_to_date(data.loc[i, "date"]),
                        method="percentage_excursion",
                        evidence={"reversal_pct": params.reversal_pct, "confirmation_index": i},
                    )
                )
                mode = "seeking_peak"
                peak_price, peak_idx = high, i

    return landmarks
