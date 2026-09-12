from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType


@dataclass(frozen=True, slots=True)
class DoubleBottomGeometry:
    """Morphology-neutral geometry for a W-like structural sequence.

    This object intentionally carries no recognized/rejected verdict. It only
    measures a confirmed structural sequence already supplied by P1/P2.
    """

    left_high: LandmarkCandidate
    trough_1: LandmarkCandidate
    middle_peak: LandmarkCandidate
    trough_2: LandmarkCandidate
    right_recovery_high: LandmarkCandidate | None
    confirmed_date: date
    duration_sessions: int
    overall_depth_pct: float
    trough_spacing_sessions: int
    trough2_vs_trough1_pct: float
    middle_peak_rebound_pct: float
    middle_peak_recovered_fraction: float
    right_recovery_pct: float | None
    right_recovery_to_left_high_ratio: float | None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        expected = (
            (self.left_high, LandmarkType.SWING_HIGH),
            (self.trough_1, LandmarkType.SWING_LOW),
            (self.middle_peak, LandmarkType.SWING_HIGH),
            (self.trough_2, LandmarkType.SWING_LOW),
        )
        for item, kind in expected:
            if item.type != kind:
                raise ValueError(f"expected {kind.value}, got {item.type.value}")
        if self.right_recovery_high is not None and self.right_recovery_high.type != LandmarkType.SWING_HIGH:
            raise ValueError("right recovery must be SWING_HIGH")
        if self.duration_sessions <= 0 or self.trough_spacing_sessions <= 0:
            raise ValueError("session counts must be positive")
        if self.overall_depth_pct < 0:
            raise ValueError("overall depth cannot be negative")
        if self.confirmed_date < self.trough_2.confirmed_date:
            raise ValueError("geometry cannot be confirmed before trough 2")


def build_double_bottom_geometry(
    session_index: Mapping[date, int],
    left_high: LandmarkCandidate,
    trough_1: LandmarkCandidate,
    middle_peak: LandmarkCandidate,
    trough_2: LandmarkCandidate,
    right_recovery_high: LandmarkCandidate | None = None,
) -> DoubleBottomGeometry:
    """Measure a chronological high-low-high-low-(high) W sequence."""
    marks = [left_high, trough_1, middle_peak, trough_2]
    if right_recovery_high is not None:
        marks.append(right_recovery_high)

    for mark in marks:
        if mark.price_date not in session_index:
            raise ValueError(f"landmark date missing from session index: {mark.price_date}")

    indices = [session_index[m.price_date] for m in marks]
    if indices != sorted(indices) or len(indices) != len(set(indices)):
        raise ValueError("Double Bottom landmarks must be strictly chronological")

    deeper_trough = min(trough_1.price, trough_2.price)
    overall_depth = (left_high.price - deeper_trough) / left_high.price
    if overall_depth < 0:
        raise ValueError("trough cannot exceed left high")

    trough2_vs_trough1 = (trough_2.price - trough_1.price) / trough_1.price
    middle_peak_rebound = (middle_peak.price - trough_1.price) / trough_1.price
    first_decline = left_high.price - trough_1.price
    middle_recovered_fraction = (
        (middle_peak.price - trough_1.price) / first_decline if first_decline > 0 else 0.0
    )

    right_recovery_pct = None
    right_recovery_to_left = None
    if right_recovery_high is not None:
        right_recovery_pct = (right_recovery_high.price - trough_2.price) / trough_2.price
        right_recovery_to_left = right_recovery_high.price / left_high.price

    confirmed = max(m.confirmed_date for m in marks)
    end_index = indices[-1]

    return DoubleBottomGeometry(
        left_high=left_high,
        trough_1=trough_1,
        middle_peak=middle_peak,
        trough_2=trough_2,
        right_recovery_high=right_recovery_high,
        confirmed_date=confirmed,
        duration_sessions=end_index - indices[0] + 1,
        overall_depth_pct=overall_depth,
        trough_spacing_sessions=indices[3] - indices[1],
        trough2_vs_trough1_pct=trough2_vs_trough1,
        middle_peak_rebound_pct=middle_peak_rebound,
        middle_peak_recovered_fraction=middle_recovered_fraction,
        right_recovery_pct=right_recovery_pct,
        right_recovery_to_left_high_ratio=right_recovery_to_left,
        evidence={
            "version": "double-bottom-geometry-v0",
            "second_trough_undercuts_first": trough_2.price < trough_1.price,
            "right_recovery_present": right_recovery_high is not None,
        },
    )
