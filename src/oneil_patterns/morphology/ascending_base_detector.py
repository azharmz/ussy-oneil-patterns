from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .ascending_base import AscendingBaseGeometry

MIN_DURATION_SESSIONS = 45
MAX_DURATION_SESSIONS = 80

# Research-only shape band; not an official IBD numeric rule.
MAX_PULLBACK_DEPTH_DISPERSION = 0.05


class AscendingBaseState(str, Enum):
    RECOGNIZED = "ASCENDING_BASE_RECOGNIZED"
    REJECTED = "ASCENDING_BASE_REJECTED"
    AMBIGUOUS = "ASCENDING_BASE_AMBIGUOUS"


class AscendingBaseFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    TOO_LONG = "TOO_LONG"
    NON_ASCENDING_TROUGHS = "NON_ASCENDING_TROUGHS"
    NON_ASCENDING_PEAKS = "NON_ASCENDING_PEAKS"
    PULLBACK_DEPTH_INCONSISTENT = "PULLBACK_DEPTH_INCONSISTENT"


@dataclass(frozen=True, slots=True)
class AscendingBaseAssessment:
    state: AscendingBaseState
    faults: tuple[AscendingBaseFault, ...]
    geometry: AscendingBaseGeometry
    theory_gates_pass: bool
    research_bands_pass: bool


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
            research_bands_pass=False,
        )

    if geometry.pullback_depth_dispersion > MAX_PULLBACK_DEPTH_DISPERSION:
        faults.append(AscendingBaseFault.PULLBACK_DEPTH_INCONSISTENT)
        return AscendingBaseAssessment(
            AscendingBaseState.AMBIGUOUS,
            tuple(faults),
            geometry,
            theory_gates_pass=True,
            research_bands_pass=False,
        )

    return AscendingBaseAssessment(
        AscendingBaseState.RECOGNIZED,
        tuple(faults),
        geometry,
        theory_gates_pass=True,
        research_bands_pass=True,
    )
