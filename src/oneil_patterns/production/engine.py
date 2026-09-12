from __future__ import annotations

from datetime import date

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.adapters import (
    normalize_ascending_base,
    normalize_base_on_base,
    normalize_cup_body,
    normalize_cup_family,
    normalize_double_bottom,
    normalize_flat_base,
    normalize_handle,
)
from oneil_patterns.morphology.ascending_base import build_ascending_base_geometry
from oneil_patterns.morphology.ascending_base_detector import assess_ascending_base
from oneil_patterns.morphology.base_on_base import (
    BaseRegionSummary,
    assess_base_on_base,
    build_base_on_base_geometry,
)
from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.morphology.cup_body_detector import CupBodyState, assess_cup_body
from oneil_patterns.morphology.cup_family import (
    CupFamilyState,
    assess_handle,
    build_handle_geometry,
    classify_cup_family,
)
from oneil_patterns.morphology.double_bottom import build_double_bottom_geometry
from oneil_patterns.morphology.double_bottom_detector import assess_double_bottom
from oneil_patterns.morphology.flat_base import FlatBaseState, assess_flat_base
from oneil_patterns.segmentation.segmenter import segment_base_candidates
from .output import ProductionAssessmentRecord


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {d: i for i, d in enumerate(dates)}


def _record(
    *,
    security_id: str,
    ticker: str,
    asof_date: date,
    envelope,
    start: date | None,
    end: date | None,
    confirmed: date | None,
) -> ProductionAssessmentRecord:
    return ProductionAssessmentRecord.from_envelope(
        security_id=security_id,
        ticker=ticker,
        asof_date=asof_date,
        envelope=envelope,
        structural_start=start,
        structural_end=end,
        confirmed_date=confirmed,
    )


def analyze_security(
    security_id: str,
    ticker: str,
    frame: pd.DataFrame,
    asof_date: date,
) -> list[ProductionAssessmentRecord]:
    """Run the frozen first-pass morphology stack on one PIT-safe security slice."""
    if frame.empty:
        return []

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("analyze_security received future bars")

    primary = extract_excursion_landmarks(ordered)
    auxiliary = extract_confirmed_window_landmarks(ordered)
    candidates = fuse_landmark_sources(ordered, primary, auxiliary)
    candidates = [c for c in candidates if c.confirmed_date <= asof_date]
    candidates.sort(key=lambda c: (c.price_date, c.confirmed_date, c.type.value))
    index = _session_index(ordered)

    records: list[ProductionAssessmentRecord] = []
    recognized_components: list[BaseRegionSummary] = []

    segments = segment_base_candidates(ordered, candidates, asof_date=asof_date)
    for segment in segments:
        flat = assess_flat_base(ordered, segment)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_flat_base(flat), start=segment.start_date,
            end=segment.end_date, confirmed=segment.confirmed_date,
        ))
        if flat.state == FlatBaseState.RECOGNIZED:
            region_dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
            region = ordered.loc[(region_dates >= segment.start_date) & (region_dates <= segment.end_date)]
            recognized_components.append(BaseRegionSummary(
                pattern="FLAT_BASE", start_date=segment.start_date,
                end_date=segment.end_date, confirmed_date=segment.confirmed_date,
                high_price=float(region["high"].max()), low_price=float(region["low"].min()),
            ))

    for i in range(len(candidates) - 4):
        marks = candidates[i : i + 5]
        expected = [LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH]
        if [m.type for m in marks] != expected:
            continue
        try:
            geometry = build_double_bottom_geometry(index, *marks)
        except ValueError as exc:
            # Alternating turns are necessary but not sufficient for a DB.
            # Geometry can be inapplicable, e.g. a later higher-low already sits
            # above the first peak in a strong stair-step advance. That is a
            # non-candidate for DB, not a fatal batch error.
            if "trough cannot exceed left high" in str(exc):
                continue
            raise
        assessment = assess_double_bottom(geometry)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_double_bottom(assessment), start=marks[0].price_date,
            end=marks[3].price_date, confirmed=geometry.confirmed_date,
        ))

    for i in range(len(candidates) - 2):
        body_marks = candidates[i : i + 3]
        if [m.type for m in body_marks] != [LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH]:
            continue
        geometry = build_cup_body_geometry(ordered, *body_marks)
        body = assess_cup_body(geometry)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_cup_body(body), start=body_marks[0].price_date,
            end=body_marks[2].price_date, confirmed=geometry.confirmed_date,
        ))
        if body.state != CupBodyState.RECOGNIZED:
            continue

        handle_assessment = None
        family_end = body_marks[2].price_date
        family_confirmed = geometry.confirmed_date
        if i + 4 < len(candidates):
            handle_marks = candidates[i + 3 : i + 5]
            if [m.type for m in handle_marks] == [LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH]:
                handle_geometry = build_handle_geometry(geometry, index, *handle_marks)
                handle_assessment = assess_handle(handle_geometry)
                records.append(_record(
                    security_id=security_id, ticker=ticker, asof_date=asof_date,
                    envelope=normalize_handle(handle_assessment), start=body_marks[2].price_date,
                    end=handle_marks[1].price_date, confirmed=handle_geometry.confirmed_date,
                ))
                family_end = handle_marks[1].price_date
                family_confirmed = handle_geometry.confirmed_date

        family_state = classify_cup_family(body, handle_assessment, right_edge_context_complete=False)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_cup_family(family_state), start=body_marks[0].price_date,
            end=family_end, confirmed=family_confirmed,
        ))
        if family_state == CupFamilyState.CUP_WITH_HANDLE:
            region_dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
            region = ordered.loc[(region_dates >= body_marks[0].price_date) & (region_dates <= family_end)]
            recognized_components.append(BaseRegionSummary(
                pattern="CUP_WITH_HANDLE", start_date=body_marks[0].price_date,
                end_date=family_end, confirmed_date=family_confirmed,
                high_price=float(region["high"].max()), low_price=float(region["low"].min()),
            ))

    for i in range(len(candidates) - 6):
        marks = candidates[i : i + 7]
        expected = [LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW, LandmarkType.SWING_HIGH]
        if [m.type for m in marks] != expected:
            continue
        geometry = build_ascending_base_geometry(index, *marks)
        assessment = assess_ascending_base(geometry)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_ascending_base(assessment), start=marks[0].price_date,
            end=marks[-1].price_date, confirmed=geometry.confirmed_date,
        ))

    recognized_components.sort(key=lambda b: (b.start_date, b.end_date, b.pattern))
    for first, second in zip(recognized_components, recognized_components[1:]):
        if first.start_date >= second.start_date or first.end_date >= second.end_date:
            continue
        geometry = build_base_on_base_geometry(ordered, first, second)
        assessment = assess_base_on_base(geometry)
        records.append(_record(
            security_id=security_id, ticker=ticker, asof_date=asof_date,
            envelope=normalize_base_on_base(assessment), start=first.start_date,
            end=second.end_date, confirmed=geometry.confirmed_date,
        ))

    by_id = {record.assessment_id: record for record in records}
    return [by_id[key] for key in sorted(by_id)]
