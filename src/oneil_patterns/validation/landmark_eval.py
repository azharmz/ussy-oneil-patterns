from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

import pandas as pd

from oneil_patterns.landmarks.model import Landmark


Extractor = Callable[[pd.DataFrame], list[Landmark]]


@dataclass(frozen=True, slots=True)
class StabilityResult:
    prefixes_checked: int
    violations: int
    stable: bool


def _signature(items: Iterable[Landmark]) -> list[tuple[str, float, object, object, str]]:
    return [
        (x.type.value, round(float(x.price), 10), x.price_date, x.confirmed_date, x.method)
        for x in items
    ]


def prefix_stability(frame: pd.DataFrame, extractor: Extractor, min_prefix: int = 6) -> StabilityResult:
    """Detect repainting of landmarks that were already knowable at each prefix."""
    if len(frame) < min_prefix:
        return StabilityResult(0, 0, True)

    data = frame.sort_values("date").reset_index(drop=True)
    full = extractor(data)
    violations = 0
    checked = 0

    for end in range(min_prefix, len(data) + 1):
        prefix = data.iloc[:end].copy()
        cutoff = pd.Timestamp(prefix.iloc[-1]["date"]).date()
        contemporary = extractor(prefix)
        eventual_known = [x for x in full if x.confirmed_date <= cutoff]
        checked += 1
        if _signature(contemporary) != _signature(eventual_known):
            violations += 1

    return StabilityResult(checked, violations, violations == 0)


def landmark_signature(items: Iterable[Landmark]) -> list[tuple[str, object, object]]:
    return [(x.type.value, x.price_date, x.confirmed_date) for x in items]


def agreement_by_date(a: Iterable[Landmark], b: Iterable[Landmark], tolerance_sessions: int = 1) -> dict[str, float]:
    """Simple morphology-facing agreement metric independent of returns."""
    if tolerance_sessions < 0:
        raise ValueError("tolerance_sessions must be >= 0")

    a = list(a)
    b = list(b)
    if not a and not b:
        return {"matched": 0.0, "precision_like": 1.0, "recall_like": 1.0}

    used: set[int] = set()
    matched = 0
    max_calendar_days = tolerance_sessions * 3
    for x in a:
        best = None
        best_dist = None
        for j, y in enumerate(b):
            if j in used or x.type != y.type:
                continue
            dist = abs((pd.Timestamp(x.price_date) - pd.Timestamp(y.price_date)).days)
            if dist <= max_calendar_days and (best_dist is None or dist < best_dist):
                best = j
                best_dist = dist
        if best is not None:
            used.add(best)
            matched += 1

    return {
        "matched": float(matched),
        "precision_like": matched / len(a) if a else 1.0,
        "recall_like": matched / len(b) if b else 1.0,
    }
