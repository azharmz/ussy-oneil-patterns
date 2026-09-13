from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from statistics import mean
from typing import Any, Mapping

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.ascending_base_detector import (
    AscendingBaseAssessment,
    AscendingBaseFault,
    AscendingBaseState,
    MARKETSMITH_PULLBACK_MAX,
    MARKETSMITH_PULLBACK_MIN,
    MAX_DURATION_SESSIONS,
    MIN_DURATION_SESSIONS,
    TEXTBOOK_PULLBACK_MAX,
    TEXTBOOK_PULLBACK_MIN,
)

ASCENDING_BASE_RIGHT_EDGE_CONTRACT_VERSION = "ascending-base-v3"


@dataclass(frozen=True, slots=True)
class AscendingBaseRightEdgeGeometry:
    peak_1: LandmarkCandidate
    trough_1: LandmarkCandidate
    peak_2: LandmarkCandidate
    trough_2: LandmarkCandidate
    peak_3: LandmarkCandidate
    observed_trough_3_date: date
    observed_trough_3_price: float
    asof_date: date
    confirmed_date: date
    duration_sessions: int
    pullback_depths: tuple[float, float, float]
    trough_stepups: tuple[float, float]
    peak_stepups: tuple[float, float]
    mean_pullback_pct: float
    max_pullback_pct: float
    evidence: Mapping[str, Any] = field(default_factory=dict)


def build_ascending_base_right_edge_geometry(
    frame: pd.DataFrame,
    session_index: Mapping[date, int],
    peak_1: LandmarkCandidate,
    trough_1: LandmarkCandidate,
    peak_2: LandmarkCandidate,
    trough_2: LandmarkCandidate,
    peak_3: LandmarkCandidate,
    *,
    asof_date: date,
) -> AscendingBaseRightEdgeGeometry:
    marks = (peak_1, trough_1, peak_2, trough_2, peak_3)
    expected = (
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
        if mark.confirmed_date > asof_date:
            raise ValueError("ascending-base landmark is not confirmed by as-of date")

    indices = [session_index[item.price_date] for item in marks]
    if indices != sorted(indices) or len(indices) != len(set(indices)):
        raise ValueError("Ascending Base landmarks must be strictly chronological")

    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    if asof_date not in set(dates):
        raise ValueError("as-of date missing from frame")
    after_peak = (dates > peak_3.price_date) & (dates <= asof_date)
    region = frame.loc[after_peak]
    if region.empty:
        raise ValueError("third pullback has no observed bars after peak_3")
    lows = pd.to_numeric(region["low"], errors="raise").astype(float)
    low_position = lows.idxmin()
    observed_low = float(lows.loc[low_position])
    observed_low_date = dates.loc[low_position]
    if observed_low <= 0:
        raise ValueError("third pullback observed low must be positive")
    if observed_low >= peak_3.price:
        raise ValueError("third pullback has not declined below peak_3")

    peaks = (peak_1.price, peak_2.price, peak_3.price)
    troughs = (trough_1.price, trough_2.price, observed_low)
    if any(value <= 0 for value in peaks + troughs):
        raise ValueError("prices must be positive")

    pullbacks = (
        (peak_1.price - trough_1.price) / peak_1.price,
        (peak_2.price - trough_2.price) / peak_2.price,
        (peak_3.price - observed_low) / peak_3.price,
    )
    trough_stepups = (
        (trough_2.price - trough_1.price) / trough_1.price,
        (observed_low - trough_2.price) / trough_2.price,
    )
    peak_stepups = (
        (peak_2.price - peak_1.price) / peak_1.price,
        (peak_3.price - peak_2.price) / peak_2.price,
    )
    low_index = session_index[observed_low_date]

    return AscendingBaseRightEdgeGeometry(
        peak_1=peak_1,
        trough_1=trough_1,
        peak_2=peak_2,
        trough_2=trough_2,
        peak_3=peak_3,
        observed_trough_3_date=observed_low_date,
        observed_trough_3_price=observed_low,
        asof_date=asof_date,
        confirmed_date=max(item.confirmed_date for item in marks),
        duration_sessions=low_index - indices[0] + 1,
        pullback_depths=pullbacks,
        trough_stepups=trough_stepups,
        peak_stepups=peak_stepups,
        mean_pullback_pct=mean(pullbacks),
        max_pullback_pct=max(pullbacks),
        evidence={
            "version": ASCENDING_BASE_RIGHT_EDGE_CONTRACT_VERSION,
            "right_edge_third_pullback": True,
            "ascending_troughs": trough_1.price < trough_2.price < observed_low,
            "ascending_peaks": peak_1.price < peak_2.price < peak_3.price,
            "third_peak_confirmed_by": peak_3.confirmed_date.isoformat(),
        },
    )


def assess_ascending_base_right_edge(geometry: AscendingBaseRightEdgeGeometry):
    faults: list[AscendingBaseFault] = []
    if geometry.duration_sessions < MIN_DURATION_SESSIONS:
        faults.append(AscendingBaseFault.TOO_SHORT)
    if geometry.duration_sessions > MAX_DURATION_SESSIONS:
        faults.append(AscendingBaseFault.TOO_LONG)
    if not geometry.evidence["ascending_troughs"]:
        faults.append(AscendingBaseFault.NON_ASCENDING_TROUGHS)
    if not geometry.evidence["ascending_peaks"]:
        faults.append(AscendingBaseFault.NON_ASCENDING_PEAKS)

    textbook = tuple(
        TEXTBOOK_PULLBACK_MIN <= value <= TEXTBOOK_PULLBACK_MAX
        for value in geometry.pullback_depths
    )
    hard = {
        AscendingBaseFault.TOO_SHORT,
        AscendingBaseFault.TOO_LONG,
        AscendingBaseFault.NON_ASCENDING_TROUGHS,
        AscendingBaseFault.NON_ASCENDING_PEAKS,
    }
    if any(item in hard for item in faults):
        return AscendingBaseAssessment(
            AscendingBaseState.REJECTED,
            tuple(faults),
            geometry,
            theory_gates_pass=False,
            source_guardrails_pass=False,
            textbook_pullbacks=textbook,
        )

    if any(
        value < MARKETSMITH_PULLBACK_MIN or value > MARKETSMITH_PULLBACK_MAX
        for value in geometry.pullback_depths
    ):
        faults.append(AscendingBaseFault.PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE)
        return AscendingBaseAssessment(
            AscendingBaseState.AMBIGUOUS,
            tuple(faults),
            geometry,
            theory_gates_pass=True,
            source_guardrails_pass=False,
            textbook_pullbacks=textbook,
        )

    return AscendingBaseAssessment(
        AscendingBaseState.RECOGNIZED,
        tuple(faults),
        geometry,
        theory_gates_pass=True,
        source_guardrails_pass=True,
        textbook_pullbacks=textbook,
    )
