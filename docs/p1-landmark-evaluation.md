# P1 Landmark Evaluation — Synthetic Morphology Diagnostics

Date: 2026-09-12
Status: RESEARCH DIAGNOSTIC — NOT FROZEN PARAMETER SET

## Purpose

Compare PIT-safe landmark extractors on labelled synthetic morphology fixtures without using downstream returns.

Evaluated candidates:

- percentage excursion (`reversal_pct=0.08`, `min_separation_sessions=2`)
- confirmed window (`confirm_sessions=2`, `min_excursion_pct=0.015`)

These values are research defaults only. They are not promoted detector parameters.

## Labelled fixture corpus

The synthetic corpus currently contains:

- V-shape
- W-shape
- flat/sideways
- rounded cup
- noisy loose range

Expected structural turns are represented as index regions rather than one exact bar where appropriate. Evaluation records:

- matched expected turns
- missed expected turns
- false structural turns
- mean/max absolute landmark-index error for matched turns
- PIT prefix stability separately

## Diagnostic observations under current research defaults

### V-shape

Confirmed-window identifies the central V trough cleanly.

Percentage-excursion identifies the V trough but also emits an initial boundary swing-high because the series begins at a local high and later declines enough to confirm it.

Interpretation: percentage excursion needs explicit candidate-boundary semantics before its first emitted extremum can be treated as a morphology landmark.

### W-shape

Both methods recover the core W interior structure:

- first bottom
- middle peak
- second bottom

Percentage-excursion also emits an initial boundary swing-high. Confirmed-window does not.

Interpretation: both are viable for W interior landmarks, but confirmed-window currently has cleaner precision at the left boundary.

### Flat / sideways

Both research defaults emit no structural turns.

Interpretation: both currently suppress trivial flat-range oscillation adequately on this fixture.

### Rounded cup

Percentage-excursion identifies the central cup trough.

Confirmed-window emits no trough under the current local-prominence threshold because a smooth rounded bottom lacks a sufficiently prominent single local minimum versus its immediate confirmation-window neighbors.

Interpretation: a pure local-prominence detector is structurally unsuitable as the sole landmark source for rounded cup morphology.

### Noisy loose range

Confirmed-window identifies the major central high and major lows with relatively sparse output.

Percentage-excursion identifies some major turns but also produces extra large-amplitude turns and may leave the final trough unconfirmed when the fixture ends before a sufficient reversal occurs.

Interpretation: excursion captures directional structural movement well, but endpoint/boundary treatment and loose-range over-segmentation need explicit controls.

## Current verdict

Do **not** freeze either extractor as the universal landmark engine yet.

The evidence currently supports a layered approach:

1. keep percentage-excursion as a causal structural-movement candidate generator;
2. keep confirmed-window/prominence evidence as a local-extremum quality descriptor;
3. preserve both `price_date` and `confirmed_date`;
4. do not require every valid structural landmark to satisfy local prominence, because rounded cups can have diffuse bottoms;
5. do not automatically trust the first/last excursion landmark when the candidate region starts or ends before the surrounding trend context is known.

A likely next design is a shared landmark-candidate layer where excursion provides candidate turns and independent evidence fields describe local prominence, separation, amplitude, and boundary status. Pattern classifiers can then use morphology-appropriate evidence instead of requiring one universal swing rule.

## Anti-overfitting rule

No parameter may be selected from CAGR, profit factor, win rate, SPY alpha, or later breakout outcomes.

Further parameter work must be justified by:

- labelled morphology agreement;
- false/missed structural turns;
- landmark timing/price error;
- PIT stability;
- robustness across small parameter perturbations;
- theory fidelity.

## Next gate before base segmentation

Implement a reusable `LandmarkCandidate` evidence object with at minimum:

- swing type
- price / price date
- confirmed date
- excursion amplitude
- local prominence evidence
- temporal separation
- boundary flag
- extraction method provenance

Then run the labelled corpus through the evidence-rich representation. If interior structural landmarks remain stable across reasonable parameter perturbations, P1 can be frozen sufficiently to begin P2 base segmentation.
