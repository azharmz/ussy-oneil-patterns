# P8 canonical prediction adapter v0.1

Date: 2026-09-13

Status: IMPLEMENTED ON DEVELOPMENT BRANCH

## Purpose

Canonical P8 source-dimension evaluation needs detector-emitted pattern facts with their native geometry and pivot before the production serializer discards those details.

`extract_core_morphology_predictions()` therefore mirrors the frozen landmark-first P1-P5 construction and adapts those structures directly into `MorphologyPrediction`.

It does not import the superseded CAN SLIM parent detector, identity, or lineage implementation.

## Pattern handling

- `FLAT_BASE`: every P2 segment evaluated by the frozen Flat Base assessment is retained with its native detector state and left/base-high pivot.
- `DOUBLE_BOTTOM`: frozen high-low-high-low-high sequences are evaluated; middle-peak pivot is persisted.
- `CUP_WITH_HANDLE`: a recognized cup body followed by a handle attempt is retained as CWH. A non-recognized handle does not disappear; it is reported as `CUP_WITH_HANDLE_AMBIGUOUS` so source agreement cannot hide detector uncertainty.
- `CUP_WITHOUT_HANDLE`: emitted only when the cup body is recognized, no immediate handle attempt is present, and right-edge context is complete.

## Cup-without-Handle right-edge context

The preregistered daily-data completion rule is:

`observed sessions after right rim >= MIN_HANDLE_DURATION_SESSIONS - 1`

This gives the minimum handle-duration window an opportunity to exist before absence of a handle is treated as structurally meaningful. It does not inspect breakout returns or the authoritative label.

## PIT / leakage guardrails

- future bars are rejected;
- only landmarks confirmed by `asof_date` are used;
- pivots come from `p8-pivot-adapter-v0.2`;
- source labels are not inputs to candidate extraction;
- no return/CAGR/PF/FWD1 data is used;
- candidate IDs are deterministic semantic hashes;
- NFLX VALIDATION remains outside DEVELOPMENT execution.

## Next slice

Wire strict `R2 -> Yahoo -> Tiingo` providers into a DEVELOPMENT-only runner, execute the five canonical DEVELOPMENT labels with adequate warm-up context, and persist the canonical report for disagreement classification.
