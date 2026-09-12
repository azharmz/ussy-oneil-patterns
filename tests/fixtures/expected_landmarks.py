from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd

from oneil_patterns.landmarks.model import LandmarkType
from tests.fixtures.morphologies import flat_sideways, noisy_loose_range, rounded_cup, v_shape, w_shape


@dataclass(frozen=True, slots=True)
class ExpectedRegion:
    type: LandmarkType
    start_index: int
    end_index: int
    label: str

    def __post_init__(self) -> None:
        if self.start_index < 0 or self.end_index < self.start_index:
            raise ValueError("invalid expected landmark region")


@dataclass(frozen=True, slots=True)
class LabelledFixture:
    name: str
    frame_factory: Callable[[], pd.DataFrame]
    expected: tuple[ExpectedRegion, ...]


FIXTURES: tuple[LabelledFixture, ...] = (
    LabelledFixture(
        name="v_shape",
        frame_factory=v_shape,
        expected=(
            ExpectedRegion(LandmarkType.SWING_LOW, 4, 6, "V trough"),
        ),
    ),
    LabelledFixture(
        name="w_shape",
        frame_factory=w_shape,
        expected=(
            ExpectedRegion(LandmarkType.SWING_LOW, 3, 5, "first bottom"),
            ExpectedRegion(LandmarkType.SWING_HIGH, 5, 7, "middle peak"),
            ExpectedRegion(LandmarkType.SWING_LOW, 8, 10, "second bottom"),
        ),
    ),
    LabelledFixture(
        name="flat_sideways",
        frame_factory=flat_sideways,
        expected=(),
    ),
    LabelledFixture(
        name="rounded_cup",
        frame_factory=rounded_cup,
        expected=(
            ExpectedRegion(LandmarkType.SWING_LOW, 13, 17, "rounded cup low"),
        ),
    ),
    LabelledFixture(
        name="noisy_loose_range",
        frame_factory=noisy_loose_range,
        expected=(
            ExpectedRegion(LandmarkType.SWING_HIGH, 6, 8, "major loose-range high"),
            ExpectedRegion(LandmarkType.SWING_LOW, 5, 7, "major loose-range low before high"),
            ExpectedRegion(LandmarkType.SWING_LOW, 11, 13, "major late loose-range low"),
        ),
    ),
)
