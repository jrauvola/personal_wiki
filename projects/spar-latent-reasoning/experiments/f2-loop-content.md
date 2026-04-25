---
type: experiment
title: "F2 — Question-specific loop content"
slug: f2-loop-content
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "If the model is reading the question during loop emission, looped substrings should contain question digits >>50% of the time. <20% would indicate context-free format-prior emission."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - research_findings/f1_f2_f3_inert_latent_tests.md
  - research_findings/inert_latent_F1_F2_F3.json
updated: 2026-04-25
---

# F2 — Question-specific loop content

## Parent context

Second logit-lens test in the F1-F6 battery, branched off [[phase-1-v2-bf16-training]]. After [[prediction-degeneracy-analysis]] established that 95-99% of V2's predictions contain a loop, F2 asks whether those loops are reading from the question (real but loopy reasoning) or context-free format-prior emission.

## Hypothesis

For 100 random V2 bf16 (n=8) looped predictions per benchmark, extract the looped substring (≥15 chars repeated ≥3×) and check whether any digit in the loop substring also appears in the question. Floor: >70% would imply the model is reading the question during loop emission; <20% would imply context-free emission.

## Method

- Inputs: V2 bf16 num_latent=8 predictions on GSM8k (1319), gsm-hard (1319), SVAMP (300).
- Loop detection via `prediction_degeneracy_analysis`'s rule (≥15-char substring repeating ≥3× consecutively).
- 100 random looped predictions per benchmark → extract loop substring → check overlap of loop digits with question digits and target digits.

## Result

| Benchmark | fraction with loop | loop-has-question-digit | loop-has-target-digit |
|---|---|---|---|
| GSM8k | 99.9% | **12%** | 26% |
| GSM-hard | 100.0% | **13%** | 9% |
| SVAMP | 100.0% | **12%** | 54% |

Representative loops:
- `gsm8k-789`: question digits `{32, 33, 45, 5}`, loop digits `{2, 4}` → 0 shared. Loop: `"the answer is: 2.4. ..."`.
- `gsm-hard-1068`: question digits `{15, 389925, 389925000, 500, 600}`, loop digits `{0}` (80+ zeros) → 0 shared.
- `svamp-287`: question digits `{36, 6}`, loop digits `{6, 000000000000001}` → 1 shared.

SVAMP's 54% loop-has-target-digit rate is explained by SVAMP's small target range — many single-digit targets coincide with loop digits even when question digits don't.

## Verdict

**Success — loops are context-free format-prior emission.** Only ~12% of loop substrings contain any digit from the question, well below any reasonable "question-reading" floor. The model's loop mechanism is not consulting the question's numbers; it is emitting a format-prior template whose digits are decoupled from the input.

## Revert info

- Pure analysis, no training. Reversible by deleting `research_findings/f1_f2_f3_inert_latent_tests.md`, `research_findings/inert_latent_F1_F2_F3.json`, and removing F2 sections from `inert_latent_hypothesis_tests.md`.
- Script: `latent_eval_training_harness/scripts/f1_f2_f3_inert_latent_tests.py` — reusable on Phase 2 checkpoints.

## Follow-ups / branch-offs

- F2 feeds the loop-mode-emission framing in [[concepts/Loop-Mode Emission]].
- Re-running on Phase 2 checkpoints is part of [[lt-tuning-f-battery-eval]].
