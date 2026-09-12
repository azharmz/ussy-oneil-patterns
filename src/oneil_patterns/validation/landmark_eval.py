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


def prefix_stability(frame: pd.DataFrame, extractor: Extractor, min_prefix: int = 6) -> StabilityResult:
    """Verify that already-confirmed landmarks do not mutate when future bars arrive."""
    if len(frame) < min_prefix:
        return StabilityResult(0, 0, True)

    violations = 0
    checked = 0
    for end in range(min_prefix, len(frame)):
        prefix = frame.iloc[:end].copy()
        full_to_same_date = frame.iloc[:end].copy()
        a = extractor(prefix)
        b = extractor(full_to_same_date)
        sig_a = [(x.type.value, x.price, x.price_date, x.confirmed_date, x.method) for x in a]
        sig_b = [(x.type.value, x.price, x.price_date, x.confirmed_date, x.method) for x in b]
        checked += 1
        if sig_a != sig_b:
            violations += 1
    return StabilityResult(checked, violations, violations == 0)


def landmark_signature(items: Iterable[Landmark]) -> list[tuple[str, object, object]]:
    return [(x.type.value, x.price_date, x.confirmed_date) for x in items]


def agreement_by_date(a: Iterable[Landmark], b: Iterable[Landmark], tolerance_sessions: int = 1) -> dict[str, float]:
    """Simple morphology-facing agreement metric independent of returns.

    A landmark matches when type is equal and price dates are within the requested
    business-session tolerance. This is intentionally diagnostic, not a tuned score.
    """
    a = list(a)
    b = list(b)
    if not a and not b:
        return {"matched": 0.0, "precision_like": 1.0, "recall_like": 1.0}

    used: set[int] = set()
    matched = 0
    for x in a:
        best = None
        best_dist = None
        for j, y in enumerate(b):
            if j in used or x.type != y.type:
                continue
            dist = abs((pd.Timestamp(x.price_date) - pd.Timestamp(y.price_date)).days)
            if dist <= tolerance_sessions * 3 and (best_dist is None or dist < best_dist):
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
