from __future__ import annotations

from dataclasses import replace
from datetime import date

import pandas as pd

from oneil_patterns.landmarks.boundary import to_candidate_with_boundary
from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.confirmed_window import ConfirmedWindowParams, extract_confirmed_window_landmarks
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import HandleGeometry, build_handle_geometry
from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry, build_double_bottom_geometry
from oneil_patterns.segmentation.model import BaseSegmentCandidate
from oneil_patterns.segmentation.segmenter import _build_segment

STRUCTURAL_ASSEMBLY_VERSION = "p8-structural-assembly-v0.2"
DB_LOCAL_TURN_ASSEMBLY_VERSION = "p8-db-local-turn-v0.1"


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    if frame.empty:
        return {}
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    if len(dates) != len(set(dates)):
        raise ValueError("frame contains duplicate dates")
    return {value: i for i, value in enumerate(dates)}


def _known_landmarks(frame, landmarks, *, asof_date):
    index = _session_index(frame)
    known = [item for item in landmarks if item.confirmed_date <= asof_date and item.price_date in index]
    known.sort(key=lambda item: (item.price_date, item.confirmed_date, item.type.value, item.price))
    return known, index


def assemble_multiturn_segments(frame, landmarks, *, asof_date):
    known, index = _known_landmarks(frame, landmarks, asof_date=asof_date)
    highs = [item for item in known if item.type == LandmarkType.SWING_HIGH]
    lows = [item for item in known if item.type == LandmarkType.SWING_LOW]
    out = {}
    for start in highs:
        for recovery in highs:
            if recovery.price_date <= start.price_date:
                continue
            between = [low for low in lows if start.price_date < low.price_date < recovery.price_date and low.confirmed_date <= recovery.confirmed_date]
            if not between:
                continue
            trough = min(between, key=lambda item: (item.price, item.price_date, item.confirmed_date))
            if trough.price >= start.price or recovery.price < trough.price:
                continue
            try:
                segment = _build_segment(index, start, trough, recovery, asof_date=asof_date)
            except ValueError:
                continue
            segment = replace(segment, evidence={**dict(segment.evidence), "structural_assembly_version": STRUCTURAL_ASSEMBLY_VERSION, "assembly_mode": "MULTITURN_HIGH_DEEPEST_LOW_HIGH", "intervening_landmarks_allowed": True})
            out[(start.price_date, trough.price_date, recovery.price_date)] = segment
    return [out[key] for key in sorted(out)]


def assemble_multiturn_double_bottoms(frame, landmarks, *, asof_date):
    known, index = _known_landmarks(frame, landmarks, asof_date=asof_date)
    highs = [item for item in known if item.type == LandmarkType.SWING_HIGH]
    lows = [item for item in known if item.type == LandmarkType.SWING_LOW]
    out = {}
    for trough_1 in lows:
        for trough_2 in lows:
            if trough_2.price_date <= trough_1.price_date:
                continue
            middle_highs = [high for high in highs if trough_1.price_date < high.price_date < trough_2.price_date and high.confirmed_date <= trough_2.confirmed_date]
            if not middle_highs:
                continue
            middle_peak = max(middle_highs, key=lambda item: (item.price, -index[item.price_date], item.price_date))
            for left_high in highs:
                if left_high.price_date >= trough_1.price_date or left_high.confirmed_date > trough_1.confirmed_date:
                    continue
                try:
                    geometry = build_double_bottom_geometry(index, left_high, trough_1, middle_peak, trough_2, None)
                except ValueError:
                    continue
                key = (left_high.price_date, trough_1.price_date, middle_peak.price_date, trough_2.price_date)
                out[key] = geometry
    return [out[key] for key in sorted(out)]


def assemble_local_turn_double_bottoms(frame: pd.DataFrame, *, asof_date: date) -> list[DoubleBottomGeometry]:
    """Broad, PIT-safe W candidate source for shallow structures.

    P1's frozen 8% excursion scale can omit legitimate shallow Double Bottoms.
    This DEVELOPMENT-only auxiliary uses strict three-session local extrema with
    no amplitude floor. The extrema are still causal: each turn is knowable only
    after three later sessions. No source label is consulted and all morphology
    gates remain downstream.
    """
    raw = extract_confirmed_window_landmarks(
        frame,
        ConfirmedWindowParams(confirm_sessions=3, min_excursion_pct=0.0),
    )
    candidates: list[LandmarkCandidate] = []
    for mark in raw:
        if mark.confirmed_date > asof_date:
            continue
        prominence = mark.evidence.get("prominence_pct")
        candidate = to_candidate_with_boundary(
            frame,
            mark,
            prominence_pct=float(prominence) if prominence is not None else None,
        )
        candidate = LandmarkCandidate.from_landmark(
            mark,
            amplitude_pct=candidate.amplitude_pct,
            prominence_pct=candidate.prominence_pct,
            separation_sessions=candidate.separation_sessions,
            boundary=candidate.boundary,
            extra_evidence={
                **candidate.evidence,
                "p8_auxiliary_role": "DOUBLE_BOTTOM_LOCAL_TURN",
                "p8_auxiliary_version": DB_LOCAL_TURN_ASSEMBLY_VERSION,
            },
        )
        candidates.append(candidate)

    geometries = assemble_multiturn_double_bottoms(frame, candidates, asof_date=asof_date)
    highs = [item for item in candidates if item.type == LandmarkType.SWING_HIGH and item.confirmed_date <= asof_date]
    out: list[DoubleBottomGeometry] = []
    for geometry in geometries:
        right_edge_open = not any(item.price_date > geometry.trough_2.price_date for item in highs)
        out.append(
            replace(
                geometry,
                evidence={
                    **dict(geometry.evidence),
                    "p8_auxiliary_version": DB_LOCAL_TURN_ASSEMBLY_VERSION,
                    "p8_local_right_edge_open": right_edge_open,
                },
            )
        )
    return out


def assemble_handle_geometries(frame, cup, landmarks, *, asof_date):
    known, index = _known_landmarks(frame, landmarks, asof_date=asof_date)
    lows = [item for item in known if item.type == LandmarkType.SWING_LOW and item.price_date > cup.right_rim.price_date]
    highs = [item for item in known if item.type == LandmarkType.SWING_HIGH]
    out = {}
    for low in lows:
        recoveries = [high for high in highs if high.price_date > low.price_date and high.confirmed_date <= asof_date]
        if not recoveries:
            continue
        recovery = min(recoveries, key=lambda item: (item.price_date, item.confirmed_date, item.price))
        try:
            handle = build_handle_geometry(cup, index, low, recovery)
        except ValueError:
            continue
        out[(low.price_date, recovery.price_date)] = handle
    return [out[key] for key in sorted(out)]
