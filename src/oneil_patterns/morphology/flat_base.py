from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

import pandas as pd

from oneil_patterns.segmentation.model import BaseSegmentCandidate

MIN_DURATION_WEEKS = 5
# Retained for compatibility/evidence only; vNext does not use this as the duration gate.
MIN_DURATION_SESSIONS = 25
MAX_DEPTH_PCT = 0.15

# Research bands, not claimed as official O'Neil/IBD thresholds. They are
# preregistered for morphology validation only and must not be tuned to return.
TIGHT_MAX_NORMALIZED_RANGE = 0.03
TIGHT_MAX_CLOSE_DISPERSION = 0.01
WIDE_LOOSE_MIN_NORMALIZED_RANGE = 0.07
WIDE_LOOSE_MIN_CLOSE_DISPERSION = 0.03


class FlatBaseState(str, Enum):
    RECOGNIZED = "FLAT_BASE_RECOGNIZED"
    REJECTED = "FLAT_BASE_REJECTED"
    AMBIGUOUS = "FLAT_BASE_AMBIGUOUS"
    NOT_EVALUABLE = "FLAT_BASE_NOT_EVALUABLE"


class FlatBaseFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    TOO_DEEP = "TOO_DEEP"
    WIDE_LOOSE = "WIDE_LOOSE"
    BOUNDARY_CONTEXT = "BOUNDARY_CONTEXT"


@dataclass(frozen=True, slots=True)
class FlatBaseAssessment:
    state: FlatBaseState
    duration_gate: bool
    depth_gate: bool
    normalized_high_low_range: float | None
    close_dispersion_pct: float | None
    upper_band_fraction_5pct: float | None
    faults: tuple[FlatBaseFault, ...] = ()
    evidence: Mapping[str, Any] = field(default_factory=dict)


def _region(frame: pd.DataFrame, segment: BaseSegmentCandidate) -> pd.DataFrame:
    required = {"date", "high", "low", "close"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"frame missing required columns: {sorted(missing)}")
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    return frame.loc[(dates >= segment.start_date) & (dates <= segment.end_date)].copy()


def assess_flat_base(frame: pd.DataFrame, segment: BaseSegmentCandidate) -> FlatBaseAssessment:
    """Assess Flat Base morphology using theory gates plus research tightness bands.

    Theory gates:
    - duration >= 25 sessions;
    - depth <= 15%.

    Tightness/wide-loose thresholds are explicitly research-only. P8 v0.2 keeps
    `WIDE_LOOSE` as fault evidence but no longer lets that research-only band
    create a hard rejection when the theory gates pass.
    """
    region = _region(frame, segment)
    trading_weeks = pd.to_datetime(region["date"], errors="raise").dt.to_period("W-FRI").nunique() if not region.empty else 0
    duration_gate = trading_weeks >= MIN_DURATION_WEEKS
    depth_gate = segment.depth_pct <= MAX_DEPTH_PCT

    if region.empty or region[["high", "low", "close"]].isna().any().any():
        return FlatBaseAssessment(
            state=FlatBaseState.NOT_EVALUABLE,
            duration_gate=duration_gate,
            depth_gate=depth_gate,
            normalized_high_low_range=None,
            close_dispersion_pct=None,
            upper_band_fraction_5pct=None,
            evidence={"reason": "missing_or_empty_region", "version": "flat-base-vnext-r2d"},
        )

    base_high = float(region["high"].max())
    base_low = float(region["low"].min())
    mean_close = float(region["close"].mean())
    if base_high <= 0 or mean_close <= 0:
        raise ValueError("prices must be positive")

    normalized_range = (base_high - base_low) / base_high
    close_dispersion = float(region["close"].std(ddof=0)) / mean_close
    upper_band_fraction = float((region["close"] >= base_high * 0.95).mean())

    faults: list[FlatBaseFault] = []
    if not duration_gate:
        faults.append(FlatBaseFault.TOO_SHORT)
    if not depth_gate:
        faults.append(FlatBaseFault.TOO_DEEP)

    wide_loose = (
        normalized_range >= WIDE_LOOSE_MIN_NORMALIZED_RANGE
        or close_dispersion >= WIDE_LOOSE_MIN_CLOSE_DISPERSION
    )
    if wide_loose:
        faults.append(FlatBaseFault.WIDE_LOOSE)

    boundary_context = segment.start.boundary or segment.trough.boundary or (
        segment.recovery.boundary if segment.recovery is not None else False
    )
    if boundary_context:
        faults.append(FlatBaseFault.BOUNDARY_CONTEXT)

    tight = (
        normalized_range <= TIGHT_MAX_NORMALIZED_RANGE
        and close_dispersion <= TIGHT_MAX_CLOSE_DISPERSION
    )

    if not duration_gate or not depth_gate:
        state = FlatBaseState.REJECTED
        reason = "source_backed_hard_gate_failure"
    elif boundary_context:
        state = FlatBaseState.AMBIGUOUS
        reason = "boundary_context_requires_caution"
    else:
        state = FlatBaseState.RECOGNIZED
        reason = "vnext_structural_gates_pass"

    return FlatBaseAssessment(
        state=state,
        duration_gate=duration_gate,
        depth_gate=depth_gate,
        normalized_high_low_range=normalized_range,
        close_dispersion_pct=close_dispersion,
        upper_band_fraction_5pct=upper_band_fraction,
        faults=tuple(faults),
        evidence={
            "version": "flat-base-vnext-r2d",
            "reason": reason,
            "min_duration_weeks": MIN_DURATION_WEEKS,
            "duration_semantics": "distinct_trading_weeks_W_FRI",
            "trading_weeks": int(trading_weeks),
            "legacy_min_duration_sessions_evidence_only": MIN_DURATION_SESSIONS,
            "max_depth_pct": MAX_DEPTH_PCT,
            "tightness_policy": "research_only",
            "wide_loose_state_policy": "EVIDENCE_ONLY",
            "tight_max_normalized_range": TIGHT_MAX_NORMALIZED_RANGE,
            "tight_max_close_dispersion": TIGHT_MAX_CLOSE_DISPERSION,
            "wide_loose_min_normalized_range": WIDE_LOOSE_MIN_NORMALIZED_RANGE,
            "wide_loose_min_close_dispersion": WIDE_LOOSE_MIN_CLOSE_DISPERSION,
        },
    )
