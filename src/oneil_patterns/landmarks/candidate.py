from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Mapping

from .model import Landmark, LandmarkType


@dataclass(frozen=True, slots=True)
class LandmarkCandidate:
    """Evidence-rich, PIT-safe structural-turn candidate.

    A candidate is deliberately not an O'Neil pattern landmark yet.  It keeps
    detector evidence and provenance so later segmentation/morphology layers
    can decide how much weight to give the turn without rebuilding swing logic.
    """

    type: LandmarkType
    price: float
    price_date: date
    confirmed_date: date
    method: str
    amplitude_pct: float | None = None
    prominence_pct: float | None = None
    separation_sessions: int | None = None
    boundary: bool = False
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.type not in {LandmarkType.SWING_HIGH, LandmarkType.SWING_LOW}:
            raise ValueError("LandmarkCandidate must be SWING_HIGH or SWING_LOW")
        if self.confirmed_date < self.price_date:
            raise ValueError("confirmed_date cannot precede price_date")
        if self.price <= 0:
            raise ValueError("candidate price must be positive")
        if not self.method:
            raise ValueError("candidate method is required")
        for name, value in (
            ("amplitude_pct", self.amplitude_pct),
            ("prominence_pct", self.prominence_pct),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name} cannot be negative")
        if self.separation_sessions is not None and self.separation_sessions < 0:
            raise ValueError("separation_sessions cannot be negative")

    @classmethod
    def from_landmark(
        cls,
        landmark: Landmark,
        *,
        amplitude_pct: float | None = None,
        prominence_pct: float | None = None,
        separation_sessions: int | None = None,
        boundary: bool = False,
        extra_evidence: Mapping[str, Any] | None = None,
    ) -> "LandmarkCandidate":
        evidence = dict(landmark.evidence)
        if extra_evidence:
            evidence.update(extra_evidence)
        return cls(
            type=landmark.type,
            price=landmark.price,
            price_date=landmark.price_date,
            confirmed_date=landmark.confirmed_date,
            method=landmark.method,
            amplitude_pct=amplitude_pct,
            prominence_pct=prominence_pct,
            separation_sessions=separation_sessions,
            boundary=boundary,
            evidence=evidence,
        )

    def is_known_asof(self, asof_date: date) -> bool:
        return self.confirmed_date <= asof_date
