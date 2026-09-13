from oneil_patterns.morphology.ascending_base_detector import (
    AscendingBaseFault,
    AscendingBaseState,
    assess_ascending_base,
)
from tests.fixtures.ascending_bases import ascending_base_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in ascending_base_fixtures()}


def test_canonical_ascending_base_is_recognized():
    result = assess_ascending_base(_by_name()["canonical"].geometry)
    assert result.state == AscendingBaseState.RECOGNIZED
    assert result.theory_gates_pass is True
    assert result.source_guardrails_pass is True


def test_nonascending_trough_is_rejected():
    result = assess_ascending_base(_by_name()["nonascending_trough"].geometry)
    assert result.state == AscendingBaseState.REJECTED
    assert AscendingBaseFault.NON_ASCENDING_TROUGHS in result.faults


def test_nonascending_peak_is_rejected():
    result = assess_ascending_base(_by_name()["nonascending_peak"].geometry)
    assert result.state == AscendingBaseState.REJECTED
    assert AscendingBaseFault.NON_ASCENDING_PEAKS in result.faults


def test_duration_bounds_are_hard_first_pass_gates():
    short = assess_ascending_base(_by_name()["too_short"].geometry)
    long = assess_ascending_base(_by_name()["too_long"].geometry)
    assert short.state == AscendingBaseState.REJECTED
    assert long.state == AscendingBaseState.REJECTED
    assert AscendingBaseFault.TOO_SHORT in short.faults
    assert AscendingBaseFault.TOO_LONG in long.faults


def test_pullback_outside_marketsmith_envelope_is_ambiguous():
    result = assess_ascending_base(_by_name()["irregular_depth"].geometry)
    assert result.state == AscendingBaseState.AMBIGUOUS
    assert result.theory_gates_pass is True
    assert result.source_guardrails_pass is False
    assert AscendingBaseFault.PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE in result.faults
