# #33 Progress Board

Last updated: 2026-09-21

`azharmz/ussy-oneil-patterns` is the canonical implementation repository for #33 O'Neil Pattern Recognition. `azharmz/ussy-canslim-research` is the parent/HQ consumer and must not host a parallel pattern engine.

## Project state

| Phase | Status | Notes |
|---|---|---|
| P0 Bootstrap | COMPLETE | baseline complete |
| Parent #32 contract confirmation | COMPLETE | #33 authorized |
| R2 OHLCV contract inspection | COMPLETE | raw-vs-adjusted semantics documented |
| PIT-safe data reader | COMPLETE | explicit as-of cutoff |
| P1 Structural Landmark Engine | COMPLETE | `p1-landmark-v1` |
| P2 Base Segmentation | COMPLETE FOR FROZEN CORE P8 | confirmed structure plus explicit right-edge observation semantics |
| P3 Flat Base | FROZEN CORE | `flat-base-v2` |
| P4 Double Bottom | FROZEN CORE | `double-bottom-v3`; 35-session gate retained |
| P5 Cup family | FROZEN CORE | `cup-family-v2`; explicit right-edge CWH/CNH |
| P6 Advanced patterns | **TERMINALLY DEFERRED / NOT PRODUCTION-VALIDATED** | Cycle 1 validation failed; Cycle 2 stopped at authoritative morphology-evidence boundary before VALIDATION |
| P7 Fault/ambiguity layer | COMPLETE | ambiguity/fault states persisted |
| P8 Labelled morphology validation | COMPLETE — CONDITIONAL PASS | 20 DEVELOPMENT examples + one frozen NFLX VALIDATION execution |
| P9 Productionization | COMPLETE / FROZEN v2 | production consumes frozen P8 core predictions only |

## Frozen production core

Production schema `oneil-pattern-output-v2` remains limited to:

- `FLAT_BASE` — `flat-base-v2`
- `DOUBLE_BOTTOM` — `double-bottom-v3`
- `CUP_WITHOUT_HANDLE` — `cup-family-v3-cwoh-fragmentation`
- `CUP_WITH_HANDLE` — `cup-family-v3-cwoh-fragmentation`

Canonical adapter: `p8-canonical-prediction-adapter-v1.2-cwh-measurement`.
Production engine: `33-core-p8-frozen-v2`.
Base identity: `core-base-id-v1`.
Lineage: `core-lineage-v1`.

P8 frozen DEVELOPMENT: 20/20 source-dimension `MATCH`, zero boundary/landmark/pattern miss, zero true identity `STATUS_CONFLICT`. NFLX untouched VALIDATION was opened once after freeze and structurally matched uniquely at start `2023-02-03`, while retaining frozen `CUP_WITH_HANDLE_AMBIGUOUS / BELOW_CUP_MIDPOINT` debt. No post-validation tuning is allowed.

## P6 Cycle 1 — historical failed validation

Cycle 1 used 5 authoritative `ASCENDING_BASE` and 5 authoritative `BASE_ON_BASE` DEVELOPMENT positives, then opened locked STT and C once after freeze.

DEVELOPMENT: 10/10 source-dimension `MATCH`, identity `STATUS_CONFLICT=0`, but morphology presentation was weak: Ascending Base 1 recognized / 1 ambiguous / 3 rejected; Base-on-Base 1 recognized / 4 ambiguous.

Untouched VALIDATION:

- STT `ASCENDING_BASE`: source dimensions MATCH, detector `ASCENDING_BASE_REJECTED`;
- C `BASE_ON_BASE`: source dimensions MATCH, detector `BASE_ON_BASE_AMBIGUOUS`.

Cycle 1 verdict: `VALIDATION FAIL / NOT PRODUCTION-VALIDATED`. STT/C are consumed evidence and cannot be reused as untouched validation.

## P6 Cycle 2 — terminal evidence-boundary stop

Fresh locked corpus: `data/p6/labels_cycle2_v0.csv`.

DEVELOPMENT:

- `ASCENDING_BASE`: AVGO, TME, CCJ, SNOW, NAVN;
- `BASE_ON_BASE`: META, TRV, SE, JLL, SEI.

Untouched VALIDATION reserved before DEVELOPMENT scoring:

- MRX — `ASCENDING_BASE`;
- CAT — `BASE_ON_BASE`.

Final Cycle 2 DEVELOPMENT evidence:

```text
all DEVELOPMENT                     9 MATCH / 1 MISS_PATTERN
candidate identity STATUS_CONFLICT  0

ASCENDING_BASE                      5/5 MATCH
candidate resolution                5/5 SOURCE_EQUIVALENT_MULTIPLE
presentation detector state         4 RECOGNIZED / 1 REJECTED

BASE_ON_BASE                        4/5 MATCH / 1 MISS_PATTERN
candidate resolution                4 SOURCE_EQUIVALENT_MULTIPLE / 1 NONE
presentation detector state         4 AMBIGUOUS / 1 NO_MATCH
```

Execution commit: `9cab74ace28a55f7715b7bf1bdecddf2cee758e4`.
Workflow run: `34753213531`.
Artifact id: `10316012884`.
Artifact digest: `sha256:303276ed83abae1f74b83f690d102fdf4c5a6a9c7e2bb1aada8e31d50a93db26`.

### Terminal blockers

**Ascending Base candidate identity:** authoritative sources generally provide pattern name/pivot and sometimes approximate start, but not exact pullback #1/#2/#3 landmarks or detector-comparable boundaries. All five Cycle 2 examples therefore have multiple source-equivalent candidates. Selecting the candidate with the most convenient detector state would be circular.

**Base-on-Base `mostly above`:** authoritative guidance permits the second base to be `entirely or mostly above` the first but does not provide a universal quantitative overlap/support threshold. Inventing 50%, 60%, 70%, 75%, etc. would create unsupported precision.

**Core composition boundary:** META is a genuine `MISS_PATTERN`. Repairing it by loosening frozen P3/P4/P5/P8 constituent morphology would reopen frozen core through P6 and is prohibited.

### Why Cycle 2 VALIDATION was not opened

Cycle 2 DEVELOPMENT did not reach a defensible specification/candidate-identity freeze gate. Opening MRX/CAT would consume untouched evidence without resolving the specification problem. Therefore MRX and CAT remain untouched; they are neither DEVELOPMENT nor validation results.

## Terminal P6 verdict

**DEFERRED / NOT PRODUCTION-VALIDATED / FROZEN UNTIL NEW AUTHORITATIVE MORPHOLOGY EVIDENCE EXISTS**.

Do not open Cycle 3 merely because more articles provide another ticker, pattern name, pivot, or approximate start. Reopening requires a genuinely new evidence type that resolves at least one missing operational dimension, for example:

1. exact authoritative Ascending Base pullback landmarks or unambiguous detector-comparable boundaries;
2. authoritative quantitative Base-on-Base `mostly above` / prior-base-top support semantics; or
3. an authoritative labelled MarketSurge/O'Neil dataset that independently resolves candidate identity.

Canonical P6 records:

- `data/p6/labels_cycle2_v0.csv`
- `docs/p6-cycle2-source-audit.md`
- `docs/decisions/p6-cycle2-terminal-verdict.md`
- `docs/decisions/p6-final-verdict.md`

Cycle 1 records/artifacts remain historical evidence and must not be removed.

Final P6 documentation commit: `a4e38503913731c50589b51097cd8e3b580082f2`.
Final CI run: `34753292331` — pytest SUCCESS; P6 DEVELOPMENT skipped; P8 DEVELOPMENT skipped.

## Production consequence

No production promotion occurred for P6:

- `ASCENDING_BASE` remains outside `oneil-pattern-output-v2`;
- `BASE_ON_BASE` remains outside `oneil-pattern-output-v2`;
- frozen P3/P4/P5/P8 core remains unchanged.

Downstream consumers must preserve explicit `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` state, candidate/base/lineage identity, semantics, faults, and provenance. P6 must not be described as P8-equivalent or production-validated.

## #33 stop boundary

For the evidence currently available, #33 governance is complete:

- four core families are frozen and production-emitted under v2;
- P6 advanced families are terminally deferred under explicit reopening conditions;
- no further #33 detector work is authorized absent new authoritative morphology evidence satisfying the P6 reopening gate.

The next CAN SLIM workstream is #34 in the parent repository. This O'Neil Pattern repo/chat must not implement #34.


## CWOH vNext closure — 2026-09-21

CUP_WITHOUT_HANDLE residual `FRAGMENTED_BOTTOM` semantics completed independent DEVELOPMENT and locked VALIDATION, then promoted to production. The narrow production change keeps `FRAGMENTED_BOTTOM` as evidence but makes it non-state-bearing when it is the sole research-band fault. SHARP_V, WEAK_RIGHT_RIM_RECOVERY, duration/depth gates, pivots, candidate construction, source matching, base identity and lineage semantics remain unchanged. Validation: INTC/ARW/AMD/SE 4/4 source-dimension MATCH. Production promotion SHA before contract-version closure: `130cfce5d71c85b9832dd50a3a44f7c193a0c1d7`.
