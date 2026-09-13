from __future__ import annotations

from datetime import date

import pandas as pd

from oneil_patterns.landmarks.confirmed_window import extract_confirmed_window_landmarks
from oneil_patterns.landmarks.excursion import extract_excursion_landmarks
from oneil_patterns.landmarks.fusion import fuse_landmark_sources
from oneil_patterns.segmentation.segmenter import segment_base_candidates

from .structural_assembly import STRUCTURAL_ASSEMBLY_VERSION, assemble_multiturn_segments

STRUCTURAL_DIAGNOSTIC_VERSION = "p8-structural-diagnostic-v0.1"


def _landmark_dict(item) -> dict:
    return {
        "type": item.type.value,
        "price_date": item.price_date.isoformat(),
        "confirmed_date": item.confirmed_date.isoformat(),
        "price": float(item.price),
        "boundary": bool(item.boundary),
    }


def _segment_dict(item, *, assembly_mode: str) -> dict:
    return {
        "assembly_mode": assembly_mode,
        "stage": item.stage.value,
        "start_date": item.start_date.isoformat(),
        "trough_date": item.trough.price_date.isoformat(),
        "end_date": item.end_date.isoformat(),
        "confirmed_date": item.confirmed_date.isoformat(),
        "duration_sessions": int(item.duration_sessions),
        "depth_pct": float(item.depth_pct),
        "start_price": float(item.start.price),
        "trough_price": float(item.trough.price),
        "recovery_price": float(item.recovery.price) if item.recovery is not None else None,
    }


def extract_structural_diagnostics(frame: pd.DataFrame, *, asof_date: date) -> dict:
    """Expose P1/P2 structure for P8 diagnosis without changing detector output.

    This ledger is intentionally diagnostic-only. It uses exactly the canonical
    frozen landmark extractors and existing atomic/multi-turn segment assembly.
    No source label enters landmark discovery or segment construction.
    """
    if frame.empty:
        return {
            "diagnostic_version": STRUCTURAL_DIAGNOSTIC_VERSION,
            "structural_assembly_version": STRUCTURAL_ASSEMBLY_VERSION,
            "landmarks": [],
            "atomic_segments": [],
            "multiturn_segments": [],
        }

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("structural diagnostic received future bars")
    if asof_date not in set(dates):
        eligible = dates[dates <= asof_date]
        if eligible.empty:
            raise ValueError("no eligible bars on or before asof_date")
        asof_date = eligible.iloc[-1]

    primary = extract_excursion_landmarks(ordered)
    auxiliary = extract_confirmed_window_landmarks(ordered)
    landmarks = fuse_landmark_sources(ordered, primary, auxiliary)
    landmarks = [item for item in landmarks if item.confirmed_date <= asof_date]
    landmarks.sort(key=lambda item: (item.price_date, item.confirmed_date, item.type.value, item.price))

    atomic = segment_base_candidates(ordered, landmarks, asof_date=asof_date)
    multiturn = assemble_multiturn_segments(ordered, landmarks, asof_date=asof_date)

    return {
        "diagnostic_version": STRUCTURAL_DIAGNOSTIC_VERSION,
        "structural_assembly_version": STRUCTURAL_ASSEMBLY_VERSION,
        "landmarks": [_landmark_dict(item) for item in landmarks],
        "atomic_segments": [_segment_dict(item, assembly_mode="ATOMIC_P2") for item in atomic],
        "multiturn_segments": [
            _segment_dict(item, assembly_mode="MULTITURN_HIGH_DEEPEST_LOW_HIGH") for item in multiturn
        ],
    }
