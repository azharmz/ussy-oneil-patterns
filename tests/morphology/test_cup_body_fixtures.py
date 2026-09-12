from tests.fixtures.cup_bodies import cup_body_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in cup_body_fixtures()}


def test_rounded_u_has_broader_bottom_than_sharp_v():
    fixtures = _by_name()
    u = fixtures["rounded_u"].geometry
    v = fixtures["sharp_v"].geometry

    assert fixtures["rounded_u"].label == "POSITIVE"
    assert fixtures["sharp_v"].label == "NEGATIVE"
    assert u.sessions_within_5pct_of_trough > v.sessions_within_5pct_of_trough
    assert u.max_bottom_run_10pct > v.max_bottom_run_10pct
    assert u.lower_third_fraction > v.lower_third_fraction


def test_rounded_u_meets_first_pass_normal_depth_and_duration():
    g = _by_name()["rounded_u"].geometry
    assert g.duration_sessions >= 30
    assert 0.12 <= g.depth_pct <= 0.33
    assert g.right_rim_to_left_rim_ratio >= 0.95


def test_flat_fixture_is_shallow_not_a_normal_cup():
    fixture = _by_name()["flat_shallow"]
    assert fixture.label == "NEGATIVE"
    assert fixture.geometry.depth_pct < 0.12


def test_w_fixture_has_fragmented_bottom_relative_to_rounded_u():
    fixtures = _by_name()
    w = fixtures["double_bottom_w"].geometry
    u = fixtures["rounded_u"].geometry
    assert fixtures["double_bottom_w"].label == "NEGATIVE"
    assert w.max_bottom_run_10pct < u.max_bottom_run_10pct


def test_wide_loose_fixture_is_not_silently_positive():
    fixture = _by_name()["wide_loose"]
    assert fixture.label == "NEGATIVE"
    assert fixture.geometry.duration_sessions >= 30
    assert fixture.geometry.evidence["roundedness_threshold_frozen"] is False
