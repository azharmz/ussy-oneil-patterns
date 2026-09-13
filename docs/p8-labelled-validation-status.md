# P8 Labelled Morphology Validation — Status

Status: **CANONICAL DEVELOPMENT DISAGREEMENT ANALYSIS IN PROGRESS**

## Canonical boundary

`azharmz/ussy-oneil-patterns` is the source of truth for #33/P8 implementation and validation.

The former parallel P8 implementation in parent `azharmz/ussy-canslim-research` is retained only as migration evidence. It is not a second canonical detector stack.

Decision: `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

## What is complete

P8 now has:

- machine-readable authoritative labels and provenance;
- DEVELOPMENT / VALIDATION split with leakage guardrails;
- source precision semantics (`DAY`, `MONTH`);
- optional source dimensions rather than invented exact boundaries;
- explicit authoritative pivot price plus optional pivot date;
- explicit corporate-action comparison factor while preserving source price verbatim;
- strict OHLCV routing `R2 -> Yahoo/yfinance -> Tiingo`;
- canonical source-dimension evaluator `p8-source-dimension-eval-v0.2`;
- canonical pivot adapter `p8-pivot-adapter-v0.2`;
- canonical prediction adapter `p8-canonical-prediction-adapter-v0.2`;
- DEVELOPMENT live runner and GitHub Actions artifact;
- detector state/fault persistence;
- diagnostic Cup-body ledger for structural-span analysis.

## Corpus state

Canonical committed corpus: `data/p8/labels_v0.csv`.

Current authoritative examples:

- `p8-label-0001`: SNPS — `FLAT_BASE` — DEVELOPMENT;
- `p8-label-0003`: CTSH — `CUP_WITH_HANDLE` — DEVELOPMENT;
- `p8-label-0004`: FOUR — `CUP_WITH_HANDLE` — DEVELOPMENT;
- `p8-label-0005`: SEI — `DOUBLE_BOTTOM` — DEVELOPMENT;
- `p8-label-0006`: AMZN — `CUP_WITHOUT_HANDLE` — DEVELOPMENT;
- `p8-label-0002`: NFLX — `CUP_WITH_HANDLE` — VALIDATION, **LOCKED / UNTOUCHED**.

The five DEVELOPMENT rows give initial coverage across all four implemented core pattern families. This is coverage, not a validation verdict.

## Canonical DEVELOPMENT batch — current state

The current canonical v0.2 batch uses the strict source router. Repository Actions now has R2 and Tiingo secrets configured. SNPS is read from R2; CTSH, FOUR, SEI and AMZN fall through to Yahoo because those tickers are absent from the current frozen R2 membership snapshot. The fallback is therefore explicit source unavailability, not morphology-driven provider selection.

Current source-dimension result:

```text
MATCH                  = 2
BOUNDARY_DISAGREEMENT  = 2
LANDMARK_DISAGREEMENT  = 1
MISS_PATTERN           = 0
```

| Example | Source-dimension result | Detector status | Current diagnosis |
|---|---|---|---|
| SNPS / FLAT_BASE | **MATCH** | `FLAT_BASE_REJECTED` | source start and 392.79 pivot match exactly; P2 emits a shorter span that trips `TOO_SHORT` + research-only `WIDE_LOOSE` |
| CTSH / CUP_WITH_HANDLE | **BOUNDARY_DISAGREEMENT** | `CUP_WITH_HANDLE_RECOGNIZED` | split-normalized pivot is reproduced closely (~0.37% error), but canonical left-rim/start remains materially earlier than the source January-2004 anchor |
| FOUR / CUP_WITH_HANDLE | **LANDMARK_DISAGREEMENT** | `CUP_WITH_HANDLE_RECOGNIZED` | February-2024 start is represented, but the persisted handle/pivot landmark for that span is ~72–75 rather than source 84.26; other ~84.90 pivots belong to earlier/ambiguous spans |
| SEI / DOUBLE_BOTTOM | **MATCH** | `DOUBLE_BOTTOM_REJECTED` | late-July start and 12.74 pivot match; selected source-aligned W is rejected by the current duration gate (`TOO_SHORT`) |
| AMZN / CUP_WITHOUT_HANDLE | **BOUNDARY_DISAGREEMENT** | `CUP_WITHOUT_HANDLE_RECOGNIZED` | cup family is now emitted; source 145.86 landmark exists in diagnostics, but current candidate spans start in February/April rather than the source September base |

Detailed audit: `docs/decisions/2026-09-13-p8-development-morphology-audit-v0.md`.

## Morphology-only verdicts from current evidence

No current DEVELOPMENT example, by itself, justifies a threshold change.

| Area | Current verdict |
|---|---|
| source window-end vs detector structural-end semantics | `KEEP` evaluator v0.2 behavior: unspecified source-end role is preserved but not scored |
| Flat Base acceptance bands | `UNRESOLVED` — SNPS is source-aligned but the canonical structural span is truncated relative to the source-described base |
| CWH start / left-rim semantics | `UNRESOLVED` — CTSH pivot is good but structural start is earlier than source wording |
| CWH handle-high / pivot role | `UNRESOLVED` — FOUR has a source-aligned start but wrong canonical pivot landmark for that span |
| Double Bottom duration gate | `UNRESOLVED` — SEI source-aligned W is rejected as too short |
| Double Bottom second-trough undercut | `UNRESOLVED` — other SEI candidate scales repeatedly trip `NO_SECOND_TROUGH_UNDERCUT`; more authoritative DB examples are required |
| Cup-without-Handle candidate-span semantics | `UNRESOLVED` — AMZN broader cup morphology is recognized, but the September-November source base is not emitted as the source-aligned instance |
| BaseIdentity / Lineage freeze | `NOT READY` — candidate-span semantics remain unstable enough to affect identity grouping |

## Central interpretation

`source-dimension MATCH` and detector acceptance are intentionally different layers.

SNPS and SEI demonstrate that a detector-emitted candidate can agree with the authoritative source dimensions while still being `REJECTED` under current theory/research gates. Conversely, CTSH and FOUR show that a pattern family can be recognized while the structural instance or pivot landmark is not the source-described one.

The next work therefore remains morphology/structure driven, not performance driven:

1. expand targeted authoritative DEVELOPMENT evidence for the unresolved bands;
2. compare multiple plausible structural scales explicitly rather than forcing one winner;
3. determine whether disagreement is caused by P1/P2 span assembly, pattern landmark semantics, or actual morphology gates;
4. only make a versioned detector/assembly revision when supported by multiple source-grounded examples;
5. re-run all DEVELOPMENT labels after each justified revision;
6. freeze detector + BaseIdentity/Lineage only after structural churn is acceptable;
7. open NFLX VALIDATION exactly once after DEVELOPMENT freeze.

## Guardrails

- DEVELOPMENT only during tuning;
- NFLX VALIDATION remains locked and untouched;
- no return, CAGR, PF, win-rate, FWD1, breakout-performance, or entry-optimization input;
- no source precision may be invented from detector output;
- authoritative source prices remain immutable;
- corporate-action normalization must remain explicit and versioned;
- synthetic fixtures are regression-only and cannot substitute for authoritative P8 evidence;
- low-coverage or contradictory bands remain `UNRESOLVED`;
- #34 must not begin until P8/#33 has a defensible final verdict.

## Completion requirement

P8 may be frozen only after:

1. disagreement causes are classified explicitly across a broader DEVELOPMENT corpus;
2. any morphology-driven revisions are versioned and frozen;
3. targeted corpus expansion closes or explicitly documents unresolved bands;
4. BaseIdentity/Lineage churn is acceptable under the revised candidate semantics;
5. untouched NFLX VALIDATION is evaluated exactly once after DEVELOPMENT freeze;
6. final `KEEP` / `REVISE` / `UNRESOLVED` verdicts are recorded before #34 begins.
