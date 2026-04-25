---
type: experiment
title: "Prediction degeneracy analysis — loop rate × accuracy decomposition"
slug: prediction-degeneracy-analysis
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "CODI's reported accuracy is mostly loop-lucky-match: loops happen to emit the right number first, then degenerate."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/prediction_degeneracy_analysis.md
  - research_findings/prediction_degeneracy.json
  - "script: latent_eval_training_harness/scripts/prediction_degeneracy_analysis.py"
updated: 2026-04-25
---

# Prediction degeneracy analysis

## Parent context

Branched off [[phase-1-v2-bf16-training]]. Sample inspection of V2 bf16 predictions revealed strings like `"The answer is: 100.00. Therefore, the answer is: 100.00..."` repeated 20+ times. Question: how much of CODI's reported accuracy is this kind of loop?

## Hypothesis

Detect whether each prediction contains a substring (≥15 chars) that repeats ≥3 times. Measure overall loop rate and split by correct/wrong outcome. If correct-loop rate is high and rises with num_latent, the rising num_latent curve is loop-driven, not reasoning-driven.

## Method

- Loop heuristic: longest substring of length ≥ 15 repeating ≥ 3× consecutively.
- Apply to all 4 CODI variants (Q-P0, Q-V2 bf16, Q-V2' fp32, Q-V3') × 3 benchmarks × 4 num_latent + zero-shot baseline.
- Decompose accuracy into loop-correct vs non-loop-correct.
- Cross-check zero-shot CoT (~0.86 GSM8k) — if loops are model-default, zero-shot should also loop heavily.

## Result

**Headline numbers:**

- Zero-shot CoT (Qwen3-4B base, 0.86 GSM8k): loop rate **<1%** on all 3 benchmarks. High accuracy comes from real reasoning.
- CODI variants — catastrophic loop mode:

| Variant | GSM8k overall loop rate (n=0/2/4/8) | GSM8k correct-loop rate (n=0/2/4/8) |
|---|---|---|
| Q-P0 | 44/46/46/45% | 62/67/68/67% |
| **Q-V2 bf16** | **58/69/77/81%** | **55/72/74/82%** |
| Q-V2' fp32 | 47/67/81/84% | 51/76/89/90% |
| Q-V3' | 55/55/55/55% | 78/75/75/75% |

SVAMP at num_latent=8: V2' fp32 has **92.3% correct-loop rate**.

**V2 bf16 num_latent=0 vs n=8 decomposition (GSM8k):**

| n | correct | correct-loop rate | non-loop correct | non-loop accuracy |
|---|---|---|---|---|
| 0 | 159 | 55% | 71 | 5.4% |
| 8 | 214 | 82% | 38 | **2.9%** |

**The rising curve INVERTS once loop-correct is stripped: non-loop accuracy 5.4% → 2.9%.**

## Verdict

**Success — definitive identification of loop-emission as the dominant accuracy mechanism.**

1. "CODI at 4B has rising latent-utility curves" is FALSE as stated. It is a loop-emission artifact.
2. Capability collapse is sharper than initially thought — the ~15% reported accuracy is mostly loop-lucky matches; <5% is real reasoning.
3. Zero-shot's <1% loop rate confirms this is a CODI-specific failure mode, not a base-model issue.
4. Phase 2 becomes pass-fail: do SIM-CoT / LT-Tuning prevent loop mode? If they also loop at 80%, capability-collapse is deeper than any targeted method.

V2 bf16's "win" over V2' fp32 explained: same 80% correct-loop rate, but bf16's digit attractor (`0`) aligns with GSM8k/SVAMP target distribution, fp32's (`2`) does not.

## Revert info

- Pure analysis. Reversible by deleting:
  - `research_findings/prediction_degeneracy_analysis.md`
  - `research_findings/prediction_degeneracy.json`
  - `latent_eval_training_harness/scripts/prediction_degeneracy_analysis.py`
- Loop-detection heuristic is reused by [[f4-per-example-diagnosis]] and the F2 loop content analysis; the script can stay even if this report is removed.

## Follow-ups / branch-offs

- Triggered the F1-F6 inert-latent battery (F1, F2, F3, F4, F5, F6).
- Triggered [[track-a-first-sentence-trim]] — the post-hoc trim regrade that flattens the rising curve.
- Loop-rate metric is the key Phase 2 pass-fail criterion: a working V3 must reduce loop rate meaningfully below zero-shot's 1% bar.
