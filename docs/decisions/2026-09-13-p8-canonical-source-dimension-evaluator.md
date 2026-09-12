# P8 canonical source-dimension evaluator

Date: 2026-09-13

Status: IMPLEMENTED ON DEVELOPMENT BRANCH

## Decision

`ussy-oneil-patterns` now owns the authoritative source-dimension comparison semantics for #33/P8.

The evaluator compares only facts actually published by the source:

- named pattern;
- source start anchor at its declared precision (`DAY` or `MONTH`);
- optional end anchor;
- optional pivot date;
- optional pivot price;
- explicit corporate-action comparison factor when required.

Missing source dimensions are not failures and are not invented.

The evaluator is DEVELOPMENT-only. A VALIDATION label raises before comparison, preserving the NFLX lock.

## Prediction boundary

The evaluator consumes a small canonical `MorphologyPrediction` adapter rather than importing the superseded CAN SLIM parent detector/identity/lineage implementation.

A prediction may carry:

- detector-emitted pattern;
- detector-emitted start/end facts;
- detector-emitted pivot date/price when the canonical detector exposes them;
- detector ambiguity/status independently from source-dimension agreement.

Therefore `MATCH` means that the detector-emitted candidate agrees with all source-published dimensions. It does **not** mean that the detector is unambiguous.

## Corporate actions

Authoritative source prices remain immutable. `pivot_price_adjustment_factor` changes only the comparison basis.

For CTSH, source pivot `26.74` and factor `4` yield comparison level `6.685`; the stored source price remains `26.74`.

## Important blocker discovered

The canonical first-pass production record currently preserves pattern/status/start/end/confirmation/faults, but does not yet expose a generic pattern-specific pivot date/price field. P3/P4/P5 native geometry likewise has different pivot semantics and must not be guessed in the evaluator.

Next work is therefore to add a **canonical detector-to-validation adapter** that derives/persists pattern-specific pivot facts from existing native structures under a versioned contract. This must be theory/morphology driven and must not be altered merely to reproduce parent-side `5 MATCH / 5 AMBIGUOUS` migration evidence.

## Guardrails

- no performance/return/CAGR/PF/FWD1 inputs;
- no VALIDATION inspection;
- no source precision invention;
- no label-derived detector facts;
- ambiguity retained separately;
- no CAN SLIM parent detector code imported.
