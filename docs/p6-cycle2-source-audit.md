# P6 Validation Cycle 2 — Authoritative Source Audit

Date: 2026-09-13

## Purpose

Cycle 2 exists because Cycle 1 failed independent morphology recognition. It is a new versioned research cycle, not a rewrite of Cycle 1. STT and Citigroup are consumed evidence and are not reused as untouched validation. Frozen P3/P4/P5/P8 core is out of scope.

## Authoritative morphology rules recovered

### ASCENDING_BASE

IBD/MarketSurge guidance is materially specific:

- three pullbacks;
- each successive pullback produces higher highs and higher lows;
- typical duration 9–16 weeks;
- current MarketSurge guidance permits roughly 6%–25% pullback depth, while older/textbook IBD material commonly describes 10%–20%;
- buy point is the high of the entire pattern / breakout after the third pullback.

Cycle 2 therefore does not invent a dispersion threshold or a fourth mandatory recovery swing. Pattern identity must be judged from the three-pullback staircase itself.

New DEVELOPMENT positives locked before scoring: AVGO, TME, CCJ, SNOW, NAVN.

Untouched VALIDATION locked before scoring: MRX.

### BASE_ON_BASE

IBD/O'Neil guidance recovered in Cycle 2 is stronger than the old overlap heuristic:

- a proper first base breaks out;
- the stock advances less than the normal ~20%–25% before another consolidation begins;
- the later base forms on top of the prior base and usually finds support around the top of the prior base;
- current IBD wording says the second base should form entirely or mostly above the first;
- the buy point is derived from the second/current base;
- a base-on-base counts as one stage.

This evidence directly rejects the old assumption that only `second_base.low >= first_base.high` can be recognized. However, the sources still do **not** publish a universal numeric percentage for `mostly above` or a numeric tolerance around `support at the top of prior base`. Cycle 2 must not manufacture one from validation outcomes.

New DEVELOPMENT positives locked before scoring: META, TRV, SE, JLL, SEI.

Untouched VALIDATION locked before scoring: CAT.

## Source set

The locked corpus is `data/p6/labels_cycle2_v0.csv`. Sources are IBD, MarketSurge-attributed IBD articles, and official IBD educational material. Examples are disjoint from the consumed Cycle 1 VALIDATION rows.

## Validation discipline

1. Score DEVELOPMENT only.
2. Any P6-only assembly change must be justified by general source morphology plus DEVELOPMENT evidence, never MRX/CAT.
3. Freeze code, corpus, versions and DEVELOPMENT evidence.
4. Open MRX/CAT once.
5. Do not retune after opening VALIDATION.
6. If authoritative evidence remains insufficient to resolve a morphology decision without an invented numeric rule, stop with `NOT QUANTIFIABLE WITH AVAILABLE AUTHORITATIVE EVIDENCE` rather than optimize a threshold.
7. Trading returns, breakout performance, CAGR, PF, FWD1 and entry outcomes are prohibited evidence.

## Evidence limitation to watch

The principal unresolved dimension is Base-on-Base vertical overlap. Authoritative wording establishes `entirely or mostly above` and `support at the top of prior base`, but not a machine threshold for `mostly`. A defensible implementation may use categorical structural evidence already supplied by constituent base/pivot geometry, but it may not infer a percentage cutoff from CAT or any other untouched validation row.
