from oneil_patterns.morphology.cup_body_detector import (
    CupBodyFault,
    CupBodyState,
    assess_cup_body,
)
from tests.fixtures.cup_bodies import cup_body_fixtures


def _by_name():
    return {fixture.name: fixture for fixture in cup_body_fixtures()}


def test_rounded_u_is_recognized():
    result = assess_cup_body(_by_name()["rounded_u"].geometry)
    assert result.state == CupBodyState.RECOGNIZED
    assert result.theory_gates_pass is True
    assert result.research_bands_pass is True


def test_sharp_v_is_rejected_by_research_morphology():
    result = assess_cup_body(_by_name()["sharp_v"].geometry)
    assert result.state == CupBodyState.REJECTED
    assert CupBodyFault.SHARP_V in result.faults
    assert result.theory_gates_pass is True


def test_double_bottom_w_is_rejected_as_fragmented_bottom():
    result = assess_cup_body(_by_name()["double_bottom_w"].geometry)
    assert result.state == CupBodyState.REJECTED
    assert CupBodyFault.FRAGMENTED_BOTTOM in result.faults


def test_flat_shallow_is_rejected_as_non_cup_research_fault():
    result = assess_cup_body(_by_name()["flat_shallow"].geometry)
    assert result.state == CupBodyState.REJECTED
    assert CupBodyFault.SHALLOW_NON_CUP in result.faults


def test_wide_loose_is_rejected_as_fragmented_bottom():
    result = assess_cup_body(_by_name()["wide_loose"].geometry)
    assert result.state == CupBodyState.REJECTED
    assert CupBodyFault.FRAGMENTED_BOTTOM in result.faults
