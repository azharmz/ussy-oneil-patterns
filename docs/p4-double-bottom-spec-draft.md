# P4 Double Bottom — Morphology Specification Draft

Status: **DRAFT / THEORY-TO-GEOMETRY PHASE**

P4 begins after `flat-base-v1` is frozen. It consumes the same frozen P1/P2 structural primitives and must not invent a separate swing engine.

## Core structural idea

A Double Bottom is represented as a W-like sequence built from structural turns:

`left-side high -> trough 1 -> middle peak -> trough 2 -> recovery / right-side high`

The morphology layer must distinguish a meaningful W from:

- one broad U/cup with incidental noise;
- a V-shaped reversal;
- two unrelated declines;
- a wide/loose erratic range;
- a second trough that is not structurally distinct from the first.

## Required landmarks

Candidate DB evidence should identify:

- `left_high`
- `trough_1`
- `middle_peak`
- `trough_2`
- optional/confirmed `right_recovery_high`

Pattern-specific labels are assigned only inside P4 after P1/P2 structural turns already exist.

## Geometry dimensions to formalize

### 1. Overall duration

The complete W must span a non-trivial structural interval. Exact minimum/typical duration must be theory-audited before freezing a detector threshold.

### 2. Overall depth

Measure decline from left-side high to the deeper of the two troughs. Exact acceptable depth range must be source-audited and must not be tuned from returns.

### 3. Two-trough distinctness

The two troughs must be separated by an intervening structural peak and enough temporal distance to be separate structural events rather than repeated bars from one low.

Candidate features:

- sessions between troughs;
- price difference between troughs as percentage of left-side high;
- trough-2 relative depth versus trough-1.

### 4. Middle-peak prominence

The center of the W must recover sufficiently from trough 1 to form a meaningful middle peak.

Candidate features:

- `middle_peak_rebound_pct = (middle_peak - trough_1) / trough_1`;
- recovered fraction of the first decline;
- middle-peak prominence evidence from P1 auxiliary landmark corroboration.

No numerical threshold is frozen yet.

### 5. Second-trough relation

A canonical Double Bottom often has the second trough near or below the first trough, but exact tolerances and whether a slightly higher second trough is still admissible must be source-audited rather than assumed.

Candidate descriptors:

- `trough2_vs_trough1_pct`;
- which trough is deeper;
- symmetry/asymmetry of left and right legs.

### 6. Right-side recovery

A recovery after trough 2 is evidence that the W structure is complete enough to evaluate. The pattern detector must remain PIT-safe: a right-side recovery cannot be backdated before its structural high is confirmed.

### 7. Wide/loose and malformed evidence

Potential contrary/fault evidence:

- insufficient middle-peak recovery;
- troughs too close together;
- one trough dominated by boundary artifact;
- extremely asymmetric legs;
- excessive internal structural noise;
- wide/loose range;
- incomplete second recovery.

## State model — draft

Likely public states:

- `DOUBLE_BOTTOM_RECOGNIZED`
- `DOUBLE_BOTTOM_REJECTED`
- `DOUBLE_BOTTOM_AMBIGUOUS`
- `DOUBLE_BOTTOM_NOT_EVALUABLE`

The exact fault vocabulary and state policy are not frozen yet.

## PIT rule

P4 may use only structural turns with `confirmed_date <= asof_date`. A W that becomes identifiable only after the second trough or right-side recovery is confirmed must not be reported earlier.

## Non-goals

P4 does not determine:

- breakout execution;
- entry timing;
- trading returns;
- portfolio allocation;
- CAN SLIM eligibility;
- whether a Double Bottom trade succeeds afterward.

## Immediate next research tasks

1. Audit O'Neil/IBD guidance for Double Bottom duration, depth, second-trough relation, and middle-peak semantics.
2. Translate source guidance into measurable descriptors and only then preregister defensible thresholds/ranges.
3. Build synthetic positive/negative/ambiguous W fixtures before implementing recognition policy.
4. Preserve P1/P2 PIT and boundary semantics throughout.
