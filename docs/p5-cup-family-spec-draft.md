# P5 Cup Family — Morphology Specification Draft

Status: **DRAFT / THEORY-TO-GEOMETRY PHASE**

P5 begins after `double-bottom-v1` is frozen. It must reuse P1 structural turns and P2 base segmentation; it must not invent a separate swing detector.

## Scope

P5 covers a shared Cup morphology first, then distinguishes:

- Cup without Handle;
- Cup with Handle (CWH).

The handle classifier must be downstream of a valid cup body. A direct CWH detector that bypasses shared cup geometry is prohibited.

## Shared cup structural idea

A cup body is represented by a left-side high/rim, a broad trough region, and a right-side recovery/rim. The detector must distinguish a rounded U-like structure from:

- a sharp V-shaped rebound;
- a Double Bottom/W;
- a flat/sideways base;
- a wide/loose erratic decline/recovery;
- a base whose right side never meaningfully recovers toward the left rim.

## Geometry dimensions to formalize

### 1. Duration

Audit O'Neil/IBD guidance for minimum/typical cup duration before freezing a threshold.

### 2. Depth

Measure left-rim to trough decline. Audit source-supported normal and exceptional depth ranges before hard gating.

### 3. Roundedness / V-shape discrimination

The core P5 research problem is turning "rounded U" into measurable geometry without overfitting. Candidate descriptors include:

- fraction of cup duration spent near the lower portion of the depth range;
- left/right slope asymmetry;
- number and distribution of structural turns near the bottom;
- curvature or piecewise slope descriptors;
- time from left rim to trough versus trough to right rim;
- distance of the lowest region from a one-bar spike.

No numerical roundedness threshold is frozen yet.

### 4. Rim relation

Measure right-side recovery relative to the left rim:

- `right_rim_to_left_rim_ratio`;
- percentage still below left rim;
- whether recovery becomes a confirmed structural high.

### 5. Bottom-region width

A rounded cup should have a non-trivial bottom region rather than one isolated extreme bar. Candidate descriptors:

- sessions within 5%/10% of trough;
- contiguous bottom-region width;
- share of total duration spent in lower third of cup depth.

These bands are research descriptors until source/label validation supports thresholds.

## Cup without Handle

A cup-without-handle candidate is a valid cup body with no qualifying handle after the right-side recovery/rim. It must not be labelled CWH merely because no later bars are available; incomplete right-edge context should remain explicit.

## Handle segmentation — later subphase

Only after shared cup morphology is stable should P5 segment a possible handle. Handle research dimensions include:

- start after right-side recovery/rim;
- duration;
- handle depth relative to cup and right rim;
- upper-half positioning;
- downward drift/tightness;
- structural completion and PIT confirmation.

Exact handle thresholds require theory audit before implementation.

## Draft state model

Likely body states:

- `CUP_RECOGNIZED`
- `CUP_REJECTED`
- `CUP_AMBIGUOUS`
- `CUP_NOT_EVALUABLE`

Later family classification can map a recognized cup to `CUP_NO_HANDLE`, `CUP_WITH_HANDLE`, or an incomplete/ambiguous handle state.

## PIT rule

P5 may use only information known by `asof_date`. A later right rim or handle may enrich/upgrade the state but must never be backdated.

## Non-goals

P5 does not determine breakout execution, trade entry, returns, portfolio sizing, or CAN SLIM eligibility.

## Immediate next work

1. Audit official O'Neil/IBD guidance for cup duration, depth, rounded-U semantics and handle geometry.
2. Translate only supported guidance into measurable descriptors.
3. Build synthetic U, V, W, flat and loose examples before thresholding roundedness.
4. Freeze shared Cup body semantics before implementing handle classification.
