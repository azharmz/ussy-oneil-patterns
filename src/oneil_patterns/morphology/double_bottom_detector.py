from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .double_bottom import DoubleBottomGeometry

MIN_DURATION_SESSIONS = 35
MAX_DEPTH_PCT = 0.40

# Research-only morphology bands. These are not claimed as official IBD/O'Neil
# numerical rules and must not be tuned from trading returns.
MIN_CLEAR_UNDERCUT_PCT = 0.005
MIN_CLEAR_MIDDLE_RECOVERED_FRACTION = 0.50


class DoubleBottomState(str, Enum):
    RECOGNIZED = "DOUBLE_BOTTOM_RECOGNIZED"
    REJECTED = "DOUBLE_BOTTOM_REJECTED"
    AMBIGUOUS = "DOUBLE_BOTTOM_AMBIGUOUS"


class DoubleBottomFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    TOO_DEEP = "TOO_DEEP"
    NO_SECOND_TROUGH_UNDERCUT = "NO_SECOND_TROUGH_UNDERCUT"
    SHALLOW_UNDERCUT = "SHALLOW_UNDERCUT"
    WEAK_MIDDLE_REBOUND = "WEAK_MIDDLE_REBOUND"


@dataclass(frozen=True, slots=True)
class DoubleBottomAssessment:
    state: DoubleBottomState
    faults: tuple[DoubleBottomFault, ...]
    geometry: DoubleBottomGeometry
    theory_gates_pass: bool
    research_bands_pass: bool


def assess_double_bottom(geometry: DoubleBottomGeometry) -> DoubleBottomAssessment:
    faults: list[DoubleBottomFault] = []

    if geometry.duration_sessions < MIN_DURATION_SESSIONS:
        faults.append(DoubleBottomFault.TOO_SHORT)
    if geometry.overall_depth_pct > MAX_DEPTH_PCT:
        faults.append(DoubleBottomFault.TOO_DEEP)
    if geometry.trough2_vs_trough1_pct >= 0:
        faults.append(DoubleBottomFault.NO_SECOND_TROUGH_UNDERCUT)

    hard_faults = {
        DoubleBottomFault.TOO_SHORT,
        DoubleBottomFault.TOO_DEEP,
        DoubleBottomFault.NO_SECOND_TROUGH_UNDERCUT,
    }
    if any(f in hard_faults for f in faults):
        return DoubleBottomAssessment(
            DoubleBottomState.REJECTED,
            tuple(faults),
            geometry,
            theory_gates_pass=False,
            research_bands_pass=False,
        )

    if abs(geometry.trough2_vs_trough1_pct) < MIN_CLEAR_UNDERCUT_PCT:
        faults.append(DoubleBottomFault.SHALLOW_UNDERCUT)
    if geometry.middle_peak_recovered_fraction < MIN_CLEAR_MIDDLE_RECOVERED_FRACTION:
        faults.append(DoubleBottomFault.WEAK_MIDDLE_REBOUND)

    research_faults = {
        DoubleBottomFault.SHALLOW_UNDERCUT,
        DoubleBottomFault.WEAK_MIDDLE_REBOUND,
    }
    if any(f in research_faults for f in faults):
        state = DoubleBottomState.AMBIGUOUS
        research_pass = False
    else:
        state = DoubleBottomState.RECOGNIZED
        research_pass = True

    return DoubleBottomAssessment(
        state,
        tuple(faults),
        geometry,
        theory_gates_pass=True,
        research_bands_pass=research_pass,
    )
