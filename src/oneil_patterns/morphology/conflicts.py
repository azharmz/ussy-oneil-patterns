from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .faults import NormalizedStatus, PatternAssessmentEnvelope


class ConflictResolution(str, Enum):
    NO_RECOGNIZED_PATTERN = "NO_RECOGNIZED_PATTERN"
    CLEAR = "CLEAR"
    HIERARCHICAL = "HIERARCHICAL"
    MULTI_PATTERN_AMBIGUITY = "MULTI_PATTERN_AMBIGUITY"


@dataclass(frozen=True, slots=True)
class PatternConflictResult:
    resolution: ConflictResolution
    primary_pattern: str | None
    recognized_patterns: tuple[str, ...]


_CUP_FAMILY_NATIVE_STATES = {"CUP_WITH_HANDLE", "CUP_NO_HANDLE"}


def resolve_pattern_conflict(
    assessments: Iterable[PatternAssessmentEnvelope],
) -> PatternConflictResult:
    recognized = tuple(item for item in assessments if item.status == NormalizedStatus.RECOGNIZED)
    names = tuple(item.pattern for item in recognized)

    if not recognized:
        return PatternConflictResult(
            resolution=ConflictResolution.NO_RECOGNIZED_PATTERN,
            primary_pattern=None,
            recognized_patterns=(),
        )

    if len(recognized) == 1:
        return PatternConflictResult(
            resolution=ConflictResolution.CLEAR,
            primary_pattern=recognized[0].pattern,
            recognized_patterns=names,
        )

    # Cup body and downstream Cup family are intentionally hierarchical, not a
    # morphology contradiction. Prefer the family label when it is complete.
    cup_body = [item for item in recognized if item.pattern == "CUP_BODY"]
    cup_family = [
        item
        for item in recognized
        if item.pattern == "CUP_FAMILY" and item.native_state in _CUP_FAMILY_NATIVE_STATES
    ]
    non_cup = [item for item in recognized if item.pattern not in {"CUP_BODY", "CUP_FAMILY"}]
    if cup_body and len(cup_family) == 1 and not non_cup and len(recognized) == 2:
        return PatternConflictResult(
            resolution=ConflictResolution.HIERARCHICAL,
            primary_pattern=cup_family[0].native_state,
            recognized_patterns=names,
        )

    # Do not arbitrarily rank unrelated recognized patterns. Upstream callers
    # must preserve the ambiguity until labelled validation or explicit context
    # resolves it.
    return PatternConflictResult(
        resolution=ConflictResolution.MULTI_PATTERN_AMBIGUITY,
        primary_pattern=None,
        recognized_patterns=names,
    )
