# P6 Advanced Patterns — DEVELOPMENT Freeze v1

Date: 2026-09-13

Status: **FROZEN BEFORE VALIDATION OPEN**

Scope: `ASCENDING_BASE` and `BASE_ON_BASE` only. This freeze does not reopen or modify frozen P3/P4/P5/P8 core morphology.

## Frozen DEVELOPMENT evidence

Authoritative corpus: `data/p6/labels_v0.csv` DEVELOPMENT split.

Coverage:

- `ASCENDING_BASE`: 5 positive authoritative examples
- `BASE_ON_BASE`: 5 positive authoritative examples
- total DEVELOPMENT examples: 10

Frozen execution:

- evidence commit: `ba13844145095a4bb40f75d9ce477fd61d3aad50`
- workflow run: `34748254127`
- artifact: `p6-authoritative-development`
- artifact id: `10315076061`
- artifact digest: `sha256:332f7fc9aab753280b386491cb59d3a48ad4f258374c7e40b804309eb93425e8`
- repository regression at the same run: **235 tests passed**
- P8 DEVELOPMENT job at the same run: **skipped**

Frozen versions:

- advanced prediction adapter: `p6-advanced-prediction-adapter-v0.3`
- source-dimension evaluator: `p8-source-dimension-eval-v0.5`
- candidate identity audit: `p8-candidate-identity-audit-v0.4`
- source routing: unchanged P8 DEVELOPMENT routing (`R2 -> Yahoo -> Tiingo` on genuine unavailability)

## DEVELOPMENT result

Source-dimension agreement:

```text
result_count                 = 10
MATCH                        = 10
BOUNDARY_DISAGREEMENT        = 0
LANDMARK_DISAGREEMENT        = 0
MORPHOLOGY_DISAGREEMENT      = 0
MISS_PATTERN                 = 0
```

Candidate resolution:

```text
UNIQUE                       = 2
SOURCE_EQUIVALENT_MULTIPLE   = 8
```

Candidate identity audit:

```text
STABLE                       = 5004
STATUS_CONFLICT              = 0
```

Matched presentation-state counts are retained as evidence rather than used to rank source agreement:

```text
ASCENDING_BASE_RECOGNIZED    = 1
ASCENDING_BASE_AMBIGUOUS     = 1
ASCENDING_BASE_REJECTED      = 3
BASE_ON_BASE_RECOGNIZED      = 1
BASE_ON_BASE_AMBIGUOUS       = 4
```

The deterministic candidate selected for presentation is not allowed to prefer `RECOGNIZED` over `AMBIGUOUS` or `REJECTED`. Where multiple candidates are source-equivalent, detector state remains separate evidence.

## Explicit DEVELOPMENT debt

### Ascending Base — TRGP

TRGP is the only authoritative Ascending Base DEVELOPMENT example whose source-equivalent resolution is unique and whose frozen detector state is hard-rejected. The fault is `NON_ASCENDING_TROUGHS`.

The authoritative source row provides pattern identity and a published buy point but does not independently label the full trough sequence. Therefore this example is insufficient evidence to weaken the higher-low morphology rule. Changing the rule from this row would be post-hoc tuning from a thin label and is prohibited.

TRGP is frozen as detector-state validation debt, not as permission to revise the detector after VALIDATION is opened.

### Base-on-Base — qualitative “mostly above” region

Four of five DEVELOPMENT Base-on-Base matches are presented as `AMBIGUOUS`. This is consistent with the conservative source-grounded contract: published guidance permits the second base to be entirely or mostly above the first, but does not provide a universal percentage definition of “mostly.” No numerical overlap/close-fraction threshold is introduced from these examples.

## Locked VALIDATION split

The untouched VALIDATION identities are frozen as:

- `p6-label-0011`
- `p6-label-0012`

They cover the two P6 advanced families. Their source dimensions must not be used to tune P6 after this freeze. The next permitted action is a single one-shot execution of the frozen adapter/evaluator against these rows.

## Freeze rule

After this record:

- `p6-advanced-prediction-adapter-v0.3` is immutable for this validation cycle;
- the P6 source-dimension evaluator settings are immutable;
- candidate ranking must not use detector status or trading outcomes;
- no P6 threshold may be changed from VALIDATION results;
- no return, CAGR, PF, FWD1, breakout success, entry optimization, or portfolio outcome may enter morphology validation;
- P3/P4/P5/P8 core remains frozen and may not be changed from P6 evidence;
- VALIDATION may be opened exactly once, after which the result determines the final P6 verdict for this cycle.
