#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from datetime import timedelta
import json
from pathlib import Path

from oneil_patterns.validation.advanced_predictions import (
    ADVANCED_PREDICTION_ADAPTER_VERSION,
    extract_advanced_morphology_predictions,
)
from oneil_patterns.validation.candidate_identity import (
    CANDIDATE_IDENTITY_AUDIT_VERSION,
    audit_candidate_identities,
)
from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.development_sources import route_development_ohlcv
from oneil_patterns.validation.labels import CorpusSplit
from oneil_patterns.validation.source_dimension_eval import (
    EVALUATOR_VERSION,
    evaluate_positive_development_label,
)

ROOT = Path(__file__).resolve().parents[1]
CONTEXT_CALENDAR_DAYS = 320
BOUNDARY_TOLERANCE_DAYS = 10
PIVOT_DATE_TOLERANCE_DAYS = 3
PIVOT_PRICE_TOLERANCE_PCT = 0.01


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run P6 authoritative DEVELOPMENT morphology validation")
    parser.add_argument("--labels", default="data/p6/labels_v0.csv")
    parser.add_argument("--example-id")
    parser.add_argument("--output", default="results/p6-authoritative-development.json")
    return parser.parse_args()


def _run_one(label) -> dict:
    anchor = label.window_start or label.asof_date
    context_start = anchor - timedelta(days=CONTEXT_CALENDAR_DAYS)
    routed = route_development_ohlcv(label.symbol, context_start, label.asof_date)
    predictions = extract_advanced_morphology_predictions(routed.frame, asof_date=label.asof_date)
    agreement = evaluate_positive_development_label(
        label,
        predictions,
        boundary_tolerance_days=BOUNDARY_TOLERANCE_DAYS,
        pivot_date_tolerance_days=PIVOT_DATE_TOLERANCE_DAYS,
        pivot_price_tolerance_pct=PIVOT_PRICE_TOLERANCE_PCT,
    )
    same_pattern = [item for item in predictions if item.pattern == label.pattern]
    identity_audit = audit_candidate_identities(same_pattern)
    return {
        "example_id": label.example_id,
        "symbol": label.symbol,
        "pattern": label.pattern,
        "split": label.split.value,
        "context_start": context_start.isoformat(),
        "asof_date": label.asof_date.isoformat(),
        "selected_source": routed.source.value,
        "fallback_reason": routed.fallback_reason,
        "input_row_count": len(routed.frame),
        "prediction_count": len(predictions),
        "prediction_pattern_counts": dict(sorted(Counter(item.pattern for item in predictions).items())),
        "same_pattern_prediction_count": len(same_pattern),
        "agreement": agreement.to_dict(),
        "same_pattern_predictions": [asdict(item) for item in same_pattern],
        "candidate_identity_state_counts": dict(
            sorted(Counter(item.identity_state for item in identity_audit).items())
        ),
        "candidate_identities": [item.to_dict() for item in identity_audit],
    }


def main() -> int:
    args = parse_args()
    all_labels = load_label_corpus_csv(ROOT / args.labels)
    validation_ids = tuple(
        sorted(item.example_id for item in all_labels if item.split == CorpusSplit.VALIDATION)
    )
    labels = [item for item in all_labels if item.split == CorpusSplit.DEVELOPMENT]
    if args.example_id:
        labels = [item for item in labels if item.example_id == args.example_id]
    if not labels:
        raise ValueError("no P6 DEVELOPMENT labels selected")
    if any(item.pattern not in {"ASCENDING_BASE", "BASE_ON_BASE"} for item in labels):
        raise ValueError("P6 corpus contains a non-advanced DEVELOPMENT pattern")

    results = [_run_one(label) for label in labels]
    report = {
        "stage": "P6",
        "scope": "AUTHORITATIVE_DEVELOPMENT",
        "prediction_adapter_version": ADVANCED_PREDICTION_ADAPTER_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "candidate_identity_audit_version": CANDIDATE_IDENTITY_AUDIT_VERSION,
        "context_calendar_days": CONTEXT_CALENDAR_DAYS,
        "boundary_tolerance_days": BOUNDARY_TOLERANCE_DAYS,
        "pivot_date_tolerance_days": PIVOT_DATE_TOLERANCE_DAYS,
        "pivot_price_tolerance_pct": PIVOT_PRICE_TOLERANCE_PCT,
        "locked_validation_example_ids": validation_ids,
        "result_count": len(results),
        "agreement_counts": dict(
            sorted(Counter(item["agreement"]["agreement_state"] for item in results).items())
        ),
        "candidate_resolution_counts": dict(
            sorted(Counter(item["agreement"]["candidate_resolution_state"] for item in results).items())
        ),
        "matched_detector_status_counts": dict(
            sorted(
                Counter(
                    item["agreement"].get("matched_detector_status") or "NO_MATCH"
                    for item in results
                ).items()
            )
        ),
        "results": results,
        "guardrails": [
            "Only DEVELOPMENT rows are scored; VALIDATION identities are listed but their source dimensions are never opened by this runner.",
            "P6 advanced predictions consume frozen P1 and frozen core predictions without changing P3/P4/P5/P8 semantics.",
            "Source dimensions are scored only where the authoritative source publishes a comparable dimension.",
            "R2 -> Yahoo -> Tiingo source routing is inherited unchanged from P8.",
            "All inputs are truncated at each authoritative as-of date.",
            "No return, CAGR, PF, FWD1, breakout outcome, or entry optimization is used.",
            "Any DEVELOPMENT disagreement may change only the separately versioned P6 validation adapter/assembly, never frozen core detectors.",
        ],
    }

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
