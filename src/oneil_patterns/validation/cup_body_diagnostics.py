from __future__ import annotations

from datetime import date

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.morphology.cup_body_detector import assess_cup_body
from oneil_patterns.segmentation.segmenter import segment_base_candidates

from .structural_assembly import assemble_multiturn_segments

CUP_BODY_DIAGNOSTIC_VERSION = "p8-cup-body-diagnostic-v0.2"


def _segment_key(segment) -> tuple:
    return (
        segment.start.price_date,
        segment.trough.price_date,
        segment.recovery.price_date if segment.recovery is not None else None,
        segment.stage.value,
    )


def extract_cup_body_diagnostics(frame: pd.DataFrame, *, asof_date: date) -> list[dict]:
    """Return all PIT-safe cup-body assessments before Cup-family filtering.

    Diagnostic records are not detector predictions and never enter source-match
    ranking. They expose why a structural high-low-high span was recognized,
    ambiguous, or rejected by the existing Cup-body contract.
    """
    if frame.empty:
        return []

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("cup-body diagnostics received future bars")
    if asof_date not in set(dates):
        eligible = dates[dates <= asof_date]
        if eligible.empty:
            return []
        asof_date = eligible.iloc[-1]

    primary = extract_excursion_landmarks(ordered)
    auxiliary = extract_confirmed_window_landmarks(ordered)
    landmarks = fuse_landmark_sources(ordered, primary, auxiliary)
    landmarks = [item for item in landmarks if item.confirmed_date <= asof_date]
    landmarks.sort(key=lambda item: (item.price_date, item.confirmed_date, item.type.value))

    atomic = segment_base_candidates(ordered, landmarks, asof_date=asof_date)
    multiturn = assemble_multiturn_segments(ordered, landmarks, asof_date=asof_date)
    segment_map = {_segment_key(item): item for item in atomic}
    for item in multiturn:
        segment_map.setdefault(_segment_key(item), item)

    records: list[dict] = []
    for key in sorted(segment_map, key=lambda value: tuple(x or date.max for x in value[:3]) + (value[3],)):
        segment = segment_map[key]
        if segment.recovery is None:
            continue
        geometry = build_cup_body_geometry(ordered, segment.start, segment.trough, segment.recovery)
        assessment = assess_cup_body(geometry)
        records.append(
            {
                "diagnostic_version": CUP_BODY_DIAGNOSTIC_VERSION,
                "left_rim_date": geometry.left_rim.price_date.isoformat(),
                "left_rim_price": geometry.left_rim.price,
                "trough_date": geometry.trough.price_date.isoformat(),
                "trough_price": geometry.trough.price,
                "right_rim_date": geometry.right_rim.price_date.isoformat(),
                "right_rim_price": geometry.right_rim.price,
                "duration_sessions": geometry.duration_sessions,
                "decline_sessions": geometry.decline_sessions,
                "recovery_sessions": geometry.recovery_sessions,
                "depth_pct": geometry.depth_pct,
                "right_rim_to_left_rim_ratio": geometry.right_rim_to_left_rim_ratio,
                "left_right_time_ratio": geometry.left_right_time_ratio,
                "sessions_within_5pct_of_trough": geometry.sessions_within_5pct_of_trough,
                "sessions_within_10pct_of_trough": geometry.sessions_within_10pct_of_trough,
                "bottom_dwell_5pct_fraction": geometry.sessions_within_5pct_of_trough / geometry.duration_sessions,
                "bottom_dwell_10pct_fraction": geometry.sessions_within_10pct_of_trough / geometry.duration_sessions,
                "lower_third_fraction": geometry.lower_third_fraction,
                "max_bottom_run_10pct": geometry.max_bottom_run_10pct,
                "bottom_continuity_10pct": (
                    geometry.max_bottom_run_10pct / geometry.sessions_within_10pct_of_trough
                    if geometry.sessions_within_10pct_of_trough
                    else 0.0
                ),
                "state": assessment.state.value,
                "faults": [item.value for item in assessment.faults],
                "theory_gates_pass": assessment.theory_gates_pass,
                "research_bands_pass": assessment.research_bands_pass,
            }
        )
    return records
