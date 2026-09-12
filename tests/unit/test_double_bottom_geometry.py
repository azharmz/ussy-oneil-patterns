from datetime import date, timedelta

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.double_bottom import build_double_bottom_geometry


def _candidate(kind, price, d, confirm_offset=0):
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=d,
        confirmed_date=d + timedelta(days=confirm_offset),
        method="test",
    )


def test_double_bottom_geometry_measures_w_without_classifying_it():
    start = date(2026, 1, 2)
    dates = [start + timedelta(days=i) for i in range(60)]
    index = {d: i for i, d in enumerate(dates)}

    left = _candidate(LandmarkType.SWING_HIGH, 100.0, dates[2], 2)
    t1 = _candidate(LandmarkType.SWING_LOW, 75.0, dates[16], 2)
    mid = _candidate(LandmarkType.SWING_HIGH, 90.0, dates[27], 2)
    t2 = _candidate(LandmarkType.SWING_LOW, 73.0, dates[39], 2)
    right = _candidate(LandmarkType.SWING_HIGH, 92.0, dates[50], 2)

    result = build_double_bottom_geometry(index, left, t1, mid, t2, right)

    assert result.duration_sessions == 49
    assert result.trough_spacing_sessions == 23
    assert round(result.overall_depth_pct, 4) == 0.27
    assert round(result.trough2_vs_trough1_pct, 4) == round((73.0 - 75.0) / 75.0, 4)
    assert round(result.middle_peak_rebound_pct, 4) == 0.20
    assert round(result.middle_peak_recovered_fraction, 4) == 0.60
    assert round(result.right_recovery_pct, 4) == round((92.0 - 73.0) / 73.0, 4)
    assert result.right_recovery_to_left_high_ratio == 0.92
    assert result.evidence["second_trough_undercuts_first"] is True


def test_right_recovery_is_optional_and_confirmation_stops_at_trough2():
    start = date(2026, 3, 1)
    dates = [start + timedelta(days=i) for i in range(50)]
    index = {d: i for i, d in enumerate(dates)}

    left = _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1], 1)
    t1 = _candidate(LandmarkType.SWING_LOW, 80.0, dates[12], 1)
    mid = _candidate(LandmarkType.SWING_HIGH, 90.0, dates[22], 1)
    t2 = _candidate(LandmarkType.SWING_LOW, 79.0, dates[33], 3)

    result = build_double_bottom_geometry(index, left, t1, mid, t2)

    assert result.right_recovery_high is None
    assert result.right_recovery_pct is None
    assert result.right_recovery_to_left_high_ratio is None
    assert result.confirmed_date == t2.confirmed_date


def test_second_trough_need_not_undercut_at_geometry_stage():
    start = date(2026, 5, 1)
    dates = [start + timedelta(days=i) for i in range(50)]
    index = {d: i for i, d in enumerate(dates)}

    left = _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1])
    t1 = _candidate(LandmarkType.SWING_LOW, 78.0, dates[12])
    mid = _candidate(LandmarkType.SWING_HIGH, 89.0, dates[23])
    t2 = _candidate(LandmarkType.SWING_LOW, 80.0, dates[34])

    result = build_double_bottom_geometry(index, left, t1, mid, t2)

    assert result.trough2_vs_trough1_pct > 0
    assert result.evidence["second_trough_undercuts_first"] is False


def test_landmarks_must_be_strictly_chronological():
    start = date(2026, 7, 1)
    dates = [start + timedelta(days=i) for i in range(20)]
    index = {d: i for i, d in enumerate(dates)}

    left = _candidate(LandmarkType.SWING_HIGH, 100.0, dates[1])
    t1 = _candidate(LandmarkType.SWING_LOW, 80.0, dates[10])
    mid = _candidate(LandmarkType.SWING_HIGH, 90.0, dates[8])
    t2 = _candidate(LandmarkType.SWING_LOW, 78.0, dates[15])

    try:
        build_double_bottom_geometry(index, left, t1, mid, t2)
    except ValueError as exc:
        assert "strictly chronological" in str(exc)
    else:
        raise AssertionError("expected chronology validation error")
