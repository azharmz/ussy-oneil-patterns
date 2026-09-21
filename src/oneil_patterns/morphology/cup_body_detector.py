from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .cup_body import CupBodyGeometry

MIN_CUP_NO_HANDLE_DURATION_SESSIONS = 30
MAX_NORMAL_CUP_DEPTH_PCT = 0.33

# Research-only morphology bands. These are deliberately separated from the
# source-supported duration/depth gates and must not be tuned from returns.
MIN_MEANINGFUL_CUP_DEPTH_PCT = 0.08
MIN_BOTTOM_SESSIONS_WITHIN_5PCT = 3
MIN_BOTTOM_CONTIGUITY_RATIO = 0.75
MIN_RIGHT_RIM_RECOVERY_RATIO = 0.90


class CupBodyState(str, Enum):
    RECOGNIZED = "CUP_RECOGNIZED"
    REJECTED = "CUP_REJECTED"
    AMBIGUOUS = "CUP_AMBIGUOUS"


class CupBodyFault(str, Enum):
    TOO_SHORT = "TOO_SHORT"
    TOO_DEEP = "TOO_DEEP"
    SHALLOW_NON_CUP = "SHALLOW_NON_CUP"
    SHARP_V = "SHARP_V"
    FRAGMENTED_BOTTOM = "FRAGMENTED_BOTTOM"
    WEAK_RIGHT_RIM_RECOVERY = "WEAK_RIGHT_RIM_RECOVERY"


@dataclass(frozen=True, slots=True)
class CupBodyAssessment:
    state: CupBodyState
    faults: tuple[CupBodyFault, ...]
    geometry: CupBodyGeometry
    theory_gates_pass: bool
    research_bands_pass: bool


def assess_cup_body(geometry: CupBodyGeometry) -> CupBodyAssessment:
    """Assess Cup morphology under CWOH vNext validation-candidate semantics.

    Duration/depth remain hard theory gates. Roundedness/continuity numerical
    proxies remain explicit research evidence. FRAGMENTED_BOTTOM is retained as\n    evidence but is non-state-bearing in this validation candidate; SHARP_V and\n    WEAK_RIGHT_RIM_RECOVERY remain AMBIGUOUS. No numeric cutoff is changed.
    """
    faults: list[CupBodyFault] = []

    if geometry.duration_sessions < MIN_CUP_NO_HANDLE_DURATION_SESSIONS:
        faults.append(CupBodyFault.TOO_SHORT)
    if geometry.depth_pct > MAX_NORMAL_CUP_DEPTH_PCT:
        faults.append(CupBodyFault.TOO_DEEP)

    hard_faults = {CupBodyFault.TOO_SHORT, CupBodyFault.TOO_DEEP}
    if any(fault in hard_faults for fault in faults):
        return CupBodyAssessment(
            state=CupBodyState.REJECTED,
            faults=tuple(faults),
            geometry=geometry,
            theory_gates_pass=False,
            research_bands_pass=False,
        )

    if geometry.depth_pct < MIN_MEANINGFUL_CUP_DEPTH_PCT:
        faults.append(CupBodyFault.SHALLOW_NON_CUP)

    if geometry.sessions_within_5pct_of_trough < MIN_BOTTOM_SESSIONS_WITHIN_5PCT:
        faults.append(CupBodyFault.SHARP_V)

    if geometry.sessions_within_10pct_of_trough > 0:
        continuity = geometry.max_bottom_run_10pct / geometry.sessions_within_10pct_of_trough
    else:
        continuity = 0.0
    if continuity < MIN_BOTTOM_CONTIGUITY_RATIO:
        faults.append(CupBodyFault.FRAGMENTED_BOTTOM)

    if geometry.right_rim_to_left_rim_ratio < MIN_RIGHT_RIM_RECOVERY_RATIO:
        faults.append(CupBodyFault.WEAK_RIGHT_RIM_RECOVERY)

    if CupBodyFault.SHALLOW_NON_CUP in faults:
        state = CupBodyState.REJECTED
        research_pass = False
    elif any(
        fault in {
            CupBodyFault.SHARP_V,
            CupBodyFault.WEAK_RIGHT_RIM_RECOVERY,
        }
        for fault in faults
    ):
        state = CupBodyState.AMBIGUOUS
        research_pass = False
    else:
        state = CupBodyState.RECOGNIZED
        research_pass = CupBodyFault.FRAGMENTED_BOTTOM not in faults

    return CupBodyAssessment(
        state=state,
        faults=tuple(faults),
        geometry=geometry,
        theory_gates_pass=True,
        research_bands_pass=research_pass,
    )
