from oneil_patterns.morphology.double_bottom_detector import (
    DoubleBottomFault,
    DoubleBottomState,
    assess_double_bottom,
)
from tests.fixtures.double_bottoms import double_bottom_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in double_bottom_fixtures()}


def test_canonical_w_is_recognized():
    result = assess_double_bottom(_by_name()["canonical_w"].geometry)
    assert result.state == DoubleBottomState.RECOGNIZED
    assert result.theory_gates_pass is True
    assert result.research_bands_pass is True


def test_too_deep_is_rejected_by_theory_gate():
    result = assess_double_bottom(_by_name()["too_deep"].geometry)
    assert result.state == DoubleBottomState.REJECTED
    assert DoubleBottomFault.TOO_DEEP in result.faults


def test_no_second_undercut_is_explicit_ambiguity_in_v2():
    result = assess_double_bottom(_by_name()["no_second_undercut"].geometry)
    assert result.state == DoubleBottomState.AMBIGUOUS
    assert result.theory_gates_pass is True
    assert result.research_bands_pass is False
    assert DoubleBottomFault.NO_SECOND_TROUGH_UNDERCUT in result.faults


def test_weak_middle_rebound_stays_ambiguous_research_only():
    result = assess_double_bottom(_by_name()["weak_middle_rebound"].geometry)
    assert result.state == DoubleBottomState.AMBIGUOUS
    assert result.theory_gates_pass is True
    assert DoubleBottomFault.WEAK_MIDDLE_REBOUND in result.faults


def test_shallow_undercut_stays_ambiguous_research_only():
    result = assess_double_bottom(_by_name()["shallow_undercut"].geometry)
    assert result.state == DoubleBottomState.AMBIGUOUS
    assert result.theory_gates_pass is True
    assert DoubleBottomFault.SHALLOW_UNDERCUT in result.faults
