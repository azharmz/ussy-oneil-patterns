# P8 source-end role semantics

Date: 2026-09-13
Status: DEVELOPMENT evaluator correction

## Trigger

The first canonical DEVELOPMENT run showed SNPS as `BOUNDARY_DISAGREEMENT` even though the canonical extractor matched the authoritative Flat Base start (`2023-04-04`) and pivot (`392.79`) exactly.

The mismatch came from comparing:

- source `window_end = 2023-05-18`, documented by the adjudication record as the **breakout** anchor; with
- canonical prediction `end_date = 2023-04-25`, a **structural segment end**.

These are different semantic dimensions.

## Decision

Evaluator v0.2 no longer assumes that legacy corpus `window_end` means detector structural end.

Until the corpus carries an explicit versioned role for an end anchor, `window_end` is preserved as source evidence but is not scored against `MorphologyPrediction.end_date`.

Start anchors remain scored at their published precision. Explicit pivot date/price dimensions remain scored. Missing or non-comparable dimensions do not become failures.

## Why this is not detector tuning

No morphology threshold, landmark extraction, segmentation rule, pattern state, or pivot definition changes.

The correction prevents an invalid comparison between a breakout date and a structural boundary. It is source/evaluator semantics only.

## Guardrails

- DEVELOPMENT only.
- NFLX VALIDATION remains locked and is not inspected or used to choose this correction.
- No return, CAGR, PF, FWD1, breakout-performance, or entry evidence is consulted.
- A future structural-end score requires an explicit source-end role, not inference from detector output.
