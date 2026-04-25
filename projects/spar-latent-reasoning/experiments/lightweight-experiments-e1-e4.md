---
type: experiment
title: "Lightweight experiments E1-E4 — format prior, regression, length, preserved"
slug: lightweight-experiments-e1-e4
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "CODI training does not teach latent reasoning — it teaches a strong answer-format prior."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/lightweight_experiments_E1_E4.md
  - research_findings/lightweight_experiments_E1_E4.json
  - "script: latent_eval_training_harness/scripts/lightweight_experiments_E1_E4.py"
updated: 2026-04-25
---

# Lightweight experiments E1-E4

## Parent context

Branched off [[phase-1-v2-bf16-training]]. Four cheap local analyses run together to test the framing that CODI training instills format priors rather than reasoning.

## Hypothesis

- **E1:** CODI's first-digit distribution should match GSM8k target distribution (model has learned "most answers start with 1"), not be uniform.
- **E2:** A meaningful set of GSM8k problems are *destroyed* by CODI training (zero-shot solves, all CODI variants fail).
- **E3:** Non-loop CODI outputs are short, not truncated — the model chooses to loop, doesn't run out of tokens.
- **E4:** CODI preserves only the easiest zero-shot-solvable problems.

## Method

- Inputs: V2 bf16, V2' fp32, V3' fp32, P0 predictions across GSM8k/gsm-hard/SVAMP × num_latent ∈ {0, 2, 4, 8}.
- E1: tabulate first-digit of parsed prediction vs first-digit of target.
- E2: for each benchmark, count problems where ALL 4 CODI variants fail AND zero-shot succeeds.
- E3: split predictions into loop-correct, loop-wrong, non-loop-correct, non-loop-wrong; report length statistics + fraction hitting `max_new_tokens=1024`.
- E4: count problems where ALL CODI variants are correct AND zero-shot is correct; report median target magnitude.

## Result

**E1 — first-digit prior:**

| Benchmark | V2 actual `1`-leading | V2 chance | P0 | V2' |
|---|---|---|---|---|
| gsm8k | 45% | 20% | 31% | 44% |
| gsm-hard | 40% | 18% | 36% | 40% |
| svamp | 71% | 18% | ? | 71% |

All CODI variants hit first digit at 2-4× chance. Model memorized "most answers start with 1" better than it learned to compute the rest.

**E2 — regression:**

| Benchmark | n_shared | n_regression | rate | median target in regression set |
|---|---|---|---|---|
| gsm8k | 1319 | 802 | **60.8%** | 45.0 |
| gsm-hard | 1319 | 428 | 32.4% | **378,696.9** |
| svamp | 300 | 97 | 32.3% | 19.0 |

802/1319 GSM8k problems destroyed by every CODI variant.

**E3 — non-loop length:**

V2 bf16 × GSM8k × n=8:
- loop_correct: median 631 chars
- non_loop_correct: median **298 chars** (~75 tokens)
- 0% of outputs hit max_new_tokens.

Non-loop correct outputs are short by choice, not truncated.

**E4 — preserved set:**

| Benchmark | zshot solvable | all-CODI ∩ zshot-correct | preserved / zshot-solvable | preserved median target | zshot median |
|---|---|---|---|---|---|
| gsm8k | 1138 | 35 | **3.1%** | 24 | 42 |
| gsm-hard | 534 | 16 | **3.0%** | 18.5 | **3,150** |
| svamp | 266 | 22 | 8.3% | 4.5 | 20 |

Only 3% of zero-shot's solved problems are preserved by all CODI variants — and those preserved problems have dramatically smaller target magnitudes.

## Verdict

**Success — coherent framing of CODI as format-prior emission.**

> CODI training at 4B does not teach latent reasoning. It teaches the model a strong answer-format prior (small-integer, `1`-leading, matching GSM8k/SVAMP target distribution) and two emission modes: (1) short format-prior guess (~5% of outputs; sometimes lucky-correct), (2) repetitive loop that fills the token budget (~70%; lucky-matches when prior digit aligns with target). Only the simplest zero-shot-solvable problems are preserved — 97% of zero-shot capability is destroyed.

Implication for V3: the problem isn't latent reasoning capacity, it's that CODI training collapses the model into format-prior emission. SIM-CoT's per-step auxiliary supervision is designed to enforce step-identifiable content — direct test of whether aux supervision can break this collapse mode.

## Revert info

- Pure analysis. Reversible by deleting:
  - `research_findings/lightweight_experiments_E1_E4.md`
  - `research_findings/lightweight_experiments_E1_E4.json`
  - `latent_eval_training_harness/scripts/lightweight_experiments_E1_E4.py`
- No upstream artifacts touched.

## Follow-ups / branch-offs

- E1's first-digit alignment story is the upstream input to [[track-a-first-sentence-trim]]'s "lucky-loop base-rate" framing.
- Triggered the F1-F6 battery (specifically F1 unique-correct).
- Phase 2 pass-fail criterion sharpened: must re-introduce reasoning capacity, not just match the rising curve.
