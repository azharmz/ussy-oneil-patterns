from __future__ import annotations

from datetime import date
import hashlib

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.morphology.cup_body_detector import CupBodyState, assess_cup_body
from oneil_patterns.morphology.cup_family import MIN_HANDLE_DURATION_SESSIONS, HandleState, assess_handle
from oneil_patterns.morphology.double_bottom_detector import assess_double_bottom
from oneil_patterns.morphology.flat_base import assess_flat_base
from oneil_patterns.segmentation.segmenter import segment_base_candidates

from .open_right_edge_cnh import OPEN_RIGHT_EDGE_CNH_VERSION, enumerate_open_right_edge_cnh
from .open_right_edge_double_bottom import OPEN_RIGHT_EDGE_DOUBLE_BOTTOM_VERSION, observe_open_right_edge_double_bottom
from .open_right_edge_flat import OPEN_RIGHT_EDGE_FLAT_VERSION, enumerate_open_right_edge_flats
from .open_right_edge_handle import OPEN_RIGHT_EDGE_HANDLE_VERSION, enumerate_open_right_edge_handles
from .pivot_adapter import cup_with_handle_pivot, cup_without_handle_pivot, double_bottom_pivot, flat_base_pivot
from .source_dimension_eval import MorphologyPrediction
from .structural_assembly import (
    DB_LOCAL_TURN_ASSEMBLY_VERSION,
    STRUCTURAL_ASSEMBLY_VERSION,
    assemble_handle_geometries,
    assemble_local_turn_double_bottoms,
    assemble_multiturn_double_bottoms,
    assemble_multiturn_segments,
)

PREDICTION_ADAPTER_VERSION = "p8-canonical-prediction-adapter-v1.2-cwh-measurement"


def _session_index(frame: pd.DataFrame) -> dict[date, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {d: i for i, d in enumerate(dates)}


def _sig(**anchors: date) -> tuple[str, ...]:
    return tuple(f"{name.upper()}:{value.isoformat()}" for name, value in anchors.items())


def _candidate_id(pattern, start, end, pivot_date, candidate_semantics="CONFIRMED_STRUCTURE"):
    payload = "|".join([
        PREDICTION_ADAPTER_VERSION,
        STRUCTURAL_ASSEMBLY_VERSION,
        pattern,
        candidate_semantics,
        start.isoformat(),
        end.isoformat() if end else "",
        pivot_date.isoformat() if pivot_date else "",
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def _prediction(*, pattern, start, end, pivot_level, pivot_date, detector_status, depth_pct=None,\n                detector_faults=(), candidate_semantics="CONFIRMED_STRUCTURE", structural_signature=(), evidence=None):
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
        structural_signature=structural_signature,\n        evidence=evidence or {},\n    )


def _right_edge_context_complete(index, *, right_rim, asof_date):
    return right_rim in index and asof_date in index and index[asof_date] - index[right_rim] >= MIN_HANDLE_DURATION_SESSIONS - 1


def _cwh_status(body_state, handle_state):
    if body_state == CupBodyState.RECOGNIZED and handle_state == HandleState.RECOGNIZED:
        return "CUP_WITH_HANDLE_RECOGNIZED"
    return "CUP_WITH_HANDLE_AMBIGUOUS"


def _db_right_edge_is_open(landmarks, *, trough_2_date):
    return not any(item.type == LandmarkType.SWING_HIGH and item.price_date > trough_2_date for item in landmarks)


def _segment_key(segment):
    return (segment.start.price_date, segment.trough.price_date,
            segment.recovery.price_date if segment.recovery is not None else None, segment.stage.value)


def _db_signature(geometry):
    return _sig(
        left_high=geometry.left_high.price_date,
        trough_1=geometry.trough_1.price_date,
        middle_peak=geometry.middle_peak.price_date,
        trough_2=geometry.trough_2.price_date,
    )


def _append_db_predictions(predictions, ordered, geometries, *, asof_date, right_edge_open, semantics):
    for geometry in geometries:
        assessment = assess_double_bottom(geometry)
        pivot = double_bottom_pivot(geometry)
        signature = _db_signature(geometry)
        predictions.append(_prediction(
            pattern="DOUBLE_BOTTOM",
            start=geometry.left_high.price_date,
            end=geometry.trough_2.price_date,
            pivot_level=pivot.pivot_level,
            pivot_date=pivot.pivot_source_date,
            detector_status=assessment.state.value,
            depth_pct=geometry.overall_depth_pct,
            detector_faults=tuple(item.value for item in assessment.faults),
            candidate_semantics=semantics,
            structural_signature=signature,
        ))
        if right_edge_open(geometry):
            observation = observe_open_right_edge_double_bottom(ordered, geometry, asof_date=asof_date)
            if observation is not None:
                predictions.append(_prediction(
                    pattern="DOUBLE_BOTTOM",
                    start=geometry.left_high.price_date,
                    end=asof_date,
                    pivot_level=pivot.pivot_level,
                    pivot_date=pivot.pivot_source_date,
                    detector_status=observation.state.value,
                    depth_pct=geometry.overall_depth_pct,
                    detector_faults=tuple(item.value for item in observation.faults),
                    candidate_semantics=(
                        f"{semantics}:OPEN_RIGHT_EDGE_DOUBLE_BOTTOM:{OPEN_RIGHT_EDGE_DOUBLE_BOTTOM_VERSION}:"
                        f"TROUGH2={geometry.trough_2.price_date.isoformat()}"
                    ),
                    structural_signature=signature,
                ))


def extract_core_morphology_predictions(frame: pd.DataFrame, *, asof_date: date) -> list[MorphologyPrediction]:
    """Emit PIT-safe DEVELOPMENT predictions with stable structural signatures.

    Double Bottoms first use frozen P1 structural turns. If that scale produces
    no W geometry at all, a label-agnostic three-session local-turn fallback is
    allowed so shallow W structures are not categorically impossible.
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
        predictions.append(_prediction(
            pattern="FLAT_BASE", start=segment.start_date, end=segment.end_date,
            pivot_level=pivot.pivot_level, pivot_date=pivot.pivot_source_date,
            detector_status=assessment.state.value, depth_pct=segment.depth_pct,
            detector_faults=tuple(item.value for item in assessment.faults),
            structural_signature=_sig(left_high=segment.start.price_date, base_low=segment.trough.price_date),
        ))

    for observation in enumerate_open_right_edge_flats(ordered, landmarks, asof_date=asof_date):
        predictions.append(_prediction(
            pattern="FLAT_BASE", start=observation.start.price_date, end=observation.asof_date,
            pivot_level=float(observation.start.price), pivot_date=observation.start.price_date,
            detector_status=observation.state.value, depth_pct=observation.depth_from_start_pct,
            detector_faults=tuple(item.value for item in observation.faults),
            candidate_semantics=f"OPEN_RIGHT_EDGE:{OPEN_RIGHT_EDGE_FLAT_VERSION}",
            structural_signature=_sig(left_high=observation.start.price_date, base_low=observation.observed_low_date),
        ))

    db_geometries = assemble_multiturn_double_bottoms(ordered, landmarks, asof_date=asof_date)
    if db_geometries:
        _append_db_predictions(
            predictions, ordered, db_geometries, asof_date=asof_date,
            right_edge_open=lambda g: _db_right_edge_is_open(landmarks, trough_2_date=g.trough_2.price_date),
            semantics="CONFIRMED_STRUCTURE",
        )
    else:
        local_db = assemble_local_turn_double_bottoms(ordered, asof_date=asof_date)
        _append_db_predictions(
            predictions, ordered, local_db, asof_date=asof_date,
            right_edge_open=lambda g: bool(g.evidence.get("p8_local_right_edge_open")),
            semantics=f"LOCAL_TURN_AUX:{DB_LOCAL_TURN_ASSEMBLY_VERSION}",
        )

    for observation in enumerate_open_right_edge_cnh(ordered, landmarks, asof_date=asof_date):
        suffix = {CupBodyState.RECOGNIZED: "RECOGNIZED", CupBodyState.AMBIGUOUS: "AMBIGUOUS", CupBodyState.REJECTED: "REJECTED"}[observation.state]
        predictions.append(_prediction(
            pattern="CUP_WITHOUT_HANDLE", start=observation.left_rim.price_date, end=observation.asof_date,
            pivot_level=float(observation.left_rim.price), pivot_date=observation.left_rim.price_date,
            detector_status=f"CUP_WITHOUT_HANDLE_{suffix}", depth_pct=observation.depth_pct,
            detector_faults=tuple(item.value for item in observation.faults),
            candidate_semantics=f"OPEN_RIGHT_EDGE_CNH:{OPEN_RIGHT_EDGE_CNH_VERSION}:TROUGH={observation.trough.price_date.isoformat()}",
            structural_signature=_sig(left_rim=observation.left_rim.price_date, cup_low=observation.trough.price_date),
        ))

    for segment in segments:
        if segment.recovery is None:
            continue
        geometry = build_cup_body_geometry(ordered, segment.start, segment.trough, segment.recovery)
        body = assess_cup_body(geometry)
        if body.state == CupBodyState.REJECTED:
            continue
        body_faults = tuple(item.value for item in body.faults)

        for handle_geometry in assemble_handle_geometries(ordered, geometry, landmarks, asof_date=asof_date):
            handle_assessment = assess_handle(handle_geometry)
            pivot = cup_with_handle_pivot(geometry, handle_geometry)
            predictions.append(_prediction(
                pattern="CUP_WITH_HANDLE", start=geometry.left_rim.price_date,
                end=handle_geometry.handle_recovery.price_date, pivot_level=pivot.pivot_level,
                pivot_date=pivot.pivot_source_date, detector_status=_cwh_status(body.state, handle_assessment.state),
                depth_pct=geometry.depth_pct,
                detector_faults=body_faults + tuple(item.value for item in handle_assessment.faults),
                structural_signature=_sig(left_rim=geometry.left_rim.price_date, cup_low=geometry.trough.price_date,\n                                          right_rim=geometry.right_rim.price_date, handle_low=handle_geometry.handle_low.price_date),\n                evidence={\n                    "cwh_measurement_version": "cwh-vnext-r2b-v0.1",\n                    "handle_duration_sessions": handle_geometry.duration_sessions,\n                    "handle_depth_pct": handle_geometry.depth_pct,\n                    "absolute_low_in_upper_half": handle_geometry.low_in_upper_half,\n                    "median_close_position_in_cup": handle_geometry.median_close_position_in_cup,\n                    "fraction_closes_at_or_above_cup_midpoint": handle_geometry.fraction_closes_at_or_above_cup_midpoint,\n                    "minimum_close_position_in_cup": handle_geometry.minimum_close_position_in_cup,\n                    "normalized_close_slope": handle_geometry.normalized_close_slope,\n                    "handle_to_pre20_median_volume_ratio": handle_geometry.handle_to_pre20_median_volume_ratio,\n                },\n            ))

        for observation in enumerate_open_right_edge_handles(ordered, geometry, landmarks, asof_date=asof_date):
            predictions.append(_prediction(
                pattern="CUP_WITH_HANDLE", start=geometry.left_rim.price_date, end=observation.asof_date,
                pivot_level=float(geometry.right_rim.price), pivot_date=geometry.right_rim.price_date,
                detector_status=_cwh_status(body.state, observation.state), depth_pct=geometry.depth_pct,
                detector_faults=body_faults + tuple(item.value for item in observation.faults),
                candidate_semantics=f"OPEN_RIGHT_EDGE_HANDLE:{OPEN_RIGHT_EDGE_HANDLE_VERSION}",
                structural_signature=_sig(left_rim=geometry.left_rim.price_date, cup_low=geometry.trough.price_date,
                                          right_rim=geometry.right_rim.price_date, handle_low=observation.handle_low.price_date),
            ))

        if body.state == CupBodyState.RECOGNIZED and _right_edge_context_complete(index, right_rim=geometry.right_rim.price_date, asof_date=asof_date):
            pivot = cup_without_handle_pivot(geometry)
            predictions.append(_prediction(
                pattern="CUP_WITHOUT_HANDLE", start=geometry.left_rim.price_date, end=geometry.right_rim.price_date,
                pivot_level=pivot.pivot_level, pivot_date=pivot.pivot_source_date,
                detector_status="CUP_WITHOUT_HANDLE_RECOGNIZED", depth_pct=geometry.depth_pct,
                structural_signature=_sig(left_rim=geometry.left_rim.price_date, cup_low=geometry.trough.price_date),
            ))

    by_id = {item.candidate_id: item for item in predictions}
    return [by_id[key] for key in sorted(by_id)]
