from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from statistics import mean, pstdev
from typing import Any, Mapping

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType


@dataclass(frozen=True, slots=True)
class AscendingBaseGeometry:
    peak_1: LandmarkCandidate
    trough_1: LandmarkCandidate
    peak_2: LandmarkCandidate
    trough_2: LandmarkCandidate
    peak_3: LandmarkCandidate
    trough_3: LandmarkCandidate
    recovery_peak: LandmarkCandidate
    confirmed_date: date
    duration_sessions: int
    pullback_depths: tuple[float, float, float]
    trough_stepups: tuple[float, float]
    peak_stepups: tuple[float, float, float]
    mean_pullback_pct: float
    max_pullback_pct: float
    pullback_depth_dispersion: float
    evidence: Mapping[str, Any] = field(default_factory=dict)


def build_ascending_base_geometry(
    session_index: Mapping[date, int],
    peak_1: LandmarkCandidate,
    trough_1: LandmarkCandidate,
    peak_2: LandmarkCandidate,
    trough_2: LandmarkCandidate,
    peak_3: LandmarkCandidate,
    trough_3: LandmarkCandidate,
    recovery_peak: LandmarkCandidate,
) -> AscendingBaseGeometry:
    marks = (peak_1, trough_1, peak_2, trough_2, peak_3, trough_3, recovery_peak)
    expected = (
        LandmarkType.SWING_HIGH,
        LandmarkType.SWING_LOW,
        LandmarkType.SWING_HIGH,
        LandmarkType.SWING_LOW,
        LandmarkType.SWING_HIGH,
        LandmarkType.SWING_LOW,
        LandmarkType.SWING_HIGH,
    )
    for mark, kind in zip(marks, expected):
        if mark.type != kind:
            raise ValueError(f"expected {kind.value}, got {mark.type.value}")
        if mark.price_date not in session_index:
            raise ValueError(f"landmark date missing from session index: {mark.price_date}")

    indices = [session_index[m.price_date] for m in marks]
    if indices != sorted(indices) or len(indices) != len(set(indices)):
        raise ValueError("Ascending Base landmarks must be strictly chronological")

    peaks = (peak_1.price, peak_2.price, peak_3.price, recovery_peak.price)
    troughs = (trough_1.price, trough_2.price, trough_3.price)
    if any(price <= 0 for price in peaks + troughs):
        raise ValueError("prices must be positive")

    pullbacks = (
        (peak_1.price - trough_1.price) / peak_1.price,
        (peak_2.price - trough_2.price) / peak_2.price,
        (peak_3.price - trough_3.price) / peak_3.price,
    )
    if any(value < 0 for value in pullbacks):
        raise ValueError("each trough must be below its preceding peak")

    trough_stepups = (
        (trough_2.price - trough_1.price) / trough_1.price,
        (trough_3.price - trough_2.price) / trough_2.price,
    )
    peak_stepups = (
        (peak_2.price - peak_1.price) / peak_1.price,
        (peak_3.price - peak_2.price) / peak_2.price,
        (recovery_peak.price - peak_3.price) / peak_3.price,
    )

    return AscendingBaseGeometry(
        peak_1=peak_1,
        trough_1=trough_1,
        peak_2=peak_2,
        trough_2=trough_2,
        peak_3=peak_3,
        trough_3=trough_3,
        recovery_peak=recovery_peak,
        confirmed_date=max(m.confirmed_date for m in marks),
        duration_sessions=indices[-1] - indices[0] + 1,
        pullback_depths=pullbacks,
        trough_stepups=trough_stepups,
        peak_stepups=peak_stepups,
        mean_pullback_pct=mean(pullbacks),
        max_pullback_pct=max(pullbacks),
        pullback_depth_dispersion=pstdev(pullbacks),
        evidence={
            "version": "ascending-base-geometry-v0",
            "ascending_troughs": trough_1.price < trough_2.price < trough_3.price,
            "ascending_peaks": peak_1.price < peak_2.price < peak_3.price < recovery_peak.price,
        },
    )
