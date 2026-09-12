from tests.fixtures.double_bottoms import double_bottom_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in double_bottom_fixtures()}


def test_canonical_w_has_supported_theory_geometry():
    fixture = _by_name()["canonical_w"]
    g = fixture.geometry
    assert fixture.label == "POSITIVE"
    assert g.duration_sessions >= 35
    assert g.overall_depth_pct <= 0.40
    assert g.trough2_vs_trough1_pct < 0
    assert g.middle_peak_recovered_fraction > 0


def test_too_deep_fixture_exceeds_40_percent():
    fixture = _by_name()["too_deep"]
    assert fixture.label == "NEGATIVE"
    assert fixture.geometry.overall_depth_pct > 0.40


def test_non_undercutting_second_trough_is_negative_fixture():
    fixture = _by_name()["no_second_undercut"]
    assert fixture.label == "NEGATIVE"
    assert fixture.geometry.trough2_vs_trough1_pct > 0
    assert fixture.geometry.evidence["second_trough_undercuts_first"] is False


def test_research_only_dimensions_are_kept_ambiguous():
    fixtures = _by_name()
    weak = fixtures["weak_middle_rebound"]
    shallow = fixtures["shallow_undercut"]
    assert weak.label == "AMBIGUOUS"
    assert shallow.label == "AMBIGUOUS"
    assert weak.geometry.middle_peak_recovered_fraction < fixtures["canonical_w"].geometry.middle_peak_recovered_fraction
    assert abs(shallow.geometry.trough2_vs_trough1_pct) < abs(fixtures["canonical_w"].geometry.trough2_vs_trough1_pct)
