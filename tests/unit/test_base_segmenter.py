from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.segmentation.model import SegmentStage
from oneil_patterns.segmentation.segmenter import segment_base_candidates


def _frame():
    dates = pd.bdate_range("2026-01-02", periods=12)
    return pd.DataFrame({"date": dates, "close": range(12)})


def _candidate(kind, price, price_date, confirmed_date, *, boundary=False):
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=price_date,
        confirmed_date=confirmed_date,
        method="percentage_excursion",
        boundary=boundary,
    )


def test_segments_high_low_recovery_without_pattern_label():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[3]),
        _candidate(LandmarkType.SWING_LOW, 80.0, d[5], d[7]),
        _candidate(LandmarkType.SWING_HIGH, 96.0, d[9], d[10]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[11])

    assert len(result) == 1
    segment = result[0]
    assert segment.start is marks[0]
    assert segment.trough is marks[1]
    assert segment.recovery is marks[2]
    assert segment.stage == SegmentStage.RECOVERY_CONFIRMED
    assert segment.start_date == d[1]
    assert segment.end_date == d[9]
    assert segment.duration_sessions == 9
    assert segment.decline_sessions == 5
    assert segment.recovery_sessions == 5
    assert segment.depth_pct == 0.20
    assert segment.recovery_pct == 0.20
    assert segment.recovery_to_start_ratio == 0.96
    assert segment.recovered_depth_fraction == 0.80
    assert segment.confirmed_date == d[10]
    assert segment.evidence["feature_semantics"] == "p2-geometry-v1"
    assert "pattern" not in segment.evidence


def test_future_confirmed_recovery_is_not_used_asof_prefix():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[3]),
        _candidate(LandmarkType.SWING_LOW, 82.0, d[5], d[6]),
        _candidate(LandmarkType.SWING_HIGH, 95.0, d[8], d[10]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[8])

    assert len(result) == 1
    segment = result[0]
    assert segment.stage == SegmentStage.DECLINE_CONFIRMED
    assert segment.recovery is None
    assert segment.start_date == d[1]
    assert segment.end_date == d[5]
    assert segment.confirmed_date == d[6]
    assert segment.end_date != d[8]
    assert segment.decline_sessions == 5
    assert segment.recovery_sessions is None
    assert segment.recovery_pct is None
    assert segment.recovery_to_start_ratio is None
    assert segment.recovered_depth_fraction is None


def test_full_recovery_fraction_equals_one_at_prior_high():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[2]),
        _candidate(LandmarkType.SWING_LOW, 75.0, d[4], d[5]),
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[8], d[9]),
    ]

    segment = segment_base_candidates(frame, marks, asof_date=d[10])[0]

    assert segment.depth_pct == 0.25
    assert segment.recovery_to_start_ratio == 1.0
    assert segment.recovered_depth_fraction == 1.0


def test_asof_horizon_never_becomes_structural_end_date():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[1], d[2]),
        _candidate(LandmarkType.SWING_LOW, 84.0, d[4], d[5]),
    ]

    early = segment_base_candidates(frame, marks, asof_date=d[6])[0]
    late = segment_base_candidates(frame, marks, asof_date=d[11])[0]

    assert early.stage == SegmentStage.DECLINE_CONFIRMED
    assert late.stage == SegmentStage.DECLINE_CONFIRMED
    assert early.start_date == late.start_date == d[1]
    assert early.end_date == late.end_date == d[4]
    assert early.duration_sessions == late.duration_sessions


def test_boundary_evidence_is_preserved_not_deleted():
    frame = _frame()
    d = pd.to_datetime(frame.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, d[0], d[2], boundary=True),
        _candidate(LandmarkType.SWING_LOW, 85.0, d[4], d[6]),
    ]

    result = segment_base_candidates(frame, marks, asof_date=d[7])

    assert len(result) == 1
    assert result[0].evidence["start_boundary"] is True
