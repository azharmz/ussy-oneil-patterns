from datetime import date

import pytest

from oneil_patterns.landmarks.model import Landmark, LandmarkType


def test_landmark_preserves_price_and_confirmation_dates() -> None:
    lm = Landmark(
        type=LandmarkType.LEFT_PEAK,
        price=100.0,
        price_date=date(2026, 1, 5),
        confirmed_date=date(2026, 1, 8),
        method="fixture",
    )

    assert not lm.is_known_asof(date(2026, 1, 7))
    assert lm.is_known_asof(date(2026, 1, 8))


def test_confirmation_cannot_precede_price_date() -> None:
    with pytest.raises(ValueError):
        Landmark(
            type=LandmarkType.TROUGH_1,
            price=90.0,
            price_date=date(2026, 1, 8),
            confirmed_date=date(2026, 1, 7),
            method="fixture",
        )
