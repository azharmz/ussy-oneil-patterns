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
    median_close_position_in_cup: float | None = None
    fraction_closes_at_or_above_cup_midpoint: float | None = None
    minimum_close_position_in_cup: float | None = None
    normalized_close_slope: float | None = None
    handle_to_pre20_median_volume_ratio: float | None = None


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

    median_position = fraction_upper = minimum_position = normalized_slope = None
    volume_ratio = None
    handle_frame = frame.iloc[hi : ai + 1]
    closes = pd.to_numeric(handle_frame["close"], errors="raise").astype(float)
    cup_range = cup.left_rim.price - cup.trough.price
    if cup_range > 0 and not closes.empty:
        positions = (closes - cup.trough.price) / cup_range
        median_position = float(positions.median())
        fraction_upper = float((closes >= cup_midpoint).mean())
        minimum_position = float(positions.min())
        if len(closes) > 1:
            x = pd.Series(range(len(closes)), dtype=float)
            x_centered = x - x.mean()
            y_centered = closes.reset_index(drop=True) - closes.mean()
            denom = float((x_centered * x_centered).sum())
            if denom > 0 and cup.right_rim.price > 0:
                normalized_slope = float((x_centered * y_centered).sum() / denom / cup.right_rim.price)
    if "volume" in frame.columns and hi >= 20:
        pre = frame.iloc[hi - 20 : hi]
        pre_med = float(pd.to_numeric(pre["volume"], errors="raise").median())
        handle_med = float(pd.to_numeric(handle_frame["volume"], errors="raise").median())
        if pre_med > 0:
            volume_ratio = handle_med / pre_med

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
        median_close_position_in_cup=median_position,
        fraction_closes_at_or_above_cup_midpoint=fraction_upper,
        minimum_close_position_in_cup=minimum_position,
        normalized_close_slope=normalized_slope,
        handle_to_pre20_median_volume_ratio=volume_ratio,
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
