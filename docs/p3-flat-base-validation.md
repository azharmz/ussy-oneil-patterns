# P3 Flat Base Validation

Status: synthetic morphology/PIT validation for `flat-base-v0.1`.

## Scope

This validation deliberately excludes trading returns, breakout outcomes, CAGR, win rate, and portfolio behavior. It tests morphology classification behavior only.

## Invariants

### 1. Structural-window PIT stability

`assess_flat_base()` evaluates only bars between the frozen P2 `start_date` and `end_date` of the supplied segment. Appending arbitrary future bars outside that structural window must not change the assessment.

This protects the morphology layer from future-bar contamination after the candidate base has already been structurally defined.

### 2. Clear positive stability

The `textbook_tight` synthetic fixture is intentionally placed well inside the preregistered research tightness band. Uniform price-scale perturbations of +/-0.1% must not change its `RECOGNIZED` state.

### 3. Clear wide/loose stability

The `wide_loose` fixture is intentionally placed well beyond the preregistered wide/loose band. Uniform price-scale perturbations of +/-0.1% must not change its `REJECTED` state.

### 4. Corpus state agreement

Under the current research policy, the synthetic corpus is expected to map as follows:

- `textbook_tight` -> `RECOGNIZED`;
- `too_short` -> `REJECTED`;
- `too_deep` -> `REJECTED`;
- `wide_loose` -> `REJECTED`;
- `borderline_tightness` -> `AMBIGUOUS`.

## Interpretation

Passing this validation is sufficient to close the first synthetic Flat Base morphology pass, but it does **not** establish that the research tightness bands are authoritative O'Neil rules. The 3%/1% tight and 7%/3% wide-loose bands remain research-only until later authoritative/human-labelled morphology validation.

The frozen theory-grounded hard gates remain:

- minimum duration: 25 trading sessions;
- maximum depth: 15%.

## No-return rule

The research bands must not be selected, revised, or justified from downstream trading performance. Any future threshold revision must be based on morphology agreement, labelled examples, or stronger theory evidence.
