---
type: experiment
title: "Phase 2b — LT-Tuning CPF training (Qwen3-4B + V2 detach + 3-stage curriculum)"
slug: phase-2b-lt-tuning-cpf-training
status: failure
started: 2026-04-23
finished: 2026-04-24
hypothesis: "LT-Tuning's Context-Prediction-Fusion + 3-stage curriculum, layered on top of V2 detach, will force latents to participate in the embedding blend rather than collapse into routing — breaking the template lock."
parent: "root"
artifacts:
  - "branch: feature/phase2-lt-tuning"
  - "config: configs/training/qwen3_4b_codi_gh200_lt_tuning_v2_detach.yaml"
  - "code: src/latent_harness/training/lt_tuning.py, lt_tuning_data.py"
  - "tests: tests/test_lt_tuning.py (15 tests)"
  - "HF: jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach (final checkpoint, 11.5 GB)"
  - research_findings/lt_tuning_eval_diagnostic/first_cell_diagnostic.md
updated: 2026-04-25
---

# Phase 2b — LT-Tuning CPF training

## Parent context

Root child-track. Branched conceptually from [[phase-1-v2-bf16-training]] which established V2 as the only stable bf16 recipe. Phase 2's goal: do *any* additions on top of V2 break the template-routing failure mode characterized in F1-F6 + Track A + KV PCA? LT-Tuning is one of two lead candidates (the other is [[phase-2a-sim-cot-shared-head-smoke]]).

## Hypothesis

LT-Tuning's Context-Prediction-Fusion (CPF) anchors each latent against the embedding space — every latent is forced to participate in the vocab-token blend rather than be a free-form prefix. Combined with V2 step-boundary detach + 3-stage curriculum (warm-up → CPF-on → reinforce), the trained model should:
1. Train cleanly at 4B bf16 (LT-Tuning paper recipe + V2 stability layered).
2. Break F3's template lock — non-step-3 latent positions should show >0.4 bits of entropy.
3. Beat the 8.5% real-floor established by [[f4-per-example-diagnosis]].

## Method

- Model: Qwen3-4B-Instruct-2507, LoRA r=128, bf16 + V2 step-boundary detach + keep_last_2.
- Datasets: gsm8k_aug + numinamath_15.
- New code (~870 lines): `src/latent_harness/training/lt_tuning.py` (LTTuningRuntime, CurriculumScheduler, cpf_fuse, 3 thinking-token strategies — random/arithmetic/confidence — ports from upstream Latent-Thoughts-Tuning), `lt_tuning_data.py` (stage-aware dataset), `methods.py` registry entry, `trainer.py` `run_lt_tuning_training` stage orchestrator.
- CPF hyperparameters (from upstream `example_config.yaml`): fusion_top_p=0.9, fusion_temperature=1.0, per-stage `fusion_alpha = [0.5, 0.5, 0.6]`, `insertion_prob = [0.0, 0.85, 0.95]`, `reinforce_prob_threshold = [0.0, 0.3, 0.2]`, `hidden_state_layer_index = -1`, `stage_epochs = [1, 1, 3]`.
- 84 existing tests + 15 new LT-Tuning tests = 99 total pass.
- Compute: GH200, persistent tmux session, ~11.6h wall.

## Result

**Training:** clean. Started ~2026-04-23 17:30 UTC, completed 2026-04-24 ~13:16 UTC (`train_runtime=41742s, train_loss=0.539, epoch 3.0`). Auto-upload watcher mis-detected exit (kept polling tmux that was still running training session); final checkpoint pushed manually to `jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach` (model.safetensors 11.5 GB + tokenizer files, zero errors).

**Eval (first cell — gsm8k num_latent=0):** **1.67% accuracy** (22/1319), vs V2 bf16 same cell at **12.06%** (159/1319). LT-Tuning is qualitatively WORSE than V2 baseline.

Diagnostic findings (`research_findings/lt_tuning_eval_diagnostic/first_cell_diagnostic.md`):
- 99/100 first-cell predictions are loop-degenerate (vs V2's 95/100). Same trailing-zero pathology.
- Preamble is broken: starts with `isha:` (516/1319) or ` ) is:` (506/1319) instead of V2's `"The answer is:"` (~99% of V2). Looks like the model finishing partial-template tokens — CPF-trained model is responding to a *different* prompt template than the eval is supplying. Prompts byte-identical between LT-Tuning and V2 (verified).
- First-number-equals-target: 41/1319 (3.1%) vs V2 bf16 227/1319 (17.2%) — **5× worse**.
- Parsing-gap component: ~21 examples have first-number-correct but graded wrong (trailing-zero loop confuses the extractor) — fixing extractor would lift accuracy by ~1.5pp; doesn't change the picture.

**Headline cells (LT-Tuning eval, partial — F4/F5/F6 crashed before completion):** GSM8k num_latent=0 = **1.67%**, num_latent=2 = ~0.45%, num_latent=8 = ~6.67%. F3 entropy: dominant token is `1` across positions, entropies 0.16-0.64 bits — different template than V2's `The/0/0/0/.` but still template-locked.

## Verdict

**Failure of the eval; success of the training arm; diagnosed as Case C per spec §4.5.** LT-Tuning CPF + V2 detach trained cleanly at 4B bf16 — confirms the LT-Tuning recipe is *trainable* under the V2 stability layer. But the resulting checkpoint is qualitatively *worse* than V2 baseline: same loop pathology, different (and broken) preamble template, 5× lower first-number-correct rate. CPF did not break template-routing; it shifted the template to a partial-chat-template completion (`isha:` / `) is:`) that the eval can't parse. **Per spec §4.5 Case C** — promote COCONUT staged curriculum (W3.1) as the next intervention.

## Revert info

- Code: `feature/phase2-lt-tuning` branch, worktree `/tmp/harness_phase2_lt_tuning/`. Adds `src/latent_harness/training/lt_tuning.py` (~620 lines), `lt_tuning_data.py` (~250 lines), and registry entry. Tests in `tests/test_lt_tuning.py`. **Do NOT delete** — code is reusable for SIM-CoT and any future CPF arm.
- Config: `configs/training/qwen3_4b_codi_gh200_lt_tuning_v2_detach.yaml`.
- HF checkpoint: `jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach` (private). Local copy on GH200 at `/tmp/harness_phase2_lt_tuning/.../runs/qwen3_4b_codi_lt_tuning_bf16_v2detach/` — deletable (HF has the final checkpoint).
- To revert this experiment: keep the code (reusable), drop the config + HF repo if pursuing a different intervention. The diagnostic in `research_findings/lt_tuning_eval_diagnostic/` documents the failure and should be retained.

## Follow-ups / branch-offs

- [[lt-tuning-f-battery-eval]] — F-battery on the LT-Tuning checkpoint. Phase 1 + F3 + F1 ran; F4/F5/F6 crashed before reaching them. Case C confirmed.
- Spec §4.5 next steps under Case C: promote W3.1 COCONUT staged curriculum.
- Open scientific question: is the `isha:` / `) is:` preamble a training-data template artifact (chat-template tokens leaking into LT-Tuning's stage-2 confidence-thinking insertions) or a CPF-induced collapse to a different attractor? Worth investigating at the training-data level.
