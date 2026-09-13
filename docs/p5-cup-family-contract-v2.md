# P5 Cup Family Contract v2

Contract id: `cup-family-v2`

Status: P8 DEVELOPMENT REVISION - NOT FINAL-FROZEN
Date: 2026-09-13

This revision supersedes the first-pass Cup-body state mapping in `cup-family-v1` for P8 DEVELOPMENT validation. Hard duration and depth gates remain unchanged.

## Shared Cup body

Confirmed structural sequence remains `left_rim -> trough -> right_rim` using P1 landmarks.

P8 also permits an explicitly marked right-edge Cup-no-Handle observation consisting of a confirmed left rim, confirmed trough, and observed recovery through the as-of date. The as-of horizon is observation evidence, not a fabricated P1 high.

## Hard Cup-body gates

Unchanged:

- minimum Cup-no-Handle body duration: 30 observed sessions;
- normal maximum depth: 33 percent.

Failure of either gate maps to `CUP_REJECTED`.

## Research-only morphology bands

Numerical bands remain unchanged:

- minimum meaningful Cup depth: 8 percent;
- at least 3 sessions within 5 percent of the trough;
- bottom-contiguity ratio at least 0.75;
- right-rim recovery ratio at least 0.90 for an unambiguous completed body.

The v2 state mapping changes only severity:

- `SHALLOW_NON_CUP` remains `REJECTED`;
- `SHARP_V` becomes `AMBIGUOUS` with the fault retained;
- `FRAGMENTED_BOTTOM` becomes `AMBIGUOUS` with the fault retained;
- `WEAK_RIGHT_RIM_RECOVERY` remains `AMBIGUOUS`;
- no hard or research ambiguity faults maps to `RECOGNIZED`.

No numerical threshold is moved.

## DEVELOPMENT evidence

AMZN 2023 is an authoritative Cup-without-Handle example. The source describes a September start, about 19 percent depth, and a 145.86 pivot. Source-dimension evaluator v0.4 selects the right-edge candidate beginning 2023-09-14 with trough 2023-10-26 because its measured depth is about 18.86 percent and its pivot is 145.86. That candidate carries only the research-only `SHARP_V` and `FRAGMENTED_BOTTOM` faults.

The revision changes those faults from rejection to explicit ambiguity. It does not force AMZN to recognized status.

## Cup-with-Handle right-edge semantics

P8 separately preregisters an open-right-edge handle observation when the Cup body and handle low are confirmed but a post-handle recovery high is not yet a confirmed P1 landmark by the as-of date.

The Cup right rim remains the pivot anchor, the horizon remains observation evidence, and handle faults remain explicit. FOUR 2024 becomes source-dimension MATCH under this representation while remaining `CUP_WITH_HANDLE_AMBIGUOUS` because `DEEP_HANDLE_EXCEPTIONAL` is still present.

## Outstanding debt

CTSH 2004 still has unresolved source-start and left-rim semantics. Handle-depth numerical bands remain under P8 validation debt. Cup-no-Handle candidate identity and lineage effects remain to be audited. Additional authoritative Cup-no-Handle examples remain desirable before final freeze.

## Guardrails

No return-based tuning or VALIDATION data are used. NFLX remains locked until DEVELOPMENT semantics freeze.

Decision records:
- `docs/decisions/2026-09-13-p8-cup-roundedness-v0.2.md`
- `docs/decisions/2026-09-13-p8-cwh-handle-high-role-v0.1.md`
