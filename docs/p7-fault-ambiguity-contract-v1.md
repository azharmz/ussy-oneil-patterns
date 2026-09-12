# P7 Fault / Ambiguity Contract v1

Contract id: `fault-ambiguity-v1`

Status: **FROZEN FIRST PASS**

## Purpose

P7 normalizes states and faults emitted by the frozen morphology detectors without changing their native semantics. It preserves whether a rule is theory-grounded, research-only, or contextual evidence so downstream consumers cannot accidentally promote a research threshold into an O'Neil/IBD rule.

## Shared status vocabulary

- `RECOGNIZED`
- `REJECTED`
- `AMBIGUOUS`
- `INCOMPLETE`
- `NOT_EVALUABLE`

Native state strings are preserved alongside the normalized status.

## Shared fault severity

- `REJECT`: disqualifying under the emitting detector's current contract
- `AMBIGUITY`: caution/uncertainty; not a hard rejection
- `INFO`: non-disqualifying evidence reserved for later use

## Rule provenance

- `THEORY`: sourced first-pass O'Neil/IBD morphology guidance
- `RESEARCH`: numerical/algorithmic morphology translation created for #33 and subject to P8 labelled validation
- `CONTEXT`: boundary/incomplete/context evidence rather than shape theory

## Normalized envelope

Every adapted assessment emits:

- `pattern`
- normalized `status`
- `native_state`
- normalized fault tuple with severity + provenance
- `contract_version`

A normalized `RECOGNIZED` assessment is forbidden from carrying a `REJECT`-severity fault.

## Adapter coverage

P7 provides explicit adapters for:

- Flat Base (`flat-base-v1`)
- Double Bottom (`double-bottom-v1`)
- Cup body (`cup-family-v1`)
- Handle (`cup-family-v1`)
- Cup family (`cup-family-v1`)
- Ascending Base (`ascending-base-v1`)
- Base-on-Base (`advanced-patterns-v1`)

Adapters preserve native fault codes; they do not invent replacement detector judgments.

## Conflict policy

When several normalized assessments refer to the same candidate/context:

1. zero recognized patterns -> `NO_RECOGNIZED_PATTERN`;
2. exactly one recognized pattern -> `CLEAR`;
3. recognized `CUP_BODY` plus exactly one completed recognized Cup family (`CUP_WITH_HANDLE` or `CUP_NO_HANDLE`) -> `HIERARCHICAL`, with the family label as primary;
4. two or more unrelated recognized patterns -> `MULTI_PATTERN_AMBIGUITY`; no arbitrary primary pattern is selected.

Relation-level recognition such as Base-on-Base does not silently override a component morphology. If callers combine relation-level and component-level envelopes in one conflict set, the result remains explicit ambiguity unless a later contract defines a hierarchy.

## Safety invariants

- research-only rules remain labelled `RESEARCH` downstream;
- context faults remain distinguishable from shape rejection;
- native states/fault codes remain recoverable;
- no return/performance information participates in normalization or conflict resolution;
- conflict resolution never ranks unrelated pattern families by trading performance or arbitrary precedence.

## Validation

Synthetic end-to-end adapter tests verify:

- theory rejection remains distinguishable from research ambiguity;
- Cup research morphology faults retain research provenance;
- Cup family non-recognized/incomplete semantics normalize correctly;
- hierarchical Cup body/family recognition is not treated as a contradiction;
- unrelated simultaneous recognized patterns remain unresolved ambiguity;
- Base-on-Base does not silently override a recognized component pattern.

P8 remains responsible for validating research-only morphology thresholds against authoritative/human-labelled examples.
