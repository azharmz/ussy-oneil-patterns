from __future__ import annotations

from datetime import date
import hashlib

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.ascending_base import build_ascending_base_geometry
from oneil_patterns.morphology.ascending_base_detector import MAX_DURATION_SESSIONS, assess_ascending_base
from oneil_patterns.morphology.base_on_base import (
    BaseRegionSummary,
    assess_base_on_base,
    build_base_on_base_geometry,
)
from oneil_patterns.validation.canonical_predictions import extract_core_morphology_predictions
from oneil_patterns.validation.source_dimension_eval import MorphologyPrediction

ADVANCED_PREDICTION_ADAPTER_VERSION = "p6-advanced-prediction-adapter-v0.1"
_ASCENDING_SEQUENCE = (
    LandmarkType.SWING_HIGH,
    LandmarkType.SWING_LOW,
    LandmarkType.SWING_HIGH,
    LandmarkType.SWING_LOW,
    LandmarkType.SWING_HIGH,
    LandmarkType.SWING_LOW,
    LandmarkType.SWING_HIGH,
)
_CORE_COMPONENT_PATTERNS = {
    "FLAT_BASE",
    "DOUBLE_BOTTOM",
    "CUP_WITHOUT_HANDLE",
    "CUP_WITH_HANDLE",
}


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {d: i for i, d in enumerate(dates)}


def _candidate_id(pattern: str, *parts: str) -> str:
    payload = "|".join((ADVANCED_PREDICTION_ADAPTER_VERSION, pattern, *parts))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _canonical_landmarks(frame: pd.DataFrame, *, asof_date: date):
    primary = extract_excursion_landmarks(frame)
    auxiliary = extract_confirmed_window_landmarks(frame)
    landmarks = fuse_landmark_sources(frame, primary, auxiliary)
    landmarks = [item for item in landmarks if item.confirmed_date <= asof_date]
    landmarks.sort(key=lambda item: (item.price_date, item.confirmed_date, item.type.value))
    return landmarks


def _ascending_predictions(frame: pd.DataFrame, *, asof_date: date) -> list[MorphologyPrediction]:
    landmarks = _canonical_landmarks(frame, asof_date=asof_date)
    index = _session_index(frame)
    predictions: list[MorphologyPrediction] = []
    seen: set[tuple[date, ...]] = set()

    def extend(chosen: list, last_position: int, sequence_position: int) -> None:
        if sequence_position == len(_ASCENDING_SEQUENCE):
            dates = tuple(item.price_date for item in chosen)
            if dates in seen:
                return
            seen.add(dates)
            try:
                geometry = build_ascending_base_geometry(index, *chosen)
            except ValueError:
                return
            assessment = assess_ascending_base(geometry)
            pivot = geometry.peak_3
            predictions.append(
                MorphologyPrediction(
                    candidate_id=_candidate_id(
                        "ASCENDING_BASE",
                        *(item.isoformat() for item in dates),
                    ),
                    pattern="ASCENDING_BASE",
                    start_date=geometry.peak_1.price_date,
                    end_date=geometry.recovery_peak.price_date,
                    pivot_source_date=pivot.price_date,
                    pivot_level=float(pivot.price),
                    depth_pct=float(geometry.max_pullback_pct),
                    detector_status=assessment.state.value,
                    detector_faults=tuple(item.value for item in assessment.faults),
                    candidate_semantics=f"P1_ALTERNATING_SUBSEQUENCE:{ADVANCED_PREDICTION_ADAPTER_VERSION}",
                    structural_signature=tuple(
                        f"{mark.type.value}:{mark.price_date.isoformat()}" for mark in chosen
                    ),
                )
            )
            return

        expected = _ASCENDING_SEQUENCE[sequence_position]
        start_session = index[chosen[0].price_date] if chosen else None
        for position in range(last_position + 1, len(landmarks)):
            mark = landmarks[position]
            if mark.type != expected:
                continue
            if chosen:
                duration = index[mark.price_date] - start_session + 1
                if duration > MAX_DURATION_SESSIONS:
                    break
            extend(chosen + [mark], position, sequence_position + 1)

    for position, mark in enumerate(landmarks):
        if mark.type == _ASCENDING_SEQUENCE[0]:
            extend([mark], position, 1)

    predictions.sort(
        key=lambda item: (
            item.start_date,
            item.end_date or date.max,
            item.pivot_source_date or date.max,
            item.candidate_id,
        )
    )
    return predictions


def _region_summary(frame: pd.DataFrame, prediction: MorphologyPrediction) -> BaseRegionSummary:
    if prediction.end_date is None:
        raise ValueError("base-on-base component requires an end date")
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    mask = (dates >= prediction.start_date) & (dates <= prediction.end_date)
    region = frame.loc[mask]
    if region.empty:
        raise ValueError("component region is empty")
    high_col = "high" if "high" in region.columns else "close"
    low_col = "low" if "low" in region.columns else "close"
    high_price = float(pd.to_numeric(region[high_col], errors="raise").max())
    low_price = float(pd.to_numeric(region[low_col], errors="raise").min())
    return BaseRegionSummary(
        pattern=prediction.pattern,
        start_date=prediction.start_date,
        end_date=prediction.end_date,
        confirmed_date=prediction.end_date,
        high_price=high_price,
        low_price=low_price,
    )


def _is_recognized_core(prediction: MorphologyPrediction) -> bool:
    return (
        prediction.pattern in _CORE_COMPONENT_PATTERNS
        and prediction.end_date is not None
        and bool(prediction.detector_status)
        and prediction.detector_status.endswith("RECOGNIZED")
    )


def _base_on_base_predictions(frame: pd.DataFrame, *, asof_date: date) -> list[MorphologyPrediction]:
    core = [
        item
        for item in extract_core_morphology_predictions(frame, asof_date=asof_date)
        if _is_recognized_core(item)
    ]
    predictions: list[MorphologyPrediction] = []
    seen: set[tuple[str, str]] = set()

    for first in core:
        for second in core:
            if first.candidate_id == second.candidate_id:
                continue
            if not (
                first.start_date < second.start_date
                and first.end_date is not None
                and second.end_date is not None
                and first.end_date < second.end_date
            ):
                continue
            pair_key = (first.candidate_id, second.candidate_id)
            if pair_key in seen:
                continue
            seen.add(pair_key)

            try:
                geometry = build_base_on_base_geometry(
                    frame,
                    _region_summary(frame, first),
                    _region_summary(frame, second),
                )
            except ValueError:
                continue
            assessment = assess_base_on_base(geometry)
            predictions.append(
                MorphologyPrediction(
                    candidate_id=_candidate_id(
                        "BASE_ON_BASE",
                        first.candidate_id,
                        second.candidate_id,
                    ),
                    pattern="BASE_ON_BASE",
                    start_date=first.start_date,
                    end_date=second.end_date,
                    pivot_source_date=second.pivot_source_date,
                    pivot_level=second.pivot_level,
                    depth_pct=None,
                    detector_status=assessment.state.value,
                    detector_faults=tuple(item.value for item in assessment.faults),
                    candidate_semantics=(
                        f"CORE_COMPONENT_COMPOSITION:{ADVANCED_PREDICTION_ADAPTER_VERSION}:"
                        f"{first.pattern}->{second.pattern}"
                    ),
                    structural_signature=(
                        f"BASE1:{first.candidate_id}",
                        f"BASE2:{second.candidate_id}",
                    ),
                )
            )

    predictions.sort(
        key=lambda item: (
            item.start_date,
            item.end_date or date.max,
            item.pivot_source_date or date.max,
            item.candidate_id,
        )
    )
    return predictions


def extract_advanced_morphology_predictions(
    frame: pd.DataFrame,
    *,
    asof_date: date,
) -> list[MorphologyPrediction]:
    """Emit PIT-safe P6 advanced-pattern candidates without changing frozen core logic."""
    if frame.empty:
        return []

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("P6 advanced extractor received future bars")
    if asof_date not in set(dates):
        eligible = dates[dates <= asof_date]
        if eligible.empty:
            return []
        asof_date = eligible.iloc[-1]

    predictions = _ascending_predictions(ordered, asof_date=asof_date)
    predictions.extend(_base_on_base_predictions(ordered, asof_date=asof_date))
    predictions.sort(
        key=lambda item: (
            item.pattern,
            item.start_date,
            item.end_date or date.max,
            item.candidate_id,
        )
    )
    return predictions
