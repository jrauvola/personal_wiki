---
type: experiment
title: "Track A — First-sentence-trim post-hoc regrade"
slug: track-a-first-sentence-trim
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "If V2 bf16's rising num_latent curve is loop-lucky-match, trimming each prediction to its first period-terminated sentence and re-grading should flatten the curve."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/track_a_posthoc_first_sentence_regrade.md
  - research_findings/track_a_posthoc_first_sentence_regrade.json
  - "script: latent_eval_training_harness/scripts/track_a_postmatch_first_sentence.py"
updated: 2026-04-25
---

# Track A — First-sentence-trim post-hoc regrade

## Parent context

Branched off [[phase-1-v2-bf16-training]] after the rising num_latent curve was identified as the headline Phase 1 finding. Track A asks: is V2 bf16's rising curve real (more latent steps → more accurate first answer) or an artifact of loop-emission lucky matches in subsequent emissions? Trimming each prediction at its first period-terminated sentence cheaply approximates `repetition_penalty` decoding without spending GPU.

## Hypothesis

If V2 bf16's rising num_latent curve is loop-lucky-match, the trimmed accuracy at each num_latent should be roughly flat (the format-prior emission rate is independent of num_latent; only the loop-lucky matches scale with loop length). If the rise is real iterative-reasoning improvement, the trimmed curve should also rise.

## Method

- For each variant × benchmark × num_latent: trim each prediction to its first `". "` whose preceding char is non-digit (preserves decimals); re-parse the first numeric per the standard answer-extraction rule.
- Compare original (full-prediction) accuracy vs trimmed accuracy across 4 CODI variants × 3 benchmarks × 4 num_latent.
- Zero-shot sanity check: trim should be aggressive on zero-shot (which puts answers AFTER reasoning), confirming the trim is not free.

## Result

Zero-shot sanity (trim is aggressive — confirms it kills models that put answers after reasoning):
- GSM8k: 0.863 → 0.004
- SVAMP: 0.887 → 0.057

V2 bf16 (the headline result):

| Benchmark | num_latent | Original | Trimmed | Δ |
|---|---|---|---|---|
| GSM8k | 0 | 0.121 | 0.107 | -0.014 |
| GSM8k | 8 | **0.162** | **0.108** | **-0.054** |
| SVAMP | 0 | 0.290 | 0.277 | -0.013 |
| SVAMP | 8 | **0.420** | **0.263** | **-0.157** |

Other variants at GSM8k:
- V2' fp32: n=0 0.152 → 0.094
- V3' fp32: n=8 0.121 → 0.108
- P0: n=8 0.105 → 0.106 (essentially unchanged)

**V2 bf16's rising curve VANISHES after first-sentence trim.** All 4 CODI variants converge to ~10% on GSM8k when trimmed. V2's apparent "win" comes from loop-lucky matches in subsequent emissions, not from the first-emission answer rate.

## Verdict

**Success — definitive identification of the rising-curve artifact.** Phase 1's headline rising curve is a loop-reinforced format-prior emission effect, not iterative computation. V2 bf16's underlying short-answer capability (~10% GSM8k, ~26% SVAMP) is comparable to other CODI variants; the bf16 advantage is that its digit attractor (`0`) happens to align with GSM8k/SVAMP target distributions better than fp32's (`2`). Bounds on V2 bf16 capability: trimmed (no loops at all) ~10% GSM8k / ~26% SVAMP; original ~16% / ~42%. Live `repetition_penalty` would land between these.

## Revert info

- Pure analysis. Reversible by deleting `research_findings/track_a_posthoc_first_sentence_regrade.md` + `.json` and `latent_eval_training_harness/scripts/track_a_postmatch_first_sentence.py`.
- No GPU spent, no live re-eval. The prediction files themselves are shared upstream artifacts; do not touch.

## Follow-ups / branch-offs

- Stacking with F4: 76 of F4's 88 lost are still trim-correct → F4 and Track A expose *different* failure layers. See [[f4-per-example-diagnosis]] which sharpens the real capability floor to 8.5%.
- Live Track A (inference with `repetition_penalty`) was deprioritized — post-hoc result gave the answer. GPU compute was redirected to Phase 2 training.
