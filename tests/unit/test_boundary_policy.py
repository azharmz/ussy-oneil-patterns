from datetime import date

import pandas as pd

from oneil_patterns.landmarks.boundary import BoundaryPolicy, classify_boundary, to_candidate_with_boundary
from oneil_patterns.landmarks.model import Landmark, LandmarkType


def _frame():
    return pd.DataFrame({"date": pd.bdate_range("2026-01-02", periods=10)})


def _mark(day_index: int) -> Landmark:
    dt = pd.Timestamp(_frame().iloc[day_index]["date"]).date()
    return Landmark(
        type=LandmarkType.SWING_HIGH,
        price=100.0,
        price_date=dt,
        confirmed_date=dt,
        method="test",
    )


def test_left_edge_landmark_is_flagged_not_deleted():
    frame = _frame()
    mark = _mark(1)
    boundary, left, right = classify_boundary(frame, mark, BoundaryPolicy(edge_sessions=2))
    assert boundary
    assert left == 1
    assert right == 8

    candidate = to_candidate_with_boundary(frame, mark, policy=BoundaryPolicy(edge_sessions=2))
    assert candidate.boundary is True
    assert candidate.evidence["boundary_left_distance"] == 1


def test_interior_landmark_is_not_boundary():
    frame = _frame()
    mark = _mark(5)
    boundary, left, right = classify_boundary(frame, mark, BoundaryPolicy(edge_sessions=2))
    assert boundary is False
    assert left == 5
    assert right == 4


def test_right_edge_landmark_is_flagged():
    frame = _frame()
    mark = _mark(8)
    boundary, left, right = classify_boundary(frame, mark, BoundaryPolicy(edge_sessions=2))
    assert boundary
    assert left == 8
    assert right == 1


def test_zero_edge_policy_only_flags_exact_endpoints():
    frame = _frame()
    first = _mark(0)
    second = _mark(1)
    assert classify_boundary(frame, first, BoundaryPolicy(edge_sessions=0))[0] is True
    assert classify_boundary(frame, second, BoundaryPolicy(edge_sessions=0))[0] is False
