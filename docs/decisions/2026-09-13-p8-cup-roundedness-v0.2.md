# P8 Cup roundedness / continuity semantics v0.2

Date: 2026-09-13

Status: DEVELOPMENT REVISION

## Evidence

The first-pass Cup body contract explicitly labels these numerical bands as research-only proxies rather than official O'Neil/IBD rules:

- >=3 sessions within 5% of trough;
- bottom-contiguity ratio >=0.75;
- minimum meaningful depth 8%;
- right-rim recovery ratio >=0.90.

The canonical AMZN 2023 authoritative Cup-without-Handle example is now source-aligned on every published comparable dimension:

- source start: September 2023;
- canonical start: 2023-09-14;
- source pivot: 145.86;
- canonical pivot: ~145.86;
- source depth: about 19%;
- canonical source-selected trough scale depth: ~18.86%.

That exact source-selected morphology is currently rejected only by the research-only proxy faults `SHARP_V` and `FRAGMENTED_BOTTOM`.

## Revision

For Cup-body DEVELOPMENT v0.2:

- `TOO_SHORT` remains hard `REJECTED`;
- `TOO_DEEP` remains hard `REJECTED`;
- `SHALLOW_NON_CUP` remains `REJECTED` pending separate evidence because an extremely shallow structure may not constitute a Cup at all;
- `SHARP_V` becomes explicit `AMBIGUOUS` evidence rather than hard rejection;
- `FRAGMENTED_BOTTOM` becomes explicit `AMBIGUOUS` evidence rather than hard rejection;
- `WEAK_RIGHT_RIM_RECOVERY` remains `AMBIGUOUS`;
- no numerical threshold changes.

A source-aligned candidate carrying roundedness/continuity proxy faults is therefore not promoted to `RECOGNIZED`; it remains `CUP_AMBIGUOUS` / family ambiguity.

## Rationale

P8 is validating whether research-only numerical operationalizations faithfully represent authoritative morphology labels. An authoritative named Cup-without-Handle whose source-stated depth and pivot are reproduced exactly falsifies the use of these proxies as absolute identity gates, but does not prove the proxies are useless. Preserving them as ambiguity evidence is the conservative revision.

## Guardrails

- no returns or breakout outcome enter the decision;
- source dimensions were frozen before this state-mapping revision;
- thresholds remain numerically unchanged;
- NFLX VALIDATION remains locked.
