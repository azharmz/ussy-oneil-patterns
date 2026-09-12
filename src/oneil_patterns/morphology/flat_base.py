from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

import pandas as pd

from oneil_patterns.segmentation.model import BaseSegmentCandidate

MIN_DURATION_SESSIONS = 25
MAX_DEPTH_PCT = 0.15


class FlatBaseState(str, Enum):
    RECOGNIZED = "FLAT_BASE_RECOGNIZED"
    REJECTED = "FLAT_BASE_REJECTED"
    AMBIGUOUS = "FLAT_BASE_AMBIGUOUS"
    NOT_EVALUABLE = "FLAT_BASE_NOT_EVALUABLE"


@dataclass(frozen=True, slots=True)
class FlatBaseAssessment:
    state: FlatBaseState
    duration_gate: bool
    depth_gate: bool
    normalized_high_low_range: float | None
    close_dispersion_pct: float | None
    upper_band_fraction_5pct: float | None
    evidence: Mapping[str, Any] = field(default_factory=dict)


def _region(frame: pd.DataFrame, segment: BaseSegmentCandidate) -> pd.DataFrame:
    required = {"date", "high", "low", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    region = frame.loc[(dates >= segment.start_date) & (dates <= segment.end_date)].copy()
    return region


def assess_flat_base(frame: pd.DataFrame, segment: BaseSegmentCandidate) -> FlatBaseAssessment:
    """Flat Base v0: apply frozen theory gates and expose tightness descriptors.

    Tightness descriptors are deliberately not thresholded yet. Passing the
    duration/depth gates therefore yields AMBIGUOUS rather than RECOGNIZED.
    """
    duration_gate = segment.duration_sessions >= MIN_DURATION_SESSIONS
    depth_gate = segment.depth_pct <= MAX_DEPTH_PCT
    region = _region(frame, segment)

    if region.empty or region[["high", "low", "close"]].isna().any().any():
        return FlatBaseAssessment(
            state=FlatBaseState.NOT_EVALUABLE,
            duration_gate=duration_gate,
            depth_gate=depth_gate,
            normalized_high_low_range=None,
            close_dispersion_pct=None,
            upper_band_fraction_5pct=None,
            evidence={"reason": "missing_or_empty_region", "version": "flat-base-v0"},
        )

    base_high = float(region["high"].max())
    base_low = float(region["low"].min())
    mean_close = float(region["close"].mean())
    if base_high <= 0 or mean_close <= 0:
        raise ValueError("prices must be positive")

    normalized_range = (base_high - base_low) / base_high
    close_dispersion = float(region["close"].std(ddof=0)) / mean_close
    upper_band_fraction = float((region["close"] >= base_high * 0.95).mean())

    if not duration_gate or not depth_gate:
        state = FlatBaseState.REJECTED
        reason = "failed_theory_gate"
    else:
        # Official guidance establishes sideways/tight character but the v0
        # research contract has not frozen a numerical tightness threshold.
        state = FlatBaseState.AMBIGUOUS
        reason = "hard_gates_pass_tightness_unfrozen"

    return FlatBaseAssessment(
        state=state,
        duration_gate=duration_gate,
        depth_gate=depth_gate,
        normalized_high_low_range=normalized_range,
        close_dispersion_pct=close_dispersion,
        upper_band_fraction_5pct=upper_band_fraction,
        evidence={
            "version": "flat-base-v0",
            "reason": reason,
            "min_duration_sessions": MIN_DURATION_SESSIONS,
            "max_depth_pct": MAX_DEPTH_PCT,
            "tightness_threshold_frozen": False,
        },
    )
