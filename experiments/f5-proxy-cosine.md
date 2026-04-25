---
type: experiment
title: "F5 proxy — pairwise cosine similarity of latent KV (N=200)"
slug: f5-proxy-cosine
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "F5's swap-null could be (a) latent KV is identical across examples, or (b) it varies but the variation is downstream-invisible. Cosine similarity disambiguates."
parent: "[[f5-cross-example-kv-swap]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - research_findings/inert_latent_F5_proxy.json
  - "script: latent_eval_training_harness/scripts/f5_proxy_kv_similarity.py"
updated: 2026-04-25
---

# F5 proxy — pairwise cosine similarity of latent KV

## Parent context

Direct child of [[f5-cross-example-kv-swap]]. F5 at N=30 showed swap is null (B accuracy 0.100 → 0.100 under A's KV, 13% prediction change). The proxy answers: is the swap null *because* latent KV is approximately identical across examples (no per-example content), or because per-example variation is downstream-invisible?

## Hypothesis

If A and B's latent KVs are nearly identical (cosine ≈ 1.0), the swap is mechanically a no-op. If cosine is materially below 1.0 yet downstream behavior is unchanged, the per-example KV content is downstream-invisible — supporting the routing-key framing (F5 + F4 + F6 synthesis).

## Method

- Inputs: 200 GSM8k V2 bf16 num_latent=8 final-layer KV dumps from `research_findings/kv_pca/qwen3_4b_codi_bf16_kv_latent_detach_last_2/gsm8k/numlatent_8/kv_example_*.npy`.
- Flatten each example's `[num_latent=8, K/V=2, heads=8, head_dim=128]` → 16384-d vector.
- Compute pairwise cosine over all 200-choose-2 pairs.
- PCA on the 200-example matrix to characterize intrinsic dimension; distance-to-centroid statistics.

## Result

- Median pairwise cosine similarity: **0.78** (p5 = 0.69, p95 = 0.95).
- Top-1 PC explains 23% of variance; top-10 PCs 72%; **63 PCs needed for 95% variance**.
- Mean distance to centroid / mean norm: **0.46**.

## Verdict

**Success — disambiguates F5's swap-null.** Latent KV is NOT identical across examples (median cosine 0.78, not 1.0; 63 significant PCs). There is meaningful per-example variation in the latent KV. But [[f5-cross-example-kv-swap]] showed that variation does not affect the output (13% prediction change, 0% accuracy delta). Conclusion: **the per-example content the latents do carry is downstream-invisible**. This is the cleanest support for the "routing key" framing — the latents have content, but the decoder treats them as a generic prefix.

## Revert info

- Pure analysis. Reversible by deleting `research_findings/inert_latent_F5_proxy.json` and `latent_eval_training_harness/scripts/f5_proxy_kv_similarity.py`.
- The KV dumps themselves (`research_findings/kv_pca/.../kv_example_*.npy`) are shared with [[kv-pca-analysis]] and [[kv-distance-bf16-vs-fp32]] — do not delete unless those follow-ups are also being reverted.

## Follow-ups / branch-offs

- [[kv-pca-analysis]] — full PCA / centroid / sub-basin analysis on the same dumps × 3 benchmarks × 3 num_latent × 2 variants.
- Reconciliation with Christopher's ±10-12% Llama-1B KV-steering: F5 is in-basin (in-distribution swap), Christopher's perturbations may be off-basin (chosen directions). Discussed in [[kv-pca-analysis]] §4.
