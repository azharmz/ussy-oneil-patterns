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
    handle_low: LandmarkCandidate
    handle_recovery: LandmarkCandidate
    confirmed_date: date
    duration_sessions: int
    depth_pct: float
    cup_midpoint_price: float
    low_in_upper_half: bool
    recovery_to_right_rim_ratio: float


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
) -> HandleGeometry:
    if handle_low.type != LandmarkType.SWING_LOW:
        raise ValueError("handle_low must be SWING_LOW")
    if handle_recovery.type != LandmarkType.SWING_HIGH:
        raise ValueError("handle_recovery must be SWING_HIGH")

    marks = (cup.right_rim, handle_low, handle_recovery)
    for mark in marks:
        if mark.price_date not in session_index:
            raise ValueError(f"landmark date missing from session index: {mark.price_date}")

    ri, li, hi = (session_index[mark.price_date] for mark in marks)
    if not ri < li < hi:
        raise ValueError("handle must occur after right rim in high-low-high order")
    if handle_low.price >= cup.right_rim.price:
        raise ValueError("handle low must be below right rim")

    cup_midpoint = cup.trough.price + (cup.left_rim.price - cup.trough.price) / 2.0
    depth = (cup.right_rim.price - handle_low.price) / cup.right_rim.price

    return HandleGeometry(
        handle_low=handle_low,
        handle_recovery=handle_recovery,
        confirmed_date=max(cup.confirmed_date, handle_low.confirmed_date, handle_recovery.confirmed_date),
        duration_sessions=hi - ri + 1,
        depth_pct=depth,
        cup_midpoint_price=cup_midpoint,
        low_in_upper_half=handle_low.price >= cup_midpoint,
        recovery_to_right_rim_ratio=handle_recovery.price / cup.right_rim.price,
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
