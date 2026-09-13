# #33 Progress Board

Last updated: 2026-09-13

## Source-of-truth boundary

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33, including P8 morphology validation.

`azharmz/ussy-canslim-research` is the parent/HQ repository. It owns the frozen #32 upstream contract, the CAN SLIM roadmap, and later #34 consumption of frozen #33 output. It must not continue a parallel #33 detector/evaluator implementation.

Cross-repo reconciliation decision: `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

## Recovery / continuation

For continuation after lost chat context, read this board first, then the newest P8 decision records. NFLX VALIDATION remains locked until DEVELOPMENT semantics freeze.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline |
| Parent #32 contract confirmation | COMPLETE | parent specification frozen and #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | consumer pointer, schema and raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| P1 Structural Landmark Engine | COMPLETE | frozen first pass `p1-landmark-v1` |
| P2 Base Segmentation | FIRST-PASS COMPLETE / RIGHT-EDGE DEBT | confirmed-turn segmentation cannot represent every base still open at T |
| P3 Flat Base | P8 v2 DEVELOPMENT | hard duration/depth unchanged; research `WIDE_LOOSE` maps to ambiguity |
| P4 Double Bottom | P8 v2 DEVELOPMENT | no-undercut maps to ambiguity; duration debt remains |
| P5 Cup family | P8 v2 DEVELOPMENT | right-edge CWH/CNH observations active; roundedness proxies map to ambiguity |
| P6 Advanced patterns | COMPLETE | frozen first pass `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | frozen first pass `fault-ambiguity-v1` |
| P8 Labelled morphology validation | DEVELOPMENT_REVISION_IN_PROGRESS | 8 DEVELOPMENT labels; 7 source-dimension MATCH, 1 boundary disagreement |
| P9 Productionization | COMPLETE | first pass `production-v1`; still carries P8 validation debt |

## Current contracts / revisions

- P1 `p1-landmark-v1`
- P2 `p2-segmentation-v1` first pass; right-edge semantics not production-frozen
- P3 `flat-base-v2` DEVELOPMENT revision — `docs/p3-flat-base-contract-v2.md`
- P4 `double-bottom-v2` DEVELOPMENT revision — `docs/p4-double-bottom-contract-v2.md`
- P5 `cup-family-v2` DEVELOPMENT revision — `docs/p5-cup-family-contract-v2.md`
- P6 `advanced-patterns-v1`
- P7 `fault-ambiguity-v1`
- P9 `production-v1`

The normalized morphology adapters now report the v2 contract ids for Flat, Double Bottom and Cup-family assessments.

## P8 infrastructure

Implemented and active:

- authoritative label/evidence/provenance schema;
- DEVELOPMENT / VALIDATION leakage guardrails;
- optional source start/end/pivot dimensions rather than invented boundaries;
- `DAY` / `MONTH` source precision;
- explicit corporate-action comparison factor;
- optional source depth dimension with explicit tolerance;
- strict OHLCV routing `R2 -> Yahoo/yfinance -> Tiingo`;
- source-dimension evaluator `p8-source-dimension-eval-v0.4`;
- canonical prediction adapter with explicit `candidate_semantics`;
- OPEN_RIGHT_EDGE Flat, Handle and Cup-no-Handle observations;
- live DEVELOPMENT runner + Actions artifact;
- detector state/fault persistence and structural diagnostic ledgers.

## Authoritative corpus

Canonical file: `data/p8/labels_v0.csv`.

### DEVELOPMENT

1. SNPS — `FLAT_BASE`
2. CTSH — `CUP_WITH_HANDLE`
3. FOUR — `CUP_WITH_HANDLE`
4. SEI — `DOUBLE_BOTTOM`
5. AMZN — `CUP_WITHOUT_HANDLE`
6. TW — `FLAT_BASE`
7. NVDA — `DOUBLE_BOTTOM`
8. SPOT — `DOUBLE_BOTTOM`

### VALIDATION

- NFLX — `CUP_WITH_HANDLE` — LOCKED / UNTOUCHED

## Latest canonical DEVELOPMENT result

Latest eight-label live artifact:

```text
MATCH                  = 7
BOUNDARY_DISAGREEMENT  = 1
LANDMARK_DISAGREEMENT  = 0
MISS_PATTERN           = 0
```

| Example | Source agreement | Matched detector state | Current interpretation |
|---|---|---|---|
| SNPS / Flat | MATCH | `FLAT_BASE_REJECTED` selected by source rank; source-aligned right-edge candidate also exists | source dimensions are represented; Flat candidate identity/ranking still needs audit |
| TW / Flat | MATCH | `FLAT_BASE_AMBIGUOUS` | start/pivot source-aligned; `WIDE_LOOSE` retained as research ambiguity |
| CTSH / CWH | BOUNDARY_DISAGREEMENT | `CUP_WITH_HANDLE_RECOGNIZED` | split-normalized pivot is close; source January start is still not represented at the right structural scale |
| FOUR / CWH | MATCH | `CUP_WITH_HANDLE_AMBIGUOUS` | right-edge handle representation gives exact 84.26 pivot; `DEEP_HANDLE_EXCEPTIONAL` remains |
| SEI / Double Bottom | MATCH | `DOUBLE_BOTTOM_REJECTED` | source-aligned W fails only the unchanged `TOO_SHORT` duration gate |
| NVDA / Double Bottom | MATCH | `DOUBLE_BOTTOM_RECOGNIZED` | clean authoritative support for current recognized DB morphology |
| SPOT / Double Bottom | MATCH | `DOUBLE_BOTTOM_AMBIGUOUS` | exact 621.20 pivot; no-undercut now explicit ambiguity rather than rejection |
| AMZN / Cup-no-Handle | MATCH | `CUP_WITHOUT_HANDLE_AMBIGUOUS` | source depth about 19 percent selects Sep 14 -> Oct 26 instance; `SHARP_V` + `FRAGMENTED_BOTTOM` retained as ambiguity |

## Versioned P8 verdicts

| Area | Verdict |
|---|---|
| Missing-provider routing semantics | KEEP |
| Source-window end vs structural-end evaluator semantics | KEEP |
| Right-edge/open-base representation | REVISE — explicit observation semantics implemented |
| Flat `WIDE_LOOSE` severity | REVISE — ambiguity in v2 |
| Flat numeric tightness bands | UNRESOLVED |
| CWH open-right-edge handle representation | REVISE — FOUR source dimensions now match |
| CWH start / left-rim semantics | UNRESOLVED — CTSH remains sole boundary disagreement |
| Double Bottom absolute undercut requirement | REVISE — no-undercut is ambiguity in v2 |
| Double Bottom duration gate/boundary | UNRESOLVED — SEI |
| Cup roundedness proxy severity | REVISE — `SHARP_V` / `FRAGMENTED_BOTTOM` are ambiguity in v2 |
| Cup-no-Handle source-depth instance selection | KEEP — evaluator v0.4 selects the source-consistent scale |
| BaseIdentity / Lineage freeze | NOT READY |

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no fabricated authoritative labels;
- no source boundary/precision reverse-engineered from detector output;
- right-edge horizon is observation evidence, never a fabricated P1 turn;
- multiple plausible structural scales remain explicit;
- research-only thresholds stay labelled as research-only;
- NFLX VALIDATION remains untouched until DEVELOPMENT semantics freeze;
- #34 must not start until P8/#33 has a defensible final verdict.

## Next work

1. audit CTSH CWH source-start/left-rim semantics without changing thresholds;
2. adjudicate additional authoritative Double Bottom duration evidence before touching the 35-session gate;
3. audit BaseIdentity / Lineage churn and source-ranking stability under the new right-edge candidate classes;
4. expand Flat/Cup evidence only where a remaining numerical band is decision-relevant;
5. freeze DEVELOPMENT detector/assembly/evaluator semantics;
6. open NFLX VALIDATION exactly once after freeze;
7. freeze P8/#33, update the parent #33 pointer, then allow #34 to begin.
