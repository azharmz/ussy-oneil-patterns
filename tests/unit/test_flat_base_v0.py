from datetime import date, timedelta

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.flat_base import FlatBaseState, assess_flat_base
from oneil_patterns.segmentation.model import BaseSegmentCandidate, SegmentStage


def _segment(*, duration=25, depth=0.10):
    start_date = date(2026, 1, 2)
    end_date = start_date + timedelta(days=duration - 1)
    start = LandmarkCandidate(LandmarkType.SWING_HIGH, 100.0, start_date, start_date, "test")
    trough = LandmarkCandidate(LandmarkType.SWING_LOW, 100.0 * (1 - depth), end_date, end_date, "test")
    return BaseSegmentCandidate(
        start=start, trough=trough, recovery=None, stage=SegmentStage.DECLINE_CONFIRMED,
        start_date=start_date, end_date=end_date, confirmed_date=end_date,
        duration_sessions=duration, decline_sessions=duration, recovery_sessions=None,
        depth_pct=depth, recovery_pct=None, recovery_to_start_ratio=None,
        recovered_depth_fraction=None,
    )


def _frame(segment, *, loose=False):
    dates = pd.date_range(segment.start_date, segment.end_date, freq="D")
    closes = [98.0 + ((i % 3) - 1) * 0.4 for i in range(len(dates))]
    if loose:
        closes = [96.0 if i % 2 else 100.0 for i in range(len(dates))]
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
    assert result.duration_gate is False
    assert result.depth_gate is True


def test_depth_above_15_percent_rejected():
    segment = _segment(duration=25, depth=0.151)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.REJECTED
    assert result.duration_gate is True
    assert result.depth_gate is False


def test_hard_gates_pass_but_tightness_not_yet_forced_to_recognized():
    segment = _segment(duration=25, depth=0.10)
    result = assess_flat_base(_frame(segment), segment)
    assert result.state == FlatBaseState.AMBIGUOUS
    assert result.duration_gate is True
    assert result.depth_gate is True
    assert result.evidence["tightness_threshold_frozen"] is False


def test_descriptors_distinguish_tight_from_looser_fixture_without_thresholding():
    segment = _segment(duration=25, depth=0.10)
    tight = assess_flat_base(_frame(segment), segment)
    loose = assess_flat_base(_frame(segment, loose=True), segment)
    assert tight.close_dispersion_pct < loose.close_dispersion_pct
    assert tight.normalized_high_low_range < loose.normalized_high_low_range
