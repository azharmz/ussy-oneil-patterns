from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import (
    MIN_HANDLE_DURATION_SESSIONS,
    NORMAL_MAX_HANDLE_DEPTH_PCT,
    HandleFault,
    HandleState,
)

OPEN_RIGHT_EDGE_HANDLE_VERSION = "p8-open-right-edge-handle-v0.1"


@dataclass(frozen=True, slots=True)
class OpenRightEdgeHandleObservation:
    cup: CupBodyGeometry
    handle_low: LandmarkCandidate
    asof_date: date
    duration_sessions: int
    depth_pct: float
    low_in_upper_half: bool
    state: HandleState
    faults: tuple[HandleFault, ...]


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    if len(dates) != len(set(dates)):
        raise ValueError("frame contains duplicate dates")
    return {value: i for i, value in enumerate(dates)}


def observe_open_right_edge_handle(
    frame: pd.DataFrame,
    cup: CupBodyGeometry,
    handle_low: LandmarkCandidate,
    *,
    asof_date: date,
) -> OpenRightEdgeHandleObservation:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("open-right-edge handle received future bars")
    if handle_low.type != LandmarkType.SWING_LOW:
        raise ValueError("open-right-edge handle requires a SWING_LOW")
    if handle_low.price_date <= cup.right_rim.price_date:
        raise ValueError("handle low must occur after cup right rim")
    if max(cup.confirmed_date, handle_low.confirmed_date) > asof_date:
        raise ValueError("open-right-edge handle uses evidence not known by asof_date")

    index = _session_index(frame)
    if cup.right_rim.price_date not in index or handle_low.price_date not in index or asof_date not in index:
        raise ValueError("required handle date missing from frame")
    hi = index[cup.right_rim.price_date]
    li = index[handle_low.price_date]
    ai = index[asof_date]
    if not hi < li <= ai:
        raise ValueError("open-right-edge handle dates are not chronological")
    if handle_low.price >= cup.right_rim.price:
        raise ValueError("handle low must be below handle high/right rim")

    duration = ai - hi + 1
    depth = (cup.right_rim.price - handle_low.price) / cup.right_rim.price
    cup_midpoint = cup.trough.price + (cup.left_rim.price - cup.trough.price) / 2.0
    low_in_upper_half = handle_low.price >= cup_midpoint

    faults: list[HandleFault] = []
    if duration < MIN_HANDLE_DURATION_SESSIONS:
        faults.append(HandleFault.TOO_SHORT)
    if not low_in_upper_half:
        faults.append(HandleFault.BELOW_CUP_MIDPOINT)

    if faults:
        state = HandleState.REJECTED
    elif depth > NORMAL_MAX_HANDLE_DEPTH_PCT:
        faults.append(HandleFault.DEEP_HANDLE_EXCEPTIONAL)
        state = HandleState.AMBIGUOUS
    else:
        state = HandleState.RECOGNIZED

    return OpenRightEdgeHandleObservation(
        cup=cup,
        handle_low=handle_low,
        asof_date=asof_date,
        duration_sessions=duration,
        depth_pct=depth,
        low_in_upper_half=low_in_upper_half,
        state=state,
        faults=tuple(faults),
    )


def enumerate_open_right_edge_handles(
    frame: pd.DataFrame,
    cup: CupBodyGeometry,
    landmarks: list[LandmarkCandidate],
    *,
    asof_date: date,
) -> list[OpenRightEdgeHandleObservation]:
    """Return post-rim lows that have no later confirmed recovery-high by T."""
    known = [item for item in landmarks if item.confirmed_date <= asof_date]
    highs = [item for item in known if item.type == LandmarkType.SWING_HIGH]
    lows = [
        item
        for item in known
        if item.type == LandmarkType.SWING_LOW and item.price_date > cup.right_rim.price_date
    ]

    out: list[OpenRightEdgeHandleObservation] = []
    for low in lows:
        if any(high.price_date > low.price_date for high in highs):
            continue
        try:
            out.append(observe_open_right_edge_handle(frame, cup, low, asof_date=asof_date))
        except ValueError:
            continue
    return out
