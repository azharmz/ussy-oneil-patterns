from datetime import timedelta

from oneil_patterns.morphology.ascending_base import build_ascending_base_geometry
from oneil_patterns.morphology.ascending_base_detector import (
    AscendingBaseFault,
    AscendingBaseState,
    assess_ascending_base,
)
from tests.fixtures.ascending_bases import ascending_base_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in ascending_base_fixtures()}


def _marks(g):
    return (g.peak_1, g.trough_1, g.peak_2, g.trough_2, g.peak_3, g.trough_3, g.recovery_peak)


def test_future_session_index_extension_does_not_change_geometry_or_state():
    fixture = _by_name()["canonical"]
    g = fixture.geometry
    start = g.peak_1.price_date
    end = g.recovery_peak.price_date
    baseline_index = {start + timedelta(days=i): i for i in range((end - start).days + 1)}
    extended_index = {start + timedelta(days=i): i for i in range((end - start).days + 40)}

    baseline = build_ascending_base_geometry(baseline_index, *_marks(g))
    extended = build_ascending_base_geometry(extended_index, *_marks(g))

    assert extended.duration_sessions == baseline.duration_sessions
    assert extended.pullback_depths == baseline.pullback_depths
    assert assess_ascending_base(extended).state == assess_ascending_base(baseline).state == AscendingBaseState.RECOGNIZED


def test_confirmation_date_is_latest_required_landmark_confirmation():
    g = _by_name()["canonical"].geometry
    assert g.confirmed_date == max(mark.confirmed_date for mark in _marks(g))


def test_fixture_state_map_is_stable():
    expected = {
        "canonical": AscendingBaseState.RECOGNIZED,
        "nonascending_trough": AscendingBaseState.REJECTED,
        "nonascending_peak": AscendingBaseState.REJECTED,
        "too_short": AscendingBaseState.REJECTED,
        "too_long": AscendingBaseState.REJECTED,
        "irregular_depth": AscendingBaseState.AMBIGUOUS,
    }
    for fixture in ascending_base_fixtures():
        assert assess_ascending_base(fixture.geometry).state == expected[fixture.name]


def test_textbook_band_is_evidence_not_a_hidden_hard_gate():
    result = assess_ascending_base(_by_name()["canonical"].geometry)
    assert result.state == AscendingBaseState.RECOGNIZED
    assert result.source_guardrails_pass is True
    assert result.textbook_pullbacks == (True, True, True)


def test_outside_marketsmith_envelope_is_ambiguous_not_return_tuned():
    result = assess_ascending_base(_by_name()["irregular_depth"].geometry)
    assert result.state == AscendingBaseState.AMBIGUOUS
    assert result.theory_gates_pass is True
    assert result.source_guardrails_pass is False
    assert AscendingBaseFault.PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE in result.faults
