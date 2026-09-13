from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body_detector import (
    MAX_NORMAL_CUP_DEPTH_PCT,
    MIN_BOTTOM_CONTIGUITY_RATIO,
    MIN_BOTTOM_SESSIONS_WITHIN_5PCT,
    MIN_CUP_NO_HANDLE_DURATION_SESSIONS,
    MIN_MEANINGFUL_CUP_DEPTH_PCT,
    MIN_RIGHT_RIM_RECOVERY_RATIO,
    CupBodyFault,
    CupBodyState,
)

OPEN_RIGHT_EDGE_CNH_VERSION = "p8-open-right-edge-cnh-v0.3"


@dataclass(frozen=True, slots=True)
class OpenRightEdgeCupNoHandleObservation:
    left_rim: LandmarkCandidate
    trough: LandmarkCandidate
    asof_date: date
    duration_sessions: int
    depth_pct: float
    sessions_within_5pct_of_trough: int
    sessions_within_10pct_of_trough: int
    max_bottom_run_10pct: int
    observed_recovery_high: float
    recovery_to_left_rim_ratio: float
    state: CupBodyState
    faults: tuple[CupBodyFault, ...]


def _max_true_run(mask: list[bool]) -> int:
    best = current = 0
    for value in mask:
        if value:
            current += 1
            best = max(best, current)
        else:
            current = 0
    return best


def observe_open_right_edge_cnh(
    frame: pd.DataFrame,
    left_rim: LandmarkCandidate,
    trough: LandmarkCandidate,
    *,
    asof_date: date,
) -> OpenRightEdgeCupNoHandleObservation:
    if left_rim.type != LandmarkType.SWING_HIGH or trough.type != LandmarkType.SWING_LOW:
        raise ValueError("open-right-edge CNH requires SWING_HIGH -> SWING_LOW")
    if not left_rim.price_date < trough.price_date <= asof_date:
        raise ValueError("open-right-edge CNH landmarks are not chronological")
    if max(left_rim.confirmed_date, trough.confirmed_date) > asof_date:
        raise ValueError("open-right-edge CNH uses evidence not known by asof_date")
    if trough.price >= left_rim.price:
        raise ValueError("cup trough must be below left rim")

    required = {"date", "high", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")
    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("open-right-edge CNH received future bars")
    index = {value: i for i, value in enumerate(dates.tolist())}
    if left_rim.price_date not in index or trough.price_date not in index or asof_date not in index:
        raise ValueError("required CNH date missing from frame")

    li, ti, ai = index[left_rim.price_date], index[trough.price_date], index[asof_date]
    if not li < ti <= ai:
        raise ValueError("open-right-edge CNH indices are not chronological")

    region = ordered.iloc[li : ai + 1].copy()
    closes = pd.to_numeric(region["close"], errors="raise").astype(float)
    highs = pd.to_numeric(ordered.iloc[ti : ai + 1]["high"], errors="raise").astype(float)
    if (closes <= 0).any() or (highs <= 0).any():
        raise ValueError("prices must be positive")

    depth = (left_rim.price - trough.price) / left_rim.price
    within_5 = (closes <= trough.price * 1.05).tolist()
    within_10 = (closes <= trough.price * 1.10).tolist()
    observed_recovery_high = float(highs.max())
    recovery_ratio = observed_recovery_high / left_rim.price
    duration = ai - li + 1

    faults: list[CupBodyFault] = []
    if duration < MIN_CUP_NO_HANDLE_DURATION_SESSIONS:
        faults.append(CupBodyFault.TOO_SHORT)
    if depth > MAX_NORMAL_CUP_DEPTH_PCT:
        faults.append(CupBodyFault.TOO_DEEP)

    hard_faults = {CupBodyFault.TOO_SHORT, CupBodyFault.TOO_DEEP}
    if not any(f in hard_faults for f in faults):
        if depth < MIN_MEANINGFUL_CUP_DEPTH_PCT:
            faults.append(CupBodyFault.SHALLOW_NON_CUP)
        if sum(within_5) < MIN_BOTTOM_SESSIONS_WITHIN_5PCT:
            faults.append(CupBodyFault.SHARP_V)
        continuity = _max_true_run(within_10) / sum(within_10) if sum(within_10) else 0.0
        if continuity < MIN_BOTTOM_CONTIGUITY_RATIO:
            faults.append(CupBodyFault.FRAGMENTED_BOTTOM)
        if recovery_ratio < MIN_RIGHT_RIM_RECOVERY_RATIO:
            faults.append(CupBodyFault.WEAK_RIGHT_RIM_RECOVERY)

    if any(f in hard_faults for f in faults) or CupBodyFault.SHALLOW_NON_CUP in faults:
        state = CupBodyState.REJECTED
    elif any(
        f in {
            CupBodyFault.SHARP_V,
            CupBodyFault.FRAGMENTED_BOTTOM,
            CupBodyFault.WEAK_RIGHT_RIM_RECOVERY,
        }
        for f in faults
    ):
        state = CupBodyState.AMBIGUOUS
    else:
        state = CupBodyState.RECOGNIZED

    return OpenRightEdgeCupNoHandleObservation(
        left_rim=left_rim,
        trough=trough,
        asof_date=asof_date,
        duration_sessions=duration,
        depth_pct=depth,
        sessions_within_5pct_of_trough=sum(within_5),
        sessions_within_10pct_of_trough=sum(within_10),
        max_bottom_run_10pct=_max_true_run(within_10),
        observed_recovery_high=observed_recovery_high,
        recovery_to_left_rim_ratio=recovery_ratio,
        state=state,
        faults=tuple(faults),
    )


def enumerate_open_right_edge_cnh(
    frame: pd.DataFrame,
    landmarks: list[LandmarkCandidate],
    *,
    asof_date: date,
) -> list[OpenRightEdgeCupNoHandleObservation]:
    """Enumerate only cups whose post-trough structural right edge is still open.

    Once a later confirmed P1 swing high exists after a trough, that cup has a
    structural recovery/right-rim candidate and must be evaluated through the
    confirmed cup-body path. Extending the same old trough to the current as-of
    horizon would create a false lifecycle/state collision.
    """
    known = [item for item in landmarks if item.confirmed_date <= asof_date]
    highs = [item for item in known if item.type == LandmarkType.SWING_HIGH]
    lows = [item for item in known if item.type == LandmarkType.SWING_LOW]
    out: list[OpenRightEdgeCupNoHandleObservation] = []
    for high in highs:
        for low in lows:
            if low.price_date <= high.price_date:
                continue
            if any(later.price_date > low.price_date for later in highs):
                continue
            try:
                out.append(observe_open_right_edge_cnh(frame, high, low, asof_date=asof_date))
            except ValueError:
                continue
    return out
