---
type: experiment
title: "F4 — Latent-KV ablation before answer generation"
slug: f4-latent-kv-ablate
status: success
started: 2026-04-22
finished: 2026-04-23
hypothesis: "If latents are functionally inert, dropping their KV before the answer-generation rollout should leave accuracy and loop behavior unchanged. A meaningful drop refutes strict inertness."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - "raw: research_findings/f_tests_raw/qwen3_4b_codi_bf16_kv_latent_detach_last_2/{gsm8k,svamp}_{baseline,f4_ablate}/"
  - "branch: feature/f4-latent-ablate @ 6b4776e"
updated: 2026-04-25
---

# F4 — Latent-KV ablation before answer generation

## Parent context

GPU-side decisive test in the F1-F6 battery, branched off [[phase-1-v2-bf16-training]]. F1-F3 had established the logit-lens-level template framing; F4 asks the question that logit lens cannot answer: **does the downstream attention actually use the latent KV during answer generation?**

## Hypothesis

If V2's latents are strictly inert (architecturally present but functionally zero), `DynamicCache.crop(encoder_prefix_length)` removing latent entries from the cache before answer generation should leave accuracy and loop rate unchanged. Any meaningful drop refutes strict inertness — latents are doing *something* the format-prior fallback cannot replicate.

## Method

- Variant: V2 bf16, num_latent=8.
- Single modification to `latent_tap.py::generate_from_latent_with_taps`: after the latent rollout, call `DynamicCache.crop(encoder_prefix_length)` on `past_key_values`. Gated by new flag `ablate_latent_kv_before_answer`.
- Re-evaluate on full GSM8k (N=1319) and SVAMP (N=300). Greedy decoding, same hyperparameters as Phase 1.
- Compare baseline vs F4 ablate accuracies + loop rate + per-example overlap.

## Result

| Benchmark | N | Baseline (n=8) | F4 ablate | Δ | Δ relative |
|---|---|---|---|---|---|
| GSM8k | 1319 | 0.1630 | **0.1221** | -0.0409 | **-25.1%** |
| SVAMP | 300 | 0.4233 | **0.3000** | -0.1233 | **-29.1%** |

- **Output shape (GSM8k):** 62% of predictions' text changes; 47% of parsed answers change. **Loop rate stays at 99.8% baseline vs 99.8% F4** — model continues to loop, continues to emit `1`-leading format-prior answers. SVAMP: 76% text-changed, 50% parsed-changed, 100%/100% loop rate.
- **Set view (GSM8k):** of 215 baseline-correct, 127 are also F4-correct (preserved); 88 are lost; F4 additionally gets 34 new correct (gained).
- First-digit distribution of parsed predictions essentially unchanged (`1`-leading at 630 baseline vs 521 ablated).

## Verdict

**Partial — strict inert-latent hypothesis refuted; latents contribute a weak prior but do not drive the template.** The 25-30% relative drop is real evidence that latents are not 100% inert. But the model continues to loop, continues to emit format-prior answers, and continues to get 70-75% of its accuracy. The latents contribute *at the margin* — amplifying or de-amplifying specific token emissions within the fixed template — they do not drive the template itself. This is the central finding that flipped the hypothesis from "strictly inert" to "inert for reasoning, structurally necessary for routing."

## Revert info

- Code: `feature/f4-latent-ablate` @ commit `6b4776e` (later cherry-picked into LT-Tuning eval branch). Adds `ablate_latent_kv_before_answer` flag to `LatentRuntimeConfig` and `_crop_cache` helper in `latent_tap.py`.
- Raw outputs in `research_findings/f_tests_raw/qwen3_4b_codi_bf16_kv_latent_detach_last_2/{gsm8k,svamp}_f4_ablate/` (predictions.jsonl + summaries) — deletable.
- To revert: drop the flag default to false (current), or merge the branch as already-done.
- The cherry-picked LT-Tuning version is on `/tmp/harness_phase2_lt_tuning/` worktree; if reverting LT-Tuning eval changes, the F4 helper is shared and should NOT be removed.

## Follow-ups / branch-offs

- [[f4-per-example-diagnosis]] — per-example join with [[track-a-first-sentence-trim]] to characterize the lost-88 / preserved-127 / gained-34 sets. Sharpens the real capability floor to 8.5%.
- F4 is a precondition for the [[lt-tuning-f-battery-eval]] re-run on the LT-Tuning checkpoint.
