from __future__ import annotations

from datetime import date
import hashlib

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.morphology.cup_body_detector import CupBodyState, assess_cup_body
from oneil_patterns.morphology.cup_family import (
    MIN_HANDLE_DURATION_SESSIONS,
    HandleState,
    assess_handle,
)
from oneil_patterns.morphology.double_bottom_detector import assess_double_bottom
from oneil_patterns.morphology.flat_base import assess_flat_base
from oneil_patterns.segmentation.segmenter import segment_base_candidates

from .pivot_adapter import (
    cup_with_handle_pivot,
    cup_without_handle_pivot,
    double_bottom_pivot,
    flat_base_pivot,
)
from .source_dimension_eval import MorphologyPrediction
from .structural_assembly import (
    STRUCTURAL_ASSEMBLY_VERSION,
    assemble_handle_geometries,
    assemble_multiturn_double_bottoms,
    assemble_multiturn_segments,
)

PREDICTION_ADAPTER_VERSION = "p8-canonical-prediction-adapter-v0.3.1"


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {d: i for i, d in enumerate(dates)}


def _candidate_id(pattern: str, start: date, end: date | None, pivot_date: date | None) -> str:
    payload = "|".join(
        [
            PREDICTION_ADAPTER_VERSION,
            STRUCTURAL_ASSEMBLY_VERSION,
            pattern,
            start.isoformat(),
            end.isoformat() if end else "",
            pivot_date.isoformat() if pivot_date else "",
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _prediction(
    *,
    pattern: str,
    start: date,
    end: date | None,
    pivot_level: float | None,
    pivot_date: date | None,
    detector_status: str,
    detector_faults: tuple[str, ...] = (),
) -> MorphologyPrediction:
    return MorphologyPrediction(
        candidate_id=_candidate_id(pattern, start, end, pivot_date),
        pattern=pattern,
        start_date=start,
        end_date=end,
        pivot_source_date=pivot_date,
        pivot_level=pivot_level,
        detector_status=detector_status,
        detector_faults=detector_faults,
    )


def _right_edge_context_complete(index: dict[date, int], *, right_rim: date, asof_date: date) -> bool:
    """Preregistered daily-data context gate for Cup-without-Handle."""
    if right_rim not in index or asof_date not in index:
        return False
    return index[asof_date] - index[right_rim] >= MIN_HANDLE_DURATION_SESSIONS - 1


def _segment_key(segment) -> tuple:
    return (
        segment.start.price_date,
        segment.trough.price_date,
        segment.recovery.price_date if segment.recovery is not None else None,
        segment.stage.value,
    )


def extract_core_morphology_predictions(frame: pd.DataFrame, *, asof_date: date) -> list[MorphologyPrediction]:
    """Emit DEVELOPMENT predictions from the canonical landmark-first stack.

    v0.3.1 preserves first-pass atomic P2 segments and adds multi-turn spans as
    a strict superset. P1 landmarks and all morphology thresholds remain unchanged.
    Multiple structural scales and Cup-family interpretations may coexist explicitly.
    """
    if frame.empty:
        return []

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("canonical P8 extractor received future bars")
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
    index = _session_index(ordered)

    predictions: list[MorphologyPrediction] = []

    atomic_segments = segment_base_candidates(ordered, landmarks, asof_date=asof_date)
    multiturn_segments = assemble_multiturn_segments(ordered, landmarks, asof_date=asof_date)
    segment_map = {_segment_key(item): item for item in atomic_segments}
    for item in multiturn_segments:
        segment_map.setdefault(_segment_key(item), item)
    segments = [segment_map[key] for key in sorted(segment_map, key=lambda key: tuple(x or date.max for x in key[:3]) + (key[3],))]

    for segment in segments:
        assessment = assess_flat_base(ordered, segment)
        pivot = flat_base_pivot(segment)
        predictions.append(
            _prediction(
                pattern="FLAT_BASE",
                start=segment.start_date,
                end=segment.end_date,
                pivot_level=pivot.pivot_level,
                pivot_date=pivot.pivot_source_date,
                detector_status=assessment.state.value,
                detector_faults=tuple(item.value for item in assessment.faults),
            )
        )

    for geometry in assemble_multiturn_double_bottoms(ordered, landmarks, asof_date=asof_date):
        assessment = assess_double_bottom(geometry)
        pivot = double_bottom_pivot(geometry)
        predictions.append(
            _prediction(
                pattern="DOUBLE_BOTTOM",
                start=geometry.left_high.price_date,
                end=geometry.trough_2.price_date,
                pivot_level=pivot.pivot_level,
                pivot_date=pivot.pivot_source_date,
                detector_status=assessment.state.value,
                detector_faults=tuple(item.value for item in assessment.faults),
            )
        )

    for segment in segments:
        if segment.recovery is None:
            continue
        geometry = build_cup_body_geometry(ordered, segment.start, segment.trough, segment.recovery)
        body = assess_cup_body(geometry)
        if body.state != CupBodyState.RECOGNIZED:
            continue

        for handle_geometry in assemble_handle_geometries(
            ordered,
            geometry,
            landmarks,
            asof_date=asof_date,
        ):
            handle_assessment = assess_handle(handle_geometry)
            pivot = cup_with_handle_pivot(geometry, handle_geometry)
            detector_status = (
                "CUP_WITH_HANDLE_RECOGNIZED"
                if handle_assessment.state == HandleState.RECOGNIZED
                else "CUP_WITH_HANDLE_AMBIGUOUS"
            )
            predictions.append(
                _prediction(
                    pattern="CUP_WITH_HANDLE",
                    start=geometry.left_rim.price_date,
                    end=handle_geometry.handle_recovery.price_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status=detector_status,
                    detector_faults=tuple(item.value for item in handle_assessment.faults),
                )
            )

        if _right_edge_context_complete(index, right_rim=geometry.right_rim.price_date, asof_date=asof_date):
            pivot = cup_without_handle_pivot(geometry)
            predictions.append(
                _prediction(
                    pattern="CUP_WITHOUT_HANDLE",
                    start=geometry.left_rim.price_date,
                    end=geometry.right_rim.price_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status="CUP_WITHOUT_HANDLE_RECOGNIZED",
                )
            )

    by_id = {item.candidate_id: item for item in predictions}
    return [by_id[key] for key in sorted(by_id)]
