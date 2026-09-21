from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Mapping

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from .cup_body import CupBodyGeometry
from .cup_body_detector import CupBodyAssessment, CupBodyState

MIN_HANDLE_DURATION_SESSIONS = 5
NORMAL_MAX_HANDLE_DEPTH_PCT = 0.12


@dataclass(frozen=True, slots=True)
class HandleGeometry:
    # Under the current landmark-first sequence, the cup right rim is also the
    # structural high immediately preceding the handle pullback. Persist that
    # role explicitly so downstream pivot logic does not have to infer it again.
    handle_high: LandmarkCandidate
    handle_low: LandmarkCandidate
    handle_recovery: LandmarkCandidate
    confirmed_date: date
    duration_sessions: int
    depth_pct: float
    cup_midpoint_price: float
    low_in_upper_half: bool
    recovery_to_right_rim_ratio: float
    median_close_position_in_cup: float | None = None
    fraction_closes_at_or_above_cup_midpoint: float | None = None
    minimum_close_position_in_cup: float | None = None
    normalized_close_slope: float | None = None
    handle_to_pre20_median_volume_ratio: float | None = None

    def __post_init__(self) -> None:
        if self.handle_high.type != LandmarkType.SWING_HIGH:
            raise ValueError("handle_high must be SWING_HIGH")
        if self.handle_low.type != LandmarkType.SWING_LOW:
            raise ValueError("handle_low must be SWING_LOW")
        if self.handle_recovery.type != LandmarkType.SWING_HIGH:
            raise ValueError("handle_recovery must be SWING_HIGH")
        if not self.handle_high.price_date < self.handle_low.price_date < self.handle_recovery.price_date:
            raise ValueError("handle landmarks must be high-low-high in chronological order")


class HandleState(str, Enum):
    RECOGNIZED = "HANDLE_RECOGNIZED"
    REJECTED = "HANDLE_REJECTED"
    AMBIGUOUS = "HANDLE_AMBIGUOUS"


class HandleFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    BELOW_CUP_MIDPOINT = "BELOW_CUP_MIDPOINT"
    DEEP_HANDLE_EXCEPTIONAL = "DEEP_HANDLE_EXCEPTIONAL"


@dataclass(frozen=True, slots=True)
class HandleAssessment:
    state: HandleState
    faults: tuple[HandleFault, ...]
    geometry: HandleGeometry


class CupFamilyState(str, Enum):
    CUP_WITH_HANDLE = "CUP_WITH_HANDLE"
    CUP_NO_HANDLE = "CUP_NO_HANDLE"
    CUP_HANDLE_AMBIGUOUS = "CUP_HANDLE_AMBIGUOUS"
    CUP_FAMILY_INCOMPLETE = "CUP_FAMILY_INCOMPLETE"
    NOT_A_RECOGNIZED_CUP = "NOT_A_RECOGNIZED_CUP"


def build_handle_geometry(
    cup: CupBodyGeometry,
    session_index: Mapping[date, int],
    handle_low: LandmarkCandidate,
    handle_recovery: LandmarkCandidate,
    frame=None,
) -> HandleGeometry:
    if handle_low.type != LandmarkType.SWING_LOW:
        raise ValueError("handle_low must be SWING_LOW")
    if handle_recovery.type != LandmarkType.SWING_HIGH:
        raise ValueError("handle_recovery must be SWING_HIGH")

    # The existing native sequence is RIGHT_RIM(HIGH) -> HANDLE_LOW(LOW) ->
    # HANDLE_RECOVERY(HIGH). No additional high is hidden between right rim and
    # handle low in this landmark representation, so RIGHT_RIM is the persisted
    # HANDLE_HIGH role for the current contract. This is additive role
    # persistence; it does not change detector thresholds or rediscover extrema.
    handle_high = cup.right_rim
    marks = (handle_high, handle_low, handle_recovery)
    for mark in marks:
        if mark.price_date not in session_index:
            raise ValueError(f"landmark date missing from session index: {mark.price_date}")

    hi0, li, hi1 = (session_index[mark.price_date] for mark in marks)
    if not hi0 < li < hi1:
        raise ValueError("handle must occur after right rim in high-low-high order")
    if handle_low.price >= handle_high.price:
        raise ValueError("handle low must be below handle high")

    cup_midpoint = cup.trough.price + (cup.left_rim.price - cup.trough.price) / 2.0
    depth = (handle_high.price - handle_low.price) / handle_high.price

    # Additive vNext research evidence. State semantics below remain unchanged.
    median_position = fraction_upper = minimum_position = normalized_slope = None
    volume_ratio = None
    if frame is not None:
        import pandas as pd
        region = frame.copy()
        region_dates = pd.to_datetime(region["date"], errors="raise").dt.date
        mask = (region_dates >= handle_high.price_date) & (region_dates <= handle_recovery.price_date)
        handle_frame = region.loc[mask]
        closes = pd.to_numeric(handle_frame["close"], errors="raise").astype(float)
        cup_range = cup.left_rim.price - cup.trough.price
        positions = (closes - cup.trough.price) / cup_range
        median_position = float(positions.median())
        fraction_upper = float((closes >= cup_midpoint).mean())
        minimum_position = float(positions.min())
        if len(closes) > 1:
            normalized_slope = float((closes.iloc[-1] - closes.iloc[0]) / handle_high.price / (len(closes) - 1))
        if "volume" in region.columns:
            hi = region.index[region_dates == handle_high.price_date][0]
            pre = region.loc[region.index < hi].tail(20)
            if len(pre) >= 5:
                pre_med = float(pd.to_numeric(pre["volume"], errors="raise").median())
                handle_med = float(pd.to_numeric(handle_frame["volume"], errors="raise").median())
                if pre_med > 0:
                    volume_ratio = handle_med / pre_med

    return HandleGeometry(
        handle_high=handle_high,
        handle_low=handle_low,
        handle_recovery=handle_recovery,
        confirmed_date=max(cup.confirmed_date, handle_low.confirmed_date, handle_recovery.confirmed_date),
        duration_sessions=hi1 - hi0 + 1,
        depth_pct=depth,
        cup_midpoint_price=cup_midpoint,
        low_in_upper_half=handle_low.price >= cup_midpoint,
        recovery_to_right_rim_ratio=handle_recovery.price / handle_high.price,
        median_close_position_in_cup=median_position,
        fraction_closes_at_or_above_cup_midpoint=fraction_upper,
        minimum_close_position_in_cup=minimum_position,
        normalized_close_slope=normalized_slope,
        handle_to_pre20_median_volume_ratio=volume_ratio,
    )


def assess_handle(handle: HandleGeometry) -> HandleAssessment:
    faults: list[HandleFault] = []
    if handle.duration_sessions < MIN_HANDLE_DURATION_SESSIONS:
        faults.append(HandleFault.TOO_SHORT)
    if not handle.low_in_upper_half:
        faults.append(HandleFault.BELOW_CUP_MIDPOINT)

    if HandleFault.TOO_SHORT in faults or HandleFault.BELOW_CUP_MIDPOINT in faults:
        return HandleAssessment(HandleState.REJECTED, tuple(faults), handle)

    if handle.depth_pct > NORMAL_MAX_HANDLE_DEPTH_PCT:
        faults.append(HandleFault.DEEP_HANDLE_EXCEPTIONAL)
        return HandleAssessment(HandleState.AMBIGUOUS, tuple(faults), handle)

    return HandleAssessment(HandleState.RECOGNIZED, tuple(faults), handle)


def classify_cup_family(
    cup: CupBodyAssessment,
    handle: HandleAssessment | None,
    *,
    right_edge_context_complete: bool,
) -> CupFamilyState:
    if cup.state != CupBodyState.RECOGNIZED:
        return CupFamilyState.NOT_A_RECOGNIZED_CUP

    if handle is None:
        return (
            CupFamilyState.CUP_NO_HANDLE
            if right_edge_context_complete
            else CupFamilyState.CUP_FAMILY_INCOMPLETE
        )

    if handle.state == HandleState.RECOGNIZED:
        return CupFamilyState.CUP_WITH_HANDLE
    if handle.state == HandleState.AMBIGUOUS:
        return CupFamilyState.CUP_HANDLE_AMBIGUOUS

    # A malformed handle attempt does not invalidate the already-recognized cup
    # body, but it also must not be silently labelled Cup-without-handle.
    return CupFamilyState.CUP_HANDLE_AMBIGUOUS
