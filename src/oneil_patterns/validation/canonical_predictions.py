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

from .open_right_edge_cnh import (
    OPEN_RIGHT_EDGE_CNH_VERSION,
    enumerate_open_right_edge_cnh,
)
from .open_right_edge_double_bottom import (
    OPEN_RIGHT_EDGE_DOUBLE_BOTTOM_VERSION,
    observe_open_right_edge_double_bottom,
)
from .open_right_edge_flat import (
    OPEN_RIGHT_EDGE_FLAT_VERSION,
    enumerate_open_right_edge_flats,
)
from .open_right_edge_handle import (
    OPEN_RIGHT_EDGE_HANDLE_VERSION,
    enumerate_open_right_edge_handles,
)
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

PREDICTION_ADAPTER_VERSION = "p8-canonical-prediction-adapter-v0.8"


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {d: i for i, d in enumerate(dates)}


def _candidate_id(
    pattern: str,
    start: date,
    end: date | None,
    pivot_date: date | None,
    candidate_semantics: str = "CONFIRMED_STRUCTURE",
) -> str:
    payload = "|".join(
        [
            PREDICTION_ADAPTER_VERSION,
            STRUCTURAL_ASSEMBLY_VERSION,
            pattern,
            candidate_semantics,
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
    depth_pct: float | None = None,
    detector_faults: tuple[str, ...] = (),
    candidate_semantics: str = "CONFIRMED_STRUCTURE",
) -> MorphologyPrediction:
    return MorphologyPrediction(
        candidate_id=_candidate_id(pattern, start, end, pivot_date, candidate_semantics),
        pattern=pattern,
        start_date=start,
        end_date=end,
        pivot_source_date=pivot_date,
        pivot_level=pivot_level,
        depth_pct=depth_pct,
        detector_status=detector_status,
        detector_faults=detector_faults,
        candidate_semantics=candidate_semantics,
    )


def _right_edge_context_complete(index: dict[date, int], *, right_rim: date, asof_date: date) -> bool:
    if right_rim not in index or asof_date not in index:
        return False
    return index[asof_date] - index[right_rim] >= MIN_HANDLE_DURATION_SESSIONS - 1


def _cwh_status(body_state: CupBodyState, handle_state: HandleState) -> str:
    if body_state == CupBodyState.RECOGNIZED and handle_state == HandleState.RECOGNIZED:
        return "CUP_WITH_HANDLE_RECOGNIZED"
    return "CUP_WITH_HANDLE_AMBIGUOUS"


def _segment_key(segment) -> tuple:
    return (
        segment.start.price_date,
        segment.trough.price_date,
        segment.recovery.price_date if segment.recovery is not None else None,
        segment.stage.value,
    )


def extract_core_morphology_predictions(frame: pd.DataFrame, *, asof_date: date) -> list[MorphologyPrediction]:
    """Emit DEVELOPMENT predictions from the canonical landmark-first stack.

    v0.8 keeps confirmed structures and explicit right-edge observations. A
    right-edge Double Bottom observation may measure total elapsed base duration
    through T only after post-trough-2 price has recovered to the middle-peak
    pivot; T is not fabricated as a P1 landmark.
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
                depth_pct=segment.depth_pct,
                detector_faults=tuple(item.value for item in assessment.faults),
            )
        )

    for observation in enumerate_open_right_edge_flats(ordered, landmarks, asof_date=asof_date):
        predictions.append(
            _prediction(
                pattern="FLAT_BASE",
                start=observation.start.price_date,
                end=observation.asof_date,
                pivot_level=float(observation.start.price),
                pivot_date=observation.start.price_date,
                detector_status=observation.state.value,
                depth_pct=observation.depth_from_start_pct,
                detector_faults=tuple(item.value for item in observation.faults),
                candidate_semantics=f"OPEN_RIGHT_EDGE:{OPEN_RIGHT_EDGE_FLAT_VERSION}",
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
                depth_pct=geometry.overall_depth_pct,
                detector_faults=tuple(item.value for item in assessment.faults),
            )
        )

        observation = observe_open_right_edge_double_bottom(ordered, geometry, asof_date=asof_date)
        if observation is not None:
            predictions.append(
                _prediction(
                    pattern="DOUBLE_BOTTOM",
                    start=geometry.left_high.price_date,
                    end=asof_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status=observation.state.value,
                    depth_pct=geometry.overall_depth_pct,
                    detector_faults=tuple(item.value for item in observation.faults),
                    candidate_semantics=(
                        f"OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:{OPEN_RIGHT_EDGE_DOUBLE_BOTTOM_VERSION}:"
                        f"TROUGH2={geometry.trough_2.price_date.isoformat()}"
                    ),
                )
            )

    for observation in enumerate_open_right_edge_cnh(ordered, landmarks, asof_date=asof_date):
        suffix = {
            CupBodyState.RECOGNIZED: "RECOGNIZED",
            CupBodyState.AMBIGUOUS: "AMBIGUOUS",
            CupBodyState.REJECTED: "REJECTED",
        }[observation.state]
        semantics = (
            f"OPEN_RIGHT_EDGE_CNH:{OPEN_RIGHT_EDGE_CNH_VERSION}:"
            f"TROUGH={observation.trough.price_date.isoformat()}"
        )
        predictions.append(
            _prediction(
                pattern="CUP_WITHOUT_HANDLE",
                start=observation.left_rim.price_date,
                end=observation.asof_date,
                pivot_level=float(observation.left_rim.price),
                pivot_date=observation.left_rim.price_date,
                detector_status=f"CUP_WITHOUT_HANDLE_{suffix}",
                depth_pct=observation.depth_pct,
                detector_faults=tuple(item.value for item in observation.faults),
                candidate_semantics=semantics,
            )
        )

    for segment in segments:
        if segment.recovery is None:
            continue
        geometry = build_cup_body_geometry(ordered, segment.start, segment.trough, segment.recovery)
        body = assess_cup_body(geometry)
        if body.state == CupBodyState.REJECTED:
            continue

        body_faults = tuple(item.value for item in body.faults)

        for handle_geometry in assemble_handle_geometries(
            ordered,
            geometry,
            landmarks,
            asof_date=asof_date,
        ):
            handle_assessment = assess_handle(handle_geometry)
            pivot = cup_with_handle_pivot(geometry, handle_geometry)
            predictions.append(
                _prediction(
                    pattern="CUP_WITH_HANDLE",
                    start=geometry.left_rim.price_date,
                    end=handle_geometry.handle_recovery.price_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status=_cwh_status(body.state, handle_assessment.state),
                    depth_pct=geometry.depth_pct,
                    detector_faults=body_faults + tuple(item.value for item in handle_assessment.faults),
                )
            )

        for observation in enumerate_open_right_edge_handles(
            ordered,
            geometry,
            landmarks,
            asof_date=asof_date,
        ):
            predictions.append(
                _prediction(
                    pattern="CUP_WITH_HANDLE",
                    start=geometry.left_rim.price_date,
                    end=observation.asof_date,
                    pivot_level=float(geometry.right_rim.price),
                    pivot_date=geometry.right_rim.price_date,
                    detector_status=_cwh_status(body.state, observation.state),
                    depth_pct=geometry.depth_pct,
                    detector_faults=body_faults + tuple(item.value for item in observation.faults),
                    candidate_semantics=f"OPEN_RIGHT_EDGE_HANDLE:{OPEN_RIGHT_EDGE_HANDLE_VERSION}",
                )
            )

        if body.state == CupBodyState.RECOGNIZED and _right_edge_context_complete(index, right_rim=geometry.right_rim.price_date, asof_date=asof_date):
            pivot = cup_without_handle_pivot(geometry)
            predictions.append(
                _prediction(
                    pattern="CUP_WITHOUT_HANDLE",
                    start=geometry.left_rim.price_date,
                    end=geometry.right_rim.price_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status="CUP_WITHOUT_HANDLE_RECOGNIZED",
                    depth_pct=geometry.depth_pct,
                )
            )

    by_id = {item.candidate_id: item for item in predictions}
    return [by_id[key] for key in sorted(by_id)]
