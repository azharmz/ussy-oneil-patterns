from __future__ import annotations

from .ascending_base_detector import AscendingBaseAssessment
from .base_on_base import BaseOnBaseAssessment
from .cup_body_detector import CupBodyAssessment
from .cup_family import CupFamilyState, HandleAssessment
from .double_bottom_detector import DoubleBottomAssessment
from .faults import PatternAssessmentEnvelope, normalize_assessment
from .flat_base import FlatBaseAssessment


def normalize_flat_base(assessment: FlatBaseAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="FLAT_BASE",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="flat-base-v1",
    )


def normalize_double_bottom(assessment: DoubleBottomAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="DOUBLE_BOTTOM",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="double-bottom-v1",
    )


def normalize_cup_body(assessment: CupBodyAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="CUP_BODY",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="cup-family-v1",
    )


def normalize_handle(assessment: HandleAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="HANDLE",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="cup-family-v1",
    )


def normalize_cup_family(state: CupFamilyState) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="CUP_FAMILY",
        native_state=state,
        native_faults=(),
        contract_version="cup-family-v1",
    )


def normalize_ascending_base(assessment: AscendingBaseAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="ASCENDING_BASE",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="ascending-base-v1",
    )


def normalize_base_on_base(assessment: BaseOnBaseAssessment) -> PatternAssessmentEnvelope:
    return normalize_assessment(
        pattern="BASE_ON_BASE",
        native_state=assessment.state,
        native_faults=assessment.faults,
        contract_version="advanced-patterns-v1",
    )
