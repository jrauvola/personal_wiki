---
type: experiment
title: "KV-distance analysis — V2 bf16 vs V2' fp32 (Frobenius)"
slug: kv-distance-bf16-vs-fp32
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "If the two variants' divergent answer distributions come from KV content differences, bf16-right/fp32-wrong cells should have larger KV distances than both-right or both-wrong cells."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/kv_distance_bf16_vs_fp32_analysis.md
  - research_findings/kv_distance_bf16_vs_fp32.json
  - "script: latent_eval_training_harness/scripts/kv_distance_bf16_vs_fp32.py"
updated: 2026-04-25
---

# KV-distance analysis — bf16 vs fp32

## Parent context

Branched off [[phase-1-v2-bf16-training]] / [[phase-1-v2-fp32-comparator]]. After the latent-trace comparison showed both variants produce near-identical templated traces under logit lens, the question becomes: are the underlying final-layer KVs near-identical (routing-attractor story) or substantively different (with the divergence absorbed by `lm_head`)?

## Hypothesis

Compute `||KV_bf16 - KV_fp32||_F / mean(||KV||_F)` between dumped final-layer KVs at latent positions, 200 matched examples per `(benchmark, num_latent)`. If bf16-right/fp32-wrong cases have substantially larger KV distances than both-right or both-wrong, KV content is the outcome discriminator (real per-example reasoning content). If distances don't separate by outcome, the routing-attractor story is supported.

## Method

- Inputs: same KV dumps as [[kv-pca-analysis]] (3600 cells, 200 examples each).
- Compute per-example relative Frobenius distance between bf16 and fp32 versions of the same example_id.
- Split by prediction outcome: both-right / both-wrong / bf16-right-fp32-wrong / fp32-right-bf16-wrong.

## Result

| Benchmark | num_latent | n | rel_dist_mean | rel_dist_median | p10-p90 |
|---|---|---|---|---|---|
| gsm8k | 2 | 200 | 0.600 | 0.672 | 0.339-0.819 |
| gsm8k | 4 | 200 | 0.610 | 0.686 | 0.387-0.799 |
| gsm8k | 8 | 200 | 0.628 | 0.701 | 0.415-0.772 |
| gsm-hard | 8 | 200 | 0.594 | 0.709 | 0.249-0.788 |
| svamp | 8 | 200 | 0.698 | 0.735 | 0.481-0.797 |

Mean relative distances 0.58-0.70 — not near-identical (<0.3) and not orthogonal (~1.4). Meaningful content divergence with shared structure.

Outcome-conditional (GSM8k n=4):
- bf16-right / fp32-wrong: 0.627 (n=14)
- both-right: 0.537 (n=30)
- both-wrong: 0.621 (n=146)

**bf16-right/fp32-wrong does NOT dominate both-wrong.** Both-right has smaller distances than both-wrong (easy problems compress to similar states across precisions), but the outcome discriminator pattern predicted by the "KV content drives the answer" hypothesis is absent.

## Verdict

**Success — weak-to-moderate support for routing-attractor.** The final-layer latent KV differs meaningfully between variants (0.6 mean relative distance), but the difference does NOT cleanly correlate with which variant gets the answer right. Consistent with "decoder attractor downstream does the work." Caveats: only FINAL-layer KV is dumped (downstream attention reads all layers); 0.6 mean distance leaves room for KV content to carry real information that this analysis doesn't rule out. Decisive next test would be live cross-injection (inject bf16's KV into fp32's forward) — ~3-4 hrs coding + inference.

## Revert info

- Pure analysis. Reversible by deleting:
  - `research_findings/kv_distance_bf16_vs_fp32_analysis.md`
  - `research_findings/kv_distance_bf16_vs_fp32.json`
  - `latent_eval_training_harness/scripts/kv_distance_bf16_vs_fp32.py`
- KV dumps shared upstream — preserve.

## Follow-ups / branch-offs

- Live cross-injection (inject bf16's latent-position KV into fp32's forward pass) — designated decisive test for the routing-attractor hypothesis. Not yet run.
- [[kv-pca-analysis]] — fuller manifold characterization on the same data.
