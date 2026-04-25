---
type: experiment
title: "KV PCA analysis — V2 bf16 vs V2' fp32"
slug: kv-pca-analysis
status: success
started: 2026-04-18
finished: 2026-04-18
hypothesis: "If latents act as routing keys, KV vectors should live in a low-dimensional manifold; bf16's tighter rising-curve performance should correspond to a more compact basin."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/kv_pca_analysis.md
  - research_findings/kv_pca/figures/
  - research_findings/kv_pca/pca_outputs.json
  - research_findings/kv_pca/pca_per_position.json
  - research_findings/kv_pca/pca_centroid_diagnostics.json
  - "script: scripts/kv_pca_analysis.py"
updated: 2026-04-25
---

# KV PCA analysis

## Parent context

Branched off [[phase-1-v2-bf16-training]] (and [[phase-1-v2-fp32-comparator]]) using the local KV dumps from the Phase 1 eval extension. Question: do V2 bf16's "rising-curve" latents and V2' fp32's "flat-curve" latents occupy different KV manifolds, the same manifold at different sub-basins, or the same basin entirely?

## Hypothesis

If latents are routing keys, KV vectors should live in a low-dimensional subspace (small number of PCs explain most variance). bf16's tighter rising curve should correspond to a more compact basin (smaller within-variant RMS radius). Cross-variant comparison should reveal whether bf16 and fp32 differ in basin geometry or only in which sub-basin they occupy.

## Method

- Inputs: 200 examples × 3 benchmarks × 3 num_latent ∈ {2, 4, 8} × 2 variants (V2 bf16, V2' fp32) = 3600 dumps. Each `[num_latent, 2 (k/v), 8 heads, 128 head_dim]` float32.
- Flatten each latent position to 2048-d vector. Per cell `(variant, benchmark, num_latent=8)`: stack 200 examples × 8 positions = 1600 rows × 2048 cols. Compute top-20 PCs (sklearn full SVD).
- Project onto PC1/PC2 in shared basis. Measure within-variant RMS radius, centroid distance, centroid cosine, pairwise distances.
- Per-latent-position diagnostics separately.

## Result

**Headline numbers (num_latent=8):**

| Variant | Benchmark | PC1 | PC1-5 | PC1-10 | PC1-20 |
|---|---|---|---|---|---|
| bf16 | gsm8k | 22.8% | 52.0% | 70.5% | 85.3% |
| bf16 | gsm-hard | 27.0% | 53.0% | 67.5% | 84.0% |
| bf16 | svamp | 27.3% | 54.7% | 71.0% | 85.3% |
| fp32 | gsm8k | 24.3% | 55.6% | 72.3% | 86.1% |
| fp32 | gsm-hard | 31.7% | 56.4% | 70.0% | 85.6% |
| fp32 | svamp | 20.8% | 51.0% | 67.7% | 83.5% |

- **Low-rank confirmed:** ~10 PCs reach ~70% of variance in 2048-d.
- **bf16 basin 9-10% tighter:** within-variant RMS radius bf16 70.8-72.8 vs fp32 76.7-79.6 across all benchmarks.
- **Distinct sub-basins:** centroid-to-centroid distance 40-48 (vs within-radius ~70-80 — clusters overlap but are separable); centroid cosine 0.94-0.96 (same dominant direction, slightly shifted).
- **Per-position structure:** positions 0-1 carry slightly more variation than 2-7 (consistent with F3's step-3 anomaly).
- **Logit lens on top PCs skipped** — required `embed_tokens` / `o_proj` weights not locally available.

## Verdict

**Success — KV manifold characterization.** Both variants live in a low-dim subspace of 2048-d KV space; bf16's basin is materially tighter, supporting the F5 "template keys" framing — the well-performing variant has a tighter template basin. The two variants occupy *distinct sub-basins of the same manifold*. **Reconciles the F5 null-swap result with Christopher's ±10-12% Llama-1B KV-steering effect**: Christopher steered along chosen directions that can leave the template basin; F5 swapped *another example's in-distribution KV* which sits in the same basin and therefore cannot break routing. The two results are compatible.

## Revert info

- Pure analysis on local KV dumps. Reversible by deleting:
  - `research_findings/kv_pca_analysis.md`
  - `research_findings/kv_pca/figures/` (PNGs)
  - `research_findings/kv_pca/pca_outputs.json`, `pca_per_position.json`, `pca_centroid_diagnostics.json`
  - `scripts/kv_pca_analysis.py`
- The KV dumps `research_findings/kv_pca/{variant}/{bench}/numlatent_{n}/kv_example_*.npy` are shared upstream artifacts (also used by [[f5-proxy-cosine]] and [[kv-distance-bf16-vs-fp32]]); preserve unless reverting all three.

## Follow-ups / branch-offs

- Wiki refs: [[concepts/Feature Collapse]] §"KV PCA refinement" (sub-basin capture framing).
- Logit-lens-on-top-PCs is the natural extension once `embed_tokens` is downloaded — would identify which template tokens each PC direction encodes.
- [[kv-distance-bf16-vs-fp32]] — Frobenius-distance variant on the same data.
- Companion proxy at [[f5-proxy-cosine]].
