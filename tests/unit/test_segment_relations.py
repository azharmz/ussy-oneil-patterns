from datetime import date

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.segmentation.model import BaseSegmentCandidate, SegmentStage
from oneil_patterns.segmentation.relations import (
    SegmentRelation,
    annotate_segment_relations,
    classify_segment_relation,
)


def _lm(kind, price, d):
    return LandmarkCandidate(
        type=kind,
        price=price,
        price_date=d,
        confirmed_date=d,
        method="test",
    )


def _segment(start_d, trough_d, end_d, *, start_price=100.0, trough_price=80.0, end_price=95.0):
    start = _lm(LandmarkType.SWING_HIGH, start_price, start_d)
    trough = _lm(LandmarkType.SWING_LOW, trough_price, trough_d)
    recovery = _lm(LandmarkType.SWING_HIGH, end_price, end_d)
    depth = (start_price - trough_price) / start_price
    recovered = (end_price - trough_price) / (start_price - trough_price)
    return BaseSegmentCandidate(
        start=start,
        trough=trough,
        recovery=recovery,
        stage=SegmentStage.RECOVERY_CONFIRMED,
        start_date=start_d,
        end_date=end_d,
        confirmed_date=end_d,
        duration_sessions=10,
        decline_sessions=5,
        recovery_sessions=6,
        depth_pct=depth,
        recovery_pct=(end_price - trough_price) / trough_price,
        recovery_to_start_ratio=end_price / start_price,
        recovered_depth_fraction=recovered,
    )


def test_nested_segment_relation_is_directional():
    outer = _segment(date(2026, 1, 2), date(2026, 1, 8), date(2026, 1, 20))
    inner = _segment(date(2026, 1, 6), date(2026, 1, 9), date(2026, 1, 14))

    assert classify_segment_relation(outer, inner) == SegmentRelation.CONTAINS
    assert classify_segment_relation(inner, outer) == SegmentRelation.WITHIN


def test_partial_overlap_is_not_misclassified_as_nesting():
    left = _segment(date(2026, 1, 2), date(2026, 1, 8), date(2026, 1, 14))
    right = _segment(date(2026, 1, 9), date(2026, 1, 13), date(2026, 1, 20))

    assert classify_segment_relation(left, right) == SegmentRelation.OVERLAP


def test_disjoint_and_touching_are_distinct():
    left = _segment(date(2026, 1, 2), date(2026, 1, 6), date(2026, 1, 10))
    touching = _segment(date(2026, 1, 10), date(2026, 1, 13), date(2026, 1, 16))
    disjoint = _segment(date(2026, 1, 12), date(2026, 1, 15), date(2026, 1, 20))

    assert classify_segment_relation(left, touching) == SegmentRelation.TOUCHING
    assert classify_segment_relation(left, disjoint) == SegmentRelation.DISJOINT


def test_annotation_preserves_all_candidates_instead_of_suppressing_nested_one():
    outer = _segment(date(2026, 1, 2), date(2026, 1, 8), date(2026, 1, 20))
    inner = _segment(date(2026, 1, 6), date(2026, 1, 9), date(2026, 1, 14))
    later = _segment(date(2026, 1, 22), date(2026, 1, 26), date(2026, 1, 30))

    evidence = annotate_segment_relations([outer, inner, later])

    assert len(evidence) == 3
    assert any(item.relation == SegmentRelation.CONTAINS for item in evidence)
    assert any(item.relation == SegmentRelation.DISJOINT for item in evidence)
