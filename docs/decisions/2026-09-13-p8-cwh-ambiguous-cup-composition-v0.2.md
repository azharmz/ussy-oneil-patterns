# P8 CWH composition from an ambiguous Cup body v0.2

Date: 2026-09-13
Status: DEVELOPMENT REVISION

## Problem

The Cup-body v2 revision deliberately maps research-only roundedness faults such as `SHARP_V` and `FRAGMENTED_BOTTOM` to `CUP_AMBIGUOUS` rather than hard rejection. The canonical CWH prediction adapter, however, still emitted CWH only when the Cup body was fully `CUP_RECOGNIZED`.

That created a semantic contradiction: a research-ambiguous Cup body was treated downstream as if no Cup/CWH candidate existed at all.

## Authoritative DEVELOPMENT evidence

CTSH 2004 is an authoritative Cup-with-Handle example. The source states that the left side began forming in January, the handle formed in July, and the stock broke out past a source-era 26.74 entry. The corpus preserves the source value and explicitly normalizes later split effects to a comparison pivot of 6.685.

Under the v2 Cup-body state mapping, canonical structure contains a January 23 left rim and a CWH candidate with a pivot around 6.66, but the Cup body carries research ambiguity. Suppressing that candidate produced the last source boundary disagreement in the eight-example DEVELOPMENT corpus.

## Revision

For DEVELOPMENT prediction composition:

- a `CUP_REJECTED` body still cannot emit CWH;
- `CUP_RECOGNIZED` + recognized handle may emit `CUP_WITH_HANDLE_RECOGNIZED`;
- `CUP_AMBIGUOUS` + any otherwise evaluable handle emits `CUP_WITH_HANDLE_AMBIGUOUS`;
- any ambiguous handle likewise keeps the family candidate ambiguous;
- Cup-body and handle faults are both persisted in the candidate evidence.

Detector status is not used by the source-dimension evaluator to make the source match. It remains a separate morphology verdict.

## Result

The live DEVELOPMENT rerun changes CTSH from boundary disagreement to source-dimension MATCH using a January 23 candidate and a split-normalized pivot near 6.685. The candidate remains `CUP_WITH_HANDLE_AMBIGUOUS`; no threshold is relaxed and no ambiguous morphology is promoted to recognized.

The eight DEVELOPMENT examples therefore all have source-dimension MATCH after this representation revision.

## Guardrails

No return data, breakout outcome, VALIDATION label, or future evidence was used. NFLX remains locked.
