from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import HandleGeometry
from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry
from oneil_patterns.segmentation.model import BaseSegmentCandidate

PIVOT_ADAPTER_VERSION = "p8-pivot-adapter-v0.2"


class PivotEvaluationState(str, Enum):
    EVALUABLE = "EVALUABLE"
    NOT_EVALUABLE = "NOT_EVALUABLE"


@dataclass(frozen=True, slots=True)
class PivotFact:
    pattern: str
    state: PivotEvaluationState
    pivot_level: float | None
    pivot_source_date: date | None
    pivot_landmark_type: str | None
    definition_version: str
    reason: str


def _fact(pattern: str, level: float, source_date: date, landmark_type: str, reason: str) -> PivotFact:
    if level <= 0:
        raise ValueError("pivot level must be positive")
    return PivotFact(
        pattern=pattern,
        state=PivotEvaluationState.EVALUABLE,
        pivot_level=float(level),
        pivot_source_date=source_date,
        pivot_landmark_type=landmark_type,
        definition_version=PIVOT_ADAPTER_VERSION,
        reason=reason,
    )


def flat_base_pivot(segment: BaseSegmentCandidate) -> PivotFact:
    """#32 mapping: Flat Base pivot = base / left-side high."""
    return _fact(
        "FLAT_BASE",
        segment.start.price,
        segment.start.price_date,
        "FLAT_LEFT_HIGH",
        "frozen #32 pivot mapping: base/left-side structural high",
    )


def double_bottom_pivot(geometry: DoubleBottomGeometry) -> PivotFact:
    """#32 mapping: Double Bottom pivot = middle peak of the W."""
    return _fact(
        "DOUBLE_BOTTOM",
        geometry.middle_peak.price,
        geometry.middle_peak.price_date,
        "MIDDLE_PEAK",
        "frozen #32 pivot mapping: middle peak of W",
    )


def cup_without_handle_pivot(geometry: CupBodyGeometry) -> PivotFact:
    """#32 mapping: Cup-without-Handle pivot = prior / left-side high."""
    return _fact(
        "CUP_WITHOUT_HANDLE",
        geometry.left_rim.price,
        geometry.left_rim.price_date,
        "LEFT_RIM",
        "frozen #32 pivot mapping: prior/left-side high",
    )


def cup_with_handle_pivot(geometry: CupBodyGeometry, handle: HandleGeometry) -> PivotFact:
    """#32 mapping: CWH pivot = highest price in the valid handle.

    Under the current landmark-first native sequence, `handle.handle_high` is the
    persisted role of the cup right-rim swing high immediately preceding the
    handle pullback. The adapter consumes that explicit role and never substitutes
    the later handle recovery or an authoritative label value.
    """
    if handle.handle_high != geometry.right_rim:
        raise ValueError("current CWH contract requires handle_high to equal cup right_rim")
    return _fact(
        "CUP_WITH_HANDLE",
        handle.handle_high.price,
        handle.handle_high.price_date,
        "HANDLE_HIGH",
        "frozen #32 pivot mapping: highest price in valid handle",
    )
