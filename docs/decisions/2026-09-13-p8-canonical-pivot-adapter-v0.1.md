# P8 canonical pivot adapter v0.1

Date: 2026-09-13

Status: IMPLEMENTED ON DEVELOPMENT BRANCH

## Authority

The frozen parent #32 candidate specification defines canonical structural pivots as:

- `FLAT_BASE` -> base / left-side high;
- `DOUBLE_BOTTOM` -> middle peak of the W;
- `CUP_WITHOUT_HANDLE` -> prior / left-side high;
- `CUP_WITH_HANDLE` -> highest price in the valid handle.

P8 must adapt the canonical oneil native structures to these definitions without importing the superseded parent detector implementation.

## v0.1 extraction

The current canonical native structures provide enough explicit landmarks for:

- Flat Base: `BaseSegmentCandidate.start`;
- Double Bottom: `DoubleBottomGeometry.middle_peak`;
- Cup-without-Handle: `CupBodyGeometry.left_rim`.

These are exposed as versioned `PivotFact` values by `p8-pivot-adapter-v0.1`.

## CWH fail-closed decision

Current `HandleGeometry` persists:

- `handle_low`;
- `handle_recovery`.

It does **not** persist the frozen #32 `handle_high` / highest price in valid handle as an independent landmark.

Therefore CWH pivot extraction is intentionally `NOT_EVALUABLE` with reason:

`HANDLE_HIGH_NOT_PERSISTED`

The adapter must not substitute `handle_recovery`, `cup.right_rim`, a later breakout high, or a label-published pivot merely to make CTSH/FOUR agree.

## Consequence for migrated DEVELOPMENT labels

- SNPS Flat Base: canonical pivot extraction structurally eligible;
- SEI Double Bottom: canonical pivot extraction structurally eligible;
- AMZN Cup-without-Handle: canonical pivot extraction structurally eligible;
- CTSH and FOUR CWH: pivot comparison remains blocked until handle-high persistence is added to native oneil morphology;
- NFLX remains VALIDATION locked and is not inspected.

## Next slice

Version the CWH native handle landmark contract so the highest valid-handle price/date is persisted PIT-safely. Then adapt that fact into `MorphologyPrediction` and run the five DEVELOPMENT labels through the canonical source-dimension evaluator.
