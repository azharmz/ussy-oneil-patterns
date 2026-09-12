# P8 Labelled Morphology Validation — Status

Status: **LABELLED CORPUS IN PROGRESS**

## What is complete

P8 has a machine-readable validation contract:

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
- `src/oneil_patterns/validation/corpus.py`
- `tests/validation/test_labelled_validation_contract.py`
- `tests/validation/test_p8_committed_corpus.py`

## Corpus state

The project no longer has zero independent labels.

Committed real-world authoritative corpus seed:

- `data/p8/labels_v0.csv`
- `p8-label-0001`: SNPS Flat Base, DEVELOPMENT;
- `p8-label-0002`: NFLX Cup With Handle, VALIDATION.

Both labels were assigned from authoritative IBD/MarketSurge source evidence and split before detector comparison. The committed CSV passes the frozen `LabelEvidence`/anti-leakage contract in CI.

Reference-first acquisition remains active:

- `data/p8/reference_candidates_v0.csv` contains 31 authoritative candidates;
- `data/p8/adjudication_queue_v0.csv` prioritizes exact-window resolution;
- `docs/p8-adjudication-batch-01.md` records the first promotions and held-back cases;
- `docs/p8-ohlcv-source-policy.md` defines R2 vs external historical data routing.

Synthetic fixtures under `tests/fixtures/` remain explicitly **ineligible** as authoritative P8 evidence because they were created from detector assumptions.

## Current limitation

Two executable labels are sufficient to prove the corpus pipeline is real, but not sufficient for morphology validation or threshold revision.

The remaining research-only bands still require materially broader independent challenge:

- Flat Base tightness / wide-loose;
- Double Bottom undercut magnitude / middle rebound;
- Cup roundedness / bottom continuity / meaningful depth / right-rim recovery;
- Ascending Base pullback consistency;
- Base-on-Base numerical interpretation of “mostly above.”

## Current verdict

P8.4 is now **READY_FOR_DEVELOPMENT-SIDE EXECUTION AS OHLCV IS RESOLVED**, but final labelled validation is not yet eligible to run.

Rules:

- DEVELOPMENT labels may be used for detector disagreement analysis and morphology-only research-band revision;
- VALIDATION labels remain untouched until a revised detector version is frozen;
- no threshold may be tuned against post-pattern returns;
- no synthetic fixture may substitute for independent evidence;
- low-coverage pattern families remain `UNRESOLVED`.

## Completion requirement

P8 may be frozen only after:

1. a materially broader authoritative/human-labelled corpus is committed;
2. source-grounded windows and OHLCV lineage are resolved;
3. DEVELOPMENT examples are evaluated;
4. any research-only revisions are versioned and frozen;
5. untouched VALIDATION examples are evaluated once;
6. coverage gaps are reported explicitly.
