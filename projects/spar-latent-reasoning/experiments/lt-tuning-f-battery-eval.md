---
type: experiment
title: "LT-Tuning F-battery eval (Phase 1 + F1 + F3 + crashed F4/F5/F6)"
slug: lt-tuning-f-battery-eval
status: failure
started: 2026-04-24
finished: 2026-04-24
hypothesis: "Re-running the F1-F6 battery on the LT-Tuning checkpoint will reveal whether CPF broke the template-routing pattern (Case A: yes; Case B: partial; Case C: no)."
parent: "[[phase-2b-lt-tuning-cpf-training]]"
artifacts:
  - research_findings/lt_tuning_eval_diagnostic/first_cell_diagnostic.md
  - research_findings/lt_tuning_eval_diagnostic/gsm8k_numlatent_0/predictions.jsonl
  - "branches: feature/f-tests-inert-latent, feature/f4-latent-ablate, feature/f5-kv-swap, feature/f6-kv-perturb"
  - "logs: /tmp/lt_tuning_eval_phase1/battery.log on GH200 (192.222.51.198)"
updated: 2026-04-25
---

# LT-Tuning F-battery eval

## Parent context

Direct child of [[phase-2b-lt-tuning-cpf-training]]. Eval-side test of whether CPF + V2 detach training broke the template-routing failure mode characterized by F1-F6 on V2 bf16. Per spec `docs/superpowers/specs/2026-04-24-research-direction.md` §4.5 the result drives every downstream training decision (Case A → CPF component ablations, B → V3 composite, C → COCONUT).

## Hypothesis

If CPF worked: F3 entropy distribution should broaden (>0.4 bits at >1/8 positions), F5 swap should produce a meaningful accuracy delta, F4 ablation should produce a *larger* drop than V2 (latents are now load-bearing). Loop rate should drop from 99% toward zero-shot's <1%.

## Method

- **Pre-launch infra:** [[eval-harness-pre-wire-lt-tuning]] established 2 eval configs + launcher + runbook before LT-Tuning training finished.
- F-test helper commits cherry-picked from V2 branches onto `/tmp/harness_phase2_lt_tuning/`:
  - `4415115` (`feature/f-tests-inert-latent`)
  - `6b4776e` (F4 latent ablate)
  - `6ae5a7a` (F5 KV swap)
  - `f682bb1` (F6 KV perturb)
- Conflict resolution: `config.py` (keep both flags), `latent_tap.py` (HEAD already has superset), `runner.py` (keep HEAD).
- **Patched bug discovered during launch:** Qwen3-4B vocab has ~173 reserved slots (IDs 151670-151842) that map to `None` via `convert_ids_to_tokens`. Tokenizer-decode crashed on batch 1/330 with `TypeError: sequence item 0: expected str instance, NoneType found`. Added `_safe_decode` filter — see [[safe-decode-qwen3-reserved-vocab-patch]].
- Battery launched in tmux `lt_tuning_eval_battery` on GH200, log at `/tmp/lt_tuning_eval_phase1/battery.log`.

## Result

**Phase 1 + F3 + F1 ran. F4/F5/F6 crashed.**

Headline accuracy cells (LT-Tuning, GSM8k):
- num_latent=0: **1.67%** (22/1319) — vs V2 bf16 at 12.06%
- num_latent=2: ~0.45%
- num_latent=8: ~6.67%

LT-Tuning is qualitatively *worse* than V2 baseline at every num_latent.

**F3 entropy on LT-Tuning latent traces:** dominant token is `1` across positions, entropies 0.16-0.64 bits. Different template from V2's `The/0/0/0/.` (where dominant tokens were `The` then `0`s then `.`s). Still template-locked — CPF did not break the template, it *shifted* it to a different attractor.

**F1:** unique-correct vs zero-shot is essentially zero (consistent with the broken preamble; LT-Tuning rarely reaches the answer-format template at all).

**F4/F5/F6:** crashed mid-run. Cause not fully diagnosed in available logs — likely related to interactions between the cherry-picked helpers and the LT-Tuning runtime; would need re-run after a focused debug pass.

**Diagnostic (`first_cell_diagnostic.md`):** Verdict (a) real failure mode + (c) small parsing-gap component. Loop pathology preserved (99/100), preamble shifted to broken `isha:` / `) is:` template. Prompts byte-identical to V2 — not an eval bug. **Case C** per spec §4.5.

## Verdict

**Failure for the LT-Tuning intervention; partial completion of the F-battery.** Case C confirmed per spec §4.5 — CPF did not break the template-routing failure mode at 4B; it shifted to a different (and worse) template. Next step under Case C: COCONUT staged curriculum (W3.1) — see spec §4.5. F4/F5/F6 should be re-run on the LT-Tuning checkpoint after debugging the crash, but the headline accuracy is so far below V2 that a full F-battery is unlikely to add substantively to the verdict.

## Revert info

- Helper branches and the cherry-picked combination on `/tmp/harness_phase2_lt_tuning/` should be retained — F4/F5/F6 helpers are reusable.
- Diagnostic file `research_findings/lt_tuning_eval_diagnostic/first_cell_diagnostic.md` and predictions JSONL preserved.
- Pre-launch eval configs and runbook (`latent_eval_training_harness/scripts/lt_tuning_runbook.md`) — keep.
- `_safe_decode` patch — DO NOT revert (back-ported across V2 branches; see [[safe-decode-qwen3-reserved-vocab-patch]]).
- Logs on GH200 are deletable after diagnosis.
- To re-run: `tmux attach -t lt_tuning_eval_battery` (if still alive) or relaunch via the runbook.

## Follow-ups / branch-offs

- F4/F5/F6 crash investigation — focused debug pass needed.
- Phase 2a SIM-CoT full training — gated on Case C escalation per spec; queued in [[phase-2a-sim-cot-full-training]].
- Eval bug fix designated: extractor enhancement to "stop at first \\n or first non-numeric token after the leading numeric region" — would lift LT-Tuning headline by ~1.5 pp on GSM8k n=0.
