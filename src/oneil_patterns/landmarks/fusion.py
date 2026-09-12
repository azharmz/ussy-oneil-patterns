from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .boundary import BoundaryPolicy, to_candidate_with_boundary
from .candidate import LandmarkCandidate
from .model import Landmark


@dataclass(frozen=True, slots=True)
class FusionPolicy:
    """P1 landmark-source policy.

    Percentage-excursion landmarks are the primary causal structural-turn
    source.  Confirmed-window landmarks are auxiliary corroborating evidence;
    they do not create additional candidates on their own.
    """

    corroboration_tolerance_sessions: int = 2
    boundary_policy: BoundaryPolicy = BoundaryPolicy()

    def __post_init__(self) -> None:
        if self.corroboration_tolerance_sessions < 0:
            raise ValueError("corroboration_tolerance_sessions must be >= 0")


def _date_index(frame: pd.DataFrame) -> dict[object, int]:
    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    return {value: i for i, value in enumerate(dates)}


def _nearest_same_type(
    primary: Landmark,
    auxiliary: list[Landmark],
    index: dict[object, int],
    tolerance: int,
) -> tuple[Landmark | None, int | None]:
    primary_idx = index.get(primary.price_date)
    if primary_idx is None:
        return None, None

    best: Landmark | None = None
    best_distance: int | None = None
    for mark in auxiliary:
        if mark.type != primary.type:
            continue
        aux_idx = index.get(mark.price_date)
        if aux_idx is None:
            continue
        distance = abs(aux_idx - primary_idx)
        if distance <= tolerance and (best_distance is None or distance < best_distance):
            best = mark
            best_distance = distance
    return best, best_distance


def fuse_landmark_sources(
    frame: pd.DataFrame,
    primary: list[Landmark],
    auxiliary: list[Landmark],
    policy: FusionPolicy | None = None,
) -> list[LandmarkCandidate]:
    """Convert primary turns to candidates and attach auxiliary corroboration.

    This deliberately does *not* union all auxiliary extrema into the candidate
    set.  That avoids turning a local-window detector into a second independent
    morphology vocabulary while still preserving useful prominence evidence.
    """
    policy = policy or FusionPolicy()
    if frame.empty:
        return []
    required = {"date"}
    if not required.issubset(frame.columns):
        raise ValueError("frame missing required column: date")

    index = _date_index(frame)
    out: list[LandmarkCandidate] = []

    previous_primary_index: int | None = None
    for mark in sorted(primary, key=lambda x: (x.price_date, x.confirmed_date, x.type.value)):
        primary_idx = index.get(mark.price_date)
        if primary_idx is None:
            raise ValueError("primary landmark price_date is not present in frame")

        match, distance = _nearest_same_type(
            mark,
            auxiliary,
            index,
            policy.corroboration_tolerance_sessions,
        )

        separation = None if previous_primary_index is None else primary_idx - previous_primary_index
        previous_primary_index = primary_idx

        prominence = None
        extra = {
            "primary_source": True,
            "auxiliary_corroborated": match is not None,
            "auxiliary_method": match.method if match is not None else None,
            "auxiliary_price_date": match.price_date.isoformat() if match is not None else None,
            "auxiliary_distance_sessions": distance,
        }
        if match is not None:
            raw_prominence = match.evidence.get("prominence_pct")
            if raw_prominence is not None:
                prominence = float(raw_prominence)

        reversal = mark.evidence.get("reversal_pct")
        amplitude = float(reversal) if reversal is not None else None

        candidate = to_candidate_with_boundary(
            frame,
            mark,
            policy=policy.boundary_policy,
            amplitude_pct=amplitude,
            prominence_pct=prominence,
            separation_sessions=separation,
        )
        candidate = LandmarkCandidate.from_landmark(
            mark,
            amplitude_pct=candidate.amplitude_pct,
            prominence_pct=candidate.prominence_pct,
            separation_sessions=candidate.separation_sessions,
            boundary=candidate.boundary,
            extra_evidence={**candidate.evidence, **extra},
        )
        out.append(candidate)

    return out
