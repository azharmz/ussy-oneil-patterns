# #33 Frozen Core Production Output Contract v2

Status: **FROZEN**

Schema: `oneil-pattern-output-v2`
Engine: `33-core-p8-frozen-v1`
P8 status: `P8_CONDITIONAL_PASS_FROZEN`

Production is a wrapper over the exact canonical P8 prediction adapter. It must not maintain a second detector implementation.

## Scope

The v2 frozen stream contains only the four P8-validated core families:

- `FLAT_BASE`
- `DOUBLE_BOTTOM`
- `CUP_WITHOUT_HANDLE`
- `CUP_WITH_HANDLE`

Advanced families require their own evidence level and are not emitted through this frozen core contract.

## Record fields

Every record carries:

- stable `assessment_id` for one candidate observation at one `asof_date`;
- `candidate_id` from the canonical P8 prediction adapter;
- stable exact-structure `base_id`;
- conservative exact-anchor `lineage_id`;
- `pattern`;
- `normalized_status`: `RECOGNIZED`, `AMBIGUOUS`, or `REJECTED`;
- native frozen detector state;
- `candidate_semantics`;
- pattern-specific `structural_signature`;
- structural start/end;
- pivot source date and pivot level when available;
- morphology depth when available;
- detector faults;
- detector contract version;
- output/engine/P8 validation versions.

## Identity semantics

`base_id` hashes the security, pattern and exact canonical structural signature. Rolling/right-edge observation horizon and candidate semantics do not change the base identity.

`lineage_id` uses conservative exact pattern anchors with no fuzzy date or price tolerance:

- Flat: `LEFT_HIGH`
- Double Bottom: `LEFT_HIGH + TROUGH_1 + MIDDLE_PEAK`
- Cup-without-handle: `LEFT_RIM + CUP_LOW`
- Cup-with-handle: `LEFT_RIM + CUP_LOW`

This intentionally prefers under-merging over unstable fuzzy lineage merges. Later structural evolution may create a new `base_id` while retaining the same exact-anchor lineage.

## Frozen versions

- landmarks: `p1-landmark-v1`
- segmentation: `p2-segmentation-v1+explicit-right-edge-observation`
- Flat: `flat-base-v2`
- Double Bottom: `double-bottom-v3`
- Cup family: `cup-family-v2`
- prediction adapter: `p8-canonical-prediction-adapter-v1.1`
- pivot adapter: `p8-pivot-adapter-v0.2`
- candidate identity audit: `p8-candidate-identity-audit-v0.4`
- production base identity: `core-base-id-v1`
- production lineage: `core-lineage-v1`

## Downstream rule

Consumers must preserve ambiguity and faults. `AMBIGUOUS` must not be silently converted into either `RECOGNIZED` or no-pattern.

No downstream return/performance evidence may mutate this frozen contract or its morphology semantics.
