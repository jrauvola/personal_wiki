---
type: experiment
title: "_safe_decode patch — Qwen3-4B reserved-vocab None-token bug"
slug: safe-decode-qwen3-reserved-vocab-patch
status: success
started: 2026-04-24
finished: 2026-04-24
hypothesis: "Qwen3-4B's vocab has reserved slots that map to None via convert_ids_to_tokens; the F-test trace decode crashed because tokenizer concatenation hit a NoneType."
parent: "root"
artifacts:
  - "code: latent_eval_training_harness/src/latent_harness/evaluation/latent_tap.py::_safe_decode"
  - "branches affected: V2 + 4 F-test helper branches (back-ported)"
updated: 2026-04-25
---

# _safe_decode patch — Qwen3-4B reserved-vocab bug

## Parent context

Infrastructure-track experiment. Discovered during LT-Tuning F-battery launch ([[lt-tuning-f-battery-eval]]). First batch (1/330) crashed with `TypeError: sequence item 0: expected str instance, NoneType found` because Qwen3-4B's vocab has ~173 reserved slots (IDs 151670-151842 etc) that map to `None` via `convert_ids_to_tokens`. The F-test trace decode joins token strings — a single `None` poisons the join.

## Hypothesis

Adding a defensive filter `_safe_decode([t for t in tokens if t is not None])` before concatenation eliminates the crash without changing decoded behavior on valid tokens. The same bug is latent on the V2 branch and any future Qwen3-family branch — should be back-ported across all eval harnesses.

## Method

- Patch: add `_safe_decode` helper in `latent_tap.py` that filters `None` tokens from `convert_ids_to_tokens` output before string-join.
- Back-port across:
  - `feature/phase2-lt-tuning` (where the bug surfaced)
  - V2 main branch
  - `feature/f-tests-inert-latent`
  - `feature/f4-latent-ablate`
  - `feature/f5-kv-swap`
  - `feature/f6-kv-perturb`
  (5 branches total per scratchpad: "back-ported across 5 V2 branches".)
- Verify on a re-launch of the F-battery: first batch succeeds, no decode crash.

## Result

- LT-Tuning F-battery launched cleanly after the patch — first batch (gsm8k num_latent=0) completed in ~28 s for 4 examples (vs 0/330 with the crash).
- Patch back-ported across 5 V2 branches per scratchpad note.
- No false-positive filtering on the V2 baseline (V2 traces don't contain reserved-vocab slots, so the filter is a no-op there; harmless).

## Verdict

**Success — eval-harness blocker resolved across the family.** A reserved-vocab bug that any Qwen3-family eval harness running for >1 batch would hit. Without this fix the entire LT-Tuning F-battery would have been blocked; with it, the battery is rate-limited only by GPU time. The back-port across V2 branches future-proofs subsequent Qwen3 work.

## Revert info

- Defensive filter — reverting re-introduces the crash. DO NOT revert.
- Code location: `latent_eval_training_harness/src/latent_harness/evaluation/latent_tap.py::_safe_decode`.
- The filter is conservative (only drops `None`), so cannot affect any non-Qwen3 model behavior.

## Follow-ups / branch-offs

- Apply audit to other Qwen-family models we may evaluate (Qwen3-Thinking, Qwen3-8B/14B if scaled). Reserved-vocab maps are consistent across the family.
- One of three pre-launch infra fixes; companions: [[peft-modules-to-save-resize-fix]] and [[eval-harness-pre-wire-lt-tuning]].
