from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .ascending_base import AscendingBaseGeometry

MIN_DURATION_SESSIONS = 45
MAX_DURATION_SESSIONS = 80

# Source-grounded morphology guidance from IBD/MarketSmith material.
# Textbook guidance is 10%-20%; MarketSmith's programmed recognition
# envelope is broader at roughly 6%-25%. We use the latter only as an
# outer morphology guardrail so known 8%-9% textbook examples are not
# incorrectly rejected.
TEXTBOOK_PULLBACK_MIN = 0.10
TEXTBOOK_PULLBACK_MAX = 0.20
MARKETSMITH_PULLBACK_MIN = 0.06
MARKETSMITH_PULLBACK_MAX = 0.25


class AscendingBaseState(str, Enum):
    RECOGNIZED = "ASCENDING_BASE_RECOGNIZED"
    REJECTED = "ASCENDING_BASE_REJECTED"
    AMBIGUOUS = "ASCENDING_BASE_AMBIGUOUS"


class AscendingBaseFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    TOO_LONG = "TOO_LONG"
    NON_ASCENDING_TROUGHS = "NON_ASCENDING_TROUGHS"
    NON_ASCENDING_PEAKS = "NON_ASCENDING_PEAKS"
    PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE = "PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE"


@dataclass(frozen=True, slots=True)
class AscendingBaseAssessment:
    state: AscendingBaseState
    faults: tuple[AscendingBaseFault, ...]
    geometry: AscendingBaseGeometry
    theory_gates_pass: bool
    source_guardrails_pass: bool
    textbook_pullbacks: tuple[bool, bool, bool]


def assess_ascending_base(geometry: AscendingBaseGeometry) -> AscendingBaseAssessment:
    faults: list[AscendingBaseFault] = []

    if geometry.duration_sessions < MIN_DURATION_SESSIONS:
        faults.append(AscendingBaseFault.TOO_SHORT)
    if geometry.duration_sessions > MAX_DURATION_SESSIONS:
        faults.append(AscendingBaseFault.TOO_LONG)
    if not geometry.evidence["ascending_troughs"]:
        faults.append(AscendingBaseFault.NON_ASCENDING_TROUGHS)
    if not geometry.evidence["ascending_peaks"]:
        faults.append(AscendingBaseFault.NON_ASCENDING_PEAKS)

    textbook = tuple(
        TEXTBOOK_PULLBACK_MIN <= value <= TEXTBOOK_PULLBACK_MAX
        for value in geometry.pullback_depths
    )

    hard = {
        AscendingBaseFault.TOO_SHORT,
        AscendingBaseFault.TOO_LONG,
        AscendingBaseFault.NON_ASCENDING_TROUGHS,
        AscendingBaseFault.NON_ASCENDING_PEAKS,
    }
    if any(f in hard for f in faults):
        return AscendingBaseAssessment(
            AscendingBaseState.REJECTED,
            tuple(faults),
            geometry,
            theory_gates_pass=False,
            source_guardrails_pass=False,
            textbook_pullbacks=textbook,
        )

    outside_envelope = any(
        value < MARKETSMITH_PULLBACK_MIN or value > MARKETSMITH_PULLBACK_MAX
        for value in geometry.pullback_depths
    )
    if outside_envelope:
        faults.append(AscendingBaseFault.PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE)
        return AscendingBaseAssessment(
            AscendingBaseState.AMBIGUOUS,
            tuple(faults),
            geometry,
            theory_gates_pass=True,
            source_guardrails_pass=False,
            textbook_pullbacks=textbook,
        )

    return AscendingBaseAssessment(
        AscendingBaseState.RECOGNIZED,
        tuple(faults),
        geometry,
        theory_gates_pass=True,
        source_guardrails_pass=True,
        textbook_pullbacks=textbook,
    )
