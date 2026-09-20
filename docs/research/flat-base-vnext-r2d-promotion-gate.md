# Flat Base vNext R2-D — engineering promotion gate

Status: **RESEARCH CANDIDATE ENGINEERING VALIDATED**

Frozen production baseline: `c433cc1e35a5aa32a46f732cd8c5545935e36e40`

Research branch: `research/flat-base-vnext-r2d`

## Contract delta

- Flat Base duration gate becomes >=5 distinct trading weeks instead of >=25 sessions.
- Depth remains <=15%.
- Legacy tight/wide-loose metrics remain diagnostic evidence but do not block recognition after structural gates pass.
- Boundary-context ambiguity remains.
- Open-right-edge Flat uses the same duration/depth semantics.
- No algorithm change to Cup-with-Handle, Cup-without-Handle, Double-Bottom, landmarks, segmentation, or pivot adapters.
- Production output schema remains compatible; morphology evidence version identifies the candidate.

## Validation lineage

Untouched R2-E validation: source-aligned morphology-evaluable NVDA, EME, IBKR = 3/3 recognized under the preregistered R2-D candidate. VEEV remained an upstream pivot/boundary miss and was not morphology-scored.

Final repository regression: Actions run `35516416155`, pytest SUCCESS, 235 tests passed.

IBD source semantics used by the preregistered candidate: Flat Base minimum five weeks and correction no more than 15%.

## Promotion decision

The candidate has passed the research morphology gate, untouched validation gate, and repository regression gate. Promotion is implemented through a reviewed/traceable PR rather than rewriting the frozen baseline history.
