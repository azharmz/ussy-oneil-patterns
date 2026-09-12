from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import pandas as pd

from oneil_patterns.landmarks.model import Landmark


@dataclass(frozen=True, slots=True)
class RegionLabel:
    type_value: str
    start_index: int
    end_index: int
    label: str = ""


@dataclass(frozen=True, slots=True)
class LabelEvalResult:
    expected: int
    detected: int
    matched: int
    missed: int
    false_turns: int
    mean_abs_index_error: float | None
    max_abs_index_error: int | None


def _price_date_index(frame: pd.DataFrame, landmark: Landmark) -> int | None:
    dates = pd.to_datetime(frame["date"]).dt.date
    hits = dates[dates == landmark.price_date]
    if hits.empty:
        return None
    return int(hits.index[0])


def evaluate_regions(
    frame: pd.DataFrame,
    detected: Iterable[Landmark],
    expected: Sequence[RegionLabel],
) -> LabelEvalResult:
    """Match detected landmarks to labelled index regions without using returns.

    Matching is one-to-one and type-aware. Among detections inside a labelled
    region, the detection closest to the region midpoint is selected. Remaining
    detections are counted as false structural turns.
    """
    det = list(detected)
    indexed: list[tuple[int, Landmark]] = []
    for mark in det:
        idx = _price_date_index(frame, mark)
        if idx is not None:
            indexed.append((idx, mark))

    used: set[int] = set()
    errors: list[int] = []
    matched = 0

    for region in expected:
        midpoint = (region.start_index + region.end_index) / 2
        candidates: list[tuple[float, int, int]] = []
        for j, (idx, mark) in enumerate(indexed):
            if j in used or mark.type.value != region.type_value:
                continue
            if region.start_index <= idx <= region.end_index:
                candidates.append((abs(idx - midpoint), j, idx))
        if not candidates:
            continue
        _, j, idx = min(candidates)
        used.add(j)
        matched += 1
        errors.append(int(round(abs(idx - midpoint))))

    missed = len(expected) - matched
    false_turns = len(indexed) - len(used)
    return LabelEvalResult(
        expected=len(expected),
        detected=len(indexed),
        matched=matched,
        missed=missed,
        false_turns=false_turns,
        mean_abs_index_error=(sum(errors) / len(errors)) if errors else None,
        max_abs_index_error=max(errors) if errors else None,
    )
