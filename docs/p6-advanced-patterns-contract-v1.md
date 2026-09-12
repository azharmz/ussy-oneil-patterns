# P6 Advanced Patterns Contract v1

Contract id: `advanced-patterns-v1`

Status: **FROZEN FIRST PASS**

This contract freezes the first-pass morphology semantics for Ascending Base and Base-on-Base.

## Ascending Base

Sub-contract: `ascending-base-v1`

Documented in `docs/p6-ascending-base-contract-v1.md`.

Frozen structure:

`HIGH -> LOW -> HIGH -> LOW -> HIGH -> LOW -> HIGH`

with three pullbacks, successively higher troughs and recovery peaks, and a first-pass 45–80 observed-session duration neighborhood corresponding to the audited 9–16 week guidance.

Hard first-pass faults:

- `TOO_SHORT`
- `TOO_LONG`
- `NON_ASCENDING_TROUGHS`
- `NON_ASCENDING_PEAKS`

Research-only ambiguity:

- `PULLBACK_DEPTH_INCONSISTENT`

## Base-on-Base

Sub-contract: `base-on-base-v1`

Base-on-Base composes two already-recognized morphology summaries; it does not create a new swing/base detector.

Frozen component summary fields:

- pattern name
- start/end dates
- confirmed date
- high/low prices

Frozen relation geometry:

- sessions gap/touch/overlap between bases (`relation_sessions`; negative means overlap)
- combined duration
- second-base low / first-base high ratio
- fraction of second-base closes at or above the first-base high
- confirmation date = latest component confirmation

Source-supported conceptual rule:

- the second base should form entirely or mostly above the first base.

Research-only operationalization:

- fraction >= 0.75 -> `BASE_ON_BASE_RECOGNIZED`
- fraction < 0.50 -> `BASE_ON_BASE_REJECTED`
- 0.50 <= fraction < 0.75 -> `BASE_ON_BASE_AMBIGUOUS`

These fractions are not official O'Neil/IBD numeric rules. P8 must validate them from labelled morphology, never returns.

Frozen states:

- `BASE_ON_BASE_RECOGNIZED`
- `BASE_ON_BASE_REJECTED`
- `BASE_ON_BASE_AMBIGUOUS`

Frozen faults:

- `SECOND_BASE_NOT_ABOVE_FIRST`
- `SECOND_BASE_ONLY_MARGINAL_ABOVE`

Invalid component ordering raises a construction error rather than producing a misleading morphology state.

## PIT semantics

Both advanced patterns inherit P1/P2 confirmation semantics. Future dates/bars outside frozen component windows cannot rewrite an already-known result. Base-on-Base recognition requires both component bases to already be recognized/confirmed upstream.

## Validation debt

P8 must validate research-only Ascending Base pullback-consistency bands and Base-on-Base “mostly above” fractions on authoritative/human-labelled examples.
