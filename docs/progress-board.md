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
| P6 Advanced patterns | COMPLETE — CONDITIONAL PASS / FROZEN v2 | `ASCENDING_BASE` + `BASE_ON_BASE`; source-grounded conservative semantics, explicit validation debt, not P8-equivalent |
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

## Frozen P6 advanced stack

- advanced contract: `advanced-patterns-v2`
- Ascending Base adapter contract: `ascending-base-v2`
- Base-on-Base adapter contract: `advanced-patterns-v2`
- source audit: `docs/p6-source-audit-v2.md`
- P6 contract: `docs/p6-advanced-patterns-contract-v2.md`
- final verdict: `docs/decisions/p6-final-verdict.md`

P6 v2 removes the old research-only state thresholds (`0.05` pullback-depth dispersion and Base-on-Base `0.50` / `0.75` close fractions). They must not be restored or retuned from returns.

P6 remains outside `oneil-pattern-output-v2`. It does not inherit the independent P8 evidence level.

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

## Final P6 verdict

**CONDITIONAL PASS / FROZEN WITH VALIDATION DEBT** for `ASCENDING_BASE` and `BASE_ON_BASE`.

What passed:

- source audit for both advanced families;
- removal of unsupported research-only numerical state gates;
- source-grounded Ascending Base 3-pullback/higher-high/higher-low semantics and 6%–25% outer ambiguity guardrail;
- conservative Base-on-Base classification that recognizes the unambiguous entirely-above case and preserves partial overlap as ambiguous;
- PIT/future-extension invariance;
- versioned normalized fault/adapter contracts;
- full repository regression: **227 tests passed** on workflow run `34746587586`, commit `642cfe36aeadf0a488e3478bbfec8cd1e0dfdf07`.

What remains debt:

- no independent P6 labelled morphology corpus comparable to P8;
- no source-defined numeric boundary for Base-on-Base “mostly above”, so partial overlap remains ambiguous;
- Ascending Base 45–80 observed-session translation of 9–16 weeks lacks independent boundary validation;
- market weakness/prior uptrend/moving-average support and Base-on-Base initial breakout gain/stage logic remain context rather than pure morphology gates;
- P6 advanced families remain excluded from frozen production v2.

Do not tune P6 from returns or use P6 work to reopen P3/P4/P5/P8.

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

#33 core is implementation-complete and frozen for the four independently validated core families. P6 advanced morphology is also frozen separately at a conditional verdict, but remains outside core production v2 because its evidence level is lower.

The next core work item remains **#34 Theory-faithful Candidate Generator**, which belongs in the CAN SLIM parent workstream rather than further #33 morphology tuning.

A downstream #34 consumer must preserve:

- `RECOGNIZED` / `AMBIGUOUS` / `REJECTED` state;
- `candidate_id`, `base_id`, and `lineage_id`;
- candidate semantics;
- detector faults;
- source/validation provenance where applicable.

`AMBIGUOUS` must not be silently converted into either recognized or absent morphology. #34 must not reopen P8 or P6 based on returns, CAGR, PF, FWD1, breakout outcomes or entry optimization.
