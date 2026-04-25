---
type: experiment
title: "Phase 1 — V2 bf16 step-boundary detach training (Qwen3-4B-Instruct-2507)"
slug: phase-1-v2-bf16-training
status: success
started: 2026-04-18
finished: 2026-04-19
hypothesis: "Step-boundary KV+latent detach with keep_last_2 is the minimum recipe for stable bf16 LoRA CODI training at 4B scale."
parent: "root"
artifacts:
  - research_findings/qwen3_chain_results.md
  - research_findings/dgrad_probe/qwen3_4b_v2_stable_100steps/dgrad_per_layer.csv
  - "HF: jrauvola/qwen3-4b-codi-bf16-kv-latent-detach-last-2"
  - "branch: feature/detach-variants @ 9e418a6"
updated: 2026-04-25
---

# Phase 1 — V2 bf16 step-boundary detach training

## Parent context

Root experiment for the Phase 1 / Branch B detach-ablation track. Predecessors: Gemma-3 March 2026 stability struggles (Probe A-E) and Phase 0 fp32-no-detach control (Apr 17). Motivating question: is there *any* bf16 LoRA recipe that survives at 4B+ CODI without Q/K-RMSNorm?

## Hypothesis

Cache+latent step-boundary detach with `keep_last_2` shortens the backward graph enough to keep early-layer LoRA `lora_A` weights below bf16's overflow threshold. The 2026-04-18 dgrad probe on Qwen3-4B established that the bf16 NaN crash on `model.layers.0.self_attn.q_proj.lora_A.default.weight` is universal at 4B+ (4 independent reproductions across Gemma-3 and Qwen3) — Q/K RMSNorm hypothesis falsified. V2 detach should flatten the dgrad profile and survive.

## Method

- Model: Qwen3-4B-Instruct-2507. LoRA r=128 α=32 over `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`.
- Recipe: bf16, V2 step-boundary KV+latent detach, `keep_last_2`.
- Datasets: `gsm8k_aug + numinamath_15` mix, 5299 steps.
- Compute: GH200, single GPU, ~10.6h wall.
- Sibling 7-variant chain (P0/V2/V3/V4 in bf16+fp32) ran in parallel for stability matrix.
- Per-layer max-abs-dgrad probe at 100 steps.

## Result

- **Trained clean:** 5299 steps, exit=0, 2026-04-18T19:22Z → 2026-04-19T06:00Z (~10.6h).
- **Stability matrix (7-variant chain):** V2 bf16 = only stable bf16 recipe. V3 bf16 NaN'd ~5min; V4 bf16 NaN'd ~5min; V4 fp32 SIGTERM'd ~9min. P0/V2/V3' fp32 trained clean.
- **dgrad-probe headline:** layer-0 max 2.06 (V2) vs 67.0 (P0 prior) vs 4.13 (P0 new). V2 compresses dgrad 5-15× at every layer.
- **Phase 1 eval at 4 num_latent ∈ {0, 2, 4, 8} × 3 benchmarks:** GSM8k 0.121 / 0.125 / 0.153 / **0.162**; SVAMP 0.290 / 0.313 / 0.370 / **0.420**; gsm-hard 0.038-0.055. **Only variant with monotonically rising num_latent curves.**
- **Reframed by downstream characterization (F1-F6 + Track A):** the rising curve is a loop-lucky-match artifact, not iterative computation.

## Verdict

**Success on training stability; foundational anchor for everything downstream.** V2 is the minimum stable bf16 recipe at Qwen3-4B-Instruct-2507; this is the *headline-quality* stability claim of Phase 1. Capability characterization (template-routing failure mode) is the subject of every child node — V2 trains, but its latents collapse into routing rather than reasoning.

## Revert info

- Code: `feature/detach-variants` @ commit `9e418a6`. Detach config keys `detach_keep_last_k` and `detach_position_mode` in `LatentRuntimeConfig`. Helpers `_resolve_should_detach` + `_apply_boundary_detach` in `runtime.py`.
- Config: `latent_eval_training_harness/configs/training/qwen3_4b_codi_gh200_v2_keep_last_2.yaml`.
- Checkpoint: HF private repo `jrauvola/qwen3-4b-codi-bf16-kv-latent-detach-last-2`. Local copies under `latent_eval_training_harness/runs/qwen3_4b_codi_bf16_kv_latent_detach_last_2/` (deletable; checkpoint is on HF).
- To revert this entire training arm: keep the recipe as-is (it's the foundational baseline). To redo: re-run `run_training_from_config('configs/training/qwen3_4b_codi_gh200_v2_keep_last_2.yaml')`.

## Follow-ups / branch-offs

- [[f1-unique-correct]] · [[f2-loop-content]] · [[f3-trace-variance]] · [[f4-latent-kv-ablate]] · [[f5-cross-example-kv-swap]] · [[f6-kv-noise-sweep]]
- [[track-a-first-sentence-trim]] · [[kv-pca-analysis]] · [[kv-distance-bf16-vs-fp32]] · [[prediction-degeneracy-analysis]] · [[lightweight-experiments-e1-e4]]
- Phase 2 children: [[phase-2b-lt-tuning-cpf-training]] · [[phase-2a-sim-cot-shared-head-smoke]]
