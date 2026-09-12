import pandas as pd

from oneil_patterns.morphology.cup_body import build_cup_body_geometry
from oneil_patterns.morphology.cup_body_detector import CupBodyState, assess_cup_body
from tests.fixtures.cup_bodies import cup_body_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in cup_body_fixtures()}


def _rebuild(fixture, frame):
    g = fixture.geometry
    return build_cup_body_geometry(frame, g.left_rim, g.trough, g.right_rim)


def test_future_rows_after_right_rim_do_not_change_cup_assessment():
    fixture = _by_name()["rounded_u"]
    baseline = assess_cup_body(fixture.geometry)

    last_date = pd.to_datetime(fixture.frame["date"].iloc[-1])
    future = pd.DataFrame({
        "date": [last_date + pd.Timedelta(days=i) for i in range(1, 8)],
        "close": [110.0, 70.0, 115.0, 68.0, 120.0, 65.0, 125.0],
    })
    extended = pd.concat([fixture.frame, future], ignore_index=True)
    rebuilt = _rebuild(fixture, extended)
    result = assess_cup_body(rebuilt)

    assert result.state == baseline.state == CupBodyState.RECOGNIZED
    assert rebuilt.duration_sessions == fixture.geometry.duration_sessions
    assert rebuilt.sessions_within_5pct_of_trough == fixture.geometry.sessions_within_5pct_of_trough
    assert rebuilt.max_bottom_run_10pct == fixture.geometry.max_bottom_run_10pct


def test_clear_rounded_u_is_stable_under_small_close_perturbations():
    fixture = _by_name()["rounded_u"]
    for multiplier in (0.999, 1.001):
        frame = fixture.frame.copy()
        frame["close"] = frame["close"] * multiplier
        result = assess_cup_body(_rebuild(fixture, frame))
        assert result.state == CupBodyState.RECOGNIZED


def test_clear_sharp_v_remains_rejected_under_small_close_perturbations():
    fixture = _by_name()["sharp_v"]
    for multiplier in (0.999, 1.001):
        frame = fixture.frame.copy()
        frame["close"] = frame["close"] * multiplier
        result = assess_cup_body(_rebuild(fixture, frame))
        assert result.state == CupBodyState.REJECTED


def test_fixture_labels_match_first_pass_detector_states():
    expected = {
        "rounded_u": CupBodyState.RECOGNIZED,
        "sharp_v": CupBodyState.REJECTED,
        "double_bottom_w": CupBodyState.REJECTED,
        "flat_shallow": CupBodyState.REJECTED,
        "wide_loose": CupBodyState.REJECTED,
    }
    for fixture in cup_body_fixtures():
        assert assess_cup_body(fixture.geometry).state == expected[fixture.name]
