from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class RuleProvenance(str, Enum):
    THEORY = "THEORY"
    RESEARCH = "RESEARCH"
    CONTEXT = "CONTEXT"


class FaultSeverity(str, Enum):
    REJECT = "REJECT"
    AMBIGUITY = "AMBIGUITY"
    INFO = "INFO"


class NormalizedStatus(str, Enum):
    RECOGNIZED = "RECOGNIZED"
    REJECTED = "REJECTED"
    AMBIGUOUS = "AMBIGUOUS"
    INCOMPLETE = "INCOMPLETE"
    NOT_EVALUABLE = "NOT_EVALUABLE"


@dataclass(frozen=True, slots=True)
class NormalizedFault:
    code: str
    severity: FaultSeverity
    provenance: RuleProvenance
    native_code: str


@dataclass(frozen=True, slots=True)
class PatternAssessmentEnvelope:
    pattern: str
    status: NormalizedStatus
    native_state: str
    faults: tuple[NormalizedFault, ...]
    contract_version: str


_FAULT_POLICY: dict[str, tuple[FaultSeverity, RuleProvenance]] = {
    # Theory-grounded hard morphology gates.
    "TOO_SHORT": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "TOO_LONG": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "TOO_DEEP": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "NO_SECOND_TROUGH_UNDERCUT": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "BELOW_CUP_MIDPOINT": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "NON_ASCENDING_TROUGHS": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    "NON_ASCENDING_PEAKS": (FaultSeverity.REJECT, RuleProvenance.THEORY),
    # Theory-backed normality guidance but exceptional cases may remain viable.
    "DEEP_HANDLE_EXCEPTIONAL": (FaultSeverity.AMBIGUITY, RuleProvenance.THEORY),
    # Context/boundary evidence.
    "BOUNDARY_CONTEXT": (FaultSeverity.AMBIGUITY, RuleProvenance.CONTEXT),
    # Research-only numerical morphology translations.
    "WIDE_LOOSE": (FaultSeverity.REJECT, RuleProvenance.RESEARCH),
    "SHALLOW_UNDERCUT": (FaultSeverity.AMBIGUITY, RuleProvenance.RESEARCH),
    "WEAK_MIDDLE_REBOUND": (FaultSeverity.AMBIGUITY, RuleProvenance.RESEARCH),
    "SHALLOW_NON_CUP": (FaultSeverity.REJECT, RuleProvenance.RESEARCH),
    "SHARP_V": (FaultSeverity.REJECT, RuleProvenance.RESEARCH),
    "FRAGMENTED_BOTTOM": (FaultSeverity.REJECT, RuleProvenance.RESEARCH),
    "WEAK_RIGHT_RIM_RECOVERY": (FaultSeverity.AMBIGUITY, RuleProvenance.RESEARCH),
    "PULLBACK_DEPTH_INCONSISTENT": (FaultSeverity.AMBIGUITY, RuleProvenance.RESEARCH),
    "SECOND_BASE_NOT_ABOVE_FIRST": (FaultSeverity.REJECT, RuleProvenance.RESEARCH),
    "SECOND_BASE_ONLY_MARGINAL_ABOVE": (FaultSeverity.AMBIGUITY, RuleProvenance.RESEARCH),
}


def _value(value: object) -> str:
    return str(getattr(value, "value", value))


def normalize_state(native_state: object) -> NormalizedStatus:
    value = _value(native_state).upper()
    if "NOT_EVALUABLE" in value:
        return NormalizedStatus.NOT_EVALUABLE
    if "INCOMPLETE" in value:
        return NormalizedStatus.INCOMPLETE
    if "AMBIGUOUS" in value:
        return NormalizedStatus.AMBIGUOUS
    if "REJECTED" in value or value.endswith("REJECT"):
        return NormalizedStatus.REJECTED
    if "RECOGNIZED" in value or value in {"CUP_WITH_HANDLE", "CUP_NO_HANDLE"}:
        return NormalizedStatus.RECOGNIZED
    raise ValueError(f"unknown native state: {value}")


def normalize_fault(native_fault: object) -> NormalizedFault:
    code = _value(native_fault).upper()
    if code not in _FAULT_POLICY:
        raise ValueError(f"unregistered fault code: {code}")
    severity, provenance = _FAULT_POLICY[code]
    return NormalizedFault(code=code, severity=severity, provenance=provenance, native_code=code)


def normalize_assessment(
    *,
    pattern: str,
    native_state: object,
    native_faults: Iterable[object],
    contract_version: str,
) -> PatternAssessmentEnvelope:
    faults = tuple(normalize_fault(fault) for fault in native_faults)
    status = normalize_state(native_state)

    if status == NormalizedStatus.RECOGNIZED and any(f.severity == FaultSeverity.REJECT for f in faults):
        raise ValueError("recognized assessment cannot carry normalized REJECT fault")

    return PatternAssessmentEnvelope(
        pattern=pattern,
        status=status,
        native_state=_value(native_state),
        faults=faults,
        contract_version=contract_version,
    )
