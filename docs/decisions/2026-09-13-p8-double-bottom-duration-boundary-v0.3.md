# P8 Double Bottom duration-boundary semantics v0.3

Date: 2026-09-13
Status: DEVELOPMENT REVISION

## Evidence

The first-pass Double Bottom contract operationalized the seven-week minimum as a 35-session clock from the left high through trough 2. Authoritative educational material supports the seven-week minimum for Double Bottoms, but describes base duration at the base level rather than as a rule that must stop at trough 2.

SEI 2024 exposes the distinction. The authoritative source identifies a Double Bottom beginning in late July and clearing a 12.74 buy point during the week ended September 20. Canonical structure reproduces the late-July start, middle-peak/pivot at 12.74, and second trough on September 12. The frozen core-W clock through trough 2 is slightly short and receives only `TOO_SHORT`.

By September 20, however, observed price after trough 2 has recovered through the middle-peak pivot and the elapsed base duration from the left high satisfies the unchanged 35-session minimum.

An independent authoritative MarketSmith example in the corpus registry describes Mobileye as an eight-week Double Bottom, further supporting base-level duration as the relevant scale. That delisted example remains external-OHLCV debt and is not used to calibrate a new number.

## Revision

The numerical duration rule is kept:

- minimum duration remains 35 observed sessions;
- maximum depth remains unchanged;
- the core W geometry remains available and immutable.

For DEVELOPMENT validation, a separately marked `OPEN_RIGHT_EDGE_DOUBLE_BOTTOM` completion observation may measure elapsed base duration from the left high through T when all of the following hold:

1. trough 2 is already confirmed by T;
2. no future bars are used;
3. post-trough-2 observed price has recovered to at least the middle-peak pivot;
4. T is represented only as an observation horizon, never as a fabricated P1 swing high.

The original core-W candidate is retained. The completion observation is a second candidate class, not a rewrite of frozen geometry.

## Result on SEI

The source-identical core-W candidate remains `DOUBLE_BOTTOM_REJECTED` with `TOO_SHORT` through September 12.

The explicit right-edge completion candidate uses the same late-July start and 12.74 pivot, observes through September 20, satisfies the unchanged duration threshold, and becomes `DOUBLE_BOTTOM_RECOGNIZED` with no morphology fault.

Because both candidates are equally consistent with source-provided dimensions, the source evaluator must expose their candidate-class/status disagreement rather than selecting a detector verdict as ground truth.

## Verdict

- seven-week / 35-session minimum: `KEEP`;
- core-W `left_high -> trough_2` as the only duration boundary: `REVISE`;
- explicit post-trough-2 right-edge completion observation: `KEEP FOR DEVELOPMENT`, pending identity/prefix audit before production freeze.

## Guardrails

No numerical threshold was reduced. No detector status is used for source ranking. No return metric or VALIDATION data is used. NFLX remains locked.
