from __future__ import annotations

from datetime import date

import pandas as pd

from oneil_patterns.validation.canonical_predictions import extract_core_morphology_predictions

from .output import ProductionAssessmentRecord


def analyze_security(
    security_id: str,
    ticker: str,
    frame: pd.DataFrame,
    asof_date: date,
) -> list[ProductionAssessmentRecord]:
    """Run the frozen core #33/P8 morphology stack on one PIT-safe security slice.

    Production must not maintain a second detector implementation. The exact
    canonical prediction adapter frozen by P8 is the sole source of core pattern
    assessments; this wrapper only attaches production identities and schema.
    """
    if frame.empty:
        return []

    ordered = frame.sort_values("date").reset_index(drop=True).copy()
    dates = pd.to_datetime(ordered["date"], errors="raise").dt.date
    if (dates > asof_date).any():
        raise ValueError("analyze_security received future bars")

    predictions = extract_core_morphology_predictions(ordered, asof_date=asof_date)
    records = [
        ProductionAssessmentRecord.from_prediction(
            security_id=security_id,
            ticker=ticker,
            asof_date=asof_date,
            prediction=prediction,
        )
        for prediction in predictions
    ]

    by_id = {record.assessment_id: record for record in records}
    return [by_id[key] for key in sorted(by_id)]
