---
type: experiment
title: "PEFT modules_to_save × resize_token_embeddings fix"
slug: peft-modules-to-save-resize-fix
status: success
started: 2026-04-23
finished: 2026-04-23
hypothesis: "PEFT's ModulesToSaveWrapper around lm_head/embed_tokens crashes when resize_token_embeddings is called after the LoRA wrap. Resize first, wrap second."
parent: "root"
artifacts:
  - "code: src/latent_harness/training/lt_tuning.py (init order fix)"
  - "code: training pipeline `add_codi_special_tokens → resize → get_peft_model` ordering"
updated: 2026-04-25
---

# PEFT modules_to_save × resize_token_embeddings fix

## Parent context

Infrastructure-track experiment, no parent. Encountered during the LT-Tuning training launch ([[phase-2b-lt-tuning-cpf-training]]). LoRA configs in this project use `modules_to_save=["embed_tokens", "lm_head"]` (so the special-token embeddings are trained), but PEFT's `ModulesToSaveWrapper` does not survive a subsequent `resize_token_embeddings` call.

## Hypothesis

The CODI training recipe adds 3 special tokens (`<bot>`, `<eot>`, plus a memory token), requiring `resize_token_embeddings(ori_vocab_size + 3)`. If the resize is called *after* `get_peft_model` has wrapped `lm_head` / `embed_tokens` in `ModulesToSaveWrapper`, the resize crashes with TypeError or silently drops the wrapper. Fix: resize before LoRA wrap.

## Method

- Audit init order in LT-Tuning runtime construction.
- Reorder: `add_codi_special_tokens(tokenizer) → base_model.resize_token_embeddings(len(tokenizer)) → get_peft_model(base_model, lora_cfg)`.
- Verify on smoke run that `lm_head.modules_to_save` and `embed_tokens.modules_to_save` are present and trainable.

## Result

- Fix landed on `feature/phase2-lt-tuning` worktree as part of LT-Tuning pipeline preparation.
- LT-Tuning training ran 5299 steps clean (~11.6h) without resize-related TypeError — regression test that the fix holds.
- Confirmed from SIM-CoT smoke ([[phase-2a-sim-cot-shared-head-smoke]]): the shared-head fallback uses `freeze_base_embeddings=true` so `modules_to_save` is not engaged at all there; LT-Tuning is the binding case.

## Verdict

**Success — pre-launch blocker resolved.** Without this fix the LT-Tuning training would have crashed at runtime construction. The fix is in production on the LT-Tuning branch and is a precondition for any future training arm that uses `modules_to_save` + `resize_token_embeddings` (which is most CODI variants).

## Revert info

- Fix is an init-order change in the LT-Tuning runtime (and shared training pipeline). Reversing the order would re-introduce the bug.
- DO NOT revert — fix is a precondition for any current or future CODI training arm that uses LoRA with `modules_to_save`.
- The fix lives on `feature/phase2-lt-tuning`. If that branch is rebased / squashed, ensure the resize-before-wrap ordering is preserved.

## Follow-ups / branch-offs

- Apply the same audit to any future training arm that uses `modules_to_save` (V3 composite, COCONUT, SIM-CoT-full).
- This is one of three pre-launch infra fixes that unblocked Phase 2; companions: [[safe-decode-qwen3-reserved-vocab-patch]] and [[eval-harness-pre-wire-lt-tuning]].
