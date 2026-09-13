from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date

import pandas as pd

from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry
from oneil_patterns.morphology.double_bottom_detector import (
    DoubleBottomFault,
    DoubleBottomState,
    assess_double_bottom,
)

OPEN_RIGHT_EDGE_DOUBLE_BOTTOM_VERSION = "p8-open-right-edge-double-bottom-v0.1"


@dataclass(frozen=True, slots=True)
class OpenRightEdgeDoubleBottomObservation:
    geometry: DoubleBottomGeometry
    asof_date: date
    observed_duration_sessions: int
    observed_recovery_high: float
    pivot_recovered: bool
    state: DoubleBottomState
    faults: tuple[DoubleBottomFault, ...]


def observe_open_right_edge_double_bottom(
    frame: pd.DataFrame,
    geometry: DoubleBottomGeometry,
    *,
    asof_date: date,
) -> OpenRightEdgeDoubleBottomObservation | None:
    """Observe base completion after trough 2 without fabricating a P1 high.

    The frozen core-W geometry remains unchanged. For DEVELOPMENT validation we
    separately measure elapsed base duration from the left high through T when
    price has recovered to at least the middle-peak pivot after trough 2.
    """
    required = {"date", "high"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("open-right-edge Double Bottom received future bars")
    index = {value: i for i, value in enumerate(dates.tolist())}

    for needed in (geometry.left_high.price_date, geometry.trough_2.price_date, asof_date):
        if needed not in index:
            raise ValueError(f"required Double Bottom date missing from frame: {needed}")
    if geometry.trough_2.confirmed_date > asof_date:
        raise ValueError("trough 2 was not confirmed by asof_date")

    li = index[geometry.left_high.price_date]
    ti = index[geometry.trough_2.price_date]
    ai = index[asof_date]
    if not li < ti <= ai:
        raise ValueError("open-right-edge Double Bottom dates are not chronological")

    post_trough_highs = pd.to_numeric(ordered.iloc[ti : ai + 1]["high"], errors="raise").astype(float)
    if (post_trough_highs <= 0).any():
        raise ValueError("prices must be positive")
    observed_recovery_high = float(post_trough_highs.max())
    pivot_recovered = observed_recovery_high >= float(geometry.middle_peak.price)
    if not pivot_recovered:
        return None

    observed_duration = ai - li + 1
    observation_geometry = replace(geometry, duration_sessions=observed_duration)
    assessment = assess_double_bottom(observation_geometry)

    return OpenRightEdgeDoubleBottomObservation(
        geometry=geometry,
        asof_date=asof_date,
        observed_duration_sessions=observed_duration,
        observed_recovery_high=observed_recovery_high,
        pivot_recovered=True,
        state=assessment.state,
        faults=assessment.faults,
    )
