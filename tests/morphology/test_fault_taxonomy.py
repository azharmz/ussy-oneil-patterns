import pytest

from oneil_patterns.morphology.ascending_base_detector import AscendingBaseFault, AscendingBaseState
from oneil_patterns.morphology.cup_body_detector import CupBodyFault, CupBodyState
from oneil_patterns.morphology.double_bottom_detector import DoubleBottomFault, DoubleBottomState
from oneil_patterns.morphology.faults import (
    FaultSeverity,
    NormalizedStatus,
    RuleProvenance,
    normalize_assessment,
    normalize_fault,
)
from oneil_patterns.morphology.flat_base import FlatBaseFault, FlatBaseState


def test_theory_and_research_faults_remain_distinguishable():
    theory = normalize_fault(DoubleBottomFault.NO_SECOND_TROUGH_UNDERCUT)
    research = normalize_fault(DoubleBottomFault.SHALLOW_UNDERCUT)
    context = normalize_fault(FlatBaseFault.BOUNDARY_CONTEXT)

    assert theory.severity == FaultSeverity.REJECT
    assert theory.provenance == RuleProvenance.THEORY
    assert research.severity == FaultSeverity.AMBIGUITY
    assert research.provenance == RuleProvenance.RESEARCH
    assert context.provenance == RuleProvenance.CONTEXT


def test_native_states_map_to_shared_statuses():
    recognized = normalize_assessment(
        pattern="FLAT_BASE",
        native_state=FlatBaseState.RECOGNIZED,
        native_faults=(),
        contract_version="flat-base-v1",
    )
    ambiguous = normalize_assessment(
        pattern="DOUBLE_BOTTOM",
        native_state=DoubleBottomState.AMBIGUOUS,
        native_faults=(DoubleBottomFault.SHALLOW_UNDERCUT,),
        contract_version="double-bottom-v1",
    )
    rejected = normalize_assessment(
        pattern="CUP_BODY",
        native_state=CupBodyState.REJECTED,
        native_faults=(CupBodyFault.SHARP_V,),
        contract_version="cup-family-v1",
    )

    assert recognized.status == NormalizedStatus.RECOGNIZED
    assert ambiguous.status == NormalizedStatus.AMBIGUOUS
    assert rejected.status == NormalizedStatus.REJECTED


def test_source_grounded_ascending_guardrail_normalizes_as_theory_ambiguity():
    envelope = normalize_assessment(
        pattern="ASCENDING_BASE",
        native_state=AscendingBaseState.AMBIGUOUS,
        native_faults=(AscendingBaseFault.PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE,),
        contract_version="ascending-base-v2",
    )
    assert envelope.faults[0].provenance == RuleProvenance.THEORY
    assert envelope.faults[0].severity == FaultSeverity.AMBIGUITY


def test_recognized_state_cannot_carry_reject_fault():
    with pytest.raises(ValueError, match="REJECT fault"):
        normalize_assessment(
            pattern="FLAT_BASE",
            native_state=FlatBaseState.RECOGNIZED,
            native_faults=(FlatBaseFault.TOO_DEEP,),
            contract_version="flat-base-v1",
        )
