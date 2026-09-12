# P9 Production Contract v1

Status: FROZEN FIRST-PASS
Contract: `production-v1`
Project: #33 O'Neil Pattern Detection Research
Date: 2026-09-12

## Verdict

The #33 engine is production-capable as a **first-pass research-labelled morphology engine**.

It is not yet externally validated against an independent authoritative/human-labelled morphology corpus. Every production record and run manifest must therefore preserve `P8_BLOCKED_ON_CORPUS` until P8 is resolved.

This freeze does not claim that research-only numerical morphology bands are canonical O'Neil rules or validated real-world thresholds.

## Production pipeline

The frozen pipeline is:

`R2 ready pointer -> PIT-safe reader -> P1 landmarks -> P2 segmentation -> P3/P4/P5/P6 morphology -> P7 normalized envelope -> production record/manifest`

The canonical upstream source is `azharmz/ussy-data` via `production/ready/current.json`.

The engine receives only rows where `date <= asof_date`. Structural confirmation dates remain separate from structural landmark dates.

## Frozen implementation components

- `src/oneil_patterns/data/r2_ready.py` — canonical R2 ready reader, checksum/schema/manifest validation, PIT cutoff.
- `src/oneil_patterns/production/engine.py` — production morphology orchestrator composing frozen P1-P7 contracts.
- `src/oneil_patterns/production/runner.py` — deterministic per-security batch execution and direct R2 wrapper.
- `src/oneil_patterns/production/output.py` — versioned production records, stable assessment IDs, deterministic JSONL, run manifest.

## Frozen output contract

Output schema version: `oneil-pattern-output-v1`

Engine version: `33-first-pass-v1`

Labelled validation state: `P8_BLOCKED_ON_CORPUS`

Each emitted assessment retains at minimum:

- deterministic `assessment_id`;
- `security_id` and ticker;
- `asof_date`;
- pattern/family;
- normalized status and native detector state;
- structural start/end dates when available;
- confirmation date when available;
- normalized faults with severity and provenance;
- detector contract version;
- engine and output-schema versions;
- labelled-validation status.

Assessment IDs are SHA-256 hashes over semantic identity fields, not random run identifiers.

## Run manifest contract

Every production run records:

- output schema version;
- engine version;
- labelled validation status;
- `asof_date`;
- canonical source-manifest digest when available;
- frozen detector contract versions;
- record count;
- UTC generation timestamp.

The manifest must never omit or silently upgrade the P8 validation state.

## Detector contracts included

- P1 `p1-landmark-v1`
- P2 `p2-segmentation-v1`
- P3 `flat-base-v1`
- P4 `double-bottom-v1`
- P5 `cup-family-v1`
- P6 `advanced-patterns-v1`
- P7 `fault-ambiguity-v1`

## Production safety semantics

- no future bars are available to the engine;
- no backdated confirmations;
- malformed/inapplicable candidate geometry must not abort the whole security batch when it can be safely skipped as non-applicable;
- absence of a confirmed Handle at the right edge does not automatically imply Cup-without-Handle;
- simultaneous unrelated recognized patterns are not silently resolved by arbitrary winner selection;
- research-only faults remain distinguishable from theory-grounded and contextual faults;
- deterministic serialization is stable with respect to input record order.

## Validation debt

P8 remains a mandatory unresolved validation phase.

Research-only parameters requiring independent labelled evidence include at minimum:

- Flat Base tightness / wide-loose bands;
- Double Bottom clear-undercut and middle-rebound bands;
- Cup roundedness, bottom continuity, meaningful-depth and right-rim recovery bands;
- Ascending Base pullback-depth consistency;
- Base-on-Base numerical translation of “mostly above.”

Synthetic fixtures remain regression tests only and do not satisfy P8.

## #33 first-pass verdict

`FIRST_PASS_ENGINE_COMPLETE_WITH_P8_VALIDATION_DEBT`

This means implementation, PIT safety, cross-pattern normalization, deterministic production output, and end-to-end orchestration are complete for the first-pass engine. The remaining scientific task is independent morphology validation, not additional production plumbing.
