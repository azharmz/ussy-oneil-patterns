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
| P6 Advanced patterns | FIRST-PASS ONLY | do not treat as having the same P8 evidence level as the four core families |
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

## DEVELOPMENT evidence at freeze

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

## Independent VALIDATION

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

The old first-pass production path was replaced because it still carried `P8_BLOCKED_ON_CORPUS` and v1 detector contracts. Production v2 now calls the exact canonical P8 prediction adapter rather than rebuilding landmarks/morphology independently.

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

Lineage v1 uses exact anchors only—no fuzzy date/price tolerance—so it intentionally prefers under-merging to unstable lineage churn.

Production alignment regression suite: **224 tests passed** on workflow run `34741587492`.

## Downstream contract / stop boundary

#33 core is now implementation-complete and frozen for the four validated families. The next work item is **#34 Theory-faithful Candidate Generator**, which belongs in the CAN SLIM parent workstream rather than further #33 morphology tuning.

A downstream #34 consumer must preserve:

- `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` state;
- `candidate_id`, `base_id`, and `lineage_id`;
- candidate semantics;
- detector faults;
- source/validation provenance where applicable.

`AMBIGUOUS` must not be silently converted into either recognized or absent morphology. #34 must not reopen P8 based on returns, CAGR, PF, FWD1, breakout outcomes or entry optimization.
