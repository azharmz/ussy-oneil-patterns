from oneil_patterns.morphology.double_bottom import build_double_bottom_geometry
from oneil_patterns.morphology.double_bottom_detector import DoubleBottomState, assess_double_bottom
from tests.fixtures.double_bottoms import double_bottom_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in double_bottom_fixtures()}


def _scaled_geometry(geometry, factor):
    marks = [
        geometry.left_high,
        geometry.trough_1,
        geometry.middle_peak,
        geometry.trough_2,
        geometry.right_recovery_high,
    ]
    scaled = [
        type(mark)(
            type=mark.type,
            price=mark.price * factor,
            price_date=mark.price_date,
            confirmed_date=mark.confirmed_date,
            method=mark.method,
            amplitude_pct=mark.amplitude_pct,
            prominence_pct=mark.prominence_pct,
            separation_sessions=mark.separation_sessions,
            boundary=mark.boundary,
            evidence=mark.evidence,
        ) if mark is not None else None
        for mark in marks
    ]
    dates = [m.price_date for m in scaled if m is not None]
    start = min(dates)
    end = max(dates)
    from datetime import timedelta
    session_index = {start + timedelta(days=i): i for i in range((end - start).days + 1)}
    return build_double_bottom_geometry(session_index, *scaled)


def test_clear_positive_is_scale_invariant_under_small_uniform_perturbation():
    geometry = _by_name()["canonical_w"].geometry
    for factor in (0.999, 1.001):
        assert assess_double_bottom(_scaled_geometry(geometry, factor)).state == DoubleBottomState.RECOGNIZED


def test_clear_negative_is_scale_invariant_under_small_uniform_perturbation():
    geometry = _by_name()["too_deep"].geometry
    for factor in (0.999, 1.001):
        assert assess_double_bottom(_scaled_geometry(geometry, factor)).state == DoubleBottomState.REJECTED


def test_fixture_corpus_maps_to_preregistered_states():
    expected = {
        "canonical_w": DoubleBottomState.RECOGNIZED,
        "too_deep": DoubleBottomState.REJECTED,
        "no_second_undercut": DoubleBottomState.RECOGNIZED,
        "weak_middle_rebound": DoubleBottomState.AMBIGUOUS,
        "shallow_undercut": DoubleBottomState.AMBIGUOUS,
    }
    for fixture in double_bottom_fixtures():
        assert assess_double_bottom(fixture.geometry).state == expected[fixture.name]


def test_optional_right_recovery_does_not_change_core_w_classification():
    geometry = _by_name()["canonical_w"].geometry
    dates = [
        geometry.left_high.price_date,
        geometry.trough_1.price_date,
        geometry.middle_peak.price_date,
        geometry.trough_2.price_date,
    ]
    from datetime import timedelta
    start = min(dates)
    end = max(dates)
    session_index = {start + timedelta(days=i): i for i in range((end - start).days + 1)}
    no_right = build_double_bottom_geometry(
        session_index,
        geometry.left_high,
        geometry.trough_1,
        geometry.middle_peak,
        geometry.trough_2,
        None,
    )
    assert assess_double_bottom(no_right).state == DoubleBottomState.RECOGNIZED
