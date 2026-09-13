# P6 Advanced Patterns Contract v2

Contract id: `advanced-patterns-v2`

Status: **FROZEN — CONDITIONAL PASS WITH VALIDATION DEBT**

This contract supersedes `advanced-patterns-v1` for P6 state classification only. It does not revise the frozen P3/P4/P5/P8 core and it does not add advanced families to `oneil-pattern-output-v2`.

## Ascending Base

Sub-contract: `ascending-base-v2`.

Required structural sequence:

`HIGH -> LOW -> HIGH -> LOW -> HIGH -> LOW -> HIGH`

Hard morphology requirements:

- exactly three observed pullbacks;
- successively higher troughs;
- successively higher recovery peaks;
- duration 45–80 observed sessions, retained as the operational translation of the source 9–16 week guidance.

Source-grounded depth evidence:

- textbook pullback band: 10%–20% (diagnostic evidence);
- MarketSmith/IBD recognition envelope: 6%–25% (outer ambiguity guardrail).

States:

- `ASCENDING_BASE_RECOGNIZED`: hard morphology passes and all three pullbacks are inside the 6%–25% source envelope;
- `ASCENDING_BASE_REJECTED`: duration or ascending-structure hard gate fails;
- `ASCENDING_BASE_AMBIGUOUS`: hard structure passes but at least one pullback is outside the 6%–25% source envelope.

Faults:

- `TOO_SHORT` — theory/reject;
- `TOO_LONG` — theory/reject;
- `NON_ASCENDING_TROUGHS` — theory/reject;
- `NON_ASCENDING_PEAKS` — theory/reject;
- `PULLBACK_OUTSIDE_MARKETSMITH_ENVELOPE` — theory/ambiguity.

Removed from v2 state logic:

- `PULLBACK_DEPTH_INCONSISTENT`;
- the research-only `0.05` dispersion threshold.

The dispersion metric may remain in geometry as descriptive evidence but does not decide state.

## Base-on-Base

Base-on-Base composes two already-recognized base summaries. It does not create a second swing/base detector.

Frozen summary fields remain:

- pattern name;
- start/end dates;
- confirmed date;
- high/low prices.

Geometry remains:

- relation sessions (gap/touch/overlap);
- combined duration;
- second-base low / first-base high ratio;
- fraction of second-base closes at or above the first-base high;
- confirmation date = latest component confirmation.

State policy v2:

- `base_2.low_price >= base_1.high_price` -> `BASE_ON_BASE_RECOGNIZED`;
- `base_2.high_price <= base_1.high_price` -> `BASE_ON_BASE_REJECTED` + `SECOND_BASE_NOT_ABOVE_FIRST`;
- otherwise -> `BASE_ON_BASE_AMBIGUOUS` + `SECOND_BASE_OVERLAPS_FIRST`.

The close-fraction metric is diagnostic only. The v1 50%/75% thresholds are removed because no audited source supplies a universal numerical definition of “mostly above.”

This policy intentionally recognizes only the source-unambiguous “entirely above” subset. Source-valid “mostly above” candidates remain ambiguous until independent labelled morphology can calibrate that qualitative boundary without using returns.

## PIT semantics

Both advanced patterns inherit P1/P2 confirmation semantics:

- no future bar may alter geometry/state for an already-complete frozen candidate;
- confirmation date is the latest required structural confirmation;
- invalid component ordering raises a construction error;
- Base-on-Base assumes its component bases are already recognized/confirmed upstream.

## Evidence boundary

Contract v2 is supported by:

- source audit in `docs/p6-source-audit-v2.md`;
- synthetic positive/negative/ambiguous fixtures;
- future-session/future-row invariance tests;
- normalized fault/adapter regression coverage;
- repository-wide CI regression.

It is **not** supported by a P8-equivalent independent labelled corpus. Therefore:

- P6 is frozen at **CONDITIONAL PASS WITH VALIDATION DEBT**;
- advanced families remain excluded from frozen core production schema v2;
- no threshold may be tuned using trading outcomes;
- any future attempt to resolve the remaining ambiguity requires a new versioned P6 validation cycle.
