from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Any, Mapping


class LandmarkType(str, Enum):
    SWING_HIGH = "SWING_HIGH"
    SWING_LOW = "SWING_LOW"
    BASE_START = "BASE_START"
    LEFT_PEAK = "LEFT_PEAK"
    TROUGH_1 = "TROUGH_1"
    MIDDLE_PEAK = "MIDDLE_PEAK"
    TROUGH_2 = "TROUGH_2"
    RIGHT_PEAK = "RIGHT_PEAK"
    HANDLE_START = "HANDLE_START"
    HANDLE_HIGH = "HANDLE_HIGH"
    HANDLE_LOW = "HANDLE_LOW"
    BASE_END = "BASE_END"
    PIVOT = "PIVOT"


@dataclass(frozen=True, slots=True)
class Landmark:
    """PIT-aware structural landmark.

    `price_date` is where the structural price occurred.
    `confirmed_date` is when the detector could first know it using only
    information available through that date.
    """

    type: LandmarkType
    price: float
    price_date: date
    confirmed_date: date
    method: str
    confidence: str | None = None
    evidence: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.confirmed_date < self.price_date:
            raise ValueError("confirmed_date cannot precede price_date")
        if self.price <= 0:
            raise ValueError("landmark price must be positive")
        if not self.method:
            raise ValueError("landmark method is required")

    def is_known_asof(self, asof_date: date) -> bool:
        return self.confirmed_date <= asof_date
