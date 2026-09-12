# P5 Cup Family — Morphology Specification Draft

Status: **DRAFT / THEORY-AUDITED FIRST PASS**

P5 begins after `double-bottom-v1` is frozen. It must reuse P1 structural turns and P2 base segmentation; it must not invent a separate swing detector.

## Scope

P5 covers a shared Cup morphology first, then distinguishes:

- Cup without Handle;
- Cup with Handle (CWH).

The handle classifier must be downstream of a valid cup body. A direct CWH detector that bypasses shared cup geometry is prohibited.

## Audited O'Neil/IBD guidance

Official IBD material supports these first-pass constraints:

### Cup with Handle

- minimum base duration: **7 weeks**;
- typical cup depth: roughly **12% to 33%**;
- visual character: a **U-shaped / teacup-like** base rather than a sharp V;
- handle minimum duration: **5 trading sessions / 1 week**;
- proper handle forms in the **upper half of the cup**;
- normal handle depth is commonly **8% to 12%**, with deeper handles possible in exceptional severe-market conditions.

### Cup without Handle

- minimum duration: **6 weeks**;
- maximum normal depth: **33%**;
- the structure proceeds from the cup body directly toward new highs without a separate qualifying handle;
- price action should not be wide and loose.

### Prior trend context

IBD educational material commonly describes cups as forming after a meaningful prior uptrend. That context is important evidence, but P5 will keep morphology recognition separate from CAN SLIM eligibility and outcome logic.

## Shared cup structural idea

A cup body is represented by a left-side high/rim, a broad trough region, and a right-side recovery/rim. The detector must distinguish a rounded U-like structure from:

- a sharp V-shaped rebound;
- a Double Bottom/W;
- a flat/sideways base;
- a wide/loose erratic decline/recovery;
- a base whose right side never meaningfully recovers toward the left rim.

## Geometry dimensions to formalize

### 1. Duration

For first-pass shared cup-body research:

- Cup-with-handle family body must be capable of satisfying the 7-week minimum once handle context is included;
- Cup-without-handle requires at least 6 weeks;
- duration semantics must distinguish shared cup body duration from later handle duration rather than mixing them into one ambiguous field.

### 2. Depth

Measure left-rim to trough decline.

First-pass normal range guidance:

- lower-bound guidance around **12%** is typical for Cup with Handle rather than a universal rejection rule;
- normal maximum cup depth: **33%**;
- exceptional bear-market cases may be deeper, but first-pass detector policy should mark those as exceptional/ambiguous rather than silently normal.

### 3. Roundedness / V-shape discrimination

The core P5 research problem is turning the source-supported "U-shape / teacup" description into measurable geometry without overfitting. Candidate descriptors include:

- fraction of cup duration spent near the lower portion of the depth range;
- left/right slope asymmetry;
- number and distribution of structural turns near the bottom;
- curvature or piecewise slope descriptors;
- time from left rim to trough versus trough to right rim;
- distance of the lowest region from a one-bar spike;
- contiguous bottom-region width.

No official numeric roundedness threshold was found in the audited guidance. Any such threshold remains research-only and must be validated from morphology labels, not returns.

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

These bands are research descriptors until labelled validation supports thresholds.

## Cup without Handle

A cup-without-handle candidate is a valid cup body with no qualifying handle after the right-side recovery/rim. It must not be labelled CWH merely because no later bars are available; incomplete right-edge context should remain explicit.

First-pass theory gates for Cup without Handle:

- duration >= **30 observed sessions** as the 6-week operationalization;
- depth <= **33%**;
- shared Cup body must pass roundedness / non-V morphology policy once that research contract is validated.

## Handle segmentation — later subphase

Only after shared cup morphology is stable should P5 segment a possible handle.

Theory-grounded handle guidance:

- starts after the right-side cup recovery/rim region;
- duration >= **5 trading sessions**;
- should form in the **upper half** of the cup;
- normal depth commonly **8% to 12%**;
- should not be confused with another full base.

Handle volume and moving-average context appear in IBD guidance, but morphology implementation will first keep price geometry explicit and separate from later contextual evidence.

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

1. Formalize shared Cup body geometry over existing P1/P2 structure.
2. Compute duration, depth, left/right timing, rim recovery, bottom-region width and roundedness descriptors.
3. Build synthetic U, V, W, flat and loose examples before thresholding roundedness.
4. Freeze shared Cup body semantics before handle classification.
