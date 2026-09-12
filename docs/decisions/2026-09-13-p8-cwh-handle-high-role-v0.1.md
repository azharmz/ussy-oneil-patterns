# P8 CWH handle-high role v0.1

Date: 2026-09-13

Status: IMPLEMENTED ON DEVELOPMENT BRANCH

## Decision

The frozen #32 pivot contract defines Cup-with-Handle pivot as the highest price in the valid handle.

The canonical oneil landmark sequence for a recognized cup/handle is:

`LEFT_RIM(HIGH) -> CUP_LOW(LOW) -> RIGHT_RIM(HIGH) -> HANDLE_LOW(LOW) -> HANDLE_RECOVERY(HIGH)`

Because there is no additional swing high between `RIGHT_RIM` and `HANDLE_LOW` in the frozen landmark-first representation, `RIGHT_RIM` is also the structural high that starts the handle pullback.

P8 therefore persists the same landmark under an additional explicit role:

`handle_high = cup.right_rim`

This is an additive semantic role, not a new extremum and not a detector-threshold change.

## Why this is safer than alternatives

The implementation does not:

- use `handle_recovery` as the pivot;
- inspect a later breakout high;
- search raw bars for a different high outside the frozen landmark sequence;
- use the authoritative label value to select the pivot.

The role is knowable when the cup right rim is confirmed and remains PIT-safe.

## Consequence

`p8-pivot-adapter-v0.2` can now expose CWH `HANDLE_HIGH` pivot facts. All four core pattern families therefore have canonical structural pivot extraction semantics available for DEVELOPMENT re-execution.

This does not imply that any migrated DEVELOPMENT example matches. The next step is to adapt actual canonical detector candidates into `MorphologyPrediction` and execute SNPS, CTSH, FOUR, SEI, and AMZN only.

NFLX VALIDATION remains locked.
