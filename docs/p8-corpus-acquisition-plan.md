# P8 Authoritative Corpus Acquisition Plan

Status: ACTIVE
Date: 2026-09-12

## Objective

Build an independent morphology corpus that can challenge the frozen first-pass detector contracts without circularity and without using post-pattern returns.

Initial target: **30–50 real-world labelled examples**.

## Eligible evidence

Preferred evidence order:

1. explicit pattern labels in official/public IBD or Investor's Business Daily educational/article material;
2. explicit examples from O'Neil-authored or O'Neil-method reference material that can be cited and dated;
3. independent human annotation under a frozen protocol, with annotator identity recorded;
4. adjudicated labels when multiple independent annotations disagree.

Synthetic fixtures generated from detector assumptions are ineligible as authoritative P8 evidence.

## Target pattern coverage

Corpus construction should seek coverage across:

- Flat Base;
- Double Bottom;
- Cup with Handle;
- Cup without Handle / Cup family where authoritative labels permit;
- Ascending Base;
- Base-on-Base;
- explicit malformed / failed / negative examples where an authoritative source clearly identifies the fault.

Do not force equal class counts when authoritative examples are unavailable. Record the coverage gap instead.

## Required record fields

Every example must map to the frozen `LabelEvidence` schema:

- `example_id`;
- `symbol`;
- `pattern`;
- `label`: POSITIVE / NEGATIVE / AMBIGUOUS;
- `window_start`;
- `window_end`;
- `asof_date`;
- provenance: AUTHORITATIVE_SOURCE / HUMAN_ANNOTATION / ADJUDICATED;
- `source_name`;
- `source_reference`;
- optional annotator;
- rationale;
- split: DEVELOPMENT or VALIDATION;
- metadata for source date, quote context, article title, or chart notes.

## Acquisition rules

- Prefer examples where the source explicitly names the pattern rather than inferring the label from an unlabeled chart.
- Preserve the source-reported ticker and historical period.
- Record a conservative structural window around the cited formation; do not optimize the window to make the detector agree.
- If exact start/end dates are uncertain, label the example AMBIGUOUS or preserve a documented windowing rationale.
- Do not inspect detector output before assigning the label or development/validation split.
- Do not use subsequent stock performance to decide whether the morphology label was correct.

## Development / validation split

Recommended initial split after enough examples exist:

- roughly 60–70% DEVELOPMENT;
- roughly 30–40% VALIDATION.

The split is frozen before threshold revision.

Development examples may inform morphology-only revisions of research bands. Final validation examples remain untouched until a revised detector version is frozen.

## First-pass sample-size target

Minimum useful first pass:

- 30 total examples if authoritative supply is limited;
- preferred 50+ total examples;
- aim for at least 5 independent positive examples for each major pattern before drawing pattern-specific threshold conclusions;
- any pattern below that coverage remains `UNRESOLVED`, not validated by extrapolation from another pattern.

## Evaluation outputs

The P8 evaluator should produce at minimum:

- exact agreement rate;
- recognized/rejected/ambiguous confusion counts;
- per-pattern agreement;
- disagreement IDs with source references;
- breakdown by provenance;
- threshold verdict for every research-only band: `KEEP`, `REVISE`, or `UNRESOLVED`.

## Completion rule

P8 may move from `BLOCKED_ON_CORPUS` only when real independent labels have been committed and pass the frozen corpus-validation contract.

P8 may be frozen only after:

1. development examples have been evaluated;
2. any research-only revisions are versioned and justified by morphology agreement;
3. untouched validation examples are evaluated once against the revised frozen version;
4. unresolved low-coverage pattern families are explicitly reported rather than silently treated as validated.
