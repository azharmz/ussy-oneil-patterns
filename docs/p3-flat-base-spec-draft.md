# P3 Flat Base Morphology Specification — Draft

Status: RESEARCH DRAFT
Date: 2026-09-12
Upstream contracts: `p1-landmark-v1`, `p2-segmentation-v1`

## Purpose

Define the first pattern-specific morphology layer for `FLAT_BASE` without introducing breakout, entry, performance, or hidden swing logic.

The frozen parent #32 specification requires `FLAT_BASE` as a recognized pattern type, requires pattern-specific landmarks to be persisted, and defines its structural pivot as the base / left-side high. It explicitly leaves exact geometric detector thresholds to #33 implementation design and forbids return-optimized threshold derivation.

## Inputs

P3 consumes:

- frozen `BaseSegmentCandidate` objects from P2;
- frozen P1 landmarks and their PIT confirmation/evidence;
- raw OHLCV bars restricted to the candidate structural region and to the as-of information set;
- P2 overlap/nesting relations.

P3 must not rebuild extrema or change P2 start/end semantics.

## Required Flat Base output concepts

A recognized Flat Base should eventually persist at least:

- `pattern_type = FLAT_BASE`;
- `flat_left_high`;
- structural base start/end dates;
- duration sessions;
- base depth;
- morphology evidence/confidence state;
- fault flags;
- pivot source landmark/date once morphology is valid.

The pivot remains structural resistance from the Flat Base itself; breakout logic is outside P3.

## Morphology dimensions to quantify

### 1. Duration / compactness

Measure how long the provisional base persists as a structural consolidation. No universal duration threshold is frozen in this draft.

Candidate evidence:

- total structural duration;
- decline vs recovery duration balance;
- time spent near the upper portion of the base.

### 2. Depth / shallowness

Use P2 `depth_pct` as the canonical start-high-to-trough depth measure.

The detector must distinguish a relatively shallow consolidation from deeper cup-like structures, but the cutoff is not yet frozen.

### 3. Tightness / range compression

Flat Base identity requires more than simply shallow depth. Candidate within-region evidence may include:

- normalized high-low range;
- rolling range contraction;
- close-to-close dispersion;
- upper/lower excursion around a central level;
- fraction of sessions contained within a narrow band relative to the base high.

These are morphology descriptors, not trading-quality scores.

### 4. Internal structural complexity

A Flat Base should not require a large rounded cup or a clear W structure.

Candidate evidence:

- number of interior P1 structural turns;
- amplitude of interior turns relative to total base depth;
- whether a second-bottom / middle-peak sequence is strong enough to favor Double Bottom interpretation;
- whether geometry instead implies Cup family.

P3 must allow `AMBIGUOUS_BASE` rather than forcing a label.

### 5. Recovery relationship to starting high

Use P2:

- `recovery_to_start_ratio`;
- `recovered_depth_fraction`.

These describe whether the structure has returned near its left-side resistance. They do not themselves define breakout.

### 6. Wide-and-loose / fault evidence

Candidate fault descriptors should include excessive internal volatility, large alternating swings, and lack of sustained compression. Exact fault thresholds remain research items.

### 7. Boundary and incomplete evidence

Boundary-marked P1 landmarks and incomplete P2 stages remain explicit evidence. A boundary artifact must not silently become a textbook Flat Base.

### 8. Overlap / nesting context

P2 relation evidence is preserved. P3 must not discard a candidate merely because it overlaps or nests with another provisional base; later Base-on-Base / ambiguity logic may need that context.

## Decision vocabulary — draft

Flat Base classification should not be a bare Boolean. Initial research vocabulary:

- `FLAT_BASE_RECOGNIZED`
- `FLAT_BASE_REJECTED`
- `FLAT_BASE_AMBIGUOUS`
- `FLAT_BASE_NOT_EVALUABLE`

Each decision must retain the evidence used.

## Threshold policy

No numeric Flat Base morphology threshold is frozen by this draft.

Thresholds must be derived from theory-faithful O'Neil/IBD evidence and morphology validation. They must not be selected using return, breakout success, CAGR, profit factor, win rate, or portfolio performance.

## Next P3 work

1. audit authoritative O'Neil/IBD Flat Base definitions for duration, depth and tightness guidance;
2. map each textual rule to measurable daily-OHLCV geometry;
3. preregister candidate threshold ranges before labelled validation;
4. create positive, negative and ambiguous Flat Base fixtures;
5. implement the classifier only after the morphology specification is explicit enough to test.
