# P8 Labelled Morphology Validation — Status

Status: **INFRASTRUCTURE READY / CORPUS BLOCKED**

## What is complete

P8 now has a machine-readable validation contract:

- labels: `POSITIVE`, `NEGATIVE`, `AMBIGUOUS`;
- provenance: `AUTHORITATIVE_SOURCE`, `HUMAN_ANNOTATION`, `ADJUDICATED`;
- corpus split: `DEVELOPMENT`, `VALIDATION`;
- explicit source name/reference, price window and `asof_date`;
- annotator required for human labels;
- duplicate-id and development/validation leakage checks;
- agreement metrics that preserve ambiguity as a first-class outcome;
- exact-agreement, decisive accuracy, ambiguity counts and disagreement ids.

Implementation:

- `src/oneil_patterns/validation/labels.py`
- `src/oneil_patterns/validation/evaluate.py`
- `tests/validation/test_labelled_validation_contract.py`

CI is green.

## Corpus audit

Repository code/content searches did not find a pre-existing independent labelled morphology corpus suitable for P8.

Synthetic fixtures under `tests/fixtures/` are explicitly **not eligible** because they were created from the same detector assumptions and would make validation circular.

No authoritative/human-labelled manifest is currently present for the research-only bands that require external challenge:

- Flat Base tightness / wide-loose;
- Double Bottom undercut magnitude / middle rebound;
- Cup roundedness / bottom continuity / meaningful depth / right-rim recovery;
- Ascending Base pullback consistency;
- Base-on-Base numerical interpretation of “mostly above.”

## Verdict

P8.4 (`run frozen detectors against labelled corpus`) is **BLOCKED_PENDING_INDEPENDENT_LABELLED_CORPUS**.

This is a data/evidence dependency, not a software failure.

The project must not fabricate labels, reuse synthetic fixtures as authoritative evidence, or tune thresholds against post-pattern returns merely to close P8.

## What can continue

P9 productionization may proceed for the current **first-pass / research-labelled** contracts provided outputs preserve:

- detector contract versions;
- normalized fault provenance;
- ambiguity/incomplete states;
- explicit validation status showing research-only parameters remain P8-unvalidated.

Productionization must not describe research-only thresholds as fully validated O'Neil/IBD rules.
