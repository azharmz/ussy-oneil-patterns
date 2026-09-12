from datetime import date

import pandas as pd

from oneil_patterns.landmarks.fusion import FusionPolicy, fuse_landmark_sources
from oneil_patterns.landmarks.model import Landmark, LandmarkType


def _frame():
    return pd.DataFrame({"date": pd.bdate_range("2026-01-02", periods=12)})


def _mark(type_, idx, method, evidence=None):
    dates = pd.bdate_range("2026-01-02", periods=12)
    return Landmark(
        type=type_,
        price=100.0,
        price_date=dates[idx].date(),
        confirmed_date=dates[min(idx + 2, 11)].date(),
        method=method,
        evidence=evidence or {},
    )


def test_auxiliary_only_turn_does_not_create_candidate():
    frame = _frame()
    auxiliary = [_mark(LandmarkType.SWING_LOW, 5, "confirmed_window", {"prominence_pct": 0.03})]
    out = fuse_landmark_sources(frame, [], auxiliary)
    assert out == []


def test_matching_auxiliary_turn_adds_corroboration_evidence():
    frame = _frame()
    primary = [_mark(LandmarkType.SWING_LOW, 5, "percentage_excursion", {"reversal_pct": 0.08})]
    auxiliary = [_mark(LandmarkType.SWING_LOW, 6, "confirmed_window", {"prominence_pct": 0.025})]
    out = fuse_landmark_sources(frame, primary, auxiliary, FusionPolicy(corroboration_tolerance_sessions=2))

    assert len(out) == 1
    candidate = out[0]
    assert candidate.method == "percentage_excursion"
    assert candidate.amplitude_pct == 0.08
    assert candidate.prominence_pct == 0.025
    assert candidate.evidence["auxiliary_corroborated"] is True
    assert candidate.evidence["auxiliary_distance_sessions"] == 1


def test_wrong_type_nearby_does_not_corroborate():
    frame = _frame()
    primary = [_mark(LandmarkType.SWING_LOW, 5, "percentage_excursion", {"reversal_pct": 0.08})]
    auxiliary = [_mark(LandmarkType.SWING_HIGH, 5, "confirmed_window", {"prominence_pct": 0.04})]
    candidate = fuse_landmark_sources(frame, primary, auxiliary)[0]
    assert candidate.evidence["auxiliary_corroborated"] is False
    assert candidate.prominence_pct is None


def test_boundary_status_survives_fusion():
    frame = _frame()
    primary = [_mark(LandmarkType.SWING_HIGH, 0, "percentage_excursion", {"reversal_pct": 0.08})]
    candidate = fuse_landmark_sources(frame, primary, [])[0]
    assert candidate.boundary is True
