from datetime import date

import pandas as pd

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.segmentation.model import SegmentStage
from oneil_patterns.segmentation.segmenter import segment_base_candidates


def _frame(periods=14):
    dates = pd.bdate_range("2026-02-02", periods=periods)
    return pd.DataFrame({"date": dates, "close": range(periods)})


def _candidate(kind, price, price_date, confirmed_date):
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=price_date,
        confirmed_date=confirmed_date,
        method="percentage_excursion",
    )


def _signature(segment):
    return (
        segment.stage,
        segment.start_date,
        segment.trough.price_date,
        segment.end_date,
        segment.confirmed_date,
        segment.duration_sessions,
        segment.decline_sessions,
        segment.recovery_sessions,
        round(segment.depth_pct, 10),
        None if segment.recovery_pct is None else round(segment.recovery_pct, 10),
        None
        if segment.recovery_to_start_ratio is None
        else round(segment.recovery_to_start_ratio, 10),
        None
        if segment.recovered_depth_fraction is None
        else round(segment.recovered_depth_fraction, 10),
    )


def test_future_bars_alone_do_not_rewrite_known_decline_segment():
    full = _frame()
    dates = pd.to_datetime(full.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1], dates[3]),
        _candidate(LandmarkType.SWING_LOW, 82.0, dates[5], dates[7]),
    ]

    prefix = full.iloc[:9].copy()
    asof = dates[8]
    from_prefix = segment_base_candidates(prefix, marks, asof_date=asof)
    from_full = segment_base_candidates(full, marks, asof_date=asof)

    assert len(from_prefix) == len(from_full) == 1
    assert _signature(from_prefix[0]) == _signature(from_full[0])
    assert from_prefix[0].stage == SegmentStage.DECLINE_CONFIRMED


def test_unconfirmed_future_recovery_cannot_leak_into_prefix():
    full = _frame()
    dates = pd.to_datetime(full.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1], dates[3]),
        _candidate(LandmarkType.SWING_LOW, 80.0, dates[5], dates[7]),
        _candidate(LandmarkType.SWING_HIGH, 96.0, dates[9], dates[11]),
    ]

    asof = dates[9]
    result = segment_base_candidates(full, marks, asof_date=asof)

    assert len(result) == 1
    assert result[0].stage == SegmentStage.DECLINE_CONFIRMED
    assert result[0].recovery is None
    assert result[0].end_date == dates[5]


def test_segment_upgrades_only_when_recovery_is_confirmed():
    full = _frame()
    dates = pd.to_datetime(full.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1], dates[3]),
        _candidate(LandmarkType.SWING_LOW, 80.0, dates[5], dates[7]),
        _candidate(LandmarkType.SWING_HIGH, 96.0, dates[9], dates[11]),
    ]

    before = segment_base_candidates(full, marks, asof_date=dates[10])[0]
    after = segment_base_candidates(full, marks, asof_date=dates[11])[0]

    assert before.stage == SegmentStage.DECLINE_CONFIRMED
    assert before.end_date == dates[5]
    assert after.stage == SegmentStage.RECOVERY_CONFIRMED
    assert after.end_date == dates[9]
    assert after.confirmed_date == dates[11]


def test_future_second_base_does_not_modify_first_completed_base():
    full = _frame()
    dates = pd.to_datetime(full.date).dt.date.tolist()
    marks = [
        _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1], dates[2]),
        _candidate(LandmarkType.SWING_LOW, 80.0, dates[4], dates[5]),
        _candidate(LandmarkType.SWING_HIGH, 95.0, dates[7], dates[8]),
        _candidate(LandmarkType.SWING_LOW, 84.0, dates[10], dates[11]),
    ]

    first_only = segment_base_candidates(full, marks, asof_date=dates[8])
    later = segment_base_candidates(full, marks, asof_date=dates[12])

    assert len(first_only) == 1
    assert len(later) == 2
    assert _signature(first_only[0]) == _signature(later[0])
