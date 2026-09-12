from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

from oneil_patterns.landmarks.candidate import LandmarkCandidate


@dataclass(frozen=True, slots=True)
class BaseSegmentCandidate:
    """P2 provisional base region built only from frozen P1 landmark candidates."""

    start: LandmarkCandidate
    trough: LandmarkCandidate
    recovery: LandmarkCandidate | None
    start_date: date
    end_date: date
    confirmed_date: date
    duration_sessions: int
    depth_pct: float
    recovery_pct: float | None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
        if self.confirmed_date < self.end_date:
            raise ValueError("confirmed_date cannot precede end_date")
        if self.duration_sessions < 1:
            raise ValueError("duration_sessions must be >= 1")
        if not 0 <= self.depth_pct < 1:
            raise ValueError("depth_pct must be in [0, 1)")
        if self.recovery_pct is not None and self.recovery_pct < 0:
            raise ValueError("recovery_pct cannot be negative")
