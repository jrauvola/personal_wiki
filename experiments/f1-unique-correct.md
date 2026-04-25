---
type: experiment
title: "F1 — Unique-correct analysis (CODI vs zero-shot)"
slug: f1-unique-correct
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "If CODI training adds genuine latent reasoning capability beyond the base model, V2 bf16 should solve a meaningful set of problems that zero-shot CoT misses."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - research_findings/f1_f2_f3_inert_latent_tests.md
  - research_findings/inert_latent_F1_F2_F3.json
  - "script: latent_eval_training_harness/scripts/f1_f2_f3_inert_latent_tests.py"
updated: 2026-04-25
---

# F1 — Unique-correct analysis

## Parent context

First test in the F1-F6 inert-latent battery, branched off [[phase-1-v2-bf16-training]] after the rising num_latent curve was reframed by [[track-a-first-sentence-trim]] and [[prediction-degeneracy-analysis]] as a loop-lucky-match artifact. Question motivating F1: even granting the loop framing, does V2 add *any* unique reasoning capability beyond zero-shot CoT?

## Hypothesis

If V2's latents perform meaningful per-example computation, V2 should solve a non-trivial number of problems that zero-shot CoT (same base model) misses. A small unique-to-V2 set would refute the strict "latents add reasoning capability" framing and support the inert-latent picture.

## Method

- Variant: V2 bf16, num_latent=8.
- For each of GSM8k (1319) / gsm-hard (1319) / SVAMP (300): build the set `{ex : V2_correct ∧ ¬zshot_correct}` against the local zero-shot CoT predictions (Qwen3-4B-Instruct-2507 at `accuracy_zshot_gsm8k=0.863`, `gsm-hard=0.405`, `svamp=0.887`).
- Report cardinalities, target-magnitude distribution, and qualitative inspection of the unique-to-V2 set.

## Result

| Benchmark | V2 correct | zshot correct | unique to V2 | unique to zshot | V2-unique median \|target\| |
|---|---|---|---|---|---|
| GSM8k | 214 | 1138 | **10** | 934 | 15 |
| GSM-hard | 73 | 534 | **12** | 473 | 334,539 |
| SVAMP | 126 | 266 | **6** | 146 | 75,803 |

- Total unique-to-V2: 28 across all three benchmarks → **2.8% of V2-correct**.
- Unique-to-V2 examples are dominated by lucky format-prior loop matches (`"The answer is: 12.000000000000004..."` with target 12) on easy problems, plus a handful of large-target problems on gsm-hard where the base zero-shot ran out of tokens before producing an answer.

## Verdict

**Failure of the "CODI adds unique capability" hypothesis (success of the test).** CODI training adds essentially no unique reasoning capability beyond the base model — virtually every V2 win is on a problem the base model already solves. The unique-to-V2 set is too small to form a meaningful niche and is qualitatively explicable by lucky format-prior matches and base-model token-budget exhaustion on large-target problems.

## Revert info

- Pure analysis, no training. Local-only.
- Files added: `research_findings/f1_f2_f3_inert_latent_tests.md`, `research_findings/inert_latent_F1_F2_F3.json`, the synthesis section of `research_findings/inert_latent_hypothesis_tests.md`.
- Script: `latent_eval_training_harness/scripts/f1_f2_f3_inert_latent_tests.py` (kept; reusable on Phase 2 checkpoints).
- Reversible by deleting the four files above. No code changes to revert.

## Follow-ups / branch-offs

- F1 is one of three local logit-lens tests (F1 + [[f2-loop-content]] + [[f3-trace-variance]]) that ran together. F4 ([[f4-latent-kv-ablate]]) is the GPU-side decisive test; the F1 result feeds directly into the F4 interpretation (latents contribute a weak prior, not unique reasoning).
- Re-running F1 on Phase 2 checkpoints is one of the planned interpretability steps (see [[lt-tuning-f-battery-eval]]).
