# P8 DEVELOPMENT morphology audit v0

Date: 2026-09-13
Scope: canonical `ussy-oneil-patterns` DEVELOPMENT-only morphology validation.

## Guardrails

- NFLX VALIDATION remains locked and untouched.
- No return, CAGR, PF, FWD1, breakout-performance, or entry optimization evidence is used.
- Authoritative source dimensions remain immutable and are compared only at their published precision.
- Detector thresholds are not changed from a single example.

## Canonical batch state

Evaluator: `p8-source-dimension-eval-v0.2`.

Current DEVELOPMENT labels:

- SNPS / FLAT_BASE -> source-dimension `MATCH`, detector status `FLAT_BASE_REJECTED`.
- CTSH / CUP_WITH_HANDLE -> `BOUNDARY_DISAGREEMENT`, detector status `CUP_WITH_HANDLE_RECOGNIZED`.
- FOUR / CUP_WITH_HANDLE -> `LANDMARK_DISAGREEMENT`, detector status `CUP_WITH_HANDLE_RECOGNIZED`.
- SEI / DOUBLE_BOTTOM -> source-dimension `MATCH`, detector status `DOUBLE_BOTTOM_REJECTED`.
- AMZN / CUP_WITHOUT_HANDLE -> `BOUNDARY_DISAGREEMENT`, detector status `CUP_WITHOUT_HANDLE_RECOGNIZED`.

## Case audit

### SNPS Flat Base

The source start (2023-04-04) and source pivot (392.79) match the canonical candidate exactly. The candidate is still rejected because the structural span emitted by P2 ends 2023-04-25 and therefore trips both `TOO_SHORT` and research-only `WIDE_LOOSE` under `flat-base-v0.1`.

Interpretation: source agreement is real, but raw detector acceptance cannot yet be promoted. The six-week source description and the shorter P2 structural span are not the same boundary object. This is primarily a segmentation/boundary representation issue before it is a Flat Base threshold issue.

Verdict: `UNRESOLVED` for Flat Base acceptance semantics. Do not relax duration or wide/loose bands from SNPS alone.

### CTSH Cup-with-Handle

The source identifies a base beginning in January 2004 and an adjusted comparison pivot of 6.685. Canonical CWH candidates reproduce the pivot closely: 6.66 is within ~0.37%, and recognized candidates exist. However, candidate starts remain in 2003; none start in January 2004.

Interpretation: this is not a pivot or corporate-action problem anymore. The remaining disagreement is the meaning of the source phrase that the left side "began taking shape in January" versus the canonical landmark-first cup start. The detector can recognize a valid CWH and its pivot, but its left-rim/start semantics are materially earlier.

Verdict: `UNRESOLVED` boundary semantics. No CWH threshold change.

### FOUR Cup-with-Handle

The source month-level start February 2024 is represented canonically by candidates beginning 2024-02-12, so boundary agreement is good. Those candidates, however, use handle-high/pivot values around 72.43-75.28 rather than the published 84.26. Other canonical candidates have pivots near 84.90 but start much earlier (2023-08-31) and are ambiguous.

Interpretation: the detector has the right family and a source-consistent base start, but the persisted handle/pivot role for that span is not the source buy point. This is a landmark/pivot-role disagreement, not a reason to move the authoritative pivot.

Verdict: `UNRESOLVED` CWH handle/pivot landmark selection. No detector threshold change.

### SEI Double Bottom

The source month-level late-July start and 12.74 pivot are matched essentially exactly by a canonical candidate beginning 2024-07-30 with pivot 12.74. That candidate is rejected only because the core W duration is below the current 35-session theory gate (`TOO_SHORT`).

Other longer canonical W candidates are often rejected because the second trough does not undercut the first. The source-labelled late-July structure therefore provides evidence against treating every disagreement as a missing-pattern problem, but one example is insufficient to revise either the duration gate or undercut semantics.

Verdict: `UNRESOLVED` Double Bottom duration/undercut semantics. Keep current rule pending more authoritative examples.

### AMZN Cup-without-Handle

The source says the relevant base began in September 2023 with a 145.86 buy point. Canonical Cup diagnostics do contain the 145.86 landmark on 2023-09-14 and recognize multiple cup bodies, but emitted Cup-without-Handle candidates use earlier left rims (2023-02-02 or 2023-04-27) and therefore pivots around 114.00 or 110.86.

A local span beginning 2023-09-14 is diagnosed as too short when paired only with the next confirmed right-rim landmark available to the current landmark-first sequence. Thus the canonical stack sees a valid cup family in the broader history but does not segment the source-described September-November base as its own eligible Cup-without-Handle candidate.

Interpretation: strongest current evidence points to segmentation / right-edge landmark availability and candidate-span construction, not to the cup-shape research bands themselves.

Verdict: `UNRESOLVED` segmentation/candidate-span semantics. Do not change cup thresholds.

## Cross-case conclusions

1. Source-dimension `MATCH` must remain separate from detector `RECOGNIZED` / `AMBIGUOUS` / `REJECTED`.
2. No current DEVELOPMENT example justifies a morphology threshold change by itself.
3. Highest-priority follow-up evidence is targeted authoritative DEVELOPMENT coverage for:
   - Flat Base examples with explicit duration/start/pivot to test P2 span fragmentation;
   - Double Bottom examples that distinguish duration and second-trough-undercut semantics;
   - CWH examples with explicit base start plus buy point to test handle-high/pivot role selection;
   - Cup-without-Handle examples with explicit start plus pivot to test right-edge segmentation.
4. BaseIdentity/Lineage remain unfrozen until underlying candidate-span churn is acceptable.
5. NFLX stays locked until DEVELOPMENT semantics are frozen.

## Current decision

P8 detector semantics remain `NOT_FROZEN`.

All five current examples are retained as valid DEVELOPMENT evidence. The next slice is targeted corpus expansion plus diagnostic comparison, not threshold tuning.
