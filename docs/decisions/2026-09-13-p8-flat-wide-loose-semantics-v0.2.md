# P8 decision — Flat Base `WIDE_LOOSE` state semantics v0.2

Date: 2026-09-13
Decision: **REVISE** state mapping; keep numeric research bands unchanged.

## Independent DEVELOPMENT evidence

Two authoritative Flat Base examples now have source-aligned right-edge observations:

- SNPS 2023: start 2023-04-04 and pivot 392.79 match the IBD source; once the observation is extended through the source as-of date, the 25-session duration gate passes and the only remaining detector fault is `WIDE_LOOSE`.
- TW 2024: start 2024-10-15 and pivot 136.13 match the IBD source; the open-right-edge candidate likewise passes the hard duration/depth gates and the only remaining detector fault is `WIDE_LOOSE`.

The `WIDE_LOOSE` numerical band was explicitly preregistered as research-only, not as an official O'Neil/IBD hard rule. The two independent source-labelled examples therefore contradict the v0.1 policy that automatically maps this research-only band to hard `REJECTED`.

## Revision

Do **not** move the numeric thresholds to fit these examples.

Instead revise state semantics:

- duration < 25 sessions -> `REJECTED`;
- depth > 15% -> `REJECTED`;
- hard gates pass + `WIDE_LOOSE` research-band fault -> `AMBIGUOUS`;
- hard gates pass + boundary context -> `AMBIGUOUS`;
- hard gates pass + tight research band -> `RECOGNIZED`;
- hard gates pass + intermediate tightness -> `AMBIGUOUS`.

`WIDE_LOOSE` remains persisted as a fault/evidence flag. The change is only that a research-only morphology band no longer overrides source-supported hard gates as a hard rejection.

## Why this is conservative

This revision does not promote SNPS or TW to clean `RECOGNIZED`; both remain explicitly ambiguous. It therefore preserves uncertainty while avoiding a false claim that a non-official research threshold can invalidate independently labelled Flat Bases.

Synthetic wide/loose fixtures remain regression evidence for the fault flag, but are no longer authoritative evidence for a hard rejection state.

## Scope

- Flat Base only.
- DEVELOPMENT only during P8 adjudication.
- No return/performance information used.
- Numeric duration/depth/tightness bands unchanged.
- NFLX VALIDATION untouched.

## Versioning

Implementation evidence version becomes `flat-base-v0.2`. The first-pass `flat-base-v1` contract is superseded for P8 DEVELOPMENT by a versioned P8 revision document; production promotion remains pending final P8 freeze.
