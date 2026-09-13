# P8 targeted DEVELOPMENT corpus — batch 03

Date: 2026-09-13

## Purpose

Add a source-grounded Flat Base example that directly tests the current SNPS finding without changing detector thresholds.

## Promoted example

### TW — FLAT_BASE — DEVELOPMENT

Authoritative IBD evidence states that Tradeweb Markets hit a record high on 2024-10-15, pulled back, and formed a flat base with a 136.13 buy point. A subsequent IBD article records the breakout from that stage-two flat base on 2024-11-20.

Frozen source dimensions:

- pattern: `FLAT_BASE`
- start anchor: `2024-10-15`
- start precision: `DAY`
- pivot price: `136.13`
- exact source end: intentionally not scored
- exact pivot date: intentionally not scored
- split: `DEVELOPMENT`

The label is valid for morphology comparison as of 2024-11-19, before the later breakout article, because the Nov. 19 source already identifies the flat base and buy point. No post-breakout return/performance information is used.

## Guardrails

- no detector output was used to choose the source start or pivot;
- no exact end boundary is invented;
- no pivot date is inferred merely because the source buy point is close to the prior record high;
- NFLX VALIDATION remains locked;
- this sample is evidence for Flat Base span/acceptance semantics only, not a reason to tune thresholds by itself.
