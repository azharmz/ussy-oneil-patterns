from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .candidate import LandmarkCandidate
from .model import Landmark


@dataclass(frozen=True, slots=True)
class BoundaryPolicy:
    """Classify extrema too close to the observed-series edges as boundary artifacts.

    Boundary marking is evidence, not deletion.  Later morphology layers may
    choose to ignore, down-weight, or require corroboration for these turns.
    """

    edge_sessions: int = 2

    def __post_init__(self) -> None:
        if self.edge_sessions < 0:
            raise ValueError("edge_sessions must be >= 0")


def classify_boundary(
    frame: pd.DataFrame,
    landmark: Landmark,
    policy: BoundaryPolicy | None = None,
) -> tuple[bool, int | None, int | None]:
    policy = policy or BoundaryPolicy()
    if frame.empty:
        raise ValueError("frame cannot be empty")
    if "date" not in frame.columns:
        raise ValueError("frame missing required column: date")

    dates = pd.to_datetime(frame["date"], errors="raise").dt.date.tolist()
    try:
        index = dates.index(landmark.price_date)
    except ValueError as exc:
        raise ValueError("landmark price_date is not present in frame") from exc

    left_distance = index
    right_distance = len(dates) - 1 - index
    boundary = left_distance <= policy.edge_sessions or right_distance <= policy.edge_sessions
    return boundary, left_distance, right_distance


def to_candidate_with_boundary(
    frame: pd.DataFrame,
    landmark: Landmark,
    *,
    policy: BoundaryPolicy | None = None,
    amplitude_pct: float | None = None,
    prominence_pct: float | None = None,
    separation_sessions: int | None = None,
) -> LandmarkCandidate:
    boundary, left_distance, right_distance = classify_boundary(frame, landmark, policy)
    return LandmarkCandidate.from_landmark(
        landmark,
        amplitude_pct=amplitude_pct,
        prominence_pct=prominence_pct,
        separation_sessions=separation_sessions,
        boundary=boundary,
        extra_evidence={
            "boundary_left_distance": left_distance,
            "boundary_right_distance": right_distance,
            "boundary_policy_edge_sessions": (policy or BoundaryPolicy()).edge_sessions,
        },
    )
