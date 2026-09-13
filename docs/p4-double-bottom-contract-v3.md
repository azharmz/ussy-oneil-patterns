# P4 Double Bottom Contract v3

Contract id: `double-bottom-v3`

Status: P8 DEVELOPMENT REVISION - NOT FINAL-FROZEN
Date: 2026-09-13

This revision supersedes `double-bottom-v2` for P8 DEVELOPMENT validation. It keeps v2 undercut semantics and revises only the duration-boundary representation.

## Structural core

The confirmed core W remains:

`left_high -> trough_1 -> middle_peak -> trough_2 -> optional confirmed right_recovery_high`

Its geometry remains immutable and separately observable.

## Hard numerical gates

Unchanged:

- minimum Double Bottom base duration: 35 observed sessions;
- maximum depth: 40 percent.

No numerical threshold is reduced by v3.

## Duration representation

A core W can be structurally identifiable before the full source-described base has completed. Therefore `left_high -> trough_2` is no longer treated as the only admissible duration clock in P8 DEVELOPMENT.

Two explicit candidate classes may coexist:

1. `CONFIRMED_STRUCTURE`
   - uses frozen core-W duration through trough 2;
   - remains independently assessed and may receive `TOO_SHORT`.

2. `OPEN_RIGHT_EDGE_DOUBLE_BOTTOM`
   - retains the same confirmed W landmarks;
   - measures elapsed base duration from the left high through an explicit as-of horizon T;
   - may exist only after trough 2 is confirmed and observed post-trough-2 price has recovered to at least the middle-peak pivot;
   - T is observation evidence only, never a fabricated P1 swing high.

This makes completion evidence additive instead of rewriting historical geometry.

## Undercut semantics from v2

Unchanged:

- `TOO_SHORT` or `TOO_DEEP` => `REJECTED` for the candidate being assessed;
- `NO_SECOND_TROUGH_UNDERCUT` => `AMBIGUOUS`, fault retained;
- `SHALLOW_UNDERCUT` => `AMBIGUOUS`;
- `WEAK_MIDDLE_REBOUND` => `AMBIGUOUS`;
- all hard gates pass and no ambiguity fault => `RECOGNIZED`.

The research clear-undercut band remains 0.5 percent and the middle-rebound band remains 50 percent.

## DEVELOPMENT evidence

SEI 2024 reproduces the authoritative late-July start and 12.74 pivot. The core-W candidate through September 12 remains slightly short and is `DOUBLE_BOTTOM_REJECTED`. By September 20 observed price has recovered through the pivot and the elapsed base duration satisfies the unchanged minimum; the explicit right-edge completion candidate is `DOUBLE_BOTTOM_RECOGNIZED`.

NVDA remains a clean recognized authoritative example. SPOT remains source-aligned but ambiguous because its second trough does not undercut the first.

## Candidate equivalence

When multiple candidate classes are equally consistent with all source-provided dimensions, the source evaluator must expose that multiplicity and any detector-state disagreement. Detector status is never used to rank source agreement.

## PIT and guardrails

- no future bars;
- no backdated confirmation;
- no fabricated right-edge landmark;
- no outcome or return tuning;
- core and completion candidates remain separately inspectable;
- NFLX VALIDATION remains locked.

Decision records:
- `docs/decisions/2026-09-13-p8-double-bottom-undercut-v0.2.md`
- `docs/decisions/2026-09-13-p8-double-bottom-duration-boundary-v0.3.md`
