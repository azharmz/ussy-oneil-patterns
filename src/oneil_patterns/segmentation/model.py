from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Mapping

from oneil_patterns.landmarks.candidate import LandmarkCandidate


class SegmentStage(str, Enum):
    DECLINE_CONFIRMED = "DECLINE_CONFIRMED"
    RECOVERY_CONFIRMED = "RECOVERY_CONFIRMED"


@dataclass(frozen=True, slots=True)
class BaseSegmentCandidate:
    """P2 provisional base region built only from frozen P1 landmark candidates.

    Boundary semantics are explicit:
    - `start_date` is always the structural start SWING_HIGH price date.
    - while only the decline/trough is known, `end_date` is the trough price date
      and stage is `DECLINE_CONFIRMED`;
    - once a recovery SWING_HIGH is confirmed, `end_date` becomes that recovery
      price date and stage is `RECOVERY_CONFIRMED`;
    - `asof_date` is never substituted for a structural boundary.
    """

    start: LandmarkCandidate
    trough: LandmarkCandidate
    recovery: LandmarkCandidate | None
    stage: SegmentStage
    start_date: date
    end_date: date
    confirmed_date: date
    duration_sessions: int
    depth_pct: float
    recovery_pct: float | None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_date != self.start.price_date:
            raise ValueError("start_date must equal start landmark price_date")
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

        if self.stage == SegmentStage.DECLINE_CONFIRMED:
            if self.recovery is not None:
                raise ValueError("DECLINE_CONFIRMED segment cannot carry recovery")
            if self.end_date != self.trough.price_date:
                raise ValueError("decline-stage end_date must equal trough price_date")
            if self.recovery_pct is not None:
                raise ValueError("decline-stage recovery_pct must be None")
        elif self.stage == SegmentStage.RECOVERY_CONFIRMED:
            if self.recovery is None:
                raise ValueError("RECOVERY_CONFIRMED segment requires recovery")
            if self.end_date != self.recovery.price_date:
                raise ValueError("recovery-stage end_date must equal recovery price_date")
            if self.recovery_pct is None:
                raise ValueError("recovery-stage recovery_pct is required")
