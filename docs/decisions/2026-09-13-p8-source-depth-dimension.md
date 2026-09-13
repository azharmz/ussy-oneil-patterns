# P8 optional authoritative depth dimension

Date: 2026-09-13

Status: PREREGISTERED FOR DEVELOPMENT

## Problem

AMZN 2023 now has two label-agnostic OPEN_RIGHT_EDGE Cup-no-Handle candidates with the same September start and 145.86 pivot but different confirmed troughs. The authoritative IBD source explicitly describes the base as about 19% deep.

Without a source-depth dimension, both candidates tie on all currently scored dimensions and evaluator selection can fall through to deterministic candidate-id ordering. Detector state must never break that tie.

## Decision

Add an optional authoritative morphology dimension:

- `expected_depth_pct` — source-stated base depth expressed as a decimal fraction;
- `expected_depth_tolerance_pct_points` — absolute decimal tolerance around that source figure.

When absent, depth is unscored and has no effect on ranking or verdict.
When present, candidate predictions may expose `depth_pct`; the evaluator uses only the source-stated value and preregistered tolerance to rank/score candidates.

The detector state/faults remain excluded from source-dimension ranking.

## AMZN application

The authoritative source states the 2023 Cup-without-Handle base was about 19% deep. Freeze:

- `expected_depth_pct = 0.19`
- tolerance = `0.02` (±2 percentage points), reflecting the source's rounded “about 19%” wording rather than invented daily precision.

This dimension should prefer the September-to-late-October trough scale (~18.9%) over the September-to-late-September scale (~15.6%).

## Guardrails

- source depth is immutable evidence, not derived from detector output;
- no depth value is added where the source does not state one;
- detector thresholds are not changed by adding the evaluator dimension;
- NFLX VALIDATION remains locked;
- no performance/outcome information enters the comparison.
