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
| P1 Structural Landmark Engine | COMPLETE | frozen as `p1-landmark-v1` |
| P2 Base Segmentation | COMPLETE | frozen as `p2-segmentation-v1` |
| P3 Flat Base | COMPLETE | frozen first-pass as `flat-base-v1`; research tightness bands remain subject to P8 labelled validation |
| P4 Double Bottom | COMPLETE | frozen first-pass as `double-bottom-v1` |
| P5 Cup family | COMPLETE | frozen first-pass as `cup-family-v1` |
| P6 Advanced patterns | COMPLETE | frozen first-pass as `advanced-patterns-v1` |
| P7 Fault/ambiguity layer | COMPLETE | frozen as `fault-ambiguity-v1` |
| P8 Labelled morphology validation | **DEVELOPMENT_RECONCILIATION_IN_PROGRESS** | 31 reference candidates; canonical corpus now 5 DEVELOPMENT + 1 locked VALIDATION; parent-side 5 MATCH / 5 AMBIGUOUS must be re-executed canonically before verdict |
| P9 Productionization | COMPLETE | frozen as `production-v1`; deterministic PIT-safe production engine/orchestrator green, still marked with P8 validation debt |

## Frozen contracts

- P1 `p1-landmark-v1` — `docs/p1-landmark-contract-v1.md`
- P2 `p2-segmentation-v1` — `docs/p2-segmentation-contract-v1.md`
- P3 `flat-base-v1` — `docs/p3-flat-base-contract-v1.md`
- P4 `double-bottom-v1` — `docs/p4-double-bottom-contract-v1.md`
- P5 `cup-family-v1` — `docs/p5-cup-family-contract-v1.md`
- P6 `advanced-patterns-v1` — `docs/p6-advanced-patterns-contract-v1.md`
- P7 `fault-ambiguity-v1` — `docs/p7-fault-ambiguity-contract-v1.md`
- P9 `production-v1` — `docs/p9-production-contract-v1.md`

## P8 labelled validation status

Detailed status: `docs/p8-labelled-validation-status.md`.

Corpus acquisition plan: `docs/p8-corpus-acquisition-plan.md`.

OHLCV routing policy: `docs/p8-ohlcv-source-policy.md`.

Reference candidate registry: `data/p8/reference_candidates_v0.csv`.

Executable label corpus: `data/p8/labels_v0.csv`.

### Completed P8 infrastructure

- 8.1 label/evidence/provenance schema;
- 8.2 corpus split/leakage contract;
- 8.3 evaluation metrics + disagreement ids;
- repository audit for independent labels;
- acquisition protocol for 30–50 initial authoritative/human-labelled examples;
- 31 reference-first authoritative candidates collected across Flat Base, Double Bottom, Cup-with-Handle, Cup-without-Handle, Ascending Base and Base-on-Base;
- explicit R2-vs-external OHLCV routing policy, including delisted/non-universe securities;
- strict source routing with fallback only on source unavailability;
- source-anchor adjudication rules;
- first authoritative adjudication batch;
- canonical label schema now supports source precision (`DAY` / `MONTH`), optional source dimensions, explicit authoritative pivot fields, and explicit split/corporate-action comparison factors without mutating source prices.

### Canonical authoritative corpus

| Example | Split | Pattern | Source precision / dimensions | Canonical execution status |
|---|---|---|---|---|
| SNPS (`p8-label-0001`) | DEVELOPMENT | FLAT_BASE | DAY start/end + pivot date/price | pending canonical re-execution in reconciliation branch |
| CTSH (`p8-label-0003`) | DEVELOPMENT | CUP_WITH_HANDLE | MONTH start + pivot price; explicit factor 4 comparison normalization | pending canonical re-execution |
| FOUR (`p8-label-0004`) | DEVELOPMENT | CUP_WITH_HANDLE | MONTH start + pivot price | pending canonical re-execution |
| SEI (`p8-label-0005`) | DEVELOPMENT | DOUBLE_BOTTOM | MONTH start + pivot price | pending canonical re-execution |
| AMZN (`p8-label-0006`) | DEVELOPMENT | CUP_WITHOUT_HANDLE | MONTH start + pivot price | pending canonical re-execution |
| NFLX (`p8-label-0002`) | VALIDATION | CUP_WITH_HANDLE | DAY start/end | **LOCKED / UNTOUCHED** |

Initial coverage now spans all four implemented core pattern families. This is **coverage**, not a P8 verdict.

### Parent-branch migration evidence

Before reconciliation, the parallel parent implementation reported:

```text
source-dimension agreement:
  MATCH = 5
matched detector evidence state:
  AMBIGUOUS = 5
joint state:
  MATCH:AMBIGUOUS = 5
```

Those results are preserved as migration evidence only. They are not adopted as canonical #33 findings until the same five DEVELOPMENT labels are run through the canonical oneil landmark-first stack.

Unresolved bands carried forward from that evidence:

- Double Bottom second-trough undercut semantics (SEI);
- CWH handle-fault semantics (FOUR);
- Cup-family hierarchy / CWH-vs-Cup-without-Handle ambiguity (AMZN);
- general ambiguity rate: 5/5 parent-side source matches were still ambiguous;
- parent `base_id` / lineage churn after pivot correction was material, so those parent-specific identity semantics are not imported as a frozen oneil contract.

### P8.4 / P8.5 / P8.6 status

- P8.4 DEVELOPMENT execution: **NEXT — canonical re-execution of the five migrated DEVELOPMENT labels**;
- P8.5 morphology-only `KEEP` / `REVISE` / `UNRESOLVED`: pending canonical disagreement evidence;
- P8.6 final labelled-validation freeze: pending;
- VALIDATION execution: locked until revised DEVELOPMENT semantics are frozen.

Synthetic fixtures remain regression tests and are intentionally ineligible as P8 evidence.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`;
- external P8 routing priority remains R2 -> Yahoo/yfinance -> Tiingo -> other documented provider;
- fallback is allowed only on genuine source unavailability, not to escape auth/schema/QC failures or improve morphology agreement.

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

### Frozen production semantics

- output schema: `oneil-pattern-output-v1`;
- engine version: `33-first-pass-v1`;
- production contract: `production-v1`;
- every run/record preserves the first-pass validation-debt marker until P8 is resolved;
- stable assessment IDs use semantic SHA-256 identity fields;
- canonical R2 ready reader enforces checksum/schema/PIT cutoff;
- orchestrator composes frozen P1–P7 semantics rather than inventing parallel detectors;
- inapplicable geometry may be skipped safely without aborting an otherwise valid security batch;
- absence of confirmed right-edge evidence never silently becomes Cup-without-Handle;
- research-only, theory-grounded, and contextual fault provenance remain distinguishable in production output.

## Hard constraints

- no future bars or backdated confirmation;
- no trading-return-based detector tuning;
- no fabricated authoritative labels;
- no source boundary/precision may be reverse-engineered from detector output;
- no production output may imply research-only thresholds are P8-validated;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33;
- NFLX VALIDATION must remain untouched until DEVELOPMENT semantics freeze;
- #34 must not start until P8/#33 has a defensible final verdict.

## Next work

The active workstream is **P8 canonical reconciliation and DEVELOPMENT morphology validation**:

1. make the migrated schema/corpus green in canonical oneil CI;
2. add a canonical source-dimension evaluator/adapter against oneil detector outputs without importing the parent detector stack;
3. execute the five DEVELOPMENT labels only;
4. classify every disagreement as source precision, corporate-action normalization, morphology, ambiguity/conflict, or evaluator semantics;
5. issue morphology-only `KEEP` / `REVISE` / `UNRESOLVED` decisions and version any justified revisions;
6. expand targeted DEVELOPMENT evidence where unresolved bands need more examples;
7. freeze detector semantics only after canonical DEVELOPMENT evidence is defensible;
8. open NFLX VALIDATION exactly once after freeze;
9. freeze P8/#33, update parent #33 pointer, then allow #34 to begin.
