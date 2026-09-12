# P6 Base-on-Base — Morphology Specification Draft

Status: **DRAFT / THEORY-AUDITED FIRST PASS**

## Audited IBD guidance

Official IBD material describes Base-on-Base as two proper bases stacked closely together:

- the first base breaks out but the stock fails to make the normal ~20–25% advance;
- the stock then forms another consolidation/base on top of the first;
- the later base should form **entirely or mostly above** the first base;
- the later base often finds support near the top of the prior base;
- common first-base families include Cup, Cup-with-Handle and Double Bottom; the second base is often a Flat Base but need not always be;
- the combined structure is treated as one stage until a >20% advance separates later bases into a new stage.

Breakout and stage-counting logic are contextual evidence in #33. Morphology must remain separable from entry execution.

## Structural representation

P6 Base-on-Base composes two already-recognized base regions from frozen morphology layers plus their P2 relation/context.

Let:

- `base_1` = earlier recognized base;
- `base_2` = later recognized base.

Required ordering:

`base_1.start_date < base_1.end_date <= base_2.start_date < base_2.end_date`

Touching or slight structural overlap may be preserved as evidence rather than silently discarded.

## Core morphology descriptors

- gap/touch/overlap sessions between bases;
- second-base low relative to first-base high;
- second-base low relative to first-base start/high;
- fraction/degree by which base 2 sits above base 1;
- base-family pair (`CUP -> FLAT`, `DB -> FLAT`, etc.);
- whether the second base begins near/above the top of base 1;
- combined duration;
- PIT confirmation date = latest confirmation required by the two component bases.

## First-pass interpretation

Theory-grounded concept:

- `base_2` should be **mostly or entirely above** `base_1`.

The audited material does not supply a universal numerical percentage for “mostly above.” Any numeric threshold for this phrase remains research-only and must be morphology-labelled, not return-tuned.

## Planned states

- `BASE_ON_BASE_RECOGNIZED`
- `BASE_ON_BASE_REJECTED`
- `BASE_ON_BASE_AMBIGUOUS`

## Planned faults

Theory/conceptual:

- `SECOND_BASE_NOT_ABOVE_FIRST`
- `REVERSED_OR_INVALID_ORDER`
- `COMPONENT_NOT_RECOGNIZED`

Research-only:

- `SECOND_BASE_ONLY_MARGINAL_ABOVE`
- `EXCESSIVE_GAP`
- `EXCESSIVE_OVERLAP`

## PIT semantics

Base-on-Base may be recognized only after both component bases are themselves PIT-recognized. Later bars cannot retroactively create or backdate the second base.

## Next work

1. Implement relation geometry over two component base summaries.
2. Build clearly stacked, below-first, marginally-above and excessive-gap fixtures.
3. Add detector state/fault policy with the “mostly above” threshold explicitly marked research-only.
4. Validate composition/PIT stability and then freeze P6 advanced patterns.
