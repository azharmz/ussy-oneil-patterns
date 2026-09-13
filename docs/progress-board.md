# #33 Progress Board

Last updated: 2026-09-13

## Source-of-truth boundary

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33, including P8 morphology validation.

`azharmz/ussy-canslim-research` is the parent/HQ repository. It owns the frozen #32 upstream contract, the CAN SLIM roadmap, and later #34 consumption of frozen #33 output. It must not continue a parallel #33 detector/evaluator implementation.

Cross-repo reconciliation decision: `docs/decisions/2026-09-13-p8-cross-repo-reconciliation.md`.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | repo/package/test/docs skeleton + green CI baseline established |
| Parent #32 contract confirmation | COMPLETE | parent specification frozen and #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | official consumer pointer, schema, raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | manifest/checksum/schema validation + explicit `asof_date` cutoff |
| P1 Structural Landmark Engine | COMPLETE | frozen first-pass as `p1-landmark-v1` |
| P2 Base Segmentation | **FIRST-PASS COMPLETE / P8 REVISION REQUIRED** | canonical batch shows named-base spans can be truncated or assembled at the wrong structural scale |
| P3 Flat Base | FIRST-PASS COMPLETE | `flat-base-v1`; threshold verdict deferred until source-aligned windows exist |
| P4 Double Bottom | FIRST-PASS COMPLETE | `double-bottom-v1`; strict undercut verdict remains unresolved |
| P5 Cup family | **FIRST-PASS COMPLETE / P8 REVISION REQUIRED** | canonical CWH/CNH examples expose structural-instance / hierarchy mismatch |
| P6 Advanced patterns | COMPLETE | frozen first-pass as `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | frozen first-pass as `fault-ambiguity-v1` |
| P8 Labelled morphology validation | **DEVELOPMENT_DISAGREEMENT_ANALYSIS_IN_PROGRESS** | first canonical 5-example batch executed; 1 MATCH, 3 boundary disagreements, 1 pattern miss; structural candidate assembly revision required before threshold adjudication |
| P9 Productionization | COMPLETE | frozen first-pass as `production-v1`; still carries P8 validation debt |

## Frozen / first-pass contracts

- P1 `p1-landmark-v1` — `docs/p1-landmark-contract-v1.md`
- P2 `p2-segmentation-v1` — `docs/p2-segmentation-contract-v1.md` — first-pass contract, now carrying P8 revision debt
- P3 `flat-base-v1` — `docs/p3-flat-base-contract-v1.md`
- P4 `double-bottom-v1` — `docs/p4-double-bottom-contract-v1.md`
- P5 `cup-family-v1` — `docs/p5-cup-family-contract-v1.md` — first-pass contract, now carrying P8 revision debt
- P6 `advanced-patterns-v1` — `docs/p6-advanced-patterns-contract-v1.md`
- P7 `fault-ambiguity-v1` — `docs/p7-fault-ambiguity-contract-v1.md`
- P9 `production-v1` — `docs/p9-production-contract-v1.md`

`FROZEN FIRST-PASS` never means immune from a versioned P8 revision. P8 exists specifically to test these contracts against independent real-world morphology evidence.

## P8 labelled validation status

Detailed status: `docs/p8-labelled-validation-status.md`.

Corpus acquisition plan: `docs/p8-corpus-acquisition-plan.md`.

OHLCV routing policy: `docs/p8-ohlcv-source-policy.md`.

Reference candidate registry: `data/p8/reference_candidates_v0.csv`.

Executable label corpus: `data/p8/labels_v0.csv`.

Canonical batch decision: `docs/decisions/2026-09-13-p8-canonical-development-batch-01.md`.

### Completed P8 infrastructure

- 8.1 label/evidence/provenance schema;
- 8.2 corpus split/leakage contract;
- 8.3 evaluation metrics + disagreement ids;
- repository audit for independent labels;
- acquisition protocol for 30–50 initial authoritative/human-labelled examples;
- 31 reference-first authoritative candidates across Flat Base, Double Bottom, Cup-with-Handle, Cup-without-Handle, Ascending Base and Base-on-Base;
- explicit R2-vs-external OHLCV routing policy;
- deterministic R2 -> Yahoo/yfinance -> Tiingo routing;
- runtime provider absence classified as `SourceUnavailable`, while supplied-but-invalid auth/API/schema/QC errors remain terminal;
- source-anchor adjudication rules;
- authoritative corpus with `DAY` / `MONTH` precision, optional dimensions, pivot fields and corporate-action comparison factor;
- canonical source-dimension evaluator `p8-source-dimension-eval-v0.2`;
- canonical pattern pivot adapter `p8-pivot-adapter-v0.2`;
- canonical prediction adapter `p8-canonical-prediction-adapter-v0.2`;
- DEVELOPMENT live runner + artifact output;
- diagnostic persistence of detector state/fault codes and all emitted predictions.

### Canonical authoritative corpus and first canonical execution

GitHub Actions run #175 (`34727720184`), head `551c2bc8a4b1a21bd83bf865a869a0b1a2fa194a`.

All five DEVELOPMENT examples used Yahoo because R2 is not configured in this repository's Actions runtime. This is an explicit source fallback, not a morphology-driven provider choice.

| Example | Split | Pattern | Canonical source agreement | Detector evidence | Current P8 interpretation |
|---|---|---|---|---|---|
| SNPS (`p8-label-0001`) | DEVELOPMENT | FLAT_BASE | **MATCH** | `FLAT_BASE_REJECTED`; `TOO_SHORT`, `WIDE_LOOSE` | start/pivot exact; structural window truncation makes threshold verdict unreliable |
| CTSH (`p8-label-0003`) | DEVELOPMENT | CUP_WITH_HANDLE | **BOUNDARY_DISAGREEMENT** | `CUP_WITH_HANDLE_AMBIGUOUS`; `DEEP_HANDLE_EXCEPTIONAL` | emitted CWH is wrong earlier instance; handle-depth band unresolved |
| FOUR (`p8-label-0004`) | DEVELOPMENT | CUP_WITH_HANDLE | **BOUNDARY_DISAGREEMENT** | `CUP_WITH_HANDLE_RECOGNIZED` | recognized CWH is wrong earlier instance; candidate assembly revision required |
| SEI (`p8-label-0005`) | DEVELOPMENT | DOUBLE_BOTTOM | **BOUNDARY_DISAGREEMENT** | selected W rejected; `NO_SECOND_TROUGH_UNDERCUT` | W instance not source-aligned; undercut rule remains unresolved |
| AMZN (`p8-label-0006`) | DEVELOPMENT | CUP_WITHOUT_HANDLE | **MISS_PATTERN** | no CNH; 145.86 preserved in other structural morphologies | cup-family assembly/hierarchy disagreement |
| NFLX (`p8-label-0002`) | VALIDATION | CUP_WITH_HANDLE | **LOCKED / UNTOUCHED** | not executed | remains untouched until DEVELOPMENT semantics freeze |

Batch summary:

```text
MATCH                  = 1
BOUNDARY_DISAGREEMENT  = 3
MISS_PATTERN           = 1
```

Initial corpus coverage spans all four implemented core pattern families. This remains coverage, not a P8 validation verdict.

### P8.5 morphology-only verdicts after canonical batch 01

| Area | Verdict |
|---|---|
| Missing-provider routing semantics | `REVISE` — completed |
| Source-window end vs structural-end evaluator semantics | `REVISE` — completed in evaluator v0.2 |
| Named-base structural candidate/window assembly | **`REVISE REQUIRED`** |
| Flat Base tightness bands | `UNRESOLVED` until source-aligned window exists |
| CWH handle-depth band | `UNRESOLVED` because CTSH CWH instance is misaligned |
| Double Bottom strict second-trough undercut | `UNRESOLVED` because SEI W instance is misaligned |
| Cup-no-Handle hierarchy | `UNRESOLVED / TARGETED DEVELOPMENT REQUIRED` |

The central finding is structural: the current consecutive/atomic landmark assembly can identify plausible morphology, but repeatedly at a different structural scale than the authoritative named base. Threshold tuning before fixing candidate assembly would confound geometry with window selection and is prohibited.

### Parent-branch migration evidence

The superseded parallel CAN SLIM implementation had reported `5 MATCH / 5 AMBIGUOUS`. That result remains historical migration evidence only. The canonical oneil result above supersedes it for #33 decisions.

### P8.4 / P8.5 / P8.6 status

- P8.4 DEVELOPMENT execution: **COMPLETE for canonical batch 01**;
- P8.5 morphology-only `KEEP` / `REVISE` / `UNRESOLVED`: **IN PROGRESS**; structural assembly is `REVISE REQUIRED`, threshold bands remain unresolved;
- P8.6 final labelled-validation freeze: pending;
- VALIDATION execution: **LOCKED** until revised DEVELOPMENT semantics are frozen.

Synthetic fixtures remain regression tests and are intentionally ineligible as authoritative P8 evidence.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`;
- external P8 routing priority remains R2 -> Yahoo/yfinance -> Tiingo -> other documented provider;
- fallback is allowed only on genuine source/provider unavailability, not to escape supplied auth/schema/QC failures or improve morphology agreement.

## P9 — Productionization freeze

Contract: `production-v1`

First-pass verdict:

`FIRST_PASS_ENGINE_COMPLETE_WITH_P8_VALIDATION_DEBT`

### P9 checklist

- 9.1 Versioned output record/schema — COMPLETE
- 9.2 Validation-status + contract manifest in every run — COMPLETE
- 9.3 Batch runner over PIT-safe R2 reader — COMPLETE
- 9.4 Deterministic serialization / stable ids — COMPLETE
- 9.5 End-to-end smoke tests + production orchestrator — COMPLETE
- 9.6 Productionization contract + #33 first-pass verdict — COMPLETE

Every production run/record must continue carrying the P8 validation-debt marker until P8 freezes.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no fabricated authoritative labels;
- no source boundary/precision may be reverse-engineered from detector output;
- no threshold revision while the compared structural instance is not source-aligned;
- multiple plausible structural scales must remain explicit rather than silently forcing a winner;
- no production output may imply research-only thresholds are P8-validated;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33;
- NFLX VALIDATION must remain untouched until DEVELOPMENT semantics freeze;
- #34 must not start until P8/#33 has a defensible final verdict.

## Next work

The active workstream is now **P8 structural candidate-assembly revision**:

1. preregister a versioned multi-turn / structural-scale candidate assembly design that can span intervening minor P1 landmarks without using labels at runtime;
2. preserve P1 initially and revise only the assembly of confirmed landmarks into named-base candidates;
3. allow multiple plausible scales/instances to coexist explicitly and deterministically;
4. implement the revision with PIT/prefix-stability tests and synthetic regression coverage;
5. re-run all five DEVELOPMENT examples and classify whether source-aligned structural instances now exist;
6. only then adjudicate Flat tightness, CWH handle-depth, DB undercut and Cup-family hierarchy bands;
7. expand targeted DEVELOPMENT evidence where those bands remain unresolved;
8. freeze DEVELOPMENT semantics only when disagreements are defensible;
9. open NFLX VALIDATION exactly once after freeze;
10. freeze P8/#33, update parent #33 pointer, then allow #34 to begin.
