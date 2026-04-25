---
type: experiment
title: "Phase 2a — SIM-CoT shared-lm_head smoke (memory footprint validation)"
slug: phase-2a-sim-cot-shared-head-smoke
status: success
started: 2026-04-24
finished: 2026-04-24
hypothesis: "SIM-CoT's shared-lm_head fallback (single-layer TransformerEncoder feeding the base model's lm_head) fits within GH200 budget at bs=2/ga=4."
parent: "root"
artifacts:
  - "config: configs/training/qwen3_4b_codi_gh200_sim_cot_shared_head_smoke.yaml"
  - "branch: feature/phase2-sim-cot @ 9638be5"
  - "log: remote /tmp/harness_phase2_sim_cot/logs/sim_cot_smoke_20260424T002607Z.log"
updated: 2026-04-25
---

# Phase 2a — SIM-CoT shared-lm_head smoke

## Parent context

Root child-track. Companion to [[phase-2b-lt-tuning-cpf-training]]. Full-LM SIM-CoT (`aux_decoder_full_lm: true`) OOM'd at step 1 on the GH200 when LT-Tuning was using ~38 GB. Smoke test validated the shared-lm_head fallback as a viable memory-conservative path for the full SIM-CoT training run.

## Hypothesis

Shared-lm_head SIM-CoT (single-layer TransformerEncoder feeding the base model's lm_head, vs full-LM aux decoder which is a 2x copy of the base) at bs=1/ga=1 should fit in <30 GB and scale to ~35-45 GB at bs=2/ga=4 — within budget when LT-Tuning has released its memory.

## Method

- Config: `configs/training/qwen3_4b_codi_gh200_sim_cot_shared_head_smoke.yaml` @ commit `9638be5` on `feature/phase2-sim-cot`.
- Setup: bs=1, ga=1, max_steps=10, max_samples_per_dataset=32. LT-Tuning concurrently training at ~38 GB on the same GPU.
- Recipe: V2 step-boundary detach + bf16 + `aux_decoder_full_lm: false` (shared-head). `freeze_base_embeddings=true` so no PEFT `ModulesToSaveWrapper` resize issue.
- 10 steps on GH200, monitor peak GPU memory.

## Result

- 10/10 steps completed in 48 s (~5 s/step).
- No OOM, no init TypeError.
- **Peak GPU memory: 22.5 GB** (shared-head fallback). Combined with LT-Tuning's 38.2 GB, GPU went from 48.7 used → 71.2 GB used at peak. Safety margin held; LT-Tuning was not disturbed.
- Loss trajectory (10 steps, loss/ce/distill/ref_ce/explain): drops from 26.22 (step 1) to 7.35 (step 3, init transient) and stabilizes 7-10 thereafter. All finite, no NaN/inf.
- Three `WARNING Large activation magnitude` at steps 6-8 (latent_absmax=135-138) — same as V2 bf16, not blocking.
- grad_norm 5-65 range; max_grad_norm=2.0 clips aggressively.

## Verdict

**Success — shared-head fallback validated at 22.5 GB.**

- **Not safe to co-run with LT-Tuning at bs=2/ga=4.** Combined budget too tight (LT-Tuning ~38 GB peak, SIM-CoT scales to ~30-40 GB at the recipe).
- **Safe after LT-Tuning finishes** — 22.5 GB at bs=1/ga=1 scales to ~35-45 GB at bs=2/ga=4, well within 94.5 GB on idle GPU.
- Recommended go-path: wait for LT-Tuning, try full-LM v2_detach first on idle GPU; fall back to shared-head if that OOMs.

This validation is what made [[phase-2a-sim-cot-full-training]] a real (gated) candidate for Case A/B follow-up.

## Revert info

- Code: `feature/phase2-sim-cot` @ commit `9638be5` (and downstream commits). DO NOT delete — this is the SIM-CoT implementation arm and is queued for Case A/B promotion.
- Smoke config: `configs/training/qwen3_4b_codi_gh200_sim_cot_shared_head_smoke.yaml`. Keep.
- Smoke log: remote `/tmp/harness_phase2_sim_cot/logs/sim_cot_smoke_20260424T002607Z.log`. Tmux session already cleaned up. Log is deletable after diagnosis is preserved in scratchpad.
- No HF push — smoke run, no checkpoint.

## Follow-ups / branch-offs

- [[phase-2a-sim-cot-full-training]] — full 5299-step run, gated on Case C escalation per spec §4.5. Currently retired auto-queue per [[phase-2b-lt-tuning-cpf-training]] outcome (Case C → COCONUT first; SIM-CoT remains in backlog).
- Wiki ref: [[meta/projects/branch-b]] §"Empirical update 2026-04-24" (SIM-CoT shared-head + OOM go-path).
