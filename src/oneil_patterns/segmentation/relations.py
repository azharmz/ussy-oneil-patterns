from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .model import BaseSegmentCandidate


class SegmentRelation(str, Enum):
    DISJOINT = "DISJOINT"
    TOUCHING = "TOUCHING"
    OVERLAP = "OVERLAP"
    CONTAINS = "CONTAINS"
    WITHIN = "WITHIN"
    IDENTICAL = "IDENTICAL"


@dataclass(frozen=True, slots=True)
class SegmentRelationEvidence:
    left: BaseSegmentCandidate
    right: BaseSegmentCandidate
    relation: SegmentRelation
    overlap_sessions: int


def classify_segment_relation(
    left: BaseSegmentCandidate,
    right: BaseSegmentCandidate,
) -> SegmentRelation:
    """Classify structural interval relation using immutable segment boundaries.

    This function is morphology-neutral: it records interval structure and does
    not decide which candidate is the 'real' base.
    """
    a0, a1 = left.start_date, left.end_date
    b0, b1 = right.start_date, right.end_date

    if a0 == b0 and a1 == b1:
        return SegmentRelation.IDENTICAL
    if a0 <= b0 and a1 >= b1:
        return SegmentRelation.CONTAINS
    if b0 <= a0 and b1 >= a1:
        return SegmentRelation.WITHIN
    if a1 == b0 or b1 == a0:
        return SegmentRelation.TOUCHING
    if a1 < b0 or b1 < a0:
        return SegmentRelation.DISJOINT
    return SegmentRelation.OVERLAP


def annotate_segment_relations(
    segments: list[BaseSegmentCandidate],
) -> list[SegmentRelationEvidence]:
    """Return pairwise non-destructive overlap/nesting evidence.

    P2 deliberately keeps all provisional candidates. Suppression, ranking, or
    pattern-specific preference belongs to later morphology layers.
    """
    ordered = sorted(segments, key=lambda x: (x.start_date, x.end_date, x.confirmed_date))
    out: list[SegmentRelationEvidence] = []

    for i, left in enumerate(ordered):
        for right in ordered[i + 1 :]:
            relation = classify_segment_relation(left, right)
            overlap_sessions = 0
            if relation not in {SegmentRelation.DISJOINT, SegmentRelation.TOUCHING}:
                # Session-count precision belongs to frame-aware consumers; here
                # we record only a positive structural-overlap sentinel.
                overlap_sessions = 1
            out.append(
                SegmentRelationEvidence(
                    left=left,
                    right=right,
                    relation=relation,
                    overlap_sessions=overlap_sessions,
                )
            )
    return out
