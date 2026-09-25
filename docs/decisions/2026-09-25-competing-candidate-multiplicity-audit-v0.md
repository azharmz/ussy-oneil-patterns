# Research-only competing-candidate multiplicity audit

Date: 2026-09-25
Status: EVIDENCE ONLY — NO PRODUCTION SEMANTICS CHANGE

## Question

Does the frozen P8 DEVELOPMENT evidence establish only authoritative recall/source-dimension agreement, or does it also control the number of competing morphology candidates emitted around those examples?

## Frozen evidence inspected

This audit reuses the immutable P8 DEVELOPMENT freeze artifact from workflow run `34740880269` / evidence commit `2ed3dadcc354f56f4cb27401248daef60b1627fa`. It does not rerun morphology and does not open or retune the NFLX validation holdout.

The freeze contains 20 authoritative DEVELOPMENT positives and records all same-pattern predictions, structural signatures, detector states and identity diagnostics.

## Result

Across the 20 DEVELOPMENT examples there are **276 RECOGNIZED same-pattern predictions**. **14/20 examples emit more than one RECOGNIZED same-pattern prediction** in their evaluation context.

This does not mean 276 false positives. It means the freeze criterion did not establish one-to-one structural specificity.

### CWH multiplicity

| Symbol | RECOGNIZED CWH | distinct LEFT_RIM | distinct CUP_LOW | distinct RIGHT_RIM | distinct HANDLE_LOW | frozen lineage groups (LEFT_RIM+CUP_LOW) |
|---|---:|---:|---:|---:|---:|---:|
| CTSH | 56 | 5 | 5 | 9 | 10 | 5 |
| FOUR | 85 | 8 | 4 | 7 | 7 | 9 |
| APH | 2 | 1 | 1 | 1 | 2 | 1 |
| NVDA | 16 | 2 | 1 | 5 | 4 | 2 |
| BAC | 0 | 0 | 0 | 0 | 0 | 0 |

Within a frozen CWH lineage (LEFT_RIM + CUP_LOW), multiple exact bases can remain RECOGNIZED as RIGHT_RIM and HANDLE_LOW evolve. CTSH lineage sizes are 22, 19, 11, 3, 1. FOUR lineage sizes are 19, 19, 19, 7, 7, 7, 5, 1, 1. NVDA has two lineages with 8 recognized exact structures each.

### Other core families

Recognized multiplicity is also present outside CWH:
- CWOH: AMZN 7, INTC 25, ARW 2, AMD 15, SE 13.
- Double Bottom: SEI 8, NVDA 11, SPOT 2, WMT 19, EMBJ 15.
- Frozen DEVELOPMENT Flat Base examples have zero RECOGNIZED predictions in this artifact; source-dimension MATCH and detector acceptance are intentionally separate.

## Interpretation

The frozen P8 result `20/20 source-dimension MATCH` establishes that a source-compatible structural representation exists under the frozen evaluator. Zero identity `STATUS_CONFLICT` establishes deterministic/coherent candidate identity under that audit.

Neither criterion establishes:
1. one authoritative source pattern maps to exactly one RECOGNIZED detector structure;
2. competing RECOGNIZED candidates are all independent valid bases;
3. a later/internal LEFT_RIM supersedes or is dominated by an earlier LEFT_RIM;
4. RIGHT_RIM/HANDLE evolution represents a new base rather than a new observation/state of an existing setup.

Therefore the current evidence supports a **candidate-multiplicity / structural-specificity validation debt**. It does not by itself justify deleting, merging, ranking, or suppressing candidates.

## Layer diagnosis

Do not repair this in `stable_base_id()` or `stable_lineage_id()`. Those functions are behaving according to their frozen contracts:
- exact structural changes -> distinct `base_id`;
- CWH lineage anchors -> `LEFT_RIM + CUP_LOW`.

The multiplicity originates upstream in candidate construction/morphology and is faithfully preserved by identity.

## Next research contract

Before any production change, define and evaluate a research-only competing-candidate relation. Candidate comparisons should be explicit and auditable, at minimum separating:

- LEFT_RIM variation with shared CUP_LOW;
- CUP_LOW variation;
- RIGHT_RIM evolution within a frozen lineage;
- HANDLE_LOW evolution within a frozen lineage;
- overlapping candidates with different lineage anchors.

No arbitrary "primary base", fuzzy merge tolerance, price-zone threshold, or detector threshold is approved by this audit.

A candidate dominance/supersession rule may be proposed only after it is preregistered and tested against authoritative DEVELOPMENT evidence without using breakout returns/performance. The locked validation evidence must not be used for tuning.

## Downstream implication for ussy-pattbreak

Until such semantics are validated, multiple `base_id` / `lineage_id` contributors to one economic breakout should be exposed as provenance/competing structural interpretations, not presented as though each is automatically a distinct visually validated O'Neil base and not silently deduplicated.
