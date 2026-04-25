---
type: experiment
title: "LT-Tuning eval harness pre-wire (configs + launcher + runbook)"
slug: eval-harness-pre-wire-lt-tuning
status: success
started: 2026-04-23
finished: 2026-04-24
hypothesis: "Staging eval configs + launch script + runbook before LT-Tuning training finishes will minimize between-run latency."
parent: "root"
artifacts:
  - "config: latent_eval_training_harness/configs/evaluation/qwen3_4b_codi_lt_tuning_bf16_v2detach_f_tests.yaml"
  - "config: latent_eval_training_harness/configs/evaluation/qwen3_4b_codi_lt_tuning_bf16_v2detach_full_ftest.yaml"
  - "script: latent_eval_training_harness/scripts/launch_lt_tuning_full_ftest_battery.sh"
  - "runbook: latent_eval_training_harness/scripts/lt_tuning_runbook.md"
updated: 2026-04-25
---

# LT-Tuning eval harness pre-wire

## Parent context

Infrastructure-track experiment. While LT-Tuning training was in flight ([[phase-2b-lt-tuning-cpf-training]]), pre-staged the eval configs + launcher + runbook so the F-battery could fire as soon as the checkpoint landed. This is the upfront-pain-for-long-term-gain framing — taking the time to design two configs (Phase 1 sweep + F-tests) and a launch script eliminates the eval-launch friction post-training.

## Hypothesis

If we stage:
1. Two eval configs covering Phase 1 num_latent sweep + F-test battery.
2. A launcher script that handles tmux + log capture + per-batch persistence.
3. A runbook with branch SHAs, expected runtime, and case-A/B/C decision criteria.

— then post-training the F-battery launches in ~5 minutes instead of half a day.

## Method

- Configs:
  - `qwen3_4b_codi_lt_tuning_bf16_v2detach_f_tests.yaml` — F1/F2/F3 + F4/F5/F6 cells
  - `qwen3_4b_codi_lt_tuning_bf16_v2detach_full_ftest.yaml` — full battery driver
- Launcher: `launch_lt_tuning_full_ftest_battery.sh` (sets up tmux session, exports env, calls runner with the full-ftest config).
- Runbook: `lt_tuning_runbook.md` documents:
  - F-test helper branch SHAs (`4415115`, `6b4776e`, `6ae5a7a`, `f682bb1`).
  - Cherry-pick / merge order onto `feature/phase2-lt-tuning`.
  - Expected total wall-clock (3-4h per pre-launch estimate).
  - Case A / B / C classification per spec §4.5.
- Pre-staged GH200 worktree at `/tmp/harness_phase2_lt_tuning/` with predictions sync-points.

## Result

- All artifacts landed before LT-Tuning training completed.
- Post-training, F-battery fired the same day (2026-04-24) without delay.
- One pre-launch issue surfaced (Qwen3 reserved-vocab decode crash) — patched in [[safe-decode-qwen3-reserved-vocab-patch]] within an hour.
- Battery progressed through Phase 1 + F3 + F1 before crashing on F4/F5/F6 — see [[lt-tuning-f-battery-eval]].

## Verdict

**Success — pre-launch wiring saved ~1 day of latency.** The eval landed the same day as training completion rather than the day after, which mattered because the result feeds the next-training-arm decision (Case A/B/C per spec §4.5). Without pre-wire the COCONUT escalation under Case C would have been a day later.

## Revert info

- Configs and runbook stay; reusable for any future Phase 2 / Phase 3 training arm.
- Launcher script is project-tooling. Keep.
- No code-side compute spent. Reversible by deleting the listed configs / scripts / runbook, but no reason to.
- HF target: `jrauvola/qwen3-4b-codi-lt-tuning-bf16-v2detach` (created by the training arm, not the eval pre-wire).

## Follow-ups / branch-offs

- Same pre-wire pattern should be applied for COCONUT (W3.1, currently next under Case C) and any V3 composite.
- Watcher logic should be hardened: the auto-upload watcher mis-detected exit because tmux was still alive in training session. Use a marker file or process-list check instead of `tmux has-session`.
- One of three pre-launch infra fixes; companions: [[peft-modules-to-save-resize-fix]] and [[safe-decode-qwen3-reserved-vocab-patch]].
