# P8 cross-repo reconciliation — CAN SLIM parent vs #33 implementation repo

Date: 2026-09-13
Status: ACTIVE MIGRATION DECISION

## Decision

`azharmz/ussy-oneil-patterns` is the canonical implementation repository and source of truth for CAN SLIM workstream **#33 — O'Neil Pattern Recognition Engine**, including P8 morphology validation.

`azharmz/ussy-canslim-research` remains the parent/HQ repository. It owns the upstream #32 contract, overall CAN SLIM roadmap, and later consumption of frozen #33 output. It must not continue a parallel #33 detector/evaluator implementation.

## Why reconciliation is required

A substantial P8 development slice was implemented on parent branch `feat/p8-labelled-development-v0`. That branch reached useful morphology-validation evidence, but continuing both implementations would create two competing detector semantics and two sources of truth.

This migration therefore preserves evidence and validation semantics without copying the parent detector stack wholesale into the canonical #33 architecture.

## Classification of parent-branch P8 work

### ALREADY_CANONICAL_IN_ONEIL

The following capabilities already exist natively in this repository and are not reimplemented from the parent branch:

- PIT-safe landmark extraction and base segmentation;
- Flat Base, Double Bottom, Cup family morphology implementation;
- explicit fault/ambiguity normalization;
- deterministic production assessment IDs;
- DEVELOPMENT / VALIDATION split contract;
- authoritative label schema and corpus validation;
- external OHLCV adapters and strict source routing;
- source-anchor adjudication rules;
- morphology-only validation guardrails;
- no return/CAGR/PF tuning.

### PORT_TO_ONEIL

The following evidence-model improvements are useful and are being ported into the canonical P8 contract:

- source precision for authoritative start anchors (`DAY`, `MONTH`);
- optional source dimensions: missing exact end or pivot date is not fabricated and is not scored;
- explicit authoritative pivot fields;
- explicit corporate-action comparison factor while preserving the source price verbatim;
- expanded authoritative corpus:
  - SNPS — `FLAT_BASE` — DEVELOPMENT;
  - CTSH — `CUP_WITH_HANDLE` — DEVELOPMENT;
  - FOUR — `CUP_WITH_HANDLE` — DEVELOPMENT;
  - SEI — `DOUBLE_BOTTOM` — DEVELOPMENT;
  - AMZN — `CUP_WITHOUT_HANDLE` — DEVELOPMENT;
  - NFLX — `CUP_WITH_HANDLE` — VALIDATION, still locked.

### SUPERSEDED / DO NOT PORT AS A PARALLEL ENGINE

The following parent-branch implementation files are not copied as canonical engine code:

- `pattern_engine_v02.py` and the parent raw-window detector stack;
- parent `base_id` / structural-lineage implementation;
- parent cross-pattern conflict implementation where it duplicates P7 canonical ambiguity/fault semantics;
- parent-specific P8 runner/diagnostic scripts and workflow wiring;
- parent-specific OHLCV provider code where canonical oneil adapters/router already exist.

Their historical results remain useful evidence for reconciliation, but the canonical detector must be evaluated through the oneil landmark-first architecture.

### PARENT-ONLY INTEGRATION

The CAN SLIM parent should retain only:

- #33 roadmap/status pointers;
- frozen upstream #32 contract;
- later #34 consumption contract after #33/P8 freezes;
- links/references to the canonical #33 repository/version.

## Migrated authoritative corpus state

The canonical corpus now carries five DEVELOPMENT examples spanning all four core pattern families plus one untouched VALIDATION example.

The parent implementation previously reported:

```text
source-dimension agreement:
  MATCH = 5
matched detector evidence state:
  AMBIGUOUS = 5
```

This result is **migration evidence, not yet the canonical oneil verdict**. It must be reproduced or contradicted by the canonical oneil detector before P8 can use it for KEEP / REVISE / UNRESOLVED decisions.

## Important unresolved bands carried forward

- Double Bottom second-trough undercut semantics: SEI was source-labelled Double Bottom although the parent-selected second low was slightly higher than the first.
- CWH handle-fault semantics: FOUR matched source pattern/pivot but parent detector flagged early handle low.
- Cup-family hierarchy: AMZN source-labelled Cup Without Handle while parent detector also emitted CWH ambiguity.
- General ambiguity: the parent batch had 5/5 source matches but 5/5 ambiguous detector states.
- Structural identity/lineage: the parent implementation showed material churn after pivot correction; its base_id/lineage semantics are not imported as a canonical contract.

## Validation lock

NFLX remains `VALIDATION` and must not be opened during DEVELOPMENT migration or tuning.

## Next canonical sequence

1. make the migrated corpus/schema green in canonical oneil CI;
2. add a canonical source-dimension evaluator/adapter against oneil detector outputs;
3. execute only the five DEVELOPMENT labels through the oneil stack;
4. classify disagreements by source precision, corporate action, morphology, and ambiguity semantics;
5. issue `KEEP` / `REVISE` / `UNRESOLVED` decisions from canonical results;
6. freeze detector semantics only when DEVELOPMENT evidence is defensible;
7. open NFLX exactly once after freeze;
8. freeze P8/#33 before #34 starts.

## Guardrails

No migration decision may be justified by future returns, CAGR, PF, win rate, FWD1, breakout performance, or entry optimization. Source boundaries and precision remain source-grounded; missing dimensions are not reverse-engineered from detector output.
