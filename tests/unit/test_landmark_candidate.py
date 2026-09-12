from datetime import date

import pytest

from oneil_patterns.landmarks.candidate import LandmarkCandidate
from oneil_patterns.landmarks.model import Landmark, LandmarkType


def test_candidate_preserves_pit_dates_and_provenance():
    landmark = Landmark(
        type=LandmarkType.SWING_LOW,
        price=90.0,
        price_date=date(2026, 1, 5),
        confirmed_date=date(2026, 1, 9),
        method="percentage_excursion",
        evidence={"reversal_pct": 0.08},
    )
    candidate = LandmarkCandidate.from_landmark(
        landmark,
        amplitude_pct=0.12,
        prominence_pct=0.04,
        separation_sessions=4,
        boundary=False,
        extra_evidence={"scale": "medium"},
    )

    assert candidate.price_date == date(2026, 1, 5)
    assert candidate.confirmed_date == date(2026, 1, 9)
    assert candidate.evidence["reversal_pct"] == 0.08
    assert candidate.evidence["scale"] == "medium"
    assert not candidate.is_known_asof(date(2026, 1, 8))
    assert candidate.is_known_asof(date(2026, 1, 9))


def test_candidate_rejects_pattern_specific_landmark_type():
    with pytest.raises(ValueError):
        LandmarkCandidate(
            type=LandmarkType.LEFT_PEAK,
            price=100.0,
            price_date=date(2026, 1, 5),
            confirmed_date=date(2026, 1, 8),
            method="test",
        )
