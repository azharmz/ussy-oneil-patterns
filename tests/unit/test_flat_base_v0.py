from datetime import date, timedelta

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.flat_base import (
    FlatBaseFault,
    FlatBaseState,
    assess_flat_base,
)
from oneil_patterns.segmentation.model import BaseSegmentCandidate, SegmentStage


def _segment(*, duration=25, depth=0.10, boundary=False):
    start_date = date(2026, 1, 2)
    end_date = start_date + timedelta(days=duration - 1)
    start = LandmarkCandidate(
        LandmarkType.SWING_HIGH, 100.0, start_date, start_date, "test", boundary=boundary
    )
    trough = LandmarkCandidate(LandmarkType.SWING_LOW, 100.0 * (1 - depth), end_date, end_date, "test")
    return BaseSegmentCandidate(
        start=start, trough=trough, recovery=None, stage=SegmentStage.DECLINE_CONFIRMED,
        start_date=start_date, end_date=end_date, confirmed_date=end_date,
        duration_sessions=duration, decline_sessions=duration, recovery_sessions=None,
        depth_pct=depth, recovery_pct=None, recovery_to_start_ratio=None,
        recovered_depth_fraction=None,
    )


def _frame(segment, *, loose=False, borderline=False):
    dates = pd.date_range(segment.start_date, segment.end_date, freq="D")
    if loose:
        closes = [96.0 if i % 2 else 100.0 for i in range(len(dates))]
    elif borderline:
        closes = [98.0 + ((i % 6) - 2.5) * 0.75 for i in range(len(dates))]
    else:
        closes = [98.0 + ((i % 3) - 1) * 0.4 for i in range(len(dates))]
    return pd.DataFrame({
        "date": dates,
        "high": [x + 0.5 for x in closes],
        "low": [x - 0.5 for x in closes],
        "close": closes,
    })


def test_duration_below_25_sessions_rejected():
    segment = _segment(duration=24, depth=0.10)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.REJECTED
    assert FlatBaseFault.TOO_SHORT in result.faults


def test_depth_above_15_percent_rejected():
    segment = _segment(duration=25, depth=0.151)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.REJECTED
    assert FlatBaseFault.TOO_DEEP in result.faults


def test_tight_research_band_can_recognize_after_hard_gates_pass():
    segment = _segment(duration=25, depth=0.10)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.RECOGNIZED
    assert result.duration_gate is True
    assert result.depth_gate is True
    assert result.evidence["tightness_policy"] == "research_only"


def test_wide_loose_fault_rejects_hard_gate_passer():
    segment = _segment(duration=25, depth=0.10)
    result = assess_flat_base(_frame(segment, loose=True), segment)
    assert result.state == FlatBaseState.REJECTED
    assert FlatBaseFault.WIDE_LOOSE in result.faults


def test_intermediate_tightness_remains_ambiguous():
    segment = _segment(duration=25, depth=0.10)
    result = assess_flat_base(_frame(segment, borderline=True), segment)
    assert result.state == FlatBaseState.AMBIGUOUS
    assert FlatBaseFault.WIDE_LOOSE not in result.faults


def test_boundary_context_prevents_textbook_recognition():
    segment = _segment(duration=25, depth=0.10, boundary=True)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.AMBIGUOUS
    assert FlatBaseFault.BOUNDARY_CONTEXT in result.faults
