from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
from typing import Iterable

from .labels import CorpusSplit, LabelEvidence, LabelValue, SourcePrecision

EVALUATOR_VERSION = "p8-source-dimension-eval-v0.4"


@dataclass(frozen=True, slots=True)
class MorphologyPrediction:
    candidate_id: str
    pattern: str
    start_date: date
    end_date: date | None = None
    pivot_source_date: date | None = None
    pivot_level: float | None = None
    depth_pct: float | None = None
    detector_status: str | None = None
    detector_faults: tuple[str, ...] = ()
    candidate_semantics: str = "CONFIRMED_STRUCTURE"


@dataclass(frozen=True, slots=True)
class SourceDimensionAgreement:
    example_id: str
    expected_pattern: str
    agreement_state: str
    matched_candidate_id: str | None
    matched_detector_status: str | None
    start_error_days: int | None
    end_error_days: int | None
    pivot_date_error_days: int | None
    pivot_price_error_pct: float | None
    depth_error_pct_points: float | None
    boundary_validation_state: str
    pivot_validation_state: str
    depth_validation_state: str
    rationale: tuple[str, ...]
    evaluator_version: str = EVALUATOR_VERSION

    def to_dict(self) -> dict:
        return asdict(self)


def _distance(left: date, right: date) -> int:
    return abs((left - right).days)


def _start_match(label: LabelEvidence, prediction: MorphologyPrediction, tolerance_days: int) -> tuple[bool, int | None]:
    if label.window_start is None:
        return True, None
    error = _distance(prediction.start_date, label.window_start)
    if label.window_start_precision == SourcePrecision.MONTH:
        return (
            prediction.start_date.year == label.window_start.year
            and prediction.start_date.month == label.window_start.month,
            error,
        )
    return error <= tolerance_days, error


def _pivot_validation_state(label: LabelEvidence, prediction: MorphologyPrediction) -> str:
    needs_date = label.expected_pivot_source_date is not None
    needs_price = label.expected_pivot_level is not None
    if not needs_date and not needs_price:
        return "SOURCE_NOT_PROVIDED"
    if needs_date and prediction.pivot_source_date is None:
        return "NOT_EVALUABLE"
    if needs_price and prediction.pivot_level is None:
        return "NOT_EVALUABLE"
    if needs_date and needs_price:
        return "DATE_AND_PRICE_EVALUATED"
    return "DATE_EVALUATED" if needs_date else "PRICE_EVALUATED"


def _depth_validation_state(label: LabelEvidence, prediction: MorphologyPrediction) -> str:
    if label.expected_depth_pct is None:
        return "SOURCE_NOT_PROVIDED"
    if prediction.depth_pct is None:
        return "NOT_EVALUABLE"
    return "DEPTH_EVALUATED"


def _boundary_validation_state(label: LabelEvidence) -> str:
    if label.window_start is None:
        return "SOURCE_START_NOT_PROVIDED"
    if label.window_end is None:
        prefix = "START_ONLY_SOURCE_ANCHOR"
    else:
        prefix = "START_SCORED_SOURCE_END_ROLE_UNSPECIFIED"
    return f"{prefix}_{label.window_start_precision.value}_START"


def evaluate_positive_development_label(
    label: LabelEvidence,
    predictions: Iterable[MorphologyPrediction],
    *,
    boundary_tolerance_days: int = 10,
    pivot_date_tolerance_days: int = 3,
    pivot_price_tolerance_pct: float = 0.01,
) -> SourceDimensionAgreement:
    if label.split != CorpusSplit.DEVELOPMENT:
        raise ValueError("source-dimension evaluator is locked to DEVELOPMENT labels")
    if label.label != LabelValue.POSITIVE:
        raise ValueError("v0.4 evaluates positive authoritative labels only")
    if boundary_tolerance_days < 0 or pivot_date_tolerance_days < 0 or pivot_price_tolerance_pct < 0:
        raise ValueError("tolerances must be non-negative")

    same_pattern = [item for item in predictions if item.pattern == label.pattern]
    if not same_pattern:
        return SourceDimensionAgreement(
            example_id=label.example_id,
            expected_pattern=label.pattern,
            agreement_state="MISS_PATTERN",
            matched_candidate_id=None,
            matched_detector_status=None,
            start_error_days=None,
            end_error_days=None,
            pivot_date_error_days=None,
            pivot_price_error_pct=None,
            depth_error_pct_points=None,
            boundary_validation_state=_boundary_validation_state(label),
            pivot_validation_state="NOT_EVALUABLE",
            depth_validation_state="NOT_EVALUABLE" if label.expected_depth_pct is not None else "SOURCE_NOT_PROVIDED",
            rationale=("frozen detector emitted no candidate with the authoritative pattern label",),
        )

    ranked: list[tuple[tuple, MorphologyPrediction, tuple]] = []
    for prediction in same_pattern:
        start_ok, start_error = _start_match(label, prediction, boundary_tolerance_days)
        end_error = None
        end_ok = True

        pivot_date_error = None
        pivot_date_ok = True
        if label.expected_pivot_source_date is not None:
            if prediction.pivot_source_date is None:
                pivot_date_ok = False
            else:
                pivot_date_error = _distance(prediction.pivot_source_date, label.expected_pivot_source_date)
                pivot_date_ok = pivot_date_error <= pivot_date_tolerance_days

        pivot_price_error = None
        pivot_price_ok = True
        comparison_level = label.comparison_pivot_level
        if comparison_level is not None:
            if prediction.pivot_level is None:
                pivot_price_ok = False
            else:
                pivot_price_error = abs(float(prediction.pivot_level) / comparison_level - 1.0)
                pivot_price_ok = pivot_price_error <= pivot_price_tolerance_pct

        depth_error = None
        depth_ok = True
        if label.expected_depth_pct is not None:
            if prediction.depth_pct is None:
                depth_ok = False
            else:
                depth_error = abs(float(prediction.depth_pct) - label.expected_depth_pct)
                depth_ok = depth_error <= float(label.expected_depth_tolerance_pct_points)

        boundary_ok = start_ok and end_ok
        pivot_ok = pivot_date_ok and pivot_price_ok
        morphology_ok = depth_ok
        rank = (
            0 if boundary_ok else 1,
            0 if pivot_ok else 1,
            0 if morphology_ok else 1,
            start_error if start_error is not None else 0,
            depth_error if depth_error is not None else float("inf"),
            pivot_date_error if pivot_date_error is not None else 10**9,
            pivot_price_error if pivot_price_error is not None else float("inf"),
            prediction.start_date,
            prediction.end_date or date.max,
            prediction.candidate_id,
        )
        ranked.append((rank, prediction, (start_ok, start_error, end_ok, end_error, pivot_date_ok, pivot_date_error, pivot_price_ok, pivot_price_error, depth_ok, depth_error)))

    _, chosen, details = min(ranked, key=lambda item: item[0])
    start_ok, start_error, end_ok, end_error, pivot_date_ok, pivot_date_error, pivot_price_ok, pivot_price_error, depth_ok, depth_error = details
    boundary_ok = start_ok and end_ok
    pivot_ok = pivot_date_ok and pivot_price_ok

    rationale: list[str] = []
    if not boundary_ok:
        state = "BOUNDARY_DISAGREEMENT"
        rationale.append("named pattern agrees but the source-provided start anchor does not")
    elif not pivot_ok:
        state = "LANDMARK_DISAGREEMENT"
        rationale.append("named pattern and comparable boundary dimensions agree but a published pivot dimension does not")
    elif not depth_ok:
        state = "MORPHOLOGY_DISAGREEMENT"
        rationale.append("named pattern/boundary/pivot agree but the source-stated depth does not")
    else:
        state = "MATCH"
        rationale.append("named pattern agrees with all currently comparable source-provided dimensions at their published precision")

    if label.window_start is None:
        rationale.append("source does not provide a detector-comparable start anchor; start is not scored or used for ranking")
    elif label.window_start_precision == SourcePrecision.MONTH:
        rationale.append(f"start evaluated only at MONTH precision ({label.window_start:%Y-%m})")
    if label.window_end is None:
        rationale.append("source does not provide an exact end anchor; end is not scored")
    else:
        rationale.append("source window end is preserved but not scored against detector structural end until its semantic role is explicitly versioned")
    if label.expected_pivot_source_date is None:
        rationale.append("source does not provide a detector-comparable pivot date; pivot date is not scored")
    if label.expected_pivot_level is None:
        rationale.append("source does not provide a detector-comparable pivot price; pivot price is not scored")
    elif label.pivot_price_adjustment_factor != 1.0:
        rationale.append(
            f"source pivot {label.expected_pivot_level:g} preserved; comparison basis divides by explicit factor "
            f"{label.pivot_price_adjustment_factor:g} -> {label.comparison_pivot_level:g}"
        )
    if label.expected_depth_pct is None:
        rationale.append("source does not provide a detector-comparable depth; depth is not scored")
    else:
        rationale.append(
            f"source depth {label.expected_depth_pct:.3f} scored with explicit +/- "
            f"{label.expected_depth_tolerance_pct_points:.3f} tolerance"
        )
    rationale.append(f"candidate semantics retained separately: {chosen.candidate_semantics}")
    if chosen.detector_status:
        rationale.append(f"detector status retained separately: {chosen.detector_status}")

    return SourceDimensionAgreement(
        example_id=label.example_id,
        expected_pattern=label.pattern,
        agreement_state=state,
        matched_candidate_id=chosen.candidate_id,
        matched_detector_status=chosen.detector_status,
        start_error_days=start_error,
        end_error_days=end_error,
        pivot_date_error_days=pivot_date_error,
        pivot_price_error_pct=round(pivot_price_error, 8) if pivot_price_error is not None else None,
        depth_error_pct_points=round(depth_error, 8) if depth_error is not None else None,
        boundary_validation_state=_boundary_validation_state(label),
        pivot_validation_state=_pivot_validation_state(label, chosen),
        depth_validation_state=_depth_validation_state(label, chosen),
        rationale=tuple(rationale),
    )
