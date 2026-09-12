# P4 Double Bottom Contract v1

Status: **FROZEN FIRST PASS**

Contract id: `double-bottom-v1`

## Structural sequence

A Double Bottom is interpreted from frozen P1/P2 turns as:

`left_high -> trough_1 -> middle_peak -> trough_2 -> optional right_recovery_high`

P4 does not create its own swing detector.

## Theory-grounded hard gates

- minimum core-W duration: **35 observed sessions**;
- duration boundary: **left_high -> trough_2**, so optional right recovery does not change the duration gate;
- maximum depth: **40%** from left high to the deeper trough;
- canonical second trough must **undercut** trough 1.

Failure of those gates maps to `DOUBLE_BOTTOM_REJECTED`.

## Research-only morphology bands

The following are first-pass research parameters, not claimed as official O'Neil/IBD numerical rules:

- clear undercut magnitude: at least 0.5% below trough 1;
- clear middle-peak recovery: at least 50% of the first decline recovered.

Candidates passing hard theory gates but failing one of these research bands remain `DOUBLE_BOTTOM_AMBIGUOUS`, not rejected.

## Public states

- `DOUBLE_BOTTOM_RECOGNIZED`
- `DOUBLE_BOTTOM_REJECTED`
- `DOUBLE_BOTTOM_AMBIGUOUS`

## Fault vocabulary

Theory-grounded hard faults:

- `TOO_SHORT`
- `TOO_DEEP`
- `NO_SECOND_TROUGH_UNDERCUT`

Research-only ambiguity faults:

- `SHALLOW_UNDERCUT`
- `WEAK_MIDDLE_REBOUND`

## Geometry contract

`DoubleBottomGeometry` exposes:

- `duration_sessions`
- `overall_depth_pct`
- `trough_spacing_sessions`
- `trough2_vs_trough1_pct`
- `middle_peak_rebound_pct`
- `middle_peak_recovered_fraction`
- optional `right_recovery_pct`
- optional `right_recovery_to_left_high_ratio`
- `confirmed_date`

Optional right-recovery evidence must not rewrite the core W duration or classification if the W was already evaluable from confirmed landmarks.

## PIT semantics

- only landmarks with their own frozen P1 confirmation semantics may participate;
- classification cannot be reported before trough 2 is confirmed;
- optional right recovery may enrich evidence later but may not backdate recognition;
- future data cannot rewrite historical geometry except through a legitimately later confirmed optional evidence field.

## Validation verdict

First-pass synthetic validation is green after resolving a duration-boundary inconsistency discovered by the PIT/robustness test. The final semantics make core W duration independent of optional right recovery.

Validated properties include:

- preregistered positive/negative/ambiguous fixture mapping;
- small uniform price-scale perturbation stability for clear positive and clear negative fixtures;
- optional right recovery does not change core-W classification;
- geometry remains separate from detector verdicts.

This is not the final empirical authority claim. P8 remains responsible for authoritative/human-labelled validation, especially of research-only undercut and middle-rebound bands.

## Non-goals

No breakout execution, entry timing, outcome optimization, portfolio logic, or CAN SLIM eligibility is part of this contract.
