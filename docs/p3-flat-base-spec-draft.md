# P3 Flat Base Morphology Specification — Draft

Status: RESEARCH DRAFT — THEORY THRESHOLDS PREREGISTERED
Date: 2026-09-12
Upstream contracts: `p1-landmark-v1`, `p2-segmentation-v1`

## Purpose

Define the first pattern-specific morphology layer for `FLAT_BASE` without introducing breakout, entry, performance, or hidden swing logic.

The frozen parent #32 specification requires `FLAT_BASE` as a recognized pattern type, requires pattern-specific landmarks to be persisted, and defines its structural pivot as the base / left-side high. Exact geometric implementation belongs to #33 and must not be optimized against returns.

## Authoritative theory audit

IBD/O'Neil educational material consistently gives the following Flat Base morphology guidance:

- minimum length: **5 weeks / 25 trading sessions**;
- maximum depth: **15% from the base high to low**;
- price action should be sideways and relatively tight;
- wide, loose, erratic action is contrary/fault evidence;
- Flat Bases commonly follow a prior uptrend and may form after an earlier base;
- structural resistance/pivot is the high/peak within the base, commonly near the beginning.

The first two rules are explicit numeric morphology constraints. Tightness is authoritative qualitatively but the audited material does not provide one canonical numeric tightness formula. Therefore this contract freezes duration/depth directly while treating tightness metrics as evidence requiring morphology validation rather than inventing a theory threshold.

Historical IBD educational material also describes Flat Bases as often second-stage structures and gives an example prior uptrend of at least 30%. This is retained as contextual theory evidence, not frozen here as a universal P3 morphology gate, because prior-uptrend/base-stage semantics belong to a broader context layer and current IBD examples describe Flat Bases more generally as following a prior uptrend.

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

## Morphology dimensions

### 1. Duration

Canonical P3 duration rule:

```text
flat_base_min_duration_sessions = 25
```

A candidate with fewer than 25 trading sessions cannot yet be a completed theory-faithful Flat Base. It may remain developing/not evaluable rather than being permanently rejected while the structure is still live.

No maximum duration is frozen: authoritative guidance explicitly allows Flat Bases to last much longer than five weeks.

### 2. Depth / shallowness

Use P2 `depth_pct` as the canonical start-high-to-trough depth measure.

Canonical P3 maximum:

```text
flat_base_max_depth_pct = 0.15
```

Depth above 15% excludes `FLAT_BASE` under the canonical morphology rule, while leaving the region available to Cup, Double Bottom, generic/ambiguous consolidation, or later morphology layers.

The 10%-15% range sometimes cited in IBD examples is descriptive of typical Flat Bases, not a minimum-depth requirement. A shallower valid consolidation must not be rejected merely for being below 10%.

### 3. Tightness / range compression

Flat Base identity requires more than simply passing duration and depth. Authoritative guidance says trading should be sideways/tight and that tighter action is preferable to wide-and-loose behavior, but does not supply one canonical numeric formula.

P3 will therefore calculate morphology descriptors without yet converting an invented cutoff into theory:

- full-base normalized high-low range;
- close-to-close dispersion;
- rolling range dispersion/contraction;
- fraction of closes contained within upper-base bands;
- maximum alternating internal swing amplitude;
- interior structural-turn count and amplitudes.

These are morphology evidence, not trading-quality or expected-return scores.

### 4. Internal structural complexity

A Flat Base should not require a large rounded cup or a clear W structure.

Candidate evidence:

- number of interior P1 structural turns;
- amplitude of interior turns relative to total base depth;
- whether a second-bottom / middle-peak sequence is strong enough to favor Double Bottom interpretation;
- whether geometry instead implies Cup family.

P3 must allow ambiguity rather than force a Flat Base label.

### 5. Recovery relationship to starting high

Use P2:

- `recovery_to_start_ratio`;
- `recovered_depth_fraction`.

These describe whether the structure has returned near its left-side resistance. They do not themselves define breakout.

### 6. Wide-and-loose / fault evidence

Wide, loose, erratic price action is explicit contrary evidence in the theory. P3 will preserve a `WIDE_LOOSE` fault/evidence state based on preregistered descriptive metrics. A numeric cutoff is not yet frozen because the authoritative material audited here does not define one.

### 7. Boundary and incomplete evidence

Boundary-marked P1 landmarks and incomplete P2 stages remain explicit evidence. A boundary artifact must not silently become a textbook Flat Base.

### 8. Overlap / nesting context

P2 relation evidence is preserved. P3 must not discard a candidate merely because it overlaps or nests with another provisional base; later Base-on-Base / ambiguity logic may need that context.

### 9. Prior-uptrend context

A prior uptrend is part of the authoritative Flat Base description. P3 records whether upstream/context evidence supports a prior uptrend, but this draft does not invent a universal quantitative prior-uptrend gate. Historical IBD material's `>=30%` example is retained as research evidence for the later context specification rather than silently promoted to a universal morphology rule.

## Decision vocabulary

- `FLAT_BASE_RECOGNIZED`
- `FLAT_BASE_REJECTED`
- `FLAT_BASE_AMBIGUOUS`
- `FLAT_BASE_NOT_EVALUABLE`

Each decision must retain the evidence used.

At minimum, `FLAT_BASE_RECOGNIZED` requires the frozen duration/depth rules plus sufficient non-wide/loose morphology evidence once the tightness policy is validated. Passing only `duration >= 25` and `depth <= 15%` is necessary but not automatically sufficient.

## Preregistered threshold policy

Frozen theory thresholds for implementation:

```text
MIN_DURATION_SESSIONS = 25
MAX_DEPTH_PCT = 0.15
```

Not frozen numerically yet:

```text
TIGHTNESS / RANGE-COMPRESSION threshold
WIDE_LOOSE threshold
internal-complexity ambiguity threshold
prior-uptrend quantitative threshold
```

Those unresolved values must be selected using morphology/label agreement and robustness only. They must not be selected using return, breakout success, CAGR, profit factor, win rate, or portfolio performance.

## Implementation sequence

1. implement the two direct theory gates (`duration >= 25`, `depth <= 15%`);
2. implement descriptive tightness/wide-loose features without a return-derived cutoff;
3. create positive, negative and ambiguous fixtures;
4. evaluate candidate tightness definitions against morphology labels and perturbation stability;
5. freeze a versioned Flat Base contract only after those semantics are explicit and reproducible;
6. only then proceed to Double Bottom morphology.
