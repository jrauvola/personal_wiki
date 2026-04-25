---
type: experiment
title: "Phase 2a — SIM-CoT full training (planned, gated on Case C escalation)"
slug: phase-2a-sim-cot-full-training
status: planned
started: pending
finished: pending
hypothesis: "SIM-CoT's per-step auxiliary decoder loss forces step-identifiable content, breaking F3's template-only decoding."
parent: "[[phase-2a-sim-cot-shared-head-smoke]]"
artifacts:
  - "branch: feature/phase2-sim-cot @ fe10e94"
  - "config: configs/training/qwen3_4b_codi_gh200_sim_cot_v2_detach.yaml"
  - "code: AuxiliaryStepDecoder, SimCotLatentRuntime, AuxDecoderDropCallback"
  - "tests: tests/test_sim_cot.py (28 tests)"
  - "HF: jrauvola/qwen3-4b-codi-sim-cot-bf16-v2detach (target)"
updated: 2026-04-25
---

# Phase 2a — SIM-CoT full training

## Parent context

Direct child of [[phase-2a-sim-cot-shared-head-smoke]] (memory smoke validated). Sibling to [[phase-2b-lt-tuning-cpf-training]]. SIM-CoT's per-step aux-decoder supervision is the second of two lead Phase 2 candidates for breaking the template-routing failure mode.

## Hypothesis

SIM-CoT's auxiliary step-decoder forces each latent step to decode a specific reasoning token from `gsm8k_aug` `<<expr=value>>` step traces. The aux loss should:
1. Train cleanly at 4B bf16 + V2 detach (smoke validated 22.5 GB).
2. Break F3's template-only logit-lens — non-step-3 latent positions should show >0.4 bits of entropy aligned with the step trace.
3. Beat the 8.5% real-floor established by [[f4-per-example-diagnosis]].
4. Reduce loop rate meaningfully below V2's 81% on GSM8k n=8.

## Method (planned)

- Model: Qwen3-4B-Instruct-2507. LoRA r=128 α=32. bf16 + V2 step-boundary detach + keep_last_2.
- Datasets: gsm8k_aug_nl + numinamath_15 mix, 5299 steps.
- New code (already landed on `feature/phase2-sim-cot`):
  - `AuxiliaryStepDecoder` with full-LM (paper default, 2× memory) and shared-lm_head fallback paths.
  - `SimCotLatentRuntime` wraps `LatentReasoningRuntime`; attaches aux decoder at train_mode only, strips `aux_decoder.*` keys from `state_dict` so saved artifacts match the CODI inference contract.
  - `drop_aux_decoder()` + `AuxDecoderDropCallback` wipe aux decoder at train_end.
  - Step-trace extraction `extract_step_texts` + `build_step_token_lists` parses `<<expr=value>>` chunks tokenizer-agnostically.
  - Loss: `total = ce + 20*distill + ref_ce + 1.0*(explain / max(1, effective_steps))`.
  - 28 new tests in `test_sim_cot.py`; full suite 123 passing.
- Launch helper: `scripts/launch_sim_cot_training.sh` (DRY_RUN=1 supported).
- Compute (planned): GH200 idle GPU after LT-Tuning released, ~5-7h wall.

## Result

**Pending — gated on Case C escalation per spec §4.5.**

Per spec §4.5 case-gating logic:
- Case A (LT-Tuning clears gates) → CPF component ablations first.
- Case B → W2.2 V3 composite first.
- **Case C (LT-Tuning fails F-battery) → W3.1 COCONUT first.** SIM-CoT remains in backlog.

[[lt-tuning-f-battery-eval]] confirmed Case C. SIM-CoT's auto-queue (`overnight_phase2_queue.sh`) was retired 2026-04-24 to `/tmp/overnight_phase2_queue.sh.RETIRED_2026-04-24` per the new case-gated policy.

## Verdict

**Planned / queued.** Code, tests, config, and memory budget all validated. Not running because Case C escalates COCONUT ahead of SIM-CoT in the queue. Will be promoted if COCONUT also fails the F-battery, or if a partial CPF / SIM-CoT composite arm is justified post-COCONUT.

**Deviations from paper (flag in any writeup):**
1. Dataset mix matches V2 headline (gsm8k_aug_nl + numinamath_15 + friends) vs paper's GSM8k-aug only.
2. V2 step-boundary KV+latent detach + keep_last_2 layered on top (isolates aux-decoder contribution from bf16 stability recipe).
3. LoRA r=128 α=32 (paper) vs V2 headline's r=16 α=16. (V2 headline used r=128 for compute parity.)
4. Shared-head fallback, if used under memory pressure, is numerically non-identical to paper's full-LM aux decoder.

## Revert info

- Code: `feature/phase2-sim-cot` @ commit `fe10e94`. **Do NOT delete** — code is reusable and remains queued for Case A/B promotion.
- Auto-queue script: retired (`/tmp/overnight_phase2_queue.sh.RETIRED_2026-04-24`). Decision rule baked into spec §4.5 — not in code.
- HF target: `jrauvola/qwen3-4b-codi-sim-cot-bf16-v2detach` — not yet created.
- No training run started, no checkpoint to delete.

## Follow-ups / branch-offs

- Will branch downstream F-battery eval (analogous to [[lt-tuning-f-battery-eval]]) once trained.
- Wiki ref: [[meta/projects/branch-b]] (Phase 2 branch-B).
