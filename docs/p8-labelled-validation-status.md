# P8 Labelled Morphology Validation — Status

Status: **CANONICAL DEVELOPMENT REVISION IN PROGRESS**

## Canonical boundary

`azharmz/ussy-oneil-patterns` is the source of truth for #33/P8 implementation and validation.

The former parallel P8 implementation in parent `azharmz/ussy-canslim-research` is retained only as migration evidence. It is not a second canonical detector stack.

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
- canonical live DEVELOPMENT runner and Actions artifact;
- detector state/fault persistence;
- Cup-body and P1/P2 structural diagnostic ledgers;
- explicit `candidate_semantics` separating confirmed structures from right-edge observations;
- Flat Base v2 DEVELOPMENT revision;
- OPEN_RIGHT_EDGE Flat PIT/prefix regression coverage.

## Corpus state

Canonical committed corpus: `data/p8/labels_v0.csv`.

### DEVELOPMENT

1. SNPS — `FLAT_BASE`
2. CTSH — `CUP_WITH_HANDLE`
3. FOUR — `CUP_WITH_HANDLE`
4. SEI — `DOUBLE_BOTTOM`
5. AMZN — `CUP_WITHOUT_HANDLE`
6. TW — `FLAT_BASE`

### VALIDATION

- NFLX — `CUP_WITH_HANDLE` — **LOCKED / UNTOUCHED**

The six DEVELOPMENT examples span all four implemented core pattern families. This is coverage, not a final validation verdict.

## Data-source state

R2 and Tiingo Actions secrets are configured.

- SNPS resolves from R2.
- CTSH, FOUR, SEI, AMZN and TW currently fall through to Yahoo because those tickers are absent from the frozen R2 membership snapshot.
- fallback is therefore explicit source unavailability, never morphology-driven provider selection.

## Current canonical DEVELOPMENT result

After multi-turn assembly, evaluator v0.2, OPEN_RIGHT_EDGE Flat observations and Flat Base v2 state semantics:

```text
MATCH                  = 3
BOUNDARY_DISAGREEMENT  = 2
LANDMARK_DISAGREEMENT  = 1
MISS_PATTERN           = 0
```

| Example | Source-dimension result | Current detector evidence | Diagnosis |
|---|---|---|---|
| SNPS / FLAT_BASE | **MATCH** | source-aligned OPEN_RIGHT_EDGE candidate is `FLAT_BASE_AMBIGUOUS`; only `WIDE_LOOSE` remains | duration/depth pass; research-only tightness band remains evidence, not hard rejection |
| TW / FLAT_BASE | **MATCH** | source-aligned OPEN_RIGHT_EDGE candidate is `FLAT_BASE_AMBIGUOUS`; only `WIDE_LOOSE` remains | start 2024-10-15 and pivot ~136.135 match source 136.13 |
| CTSH / CUP_WITH_HANDLE | **BOUNDARY_DISAGREEMENT** | canonical CWH exists; split-normalized pivot is close to source basis | structural left-rim/start remains earlier than January-2004 source anchor |
| FOUR / CUP_WITH_HANDLE | **LANDMARK_DISAGREEMENT** | February-2024 start is represented | source 84.26 pivot is not the persisted handle-high/pivot for that source-aligned span |
| SEI / DOUBLE_BOTTOM | **MATCH** | source-aligned W remains `DOUBLE_BOTTOM_REJECTED` on duration | late-July start + 12.74 pivot agree; duration/undercut semantics unresolved |
| AMZN / CUP_WITHOUT_HANDLE | **BOUNDARY_DISAGREEMENT** | CNH family is emitted | source 145.86 landmark exists, but canonical candidate scale still starts too early |

## Flat Base v2 verdict

Two independent authoritative Flat examples, SNPS and TW, support a versioned semantics revision:

- duration/depth hard-gate failure => `REJECTED`;
- hard gates pass + research-only `WIDE_LOOSE` => `AMBIGUOUS`, fault retained;
- hard gates pass + boundary context => `AMBIGUOUS`;
- hard gates pass + tight research band => `RECOGNIZED`;
- intermediate => `AMBIGUOUS`.

Numeric thresholds are unchanged.

OPEN_RIGHT_EDGE candidates are observations from a confirmed P1 start-high through the explicit as-of horizon. The horizon is never represented as a fabricated P1 turn. PIT/prefix regression is green.

## Morphology-only verdicts

| Area | Current verdict |
|---|---|
| Missing-provider routing semantics | `KEEP` after revision |
| Source-window end vs structural-end evaluator semantics | `KEEP` evaluator v0.2 |
| Need explicit right-edge/open-base representation | `REVISE` — Flat DEVELOPMENT implementation active |
| Flat `WIDE_LOOSE` hard-reject mapping | `REVISE` — Flat v2 maps it to `AMBIGUOUS` |
| Flat numeric tightness bands | `UNRESOLVED` — unchanged pending broader corpus |
| CWH start / left-rim semantics | `UNRESOLVED` — CTSH |
| CWH handle-high / pivot role | `UNRESOLVED` — FOUR |
| Double Bottom duration gate | `UNRESOLVED` — SEI |
| Double Bottom strict second-trough undercut | `UNRESOLVED` — targeted DEVELOPMENT evidence required |
| Cup-without-Handle candidate-span semantics | `UNRESOLVED` — AMZN |
| BaseIdentity / Lineage freeze | `NOT READY` |

## Current work order

1. audit CTSH/FOUR CWH structural start and handle/pivot semantics;
2. audit SEI Double Bottom duration + undercut semantics and add targeted authoritative DB evidence;
3. audit AMZN Cup-no-Handle structural-scale/right-edge representation;
4. expand targeted Flat evidence before changing numeric tightness bands;
5. audit BaseIdentity/Lineage churn after candidate semantics settle;
6. freeze DEVELOPMENT detector/assembly semantics;
7. open NFLX VALIDATION exactly once after freeze;
8. record final P8 verdict and freeze #33 before #34 starts.

## Guardrails

- DEVELOPMENT only during tuning;
- NFLX VALIDATION remains locked and untouched;
- no return, CAGR, PF, win-rate, FWD1, breakout-performance, or entry optimization;
- no source precision or structural boundary may be invented from detector output;
- authoritative source prices remain immutable;
- corporate-action normalization remains explicit and versioned;
- multiple plausible structural scales remain explicit;
- synthetic fixtures are regression-only;
- low-coverage or contradictory bands remain `UNRESOLVED`;
- #34 must not begin until P8/#33 has a defensible final verdict.
