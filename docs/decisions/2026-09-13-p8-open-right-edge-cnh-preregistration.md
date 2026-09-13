# P8 OPEN_RIGHT_EDGE Cup-no-Handle preregistration

Date: 2026-09-13

Status: PREREGISTERED FOR DEVELOPMENT

## Problem

The first-pass Cup body requires confirmed P1 landmarks:

`left_rim SWING_HIGH -> trough SWING_LOW -> right_rim SWING_HIGH`

AMZN 2023 provides an authoritative Cup-without-Handle example where the source says the base began in September, was about 19% deep, and had a 145.86 buy point. Canonical P1 contains:

- 2023-09-14 confirmed SWING_HIGH at ~145.86;
- confirmed post-rim lows on 2023-09-28 and 2023-10-26;
- no later confirmed P1 SWING_HIGH by the 2023-11-17 as-of horizon that represents the completed recovery.

The source-described base is therefore not representable under a completed `HIGH -> LOW -> HIGH` structure at that horizon.

## Revision under test

Add DEVELOPMENT-only candidate semantics:

`OPEN_RIGHT_EDGE_CNH:p8-open-right-edge-cnh-v0.1`

For every confirmed P1 `SWING_HIGH` start and confirmed P1 `SWING_LOW` after it, known by `asof_date`, measure a right-edge observation through T.

The observation stores:

- confirmed `left_rim`;
- confirmed `trough`;
- explicit `asof_date` observation horizon;
- duration from left rim through T;
- depth from left rim to trough;
- existing bottom roundedness/continuity descriptors over the observed region;
- observed post-trough recovery high through T and recovery ratio to the left rim.

The observed recovery high is evidence only. It is **not** persisted or exposed as a P1 `SWING_HIGH` and cannot backdate a structural turn.

## Existing morphology bands remain unchanged

- minimum duration: 30 observed sessions;
- max normal depth: 33%;
- minimum meaningful depth: 8%;
- at least 3 sessions within 5% of trough;
- bottom continuity ratio >= 0.75;
- right-edge recovery ratio >= 0.90 for unambiguous recognition.

The observation emits explicit RECOGNIZED / AMBIGUOUS / REJECTED diagnostic status with the existing Cup-body fault vocabulary. No threshold is changed in this slice.

The Cup-no-Handle pivot remains the confirmed left-rim high, consistent with the frozen parent #32 pivot contract.

## PIT guardrails

- only bars `<= asof_date` may enter the observation;
- start/trough must be confirmed P1 landmarks known by T;
- T and observed recovery high are never fabricated landmarks;
- multiple candidate scales may coexist;
- candidate generation is label-agnostic;
- NFLX VALIDATION remains locked.

## Expected diagnostic consequence

AMZN should gain a September-start candidate with pivot ~145.86. Whether that candidate is RECOGNIZED, AMBIGUOUS or REJECTED under existing Cup-body research bands is an empirical P8 result, not an acceptance target.
