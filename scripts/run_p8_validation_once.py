#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from dataclasses import asdict, replace
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
FREEZE_EVIDENCE_COMMIT = "2ed3dadcc354f56f4cb27401248daef60b1627fa"
FREEZE_WORKFLOW_RUN = 34740880269
FREEZE_ARTIFACT_ID = 10312239372
FREEZE_ARTIFACT_DIGEST = "sha256:d62a0c0cf8e582c25fc67b9bd2c64855554886f0779f433f69a3304d4c9673a3"
EXPECTED_VERSIONS = {
    "prediction_adapter": "p8-canonical-prediction-adapter-v1.1",
    "pivot_adapter": "p8-pivot-adapter-v0.2",
    "evaluator": "p8-source-dimension-eval-v0.5",
    "candidate_identity_audit": "p8-candidate-identity-audit-v0.4",
}
CONTEXT_CALENDAR_DAYS = 240
BOUNDARY_TOLERANCE_DAYS = 10
PIVOT_DATE_TOLERANCE_DAYS = 3
PIVOT_PRICE_TOLERANCE_PCT = 0.01


def _assert_frozen_versions() -> None:
    actual = {
        "prediction_adapter": PREDICTION_ADAPTER_VERSION,
        "pivot_adapter": PIVOT_ADAPTER_VERSION,
        "evaluator": EVALUATOR_VERSION,
        "candidate_identity_audit": CANDIDATE_IDENTITY_AUDIT_VERSION,
    }
    if actual != EXPECTED_VERSIONS:
        raise RuntimeError(f"frozen P8 versions changed before VALIDATION: {actual!r}")


def main() -> int:
    _assert_frozen_versions()
    labels = load_label_corpus_csv(ROOT / "data/p8/labels_v0.csv")
    validation = [item for item in labels if item.split == CorpusSplit.VALIDATION]
    if len(validation) != 1:
        raise RuntimeError(f"expected exactly one frozen VALIDATION label, got {len(validation)}")
    label = validation[0]
    if label.example_id != "p8-label-0002" or label.symbol != "NFLX" or label.pattern != "CUP_WITH_HANDLE":
        raise RuntimeError("frozen VALIDATION identity changed")

    anchor = label.window_start or label.asof_date
    context_start = anchor - timedelta(days=CONTEXT_CALENDAR_DAYS)
    routed = route_development_ohlcv(label.symbol, context_start, label.asof_date)
    predictions = extract_core_morphology_predictions(routed.frame, asof_date=label.asof_date)

    # The frozen evaluator intentionally refuses VALIDATION labels during tuning.
    # After freeze we score an immutable copy with only the split field changed;
    # all authoritative source dimensions remain identical.
    scoring_label = replace(label, split=CorpusSplit.DEVELOPMENT)
    agreement = evaluate_positive_development_label(
        scoring_label,
        predictions,
        boundary_tolerance_days=BOUNDARY_TOLERANCE_DAYS,
        pivot_date_tolerance_days=PIVOT_DATE_TOLERANCE_DAYS,
        pivot_price_tolerance_pct=PIVOT_PRICE_TOLERANCE_PCT,
    )

    same_pattern = [item for item in predictions if item.pattern == label.pattern]
    identity_audit = audit_candidate_identities(same_pattern)
    cup_body_diagnostics = extract_cup_body_diagnostics(routed.frame, asof_date=label.asof_date)
    structural_diagnostics = extract_structural_diagnostics(routed.frame, asof_date=label.asof_date)

    report = {
        "stage": "P8",
        "scope": "ONE_SHOT_FROZEN_VALIDATION",
        "freeze_evidence_commit": FREEZE_EVIDENCE_COMMIT,
        "freeze_workflow_run": FREEZE_WORKFLOW_RUN,
        "freeze_artifact_id": FREEZE_ARTIFACT_ID,
        "freeze_artifact_digest": FREEZE_ARTIFACT_DIGEST,
        "prediction_adapter_version": PREDICTION_ADAPTER_VERSION,
        "pivot_adapter_version": PIVOT_ADAPTER_VERSION,
        "evaluator_version": EVALUATOR_VERSION,
        "candidate_identity_audit_version": CANDIDATE_IDENTITY_AUDIT_VERSION,
        "cup_body_diagnostic_version": CUP_BODY_DIAGNOSTIC_VERSION,
        "structural_diagnostic_version": STRUCTURAL_DIAGNOSTIC_VERSION,
        "context_calendar_days": CONTEXT_CALENDAR_DAYS,
        "boundary_tolerance_days": BOUNDARY_TOLERANCE_DAYS,
        "pivot_date_tolerance_days": PIVOT_DATE_TOLERANCE_DAYS,
        "pivot_price_tolerance_pct": PIVOT_PRICE_TOLERANCE_PCT,
        "example_id": label.example_id,
        "symbol": label.symbol,
        "pattern": label.pattern,
        "original_split": label.split.value,
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
        "cup_body_diagnostics": cup_body_diagnostics,
        "structural_diagnostics": structural_diagnostics,
        "guardrails": [
            "This is the single frozen VALIDATION execution authorized after DEVELOPMENT freeze.",
            "No frozen detector/evaluator/source-routing semantics may be changed in response to this result.",
            "Only the split field is changed on an in-memory scoring copy so the frozen DEVELOPMENT evaluator can score identical authoritative dimensions.",
            "No return, CAGR, PF, FWD1, breakout-performance, or entry-optimization information is used.",
        ],
    }

    output = ROOT / "results/p8-frozen-validation-nflx.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
