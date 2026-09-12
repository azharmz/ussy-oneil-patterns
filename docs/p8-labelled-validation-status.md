# P8 Labelled Morphology Validation — Status

Status: **DEVELOPMENT RECONCILIATION IN PROGRESS**

## Canonical boundary

`azharmz/ussy-oneil-patterns` is the source of truth for #33/P8 implementation and validation.

A useful but parallel P8 slice existed in parent `azharmz/ussy-canslim-research`. Its evidence-model improvements and source-grounded labels are being migrated here; its detector stack is not being adopted as a second canonical engine.

Decision: `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

## What is complete

P8 has a machine-readable validation contract with:

- labels: `POSITIVE`, `NEGATIVE`, `AMBIGUOUS`;
- provenance: `AUTHORITATIVE_SOURCE`, `HUMAN_ANNOTATION`, `ADJUDICATED`;
- corpus split: `DEVELOPMENT`, `VALIDATION`;
- explicit source name/reference and `asof_date`;
- source start precision (`DAY`, `MONTH`);
- optional source dimensions: exact end and pivot date are not required when the source does not provide them;
- explicit authoritative pivot price and optional pivot date;
- explicit corporate-action comparison factor while preserving source price verbatim;
- annotator required for human labels;
- duplicate-id and development/validation leakage checks;
- ambiguity preserved as a first-class validation outcome.

Implementation:

- `src/oneil_patterns/validation/labels.py`
- `src/oneil_patterns/validation/evaluate.py`
- `src/oneil_patterns/validation/corpus.py`
- `tests/validation/test_labelled_validation_contract.py`
- `tests/validation/test_p8_committed_corpus.py`

## Corpus state

Canonical committed corpus: `data/p8/labels_v0.csv`.

Current authoritative examples:

- `p8-label-0001`: SNPS — `FLAT_BASE` — DEVELOPMENT;
- `p8-label-0003`: CTSH — `CUP_WITH_HANDLE` — DEVELOPMENT;
- `p8-label-0004`: FOUR — `CUP_WITH_HANDLE` — DEVELOPMENT;
- `p8-label-0005`: SEI — `DOUBLE_BOTTOM` — DEVELOPMENT;
- `p8-label-0006`: AMZN — `CUP_WITHOUT_HANDLE` — DEVELOPMENT;
- `p8-label-0002`: NFLX — `CUP_WITH_HANDLE` — VALIDATION, **LOCKED / UNTOUCHED**.

The five DEVELOPMENT rows provide initial coverage across all four implemented core pattern families. That is a coverage milestone, not a validation verdict.

Reference-first acquisition remains active:

- `data/p8/reference_candidates_v0.csv` contains 31 authoritative candidates;
- `data/p8/adjudication_queue_v0.csv` prioritizes source-grounded resolution;
- `docs/p8-adjudication-batch-01.md` records the first promotions and held-back cases;
- `docs/p8-ohlcv-source-policy.md` defines R2 vs external historical data routing.

Synthetic fixtures remain explicitly **ineligible** as authoritative P8 evidence.

## Migrated parent-side evidence

The former parallel parent implementation reported all five DEVELOPMENT examples as agreeing with source-provided dimensions, while all five selected detector candidates remained ambiguous:

```text
MATCH = 5
AMBIGUOUS = 5
```

This result is retained only as migration evidence. It must be reproduced or contradicted by the canonical oneil landmark-first stack before it can support P8 decisions.

Known unresolved bands carried forward for targeted canonical testing:

- Flat Base tightness / wide-loose;
- Double Bottom second-trough undercut semantics, highlighted by SEI;
- Cup-with-Handle handle-fault semantics, highlighted by FOUR;
- Cup-family hierarchy / Cup-without-Handle vs CWH ambiguity, highlighted by AMZN;
- general cross-pattern ambiguity;
- canonical structural identity stability after any justified morphology revision.

## Current verdict

P8.4 is **READY FOR CANONICAL DEVELOPMENT-SIDE RE-EXECUTION** after the migrated schema/corpus passes CI.

Rules:

- DEVELOPMENT labels may be used for disagreement analysis and morphology-only revision;
- VALIDATION labels remain untouched until a revised detector version is frozen;
- absent source dimensions remain unscored rather than inferred;
- source prices remain immutable; explicit factors only normalize the comparison basis;
- no threshold may be tuned against post-pattern returns, CAGR, PF, win rate, FWD1, or entry performance;
- no synthetic fixture may substitute for independent evidence;
- low-coverage or contradictory morphology bands remain `UNRESOLVED`.

## Completion requirement

P8 may be frozen only after:

1. the migrated canonical corpus/schema is CI-green;
2. the five DEVELOPMENT examples are evaluated through the canonical oneil stack;
3. disagreement causes are classified explicitly;
4. any morphology-driven revisions are versioned and frozen;
5. targeted corpus expansion closes or documents unresolved bands;
6. untouched NFLX VALIDATION is evaluated exactly once after DEVELOPMENT freeze;
7. coverage gaps and remaining ambiguity are reported explicitly;
8. the final `KEEP` / `REVISE` / `UNRESOLVED` verdict is recorded before #34 begins.
