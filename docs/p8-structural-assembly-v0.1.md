# P8 Structural Candidate Assembly v0.1

Status: **PREREGISTERED DEVELOPMENT REVISION**
Date: 2026-09-13
Contract id: `p8-structural-assembly-v0.1`

## Motivation

Canonical DEVELOPMENT batch 01 showed that the first-pass oneil stack can detect plausible morphology at the wrong structural scale:

- an authoritative six-week Flat Base is truncated into a shorter atomic segment;
- authoritative CWH examples are represented by earlier, unrelated consecutive-landmark cups;
- the authoritative SEI Double Bottom is not represented by a source-aligned W instance;
- AMZN preserves the authoritative pivot landmark but does not emit the authoritative Cup-without-Handle family.

The failure is therefore upstream of threshold adjudication. P8 must first test candidate structures that can span intervening minor, already-confirmed P1 turns.

## Non-goals

This revision does **not**:

- alter P1 landmark extraction or the 8% excursion threshold;
- change Flat Base tightness thresholds;
- change Cup body depth/roundedness bands;
- change handle depth rules;
- change Double Bottom undercut rules;
- use authoritative label dates to choose landmarks at runtime;
- use breakout performance, return, CAGR, PF, FWD1, entry or portfolio outcomes.

## Core principle

A P1 turn is evidence, not necessarily a named-base boundary.

The assembler therefore enumerates multiple candidate structural scales from the same confirmed P1 sequence. It never deletes the smaller-scale interpretation merely because a larger-scale candidate also exists.

All candidate construction is deterministic and uses only landmarks confirmed by the evaluation `asof_date`.

## A. Multi-turn high-low-high spans

For every pair of confirmed `SWING_HIGH` landmarks `H1 < H2`:

1. collect confirmed `SWING_LOW` landmarks whose price dates lie strictly between `H1` and `H2`;
2. if no such low exists, no candidate is emitted;
3. choose the lowest-price intervening low as the structural trough `L`;
4. construct a morphology-neutral `H1 -> L -> H2` candidate using the existing P2 geometry semantics;
5. retain every distinct `(H1, L, H2)` candidate.

This creates a superset of atomic P2 segments. Adjacent high-low-high structures remain present, while larger structures may span intervening minor turns.

There is no label-dependent maximum duration or source-window cutoff. The supplied PIT frame bounds the search horizon.

## B. Cup-family assembly

Each multi-turn `H1 -> L -> H2` span may be assessed by the existing frozen first-pass Cup-body rules.

If the Cup body is recognized:

- `H1` is the left rim;
- `L` is the cup trough;
- `H2` is the right rim.

### Handle candidates

For a recognized cup body, every confirmed `SWING_LOW` after the right rim may start a handle attempt. Its recovery is the first later confirmed `SWING_HIGH`.

Each such low/recovery pair is assessed by the existing handle rules. Multiple handle interpretations may coexist.

### Cup-without-Handle coexistence

A recognized cup body may emit a `CUP_WITHOUT_HANDLE` interpretation once the existing right-edge context-completeness gate is met **even when a handle interpretation also exists**.

This is deliberate. P8 must preserve Cup-family ambiguity rather than suppressing one interpretation merely because another plausible interpretation exists. Downstream conflict/ambiguity evidence may record that overlap.

## C. Multi-turn Double Bottom assembly

For every pair of confirmed `SWING_LOW` landmarks `L1 < L2`:

1. collect confirmed `SWING_HIGH` landmarks strictly between the lows;
2. if none exists, no W candidate is emitted;
3. choose the highest-price intervening high as the middle peak `M`;
4. enumerate every earlier confirmed `SWING_HIGH` `H` before `L1` as a possible structural left high;
5. construct `H -> L1 -> M -> L2` geometry without requiring consecutive landmarks;
6. retain all valid candidates and let the existing Double Bottom assessment classify them.

The strict second-trough undercut rule remains unchanged in this revision.

## D. Determinism and identity

Candidates are sorted deterministically by structural landmark dates/prices. De-duplication uses structural date tuples, never source labels or outcomes.

Adding future bars may add later candidates but must not delete or rewrite a candidate that was already constructible from the earlier confirmed landmark prefix.

## E. P8 acceptance for this revision

This assembler is not accepted because it makes labels pass. It is accepted only if:

1. synthetic tests prove deterministic multi-turn construction and prefix stability;
2. atomic candidates remain representable;
3. no future/unconfirmed landmark enters a candidate;
4. multiple scales coexist rather than one being forced;
5. the five DEVELOPMENT examples can then be re-evaluated using unchanged morphology thresholds;
6. any new agreement/disagreement is interpreted as morphology evidence, not performance evidence.

NFLX VALIDATION remains locked throughout development of this revision.
