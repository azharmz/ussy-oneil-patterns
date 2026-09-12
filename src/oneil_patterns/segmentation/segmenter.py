from __future__ import annotations

from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from .model import BaseSegmentCandidate, SegmentStage


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    if frame.empty:
        return {}
    if "date" not in frame.columns:
        raise ValueError("frame missing required column: date")
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    if len(dates) != len(set(dates)):
        raise ValueError("frame contains duplicate dates")
    return {value: i for i, value in enumerate(dates)}


def _build_segment(
    frame_index: dict[date, int],
    start: LandmarkCandidate,
    trough: LandmarkCandidate,
    recovery: LandmarkCandidate | None,
    *,
    asof_date: date,
) -> BaseSegmentCandidate:
    if start.type != LandmarkType.SWING_HIGH or trough.type != LandmarkType.SWING_LOW:
        raise ValueError("segment must begin SWING_HIGH -> SWING_LOW")
    if recovery is not None and recovery.type != LandmarkType.SWING_HIGH:
        raise ValueError("recovery must be SWING_HIGH")

    start_idx = frame_index[start.price_date]
    trough_idx = frame_index[trough.price_date]
    end_mark = recovery or trough
    end_idx = frame_index[end_mark.price_date]
    if not start_idx < trough_idx <= end_idx:
        raise ValueError("segment landmarks are not chronological")

    decline_distance = start.price - trough.price
    depth = decline_distance / start.price
    if depth < 0:
        raise ValueError("trough price cannot exceed start price for a decline segment")
    if decline_distance == 0:
        raise ValueError("decline segment requires start price above trough price")

    decline_sessions = trough_idx - start_idx + 1
    recovery_sessions = None
    recovery_pct = None
    recovery_to_start_ratio = None
    recovered_depth_fraction = None
    if recovery is not None:
        recovery_distance = recovery.price - trough.price
        recovery_pct = recovery_distance / trough.price
        if recovery_pct < 0:
            raise ValueError("recovery high cannot be below trough price")
        recovery_sessions = end_idx - trough_idx + 1
        recovery_to_start_ratio = recovery.price / start.price
        recovered_depth_fraction = recovery_distance / decline_distance

    confirmed = max(
        start.confirmed_date,
        trough.confirmed_date,
        recovery.confirmed_date if recovery is not None else trough.confirmed_date,
    )
    if confirmed > asof_date:
        raise ValueError("segment uses landmark not known as of asof_date")

    stage = (
        SegmentStage.RECOVERY_CONFIRMED
        if recovery is not None
        else SegmentStage.DECLINE_CONFIRMED
    )

    return BaseSegmentCandidate(
        start=start,
        trough=trough,
        recovery=recovery,
        stage=stage,
        start_date=start.price_date,
        end_date=end_mark.price_date,
        confirmed_date=confirmed,
        duration_sessions=end_idx - start_idx + 1,
        decline_sessions=decline_sessions,
        recovery_sessions=recovery_sessions,
        depth_pct=depth,
        recovery_pct=recovery_pct,
        recovery_to_start_ratio=recovery_to_start_ratio,
        recovered_depth_fraction=recovered_depth_fraction,
        evidence={
            "contract": "p2-segmentation-draft-v1",
            "complete_recovery_turn": recovery is not None,
            "start_boundary": start.boundary,
            "trough_boundary": trough.boundary,
            "recovery_boundary": recovery.boundary if recovery is not None else None,
            "boundary_semantics": "structural_landmark_dates_not_asof_horizon",
            "feature_semantics": "p2-geometry-v1",
        },
    )


def segment_base_candidates(
    frame: pd.DataFrame,
    candidates: list[LandmarkCandidate],
    *,
    asof_date: date,
) -> list[BaseSegmentCandidate]:
    """Create morphology-neutral high -> low -> recovery base candidates.

    Only frozen P1 candidates confirmed by ``asof_date`` participate. P2 does
    not discover new extrema and does not assign Flat/DB/Cup labels. `asof_date`
    is an information cutoff only; it never becomes a structural segment edge.
    """
    index = _session_index(frame)
    known = [
        item
        for item in candidates
        if item.confirmed_date <= asof_date and item.price_date in index
    ]
    known.sort(key=lambda x: (x.price_date, x.confirmed_date, x.type.value))

    out: list[BaseSegmentCandidate] = []
    for i in range(len(known) - 1):
        start = known[i]
        trough = known[i + 1]
        if start.type != LandmarkType.SWING_HIGH or trough.type != LandmarkType.SWING_LOW:
            continue

        recovery = None
        if i + 2 < len(known) and known[i + 2].type == LandmarkType.SWING_HIGH:
            recovery = known[i + 2]

        out.append(
            _build_segment(index, start, trough, recovery, asof_date=asof_date)
        )
    return out
