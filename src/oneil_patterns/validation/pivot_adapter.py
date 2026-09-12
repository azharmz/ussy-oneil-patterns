from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import HandleGeometry
from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry
from oneil_patterns.segmentation.model import BaseSegmentCandidate

PIVOT_ADAPTER_VERSION = "p8-pivot-adapter-v0.1"


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
    """Fail closed until the native detector persists the handle high explicitly.

    #32 freezes CWH pivot as the highest price in the valid handle. The current
    canonical HandleGeometry retains only handle_low and handle_recovery, while
    cup.right_rim belongs to the cup body. Treating recovery as the pivot would
    silently infer a missing handle-high landmark and can leak breakout-side
    information. P8 must therefore remain NOT_EVALUABLE until handle-high
    persistence is added under a versioned morphology contract.
    """
    _ = (geometry, handle)
    return PivotFact(
        pattern="CUP_WITH_HANDLE",
        state=PivotEvaluationState.NOT_EVALUABLE,
        pivot_level=None,
        pivot_source_date=None,
        pivot_landmark_type=None,
        definition_version=PIVOT_ADAPTER_VERSION,
        reason="HANDLE_HIGH_NOT_PERSISTED",
    )
