---
type: experiment
title: "Phase 1 — V2' fp32 comparator (mirror of V2 bf16)"
slug: phase-1-v2-fp32-comparator
status: partial
started: 2026-04-19
finished: 2026-04-19
hypothesis: "Same V2 recipe (cache+latent detach, keep_last_2) at fp32 should match bf16 capability if the bf16 variant is genuinely benefiting from precision-related quirk."
parent: "root"
artifacts:
  - research_findings/qwen3_chain_results.md
  - research_findings/latent_trace_bf16_vs_fp32_comparison.md
  - "HF: jrauvola/qwen3-4b-codi-fp32-kv-latent-detach-last-2 (target)"
updated: 2026-04-25
---

# Phase 1 — V2' fp32 comparator

## Parent context

Sibling of [[phase-1-v2-bf16-training]] in the 7-variant Qwen3-4B chain. Designed as a precision control: same recipe (cache+latent detach, keep_last_2), only `bf16: false`. Question: is the V2 bf16 rising num_latent curve a precision-specific phenomenon, or recipe-driven?

## Hypothesis

If the rising num_latent curve is a recipe effect (V2 detach is the load-bearing part), V2' fp32 should also rise. If it is precision-coupled (bf16 induces a particular numerical regime that the rising curve depends on), V2' fp32 will be flat. Either outcome is interpretable.

## Method

- Model: Qwen3-4B-Instruct-2507, LoRA r=128 α=32, fp32 (`bf16: false`).
- Recipe: V2 cache+latent step-boundary detach, `keep_last_2`. Otherwise identical to V2 bf16.
- Same dataset mix (`gsm8k_aug + numinamath_15`), 5299 steps.
- Compute: GH200, ~8.6h wall.

## Result

- Training: clean, 2026-04-19T06:00Z → 2026-04-19T14:45Z, exit=0.
- Phase 1 eval (V2' fp32, num_latent=0/2/4/8):
  - GSM8k: 0.152 / 0.145 / 0.160 / 0.154 — **flat**
  - gsm-hard: 0.050 / 0.049 / 0.053 / 0.054 — flat
  - SVAMP: 0.307 / 0.290 / 0.293 / 0.303 — flat
- Latent-trace comparison (`latent_trace_bf16_vs_fp32_comparison.md`): both variants collapse to the same template `word → digit → digit → digit → . → . → . → .`; top-10 sets overlap ~74%. **Key per-step difference:** bf16's digit attractor is `0`, fp32's is `2`. bf16 answer-digit distribution matches GSM8k target distribution (`0:30%, 1:17%, 2:14%`), fp32 leaks mass to wrong digits.
- KV PCA analysis: V2 bf16 within-variant RMS radius 70.8-72.8 vs fp32 76.7-79.6 (bf16 9-10% tighter). Centroid cosine 0.94-0.96, centroid-to-centroid distance 40-48 — **distinct sub-basins of the same manifold**.

## Verdict

**Partial / inconclusive.** The mechanism behind bf16's rising curve and fp32's flat curve at the same recipe is not understood. Both variants produce identical templated traces under logit lens; bf16's downstream digit distribution happens to align with target distribution, fp32's does not. Possible explanations (none directly tested): (a) bf16's restricted dynamic range nudges KV into a tighter basin that the decoder reads as "GSM8k-shaped", (b) random seed-style stochasticity that happens to favor bf16's attractor on these benchmarks, (c) genuine precision-coupled inductive bias. Cross-precision divergence remains an open scientific question; not on the critical path for the routing-mode characterization.

## Revert info

- Code: `feature/detach-variants` (same branch as V2 bf16). No code-level differences from V2 bf16 — only the config flag `bf16: false`.
- Config: `latent_eval_training_harness/configs/training/qwen3_4b_codi_gh200_v2_keep_last_2_fp32.yaml`.
- Checkpoint: local-only at present (not yet pushed to HF). Local artifact dirs under `latent_eval_training_harness/runs/qwen3_4b_codi_fp32_kv_latent_detach_last_2/`.
- To revert: not needed — this is a sibling baseline, leave in place.

## Follow-ups / branch-offs

- [[kv-pca-analysis]] (compares bf16 vs fp32 KV manifolds; informs the routing-attractor reconciliation)
- [[kv-distance-bf16-vs-fp32]] (Frobenius-distance between matched cells)
- Cross-precision mechanism is not under active investigation; logged as open question in [[meta/state-of-project-2026-04-23]].
