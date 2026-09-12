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

    Geometry semantics:
    - `duration_sessions`: inclusive start -> current structural end;
    - `decline_sessions`: inclusive start high -> trough;
    - `recovery_sessions`: inclusive trough -> recovery high, if confirmed;
    - `depth_pct`: decline from start high to trough, divided by start high;
    - `recovery_pct`: rebound from trough to recovery high, divided by trough;
    - `recovery_to_start_ratio`: recovery high / start high;
    - `recovered_depth_fraction`: recovered price distance divided by the original
      start-to-trough decline distance. 1.0 means recovery returned exactly to
      the start high; values above 1.0 are allowed.

    Boundary semantics are explicit:
    - `start_date` is always the structural start SWING_HIGH price date;
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
    decline_sessions: int
    recovery_sessions: int | None
    depth_pct: float
    recovery_pct: float | None
    recovery_to_start_ratio: float | None
    recovered_depth_fraction: float | None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.start_date != self.start.price_date:
            raise ValueError("start_date must equal start landmark price_date")
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
        if self.confirmed_date < self.end_date:
            raise ValueError("confirmed_date cannot precede end_date")
        if self.duration_sessions < 1 or self.decline_sessions < 1:
            raise ValueError("duration/decline sessions must be >= 1")
        if self.decline_sessions > self.duration_sessions:
            raise ValueError("decline_sessions cannot exceed duration_sessions")
        if not 0 <= self.depth_pct < 1:
            raise ValueError("depth_pct must be in [0, 1)")
        if self.recovery_pct is not None and self.recovery_pct < 0:
            raise ValueError("recovery_pct cannot be negative")
        if self.recovery_to_start_ratio is not None and self.recovery_to_start_ratio <= 0:
            raise ValueError("recovery_to_start_ratio must be positive")
        if self.recovered_depth_fraction is not None and self.recovered_depth_fraction < 0:
            raise ValueError("recovered_depth_fraction cannot be negative")

        if self.stage == SegmentStage.DECLINE_CONFIRMED:
            if self.recovery is not None:
                raise ValueError("DECLINE_CONFIRMED segment cannot carry recovery")
            if self.end_date != self.trough.price_date:
                raise ValueError("decline-stage end_date must equal trough price_date")
            if any(
                value is not None
                for value in (
                    self.recovery_sessions,
                    self.recovery_pct,
                    self.recovery_to_start_ratio,
                    self.recovered_depth_fraction,
                )
            ):
                raise ValueError("decline-stage recovery features must be None")
        elif self.stage == SegmentStage.RECOVERY_CONFIRMED:
            if self.recovery is None:
                raise ValueError("RECOVERY_CONFIRMED segment requires recovery")
            if self.end_date != self.recovery.price_date:
                raise ValueError("recovery-stage end_date must equal recovery price_date")
            if any(
                value is None
                for value in (
                    self.recovery_sessions,
                    self.recovery_pct,
                    self.recovery_to_start_ratio,
                    self.recovered_depth_fraction,
                )
            ):
                raise ValueError("recovery-stage recovery features are required")
            if self.recovery_sessions is not None and self.recovery_sessions < 1:
                raise ValueError("recovery_sessions must be >= 1")
