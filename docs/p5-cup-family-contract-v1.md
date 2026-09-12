# P5 Cup Family Contract v1

Contract id: `cup-family-v1`

Status: **FROZEN FIRST PASS**

## Scope

P5 classifies a shared Cup body first, then optionally a Handle. It reuses P1/P2 structure and does not create a separate swing detector.

## Shared Cup body

Structural sequence:

`left_rim SWING_HIGH -> trough SWING_LOW -> right_rim SWING_HIGH`

Frozen geometry fields:

- `duration_sessions`
- `decline_sessions`
- `recovery_sessions`
- `depth_pct`
- `right_rim_to_left_rim_ratio`
- `left_right_time_ratio`
- `sessions_within_5pct_of_trough`
- `sessions_within_10pct_of_trough`
- `lower_third_fraction`
- `max_bottom_run_10pct`

### Theory-grounded first-pass gates

- Cup-without-handle body minimum duration: 30 observed sessions (6-week operationalization)
- normal maximum depth: 33%
- rounded U / teacup morphology is required conceptually; sharp V is contrary evidence

### Research-only Cup body morphology bands

The following are first-pass morphology research parameters, not official numeric O'Neil/IBD rules:

- minimum meaningful Cup depth: 8%
- at least 3 sessions within 5% of trough for a clearly non-V bottom
- bottom-contiguity ratio >= 0.75, where `max_bottom_run_10pct / sessions_within_10pct_of_trough`
- right-rim recovery ratio >= 0.90 for an unambiguous body

These parameters must be validated/revised only from morphology labels in P8, never from trading returns.

Cup body states:

- `CUP_RECOGNIZED`
- `CUP_REJECTED`
- `CUP_AMBIGUOUS`

Cup body faults:

- `TOO_SHORT`
- `TOO_DEEP`
- `SHALLOW_NON_CUP`
- `SHARP_V`
- `FRAGMENTED_BOTTOM`
- `WEAK_RIGHT_RIM_RECOVERY`

Synthetic U/V/W/flat/loose fixtures and small perturbation/PIT tests are green.

## Handle

Handle structural sequence:

`cup.right_rim SWING_HIGH -> handle_low SWING_LOW -> handle_recovery SWING_HIGH`

Frozen handle geometry:

- `duration_sessions`
- `depth_pct`
- `cup_midpoint_price`
- `low_in_upper_half`
- `recovery_to_right_rim_ratio`
- PIT `confirmed_date`

Theory-grounded handle guidance encoded in v1:

- minimum duration: 5 trading sessions
- handle low must remain in the upper half of the Cup
- normal handle depth up to 12% for first-pass normality; deeper handles are treated as exceptional/ambiguous rather than silently normal

Handle states:

- `HANDLE_RECOGNIZED`
- `HANDLE_REJECTED`
- `HANDLE_AMBIGUOUS`

Handle faults:

- `TOO_SHORT`
- `BELOW_CUP_MIDPOINT`
- `DEEP_HANDLE_EXCEPTIONAL`

## Family classification

A family label is downstream of a recognized Cup body:

- recognized Cup + recognized Handle -> `CUP_WITH_HANDLE`
- recognized Cup + no Handle + explicitly complete right-edge context -> `CUP_NO_HANDLE`
- recognized Cup + no Handle + incomplete right-edge context -> `CUP_FAMILY_INCOMPLETE`
- recognized Cup + malformed/ambiguous Handle attempt -> `CUP_HANDLE_AMBIGUOUS`
- non-recognized Cup body -> `NOT_A_RECOGNIZED_CUP`

Absence of a Handle is never inferred merely because the input series ends.

## PIT semantics

- all landmark `price_date` and `confirmed_date` semantics remain inherited from P1
- Cup body geometry only uses bars between left and right rims
- future bars after the right rim cannot rewrite an already-known Cup body assessment
- a later Handle can enrich the family state only when its own landmarks are confirmed
- no family label may be backdated to before the evidence required for that state was known

## Non-goals

This contract does not define breakout, pivot execution, entry timing, returns, portfolio sizing, sell logic, or CAN SLIM eligibility.

## Validation debt

P8 must validate the research-only roundedness/continuity/recovery bands against authoritative or human-labelled morphology examples before they can be treated as production-stable morphology rules.
