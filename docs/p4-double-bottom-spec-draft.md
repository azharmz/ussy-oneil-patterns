# P4 Double Bottom — Morphology Specification Draft

Status: **P4.1 THEORY AUDIT COMPLETE / P4.2 GEOMETRY FORMALIZATION NEXT**

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

## P4.1 audited theory guidance

The following points are supported by official Investor's Business Daily material and are now preregistered as theory-grounded morphology constraints for #33:

1. **Minimum duration: 7 weeks.** IBD's chart-pattern buying checklist gives the Double Bottom a 7-week minimum. For the daily engine this is represented initially as **35 trading sessions minimum**; exact exchange-calendar counting remains based on observed sessions, not calendar days.
2. **Maximum base depth: 40%.** The same IBD checklist states a Double Bottom base depth of **40% or less**.
3. **The second trough should undercut the first trough.** IBD explicitly describes the second leg of a proper Double Bottom as undercutting the first. This undercut serves the shakeout role of the second leg. A second trough that remains above the first is therefore contrary evidence rather than a canonical Double Bottom.
4. **The middle peak is a structurally meaningful W landmark.** IBD defines the conventional buy point from the peak in the middle of the W. P4 does **not** implement the buy rule, but this confirms that the intervening middle peak is not incidental noise: it is a required structural landmark for morphology.
5. **Double Bottom is a W-shaped base.** The intended geometry is two distinct downward legs separated by a meaningful rebound, not merely two nearby low bars.

Sources audited:

- Investor's Business Daily, *How To Buy Stocks* chart-pattern checklist: https://get.investors.com/wp-content/uploads/2024/08/IBDD-How-to-buy-Stocks-infographic.pdf
- Investor's Business Daily, *Best Stocks To Buy Form Bullish Bases Before Big Price Gains*: https://www.investors.com/how-to-invest/investors-corner/best-stocks-to-buy-form-bullish-bases-before-big-price-gains/

These sources support the duration/depth/undercut/middle-peak structure above. They do **not** establish one canonical numerical rule for how far trough 2 must undercut trough 1, how high the middle rebound must be, or the minimum number of sessions between troughs. Those remain research geometry parameters and must not be presented as official O'Neil/IBD thresholds.

## Required landmarks

Candidate DB evidence should identify:

- `left_high`
- `trough_1`
- `middle_peak`
- `trough_2`
- optional/confirmed `right_recovery_high`

Pattern-specific labels are assigned only inside P4 after P1/P2 structural turns already exist.

## Theory-grounded hard gates

### 1. Overall duration

Preregistered minimum:

```text
MIN_DURATION_SESSIONS = 35
```

This operationalizes the IBD 7-week minimum as 35 observed trading sessions. It is a morphology gate, not a return-optimized parameter.

### 2. Overall depth

Measure the decline from `left_high` to the deeper of `trough_1` and `trough_2`:

```text
overall_depth_pct = (left_high - min(trough_1, trough_2)) / left_high
MAX_DEPTH_PCT = 0.40
```

### 3. Second-trough undercut

Canonical Double Bottom theory requires:

```text
trough_2.price < trough_1.price
```

The **magnitude** of the undercut is not frozen from theory. P4 should preserve a continuous descriptor:

```text
trough2_vs_trough1_pct = (trough_2 - trough_1) / trough_1
```

Negative values are canonical-direction undercuts; zero or positive values are contrary evidence under the current theory contract.

## Research geometry still to formalize

### 4. Two-trough distinctness

The two troughs must be separated by an intervening structural peak and enough temporal distance to be separate structural events rather than repeated bars from one low.

Candidate features:

- sessions between troughs;
- price difference between troughs as percentage of left-side high;
- trough-2 relative depth versus trough-1.

No minimum spacing threshold is frozen yet.

### 5. Middle-peak prominence

The center of the W must recover meaningfully from trough 1 to form the structurally required middle peak.

Candidate features:

- `middle_peak_rebound_pct = (middle_peak - trough_1) / trough_1`;
- `middle_peak_recovered_fraction = (middle_peak - trough_1) / (left_high - trough_1)`;
- middle-peak prominence/corroboration from P1 auxiliary evidence.

Theory confirms that the middle peak matters structurally, but no canonical numerical rebound threshold was found in the audited sources. It remains research-only until morphology validation.

### 6. Right-side recovery

A recovery after trough 2 is evidence that the W structure is complete enough to evaluate. The detector must remain PIT-safe: a right-side recovery cannot be used before its structural high is confirmed.

### 7. Symmetry / asymmetry descriptors

Preserve rather than prematurely threshold:

- left-leg duration;
- first recovery duration;
- second decline duration;
- right recovery duration when known;
- relative leg-depth ratios;
- relative temporal symmetry.

### 8. Wide/loose and malformed evidence

Potential contrary/fault evidence:

- `TOO_SHORT` (<35 sessions);
- `TOO_DEEP` (>40%);
- `SECOND_TROUGH_NOT_UNDERCUT`;
- insufficient middle-peak recovery;
- troughs too close together;
- one trough dominated by boundary artifact;
- extremely asymmetric legs;
- excessive internal structural noise;
- wide/loose range;
- incomplete second recovery.

Only the first three above are theory-grounded enough to preregister now. The others remain research/fault candidates pending fixture validation.

## State model — draft

Likely public states:

- `DOUBLE_BOTTOM_RECOGNIZED`
- `DOUBLE_BOTTOM_REJECTED`
- `DOUBLE_BOTTOM_AMBIGUOUS`
- `DOUBLE_BOTTOM_NOT_EVALUABLE`

The exact state policy is not frozen yet.

## PIT rule

P4 may use only structural turns with `confirmed_date <= asof_date`. A W that becomes identifiable only after the second trough or right-side recovery is confirmed must not be reported earlier.

## Non-goals

P4 does not determine:

- breakout execution;
- entry timing;
- the conventional buy-point offset above the middle peak;
- trading returns;
- portfolio allocation;
- CAN SLIM eligibility;
- whether a Double Bottom trade succeeds afterward.

## Immediate next research tasks

1. **P4.2:** formalize a morphology-neutral Double Bottom candidate object and measurable geometry descriptors from the five structural landmarks.
2. Build synthetic positive/negative/ambiguous W fixtures around the audited hard gates before recognition-policy tuning.
3. Preregister research-only bands for trough spacing and middle-peak recovery from morphology stability, never returns.
4. Preserve P1/P2 PIT and boundary semantics throughout.
