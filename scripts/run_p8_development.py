#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from datetime import timedelta
import json
from pathlib import Path

from oneil_patterns.validation.candidate_identity import (
    CANDIDATE_IDENTITY_AUDIT_VERSION,
    audit_candidate_identities,
)
from oneil_patterns.validation.canonical_predictions import (
    PREDICTION_ADAPTER_VERSION,
    extract_core_morphology_predictions,
)
from oneil_patterns.validation.corpus import load_label_corpus_csv
from oneil_patterns.validation.cup_body_diagnostics import (
    CUP_BODY_DIAGNOSTIC_VERSION,
    extract_cup_body_diagnostics,
)
from oneil_patterns.validation.development_sources import route_development_ohlcv
from oneil_patterns.validation.labels import CorpusSplit
from oneil_patterns.validation.pivot_adapter import PIVOT_ADAPTER_VERSION
from oneil_patterns.validation.source_dimension_eval import (
    EVALUATOR_VERSION,
    evaluate_positive_development_label,
)
from oneil_patterns.validation.structural_diagnostics import (
    STRUCTURAL_DIAGNOSTIC_VERSION,
    extract_structural_diagnostics,
)

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run canonical #33/P8 DEVELOPMENT morphology validation")
    parser.add_argument("--labels", default="data/p8/labels_v0.csv")
    parser.add_argument("--example-id")
    parser.add_argument("--validation", action="store_true", help="Run locked VALIDATION labels after candidate semantics are frozen")
    parser.add_argument("--context-calendar-days", type=int, default=240)
    parser.add_argument("--boundary-tolerance-days", type=int, default=10)
    parser.add_argument("--pivot-date-tolerance-days", type=int, default=3)
    parser.add_argument("--pivot-price-tolerance-pct", type=float, default=0.01)
    parser.add_argument("--output", default="results/p8-canonical-development.json")
    return parser.parse_args()


def _run_one(label, args) -> dict:
    anchor = label.window_start or label.asof_date
    context_start = anchor - timedelta(days=args.context_calendar_days)
    routed = route_development_ohlcv(label.symbol, context_start, label.asof_date)
    predictions = extract_core_morphology_predictions(routed.frame, asof_date=label.asof_date)
    cup_body_diagnostics = extract_cup_body_diagnostics(routed.frame, asof_date=label.asof_date)
    structural_diagnostics = extract_structural_diagnostics(routed.frame, asof_date=label.asof_date)
    agreement = evaluate_positive_development_label(
        label,
        predictions,
        boundary_tolerance_days=args.boundary_tolerance_days,
        pivot_date_tolerance_days=args.pivot_date_tolerance_days,
        pivot_price_tolerance_pct=args.pivot_price_tolerance_pct,
    )
    same_pattern = [item for item in predictions if item.pattern == label.pattern]
    identity_audit = audit_candidate_identities(same_pattern)
    pattern_counts = dict(sorted(Counter(item.pattern for item in predictions).items()))
    cup_body_state_counts = dict(sorted(Counter(item["state"] for item in cup_body_diagnostics).items()))
    identity_state_counts = dict(sorted(Counter(item.identity_state for item in identity_audit).items()))
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
        "prediction_pattern_counts": pattern_counts,
        "same_pattern_prediction_count": len(same_pattern),
        "agreement": agreement.to_dict(),
        "same_pattern_predictions": [asdict(item) for item in same_pattern],
        "all_predictions": [asdict(item) for item in predictions],
        "candidate_identity_audit_version": CANDIDATE_IDENTITY_AUDIT_VERSION,
        "candidate_identity_count": len(identity_audit),
        "candidate_identity_state_counts": identity_state_counts,
        "candidate_identities": [item.to_dict() for item in identity_audit],
        "cup_body_diagnostic_version": CUP_BODY_DIAGNOSTIC_VERSION,
        "cup_body_diagnostic_count": len(cup_body_diagnostics),
        "cup_body_state_counts": cup_body_state_counts,
        "cup_body_diagnostics": cup_body_diagnostics,
        "structural_diagnostic_version": STRUCTURAL_DIAGNOSTIC_VERSION,
        "structural_diagnostics": structural_diagnostics,
    }


def main() -> int:
    args = parse_args()
    if args.context_calendar_days < 180:
        raise ValueError("context-calendar-days must be >=180")
    if min(args.boundary_tolerance_days, args.pivot_date_tolerance_days) < 0:
        raise ValueError("date tolerances must be non-negative")
    if args.pivot_price_tolerance_pct < 0:
        raise ValueError("pivot-price-tolerance-pct must be non-negative")

    all_labels = load_label_corpus_csv(ROOT / args.labels)
    selected_split = CorpusSplit.VALIDATION if args.validation else CorpusSplit.DEVELOPMENT
    labels = [item for item in all_labels if item.split == selected_split]
    if args.example_id:
        labels = [item for item in labels if item.example_id == args.example_id]
    if not labels:
        raise ValueError(f"no {selected_split.value} labels selected")

    results = [_run_one(label, args) for label in labels]
    agreement_counts = dict(sorted(Counter(item["agreement"]["agreement_state"] for item in results).items()))
    detector_status_counts = dict(
        sorted(Counter(item["agreement"].get("matched_detector_status") or "NO_MATCH" for item in results).items())
    )
    candidate_resolution_counts = dict(
        sorted(Counter(item["agreement"]["candidate_resolution_state"] for item in results).items())
    )
    identity_state_counts = dict(
        sorted(
            Counter(
                identity["identity_state"]
                for item in results
                for identity in item["candidate_identities"]
            ).items()
        )
    )
    joint_counts = dict(
        sorted(
            Counter(
                f'{item["agreement"]["agreement_state"]}:{item["agreement"].get("matched_detector_status") or "NO_MATCH"}'
                for item in results
            ).items()
        )
    )

    report = {
        "stage": "P8",
        "scope": "CANONICAL_AUTHORITATIVE_VALIDATION" if args.validation else "CANONICAL_AUTHORITATIVE_DEVELOPMENT",
        "prediction_adapter_version": PREDICTION_ADAPTER_VERSION,
        "pivot_adapter_version": PIVOT_ADAPTER_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "candidate_identity_audit_version": CANDIDATE_IDENTITY_AUDIT_VERSION,
        "cup_body_diagnostic_version": CUP_BODY_DIAGNOSTIC_VERSION,
        "structural_diagnostic_version": STRUCTURAL_DIAGNOSTIC_VERSION,
        "context_calendar_days": args.context_calendar_days,
        "boundary_tolerance_days": args.boundary_tolerance_days,
        "pivot_date_tolerance_days": args.pivot_date_tolerance_days,
        "pivot_price_tolerance_pct": args.pivot_price_tolerance_pct,
        "result_count": len(results),
        "agreement_counts": agreement_counts,
        "candidate_resolution_counts": candidate_resolution_counts,
        "candidate_identity_state_counts": identity_state_counts,
        "matched_detector_status_counts": detector_status_counts,
        "agreement_by_detector_status": joint_counts,
        "results": results,
        "guardrails": [
            "Split selection is explicit; VALIDATION requires --validation and is only run after candidate semantics are frozen.",
            "OHLCV routing is strict R2 -> Yahoo -> Tiingo; only SourceUnavailable permits fallback.",
            "All input bars are truncated at each label asof_date.",
            "Source dimensions are scored only at their published precision and comparable semantic role.",
            "When source start is absent, context lookback is fixed from asof_date and start is not scored.",
            "Corporate-action factors alter comparison basis only; source prices stay immutable.",
            "Detector status/faults and diagnostic ledgers are evidence separate from source-dimension agreement.",
            "Source-equivalent candidate multiplicity is explicit; detector status never ranks source agreement.",
            "Candidate identity audit excludes rolling/right-edge end horizon and candidate semantics from its coarse structural key.",
            "P1/P2 structural diagnostics use canonical label-agnostic landmark/segment construction only.",
            "No return, CAGR, PF, FWD1, breakout-performance, or entry-optimization input is used.",
        ],
    }

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
