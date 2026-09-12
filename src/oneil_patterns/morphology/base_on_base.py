from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum

import pandas as pd


@dataclass(frozen=True, slots=True)
class BaseRegionSummary:
    pattern: str
    start_date: date
    end_date: date
    confirmed_date: date
    high_price: float
    low_price: float

    def __post_init__(self) -> None:
        if self.start_date > self.end_date:
            raise ValueError("base start_date cannot be after end_date")
        if self.confirmed_date < self.end_date:
            raise ValueError("base confirmed_date cannot precede end_date")
        if self.low_price <= 0 or self.high_price <= 0 or self.low_price > self.high_price:
            raise ValueError("invalid base price range")


@dataclass(frozen=True, slots=True)
class BaseOnBaseGeometry:
    base_1: BaseRegionSummary
    base_2: BaseRegionSummary
    confirmed_date: date
    relation_sessions: int
    combined_duration_sessions: int
    second_low_to_first_high_ratio: float
    second_close_fraction_above_first_high: float


class BaseOnBaseState(str, Enum):
    RECOGNIZED = "BASE_ON_BASE_RECOGNIZED"
    REJECTED = "BASE_ON_BASE_REJECTED"
    AMBIGUOUS = "BASE_ON_BASE_AMBIGUOUS"


class BaseOnBaseFault(str, Enum):
    INVALID_ORDER = "INVALID_ORDER"
    SECOND_BASE_NOT_ABOVE_FIRST = "SECOND_BASE_NOT_ABOVE_FIRST"
    SECOND_BASE_ONLY_MARGINAL_ABOVE = "SECOND_BASE_ONLY_MARGINAL_ABOVE"


@dataclass(frozen=True, slots=True)
class BaseOnBaseAssessment:
    state: BaseOnBaseState
    faults: tuple[BaseOnBaseFault, ...]
    geometry: BaseOnBaseGeometry


# Research-only translation of IBD's qualitative "entirely or mostly above".
RECOGNIZED_ABOVE_FRACTION = 0.75
REJECTED_ABOVE_FRACTION = 0.50


def build_base_on_base_geometry(
    frame: pd.DataFrame,
    base_1: BaseRegionSummary,
    base_2: BaseRegionSummary,
) -> BaseOnBaseGeometry:
    if not (base_1.start_date < base_2.start_date and base_1.end_date < base_2.end_date):
        raise ValueError("base_2 must be later than base_1")

    if "date" not in frame.columns or "close" not in frame.columns:
        raise ValueError("frame requires date and close columns")

    dates = pd.to_datetime(frame["date"], errors="raise").dt.date
    date_to_index = {d: i for i, d in enumerate(dates)}
    for d in (base_1.start_date, base_1.end_date, base_2.start_date, base_2.end_date):
        if d not in date_to_index:
            raise ValueError(f"base boundary date missing from frame: {d}")

    b2_mask = (dates >= base_2.start_date) & (dates <= base_2.end_date)
    b2_closes = pd.to_numeric(frame.loc[b2_mask, "close"], errors="raise").astype(float)
    if b2_closes.empty:
        raise ValueError("second base region is empty")

    relation_sessions = date_to_index[base_2.start_date] - date_to_index[base_1.end_date] - 1
    combined_duration = date_to_index[base_2.end_date] - date_to_index[base_1.start_date] + 1

    return BaseOnBaseGeometry(
        base_1=base_1,
        base_2=base_2,
        confirmed_date=max(base_1.confirmed_date, base_2.confirmed_date),
        relation_sessions=relation_sessions,
        combined_duration_sessions=combined_duration,
        second_low_to_first_high_ratio=base_2.low_price / base_1.high_price,
        second_close_fraction_above_first_high=float((b2_closes >= base_1.high_price).mean()),
    )


def assess_base_on_base(geometry: BaseOnBaseGeometry) -> BaseOnBaseAssessment:
    fraction = geometry.second_close_fraction_above_first_high
    faults: list[BaseOnBaseFault] = []

    if fraction < REJECTED_ABOVE_FRACTION:
        faults.append(BaseOnBaseFault.SECOND_BASE_NOT_ABOVE_FIRST)
        return BaseOnBaseAssessment(BaseOnBaseState.REJECTED, tuple(faults), geometry)

    if fraction < RECOGNIZED_ABOVE_FRACTION:
        faults.append(BaseOnBaseFault.SECOND_BASE_ONLY_MARGINAL_ABOVE)
        return BaseOnBaseAssessment(BaseOnBaseState.AMBIGUOUS, tuple(faults), geometry)

    return BaseOnBaseAssessment(BaseOnBaseState.RECOGNIZED, tuple(faults), geometry)
