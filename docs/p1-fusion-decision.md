# P1 Landmark Fusion Decision

Status: FROZEN FOR P1 pending CI verification

## Decision

P1 does **not** use a naive union of all extrema from multiple extractors.

The frozen architectural direction is:

1. **Primary structural-turn source:** causal percentage-excursion landmarks.
2. **Auxiliary evidence source:** confirmed-window/local-prominence landmarks.
3. **Candidate creation:** only primary turns create `LandmarkCandidate` records.
4. **Corroboration:** a nearby auxiliary turn of the same type may attach prominence/corroboration evidence to the primary candidate.
5. **Boundary handling:** boundary status remains explicit evidence and is never silently discarded.
6. **Pattern semantics:** no P1 component assigns `LEFT_PEAK`, `TROUGH_1`, `MIDDLE_PEAK`, etc.; those meanings belong to later morphology layers.

## Why not a multi-scale union?

Synthetic diagnostics showed complementary behavior: the local-window method is cleaner on several sharp/noisy fixtures, while excursion is better at retaining diffuse rounded-cup structure. A raw union would therefore increase candidate density and ambiguity without establishing which extrema should drive segmentation.

Using excursion as the structural source preserves a causal alternating skeleton. Local prominence remains valuable, but as evidence rather than an independent source of new structural turns.

## What this does not mean

This is not a claim that percentage excursion is universally superior. It is a contract choice for P1/P2 architecture based on morphology stability and PIT behavior only. No trading return, breakout success, CAGR, win rate, or portfolio outcome was used.

## Handoff to P2

P2 candidate-base segmentation should consume `LandmarkCandidate` objects produced under this fusion policy. It may use:

- swing type;
- price/price date;
- confirmed date;
- excursion amplitude;
- prominence corroboration;
- temporal separation;
- boundary status;
- method provenance.

P2 must not regenerate an independent swing vocabulary unless the P1 contract is explicitly revised and versioned.
