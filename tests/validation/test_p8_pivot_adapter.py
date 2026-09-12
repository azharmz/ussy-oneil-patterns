from datetime import date

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import LandmarkType
from oneil_patterns.morphology.cup_body import CupBodyGeometry
from oneil_patterns.morphology.cup_family import HandleGeometry
from oneil_patterns.morphology.double_bottom import DoubleBottomGeometry
from oneil_patterns.segmentation.model import BaseSegmentCandidate, SegmentStage
from oneil_patterns.validation.pivot_adapter import (
    PivotEvaluationState,
    cup_with_handle_pivot,
    cup_without_handle_pivot,
    double_bottom_pivot,
    flat_base_pivot,
)


def _high(price: float, day: int) -> LandmarkCandidate:
    d = date(2024, 1, day)
    return LandmarkCandidate(LandmarkType.SWING_HIGH, price, d, d, "test")


def _low(price: float, day: int) -> LandmarkCandidate:
    d = date(2024, 1, day)
    return LandmarkCandidate(LandmarkType.SWING_LOW, price, d, d, "test")


def test_flat_base_pivot_is_structural_left_high():
    start, trough, recovery = _high(100, 1), _low(92, 10), _high(99, 25)
    segment = BaseSegmentCandidate(
        start=start,
        trough=trough,
        recovery=recovery,
        stage=SegmentStage.RECOVERY_CONFIRMED,
        start_date=start.price_date,
        end_date=recovery.price_date,
        confirmed_date=recovery.confirmed_date,
        duration_sessions=25,
        decline_sessions=10,
        recovery_sessions=16,
        depth_pct=0.08,
        recovery_pct=(99 / 92) - 1,
        recovery_to_start_ratio=0.99,
        recovered_depth_fraction=7 / 8,
    )
    fact = flat_base_pivot(segment)
    assert fact.state == PivotEvaluationState.EVALUABLE
    assert fact.pivot_level == 100
    assert fact.pivot_source_date == start.price_date
    assert fact.pivot_landmark_type == "FLAT_LEFT_HIGH"


def test_double_bottom_pivot_is_middle_peak():
    left, t1, middle, t2, recovery = _high(100, 1), _low(80, 5), _high(95, 10), _low(79, 15), _high(98, 25)
    geometry = DoubleBottomGeometry(
        left_high=left,
        trough_1=t1,
        middle_peak=middle,
        trough_2=t2,
        right_recovery_high=recovery,
        confirmed_date=recovery.confirmed_date,
        duration_sessions=15,
        overall_depth_pct=0.21,
        trough_spacing_sessions=10,
        trough2_vs_trough1_pct=-0.0125,
        middle_peak_rebound_pct=0.1875,
        middle_peak_recovered_fraction=0.75,
        right_recovery_pct=0.24,
        right_recovery_to_left_high_ratio=0.98,
    )
    fact = double_bottom_pivot(geometry)
    assert fact.pivot_level == 95
    assert fact.pivot_source_date == middle.price_date
    assert fact.pivot_landmark_type == "MIDDLE_PEAK"


def _cup_geometry() -> CupBodyGeometry:
    left, trough, right = _high(120, 1), _low(90, 10), _high(118, 20)
    return CupBodyGeometry(
        left_rim=left,
        trough=trough,
        right_rim=right,
        confirmed_date=right.confirmed_date,
        duration_sessions=20,
        decline_sessions=10,
        recovery_sessions=11,
        depth_pct=0.25,
        right_rim_to_left_rim_ratio=118 / 120,
        left_right_time_ratio=10 / 11,
        sessions_within_5pct_of_trough=2,
        sessions_within_10pct_of_trough=4,
        lower_third_fraction=0.3,
        max_bottom_run_10pct=3,
    )


def test_cup_without_handle_pivot_is_left_rim():
    geometry = _cup_geometry()
    fact = cup_without_handle_pivot(geometry)
    assert fact.state == PivotEvaluationState.EVALUABLE
    assert fact.pivot_level == geometry.left_rim.price
    assert fact.pivot_source_date == geometry.left_rim.price_date
    assert fact.pivot_landmark_type == "LEFT_RIM"


def test_cwh_pivot_uses_explicit_persisted_handle_high_role():
    geometry = _cup_geometry()
    handle_low, handle_recovery = _low(110, 22), _high(117, 25)
    handle = HandleGeometry(
        handle_high=geometry.right_rim,
        handle_low=handle_low,
        handle_recovery=handle_recovery,
        confirmed_date=handle_recovery.confirmed_date,
        duration_sessions=6,
        depth_pct=(118 - 110) / 118,
        cup_midpoint_price=105,
        low_in_upper_half=True,
        recovery_to_right_rim_ratio=117 / 118,
    )
    fact = cup_with_handle_pivot(geometry, handle)
    assert fact.state == PivotEvaluationState.EVALUABLE
    assert fact.pivot_level == 118
    assert fact.pivot_source_date == geometry.right_rim.price_date
    assert fact.pivot_landmark_type == "HANDLE_HIGH"
