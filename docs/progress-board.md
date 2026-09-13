# #33 Progress Board

Last updated: 2026-09-13

## Source-of-truth boundary

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33, including P8 morphology validation.

`azharmz/ussy-canslim-research` is the parent/HQ repository. It owns the frozen #32 upstream contract, the CAN SLIM roadmap, and later #34 consumption of frozen #33 output. It must not continue a parallel #33 detector/evaluator implementation.

Cross-repo reconciliation decision: `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

## Recovery / continuation

For continuation after lost chat context, read this board first, then the latest commits and newest `docs/decisions/2026-09-13-p8-*` records. NFLX VALIDATION remains locked until DEVELOPMENT semantics freeze.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline |
| Parent #32 contract confirmation | COMPLETE | parent specification frozen and #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema, raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| P1 Structural Landmark Engine | COMPLETE | frozen first-pass as `p1-landmark-v1`; unchanged by current P8 revision |
| P2 Base Segmentation | **FIRST-PASS COMPLETE / P8 RIGHT-EDGE DEBT** | confirmed-landmark segmentation cannot by itself represent all bases still forming at the as-of right edge |
| P3 Flat Base | **P8 v2 DEVELOPMENT REVISION IN TEST** | duration/depth hard gates unchanged; research-only `WIDE_LOOSE` no longer hard-rejects when hard gates pass |
| P4 Double Bottom | FIRST-PASS COMPLETE | source-aligned SEI case exists; duration/undercut semantics still unresolved |
| P5 Cup family | **FIRST-PASS COMPLETE / P8 REVISION REQUIRED** | CTSH/FOUR/AMZN expose start, pivot-role, and candidate-span disagreements |
| P6 Advanced patterns | COMPLETE | frozen first-pass as `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | frozen first-pass as `fault-ambiguity-v1` |
| P8 Labelled morphology validation | **DEVELOPMENT_REVISION_IN_PROGRESS** | 6 DEVELOPMENT labels across 4 core families; right-edge Flat revision and Flat v2 state mapping under live rerun |
| P9 Productionization | COMPLETE | frozen first-pass as `production-v1`; still carries P8 validation debt |

## Current contracts / revisions

- P1 `p1-landmark-v1` — `docs/p1-landmark-contract-v1.md`
- P2 `p2-segmentation-v1` — confirmed-structure first pass; right-edge/open-base semantics not yet production-frozen
- P3 first pass `flat-base-v1` — historical first-pass contract
- P3 DEVELOPMENT revision `flat-base-v2` — `docs/p3-flat-base-contract-v2.md`
- P4 `double-bottom-v1`
- P5 `cup-family-v1` — first-pass contract carrying P8 revision debt
- P6 `advanced-patterns-v1`
- P7 `fault-ambiguity-v1`
- P9 `production-v1`

`FROZEN FIRST-PASS` never means immune from a versioned P8 revision. P8 exists to test these contracts against independent real-world morphology evidence.

## P8 infrastructure complete

- authoritative label/evidence/provenance schema;
- DEVELOPMENT / VALIDATION leakage contract;
- source precision semantics (`DAY`, `MONTH`);
- optional source dimensions rather than invented boundaries;
- explicit source pivot + corporate-action comparison factor;
- strict OHLCV priority `R2 -> Yahoo/yfinance -> Tiingo`;
- provider absence -> `SourceUnavailable`; supplied auth/API/schema/QC failure remains terminal;
- canonical source-dimension evaluator `p8-source-dimension-eval-v0.2`;
- canonical pivot adapter `p8-pivot-adapter-v0.2`;
- canonical live DEVELOPMENT runner + GitHub Actions artifact;
- cup-body diagnostic ledger;
- P1/P2 structural diagnostic ledger;
- explicit prediction `candidate_semantics` separating confirmed structures from experimental right-edge observations.

## Authoritative corpus

Canonical file: `data/p8/labels_v0.csv`.

### DEVELOPMENT

1. SNPS — `FLAT_BASE`
2. CTSH — `CUP_WITH_HANDLE`
3. FOUR — `CUP_WITH_HANDLE`
4. SEI — `DOUBLE_BOTTOM`
5. AMZN — `CUP_WITHOUT_HANDLE`
6. TW — `FLAT_BASE`

### VALIDATION

- NFLX — `CUP_WITH_HANDLE` — **LOCKED / UNTOUCHED**

The six DEVELOPMENT labels give initial coverage across all four implemented core pattern families. This is coverage, not a final validation verdict.

## Data-source state

R2 and Tiingo Actions secrets are configured in this repository.

- SNPS resolves from R2.
- CTSH, FOUR, SEI, AMZN and TW currently fall through to Yahoo because those tickers are absent from the current frozen R2 membership snapshot.
- this fallback is explicit source unavailability, not morphology-driven provider selection.

## Canonical DEVELOPMENT result before Flat v2 rerun

With evaluator v0.2, multi-turn structural assembly, and the experimental open-right-edge Flat candidate class, the six-label batch reached:

```text
MATCH                  = 3
BOUNDARY_DISAGREEMENT  = 2
LANDMARK_DISAGREEMENT  = 1
MISS_PATTERN           = 0
```

| Example | Source-dimension result | Matched detector state | Interpretation |
|---|---|---|---|
| SNPS / Flat | **MATCH** | `FLAT_BASE_REJECTED` on confirmed candidate; source-aligned OPEN_RIGHT_EDGE candidate also present | source start/pivot exact; right-edge observation removes `TOO_SHORT`, leaving only research-only `WIDE_LOOSE` |
| TW / Flat | **MATCH** | `FLAT_BASE_REJECTED` | new OPEN_RIGHT_EDGE candidate starts exactly 2024-10-15 and pivots ~136.135 vs source 136.13; only `WIDE_LOOSE` remains |
| CTSH / CWH | **BOUNDARY_DISAGREEMENT** | `CUP_WITH_HANDLE_RECOGNIZED` | split-normalized pivot ~6.66 is good vs 6.685 source basis, but left-rim/start is materially earlier than January-2004 source anchor |
| FOUR / CWH | **LANDMARK_DISAGREEMENT** | `CUP_WITH_HANDLE_RECOGNIZED` | February start represented, but handle/pivot landmark ~75.28 differs from source 84.26 |
| SEI / Double Bottom | **MATCH** | `DOUBLE_BOTTOM_REJECTED` | late-July start + 12.74 pivot match; source-aligned W fails current `TOO_SHORT` duration gate |
| AMZN / Cup-no-Handle | **BOUNDARY_DISAGREEMENT** | `CUP_WITHOUT_HANDLE_RECOGNIZED` | cup family recognized; source 145.86 landmark exists, but emitted candidate scale starts too early |

## Structural diagnosis

P1/P2 diagnostic run established:

- **TW:** P1 contains the source start high 2024-10-15 @ ~136.135, but no confirmed post-start SWING_LOW exists by 2024-11-19. Confirmed P2 therefore cannot emit the forming base.
- **SNPS:** P1 contains 2023-04-04 high and 2023-04-25 low, but the low is only confirmed on 2023-05-18; confirmed P2 exposes a 15-session decline-stage span rather than the full source-described base.
- **AMZN:** P1 contains 2023-09-14 high @ 145.86 and later turns, but confirmed assembly fragments the September-November source-described base into smaller structural spans.

Conclusion: current debt is not merely a P2 bug. There is a representation gap between confirmed-turn structures and bases that are still open at the as-of right edge.

Decision: `docs/decisions/2026-09-13-p8-open-right-edge-flat-preregistration.md`.

## Flat Base v2 DEVELOPMENT revision

Two independent authoritative Flat examples, SNPS and TW, become source-aligned when an explicitly marked, label-agnostic OPEN_RIGHT_EDGE observation is emitted from a confirmed P1 start-high through the as-of horizon.

Both then pass the theory duration/depth gates and trip only `WIDE_LOOSE`.

Because the wide/loose numerical band was explicitly research-only, not an official O'Neil hard rule, P8 now tests this versioned state revision:

- duration/depth failure => `REJECTED`;
- hard gates pass + `WIDE_LOOSE` => `AMBIGUOUS`, with fault retained;
- hard gates pass + boundary context => `AMBIGUOUS`;
- hard gates pass + tight band => `RECOGNIZED`;
- intermediate => `AMBIGUOUS`.

Numeric thresholds are unchanged.

Decision: `docs/decisions/2026-09-13-p8-flat-wide-loose-semantics-v0.2.md`.

Contract: `docs/p3-flat-base-contract-v2.md`.

The live DEVELOPMENT rerun for this revision is now the active slice.

## Current morphology verdicts

| Area | Verdict |
|---|---|
| Missing-provider routing semantics | `KEEP` after revision |
| Source-window end vs structural-end evaluator semantics | `KEEP` evaluator v0.2 behavior |
| Need explicit right-edge/open-base representation | **`REVISE` — Flat DEVELOPMENT experiment implemented** |
| Flat `WIDE_LOOSE` hard-reject mapping | **`REVISE` — v2 maps research-only fault to AMBIGUOUS** |
| Flat numeric tightness bands | `UNRESOLVED` — unchanged pending broader corpus |
| CWH start / left-rim semantics | `UNRESOLVED` |
| CWH handle-high / pivot role | `UNRESOLVED` |
| Double Bottom duration gate | `UNRESOLVED` |
| Double Bottom strict second-trough undercut | `UNRESOLVED` |
| Cup-no-Handle candidate-span semantics | `UNRESOLVED` |
| BaseIdentity / Lineage freeze | `NOT READY` |

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no fabricated authoritative labels;
- no source boundary/precision reverse-engineered from detector output;
- OPEN_RIGHT_EDGE end is an observation horizon, never a fabricated P1 turn;
- multiple plausible structural scales remain explicit rather than forcing one winner;
- research-only thresholds must remain labelled as such;
- NFLX VALIDATION remains untouched until DEVELOPMENT semantics freeze;
- #34 must not start until P8/#33 has a defensible final verdict.

## Next work

1. complete the live Flat v2 DEVELOPMENT rerun and verify SNPS/TW state change without harming other families;
2. test OPEN_RIGHT_EDGE prefix/candidate-count behavior before any production promotion;
3. expand targeted authoritative Flat evidence to determine whether the numeric tightness bands themselves need revision;
4. continue CTSH/FOUR CWH landmark/start audit;
5. add targeted Double Bottom evidence for duration + second-trough-undercut semantics;
6. continue AMZN/CNH structural-scale diagnosis;
7. audit BaseIdentity/Lineage churn after candidate semantics settle;
8. freeze DEVELOPMENT detector/assembly semantics;
9. open NFLX VALIDATION exactly once after freeze;
10. freeze P8/#33, update the parent #33 pointer, then allow #34 to begin.
