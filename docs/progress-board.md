# #33 Progress Board

Last updated: 2026-09-13

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
| P6 Advanced patterns | COMPLETE — VALIDATION FAIL / FROZEN | authoritative 10-row DEVELOPMENT + untouched 2-row one-shot VALIDATION completed; not production-validated |
| P7 Fault/ambiguity layer | COMPLETE | ambiguity/fault states persisted |
| P8 Labelled morphology validation | COMPLETE — CONDITIONAL PASS | 20 DEVELOPMENT examples + one frozen NFLX VALIDATION execution |
| P9 Productionization | COMPLETE / FROZEN v2 | production directly consumes frozen P8 canonical predictions; no duplicate detector path |

## Frozen core stack

- Flat: `flat-base-v2`
- Double Bottom: `double-bottom-v3`
- Cup family: `cup-family-v2`
- canonical prediction adapter: `p8-canonical-prediction-adapter-v1.1`
- pivot adapter: `p8-pivot-adapter-v0.2`
- source evaluator: `p8-source-dimension-eval-v0.5`
- candidate identity audit: `p8-candidate-identity-audit-v0.4`
- production base identity: `core-base-id-v1`
- production lineage: `core-lineage-v1`
- production schema: `oneil-pattern-output-v2`
- production engine: `33-core-p8-frozen-v1`
- OHLCV priority: R2 -> Yahoo/yfinance -> Tiingo; fallback only on genuine unavailability

Freeze record: `docs/decisions/p8-development-freeze-v1.md`.
Final verdict: `docs/decisions/p8-final-verdict.md`.
Production contract: `docs/production-output-contract-v2.md`.

## P6 authoritative validation cycle

P6 advanced families:

- `ASCENDING_BASE`
- `BASE_ON_BASE`

The earlier source-grounded v2 conditional verdict was superseded by a full authoritative validation cycle. Frozen P3/P4/P5/P8 core was not reopened.

### DEVELOPMENT freeze

Corpus: `data/p6/labels_v0.csv` DEVELOPMENT split.

Coverage:

- ASCENDING_BASE: 5 authoritative positives
- BASE_ON_BASE: 5 authoritative positives

Frozen evidence:

```text
workflow run                   = 34748254127
artifact id                    = 10315076061
artifact digest                = sha256:332f7fc9aab753280b386491cb59d3a48ad4f258374c7e40b804309eb93425e8
repository tests               = 235 passed
source-dimension MATCH         = 10 / 10
candidate STATUS_CONFLICT      = 0
```

Detector-state evidence at DEVELOPMENT freeze:

```text
ASCENDING_BASE_RECOGNIZED      = 1
ASCENDING_BASE_AMBIGUOUS       = 1
ASCENDING_BASE_REJECTED        = 3
BASE_ON_BASE_RECOGNIZED        = 1
BASE_ON_BASE_AMBIGUOUS         = 4
```

Freeze record: `docs/decisions/p6-development-freeze-v1.md`.

### Untouched one-shot VALIDATION

Locked before freeze:

- `p6-label-0011` — STT `ASCENDING_BASE`
- `p6-label-0012` — C `BASE_ON_BASE`

One-shot execution:

```text
commit                         = 2c10165e67c1486459ddf191021243ad70e90f7b
workflow run                   = 34750413835
artifact id                    = 10315775412
artifact digest                = sha256:618c72a7accbb9b5434db9040e2bad645bf0435de21b32ffac019bfe4d83ca16
source-dimension MATCH         = 2 / 2
candidate STATUS_CONFLICT      = 0
STT detector state             = ASCENDING_BASE_REJECTED
C detector state               = BASE_ON_BASE_AMBIGUOUS
```

The one-shot workflow path was removed in commit `da251cee5f8ffbc3038a198950d3b824f4b4d458` immediately after execution.

### Final P6 verdict

**VALIDATION FAIL / FROZEN — NOT PRODUCTION-VALIDATED**.

The authoritative source dimensions matched, but neither untouched positive validation example was recognized by frozen morphology. Under the same validation discipline used for core patterns, sparse pivot/pattern agreement cannot override rejected/ambiguous detector state.

Consequences:

- P6 remains outside `oneil-pattern-output-v2`;
- STT/C cannot be reused as untouched validation in a future cycle;
- no post-validation threshold or severity tuning is allowed;
- Base-on-Base “mostly above” remains unresolved because authoritative guidance supplies no universal numeric overlap boundary;
- a new cycle requires new authoritative morphology-rich DEVELOPMENT evidence and a new untouched VALIDATION set;
- P3/P4/P5/P8 remain frozen.

Final verdict: `docs/decisions/p6-final-verdict.md`.

## P8 DEVELOPMENT evidence at freeze

Canonical corpus: `data/p8/labels_v0.csv`.

Coverage:

- FLAT_BASE: 5
- CUP_WITH_HANDLE: 5
- DOUBLE_BOTTOM: 5
- CUP_WITHOUT_HANDLE: 5

Frozen DEVELOPMENT artifact:

```text
result_count                 = 20
MATCH                        = 20
BOUNDARY_DISAGREEMENT        = 0
LANDMARK_DISAGREEMENT        = 0
MISS_PATTERN                 = 0
STATUS_CONFLICT              = 0
```

Candidate identity states:

```text
STABLE                        = 940
MULTI_SEMANTIC_STABLE_STATUS  = 59
LIFECYCLE_TRANSITION          = 9
STATUS_CONFLICT               = 0
```

Freeze evidence commit: `2ed3dadcc354f56f4cb27401248daef60b1627fa`.
Freeze workflow run: `34740880269`.

## P8 Independent VALIDATION

The locked NFLX `CUP_WITH_HANDLE` case was opened exactly once after freeze.

Workflow run: `34741079533`.
Artifact id: `10312408925`.

Result:

```text
agreement_state         = MATCH
candidate_resolution    = UNIQUE
source start            = 2023-02-03
matched start           = 2023-02-03
start error             = 0 days
matched detector state  = CUP_WITH_HANDLE_AMBIGUOUS
candidate semantics     = OPEN_RIGHT_EDGE_HANDLE:p8-open-right-edge-handle-v0.1
detector fault          = BELOW_CUP_MIDPOINT
```

The one-shot workflow path was removed after execution so NFLX is not repeatedly re-used as tuning evidence.

## Final P8 verdict

**CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT** for the four core families.

What passed:

- source-grounded pattern representation;
- PIT/right-edge semantics;
- source precision and corporate-action comparison handling;
- 20/20 DEVELOPMENT source-dimension agreement;
- zero true candidate identity conflicts in the frozen DEVELOPMENT audit;
- unique independent NFLX structural match at the authoritative start date.

What remains debt:

- NFLX remains `CUP_WITH_HANDLE_AMBIGUOUS` because of frozen `BELOW_CUP_MIDPOINT` severity;
- the locked NFLX row intentionally did not score pivot/depth, so not every numeric CWH band received independent validation;
- advanced pattern families do not inherit the core P8 evidence level.

No frozen morphology threshold may now be changed from the NFLX result.

## P9 production alignment

Production v2 calls the exact canonical P8 prediction adapter rather than rebuilding landmarks/morphology independently.

Frozen production output includes only the four P8-validated core families and persists:

- canonical `candidate_id`;
- stable exact-structure `base_id`;
- conservative exact-anchor `lineage_id`;
- `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` status;
- candidate semantics;
- structural signature;
- structural start/end;
- pivot source date/level;
- depth when available;
- detector faults;
- versioned P8 and production contracts.

Production alignment regression suite: **224 tests passed** on workflow run `34741587492`.

## Downstream contract / stop boundary

#33 core is implementation-complete and frozen for the four P8 core families. P6 has now completed its requested same-standard authoritative validation cycle and is frozen with a validation-fail verdict.

The next core work item remains **#34 Theory-faithful Candidate Generator**, which belongs in the CAN SLIM parent workstream rather than further #33 morphology tuning.

A downstream #34 consumer must preserve:

- `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` state;
- `candidate_id`, `base_id`, and `lineage_id`;
- candidate semantics;
- detector faults;
- source/validation provenance where applicable.

`AMBIGUOUS` must not be silently converted into either recognized or absent morphology. #34 must not reopen P8 or the frozen P6 cycle based on returns, CAGR, PF, FWD1, breakout outcomes or entry optimization.
