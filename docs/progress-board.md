# #33 Progress Board

Last updated: 2026-09-12

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
| P8 Labelled morphology validation | LABELLED_CORPUS_IN_PROGRESS | 31 authoritative candidates; first 2 executable authoritative LabelEvidence records committed and schema-valid |
| P9 Productionization | COMPLETE | frozen as `production-v1`; deterministic PIT-safe production engine/orchestrator green |

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

Complete:

- 8.1 label/evidence/provenance schema;
- 8.2 corpus split/leakage contract;
- 8.3 evaluation metrics + disagreement ids;
- repository audit for existing independent labels;
- acquisition protocol for 30–50 initial authoritative/human-labelled examples;
- 31 reference-first authoritative candidates collected across Flat Base, Double Bottom, Cup-with-Handle, Cup-without-Handle, Ascending Base and Base-on-Base;
- explicit R2-vs-external OHLCV routing policy, including delisted/non-universe securities;
- first authoritative adjudication batch completed;
- 2 executable authoritative labels committed and validated against frozen `LabelEvidence` schema: SNPS Flat Base (DEVELOPMENT) and NFLX Cup With Handle (VALIDATION).

Current acquisition/adjudication work:

- continue exact-window adjudication for the remaining high-priority candidates;
- resolve each example to canonical R2 or a documented external OHLCV source;
- expand DEVELOPMENT coverage before interpreting detector disagreement;
- keep the committed VALIDATION example untouched until any revised detector version is frozen;
- promote only source-grounded cases; ambiguous/coarse-window candidates remain held back.

P8.4 status:

- DEVELOPMENT-side detector execution is now eligible as soon as OHLCV is resolved for committed development labels;
- final validation execution remains pending broader coverage and a frozen post-development detector version;
- 8.5 morphology-only threshold verdicts (`KEEP` / `REVISE` / `UNRESOLVED`) remain pending;
- 8.6 final labelled-validation freeze remains pending.

Synthetic fixtures remain regression tests and are intentionally ineligible as P8 evidence.

## Frozen data-consumption decisions

- upstream source of truth: `azharmz/ussy-data`;
- consume `production/ready/current.json`, never hardcode run parquet UUID;
- required fields: `date, security_id, ticker, open, high, low, close, adj_close, volume`;
- upstream Yahoo ingestion uses `auto_adjust=False`;
- raw OHLC and `adj_close` remain distinct;
- structural morphology/pivots use raw OHLC under current spec;
- historical evaluation receives only rows where `date <= asof_date`.

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
- every run/record currently preserves the frozen first-pass validation-debt marker until P8 is resolved;
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
- no production output may imply research-only thresholds are P8-validated;
- no CAN SLIM eligibility, entry optimization, portfolio, or sell logic in #33.

## Next work

P9 is closed. The active workstream is P8 labelled-corpus build and development-side validation:

1. adjudicate more P0/P1 candidates into exact source-grounded windows;
2. resolve OHLCV per promoted example: R2 when available, external historical data otherwise;
3. expand DEVELOPMENT labels toward enough coverage per pattern;
4. run frozen detectors on DEVELOPMENT labels only;
5. issue morphology-only `KEEP` / `REVISE` / `UNRESOLVED` verdicts and version any revisions;
6. evaluate untouched VALIDATION labels once against the revised frozen version;
7. freeze P8 only after coverage gaps and disagreement cases are documented.
