---
type: experiment
title: "F4 per-example diagnosis × Track A trim stacking"
slug: f4-per-example-diagnosis
status: success
started: 2026-04-23
finished: 2026-04-23
hypothesis: "F4-lost 88 examples are exactly the loop-lucky-match population that Track A trim also kills. If so, F4 alone gives the real capability floor."
parent: "[[f4-latent-kv-ablate]]"
artifacts:
  - research_findings/f4_per_example_diagnosis.md
  - research_findings/f4_per_example_diagnosis.json
updated: 2026-04-25
---

# F4 per-example diagnosis × Track A trim stacking

## Parent context

Direct child of [[f4-latent-kv-ablate]]. F4 dropped GSM8k accuracy 0.163 → 0.122, removing 88 baseline-correct predictions. The synthesis question: are those 88 the same population that [[track-a-first-sentence-trim]] also kills (loop-lucky-match), or a different failure mode?

## Hypothesis

If F4-lost = Track-A-trim-wrong, F4 is exposing exactly the loop-lucky-match component, and F4's 12.2% accuracy = V2's "real" capability floor. If F4-lost are mostly Track-A-trim-correct, the two tests expose different failure layers and the real floor is the *intersection* (lower than either alone).

## Method

- Pure local analysis: join baseline (215 correct) + F4-ablate (161 correct) predictions on all 1319 GSM8k example_ids.
- Sets: `preserved = baseline_correct ∧ F4_correct`; `lost = baseline_correct ∧ ¬F4_correct`; `gained = ¬baseline_correct ∧ F4_correct`.
- Re-derive per-example features: loop detection (≥15-char substring repeating ≥3×), target-in-loop, Track A trim grade.
- Cross-tab F4 outcome × Track A trim outcome on the baseline-correct slice (n=215).

## Result

Set sizes: `preserved=127`, `lost=88`, `gained=34`.

Lost-88 has the highest target-in-loop fraction (94.3%) and longest mean loop substring — exactly the population the open question predicted. **But 76/88 (86%) of the F4-lost are still Track-A-trim-correct.** F4 and Track A expose *different* failure layers, not the same one.

Headline cross-tab (baseline-correct slice, n=215):

|  | trim-correct | trim-wrong | total |
|---|---|---|---|
| F4-correct (preserved) | **112** | 15 | 127 |
| F4-wrong (lost) | 76 | 12 | 88 |
| total | 188 | 27 | 215 |

- Preserved ∩ Track-A-trim-correct = 112 → **"both-survive" floor = 112 / 1319 = 8.5%**.
- Below F4 alone (12.2%) and Track A alone (10.8%).
- Gained-34: 11/34 trim-correct on baseline → 24/34 trim-correct on F4 (ablation sanitized a degenerate first sentence).

## Verdict

**Success — sharpened capability floor.** F4 and Track A are *complementary*, not redundant. Track A's 10.8% trimmed accuracy ≈ "model's first-sentence declarative answer is right"; F4's 12.2% ≈ "removing latent KV did not destroy the answer." Stacking gives the **real floor of 8.5%** — predictions whose first sentence is right AND whose latent KV was not load-bearing for that first sentence. Phase 2 needs to clear ~15% on GSM8k to credibly beat the template-routing substrate. This is the strictest local capability bound on V2 bf16.

## Revert info

- Pure analysis. Reversible by deleting `research_findings/f4_per_example_diagnosis.md` + `.json` (≈800 KB).
- The upstream raw prediction files are shared; do not touch.

## Follow-ups / branch-offs

- Feeds the Phase 2 pass-fail criterion: any intervention (LT-Tuning, SIM-CoT, V3 composite) must clear ~15% on GSM8k to beat the substrate.
- Wiki refs: [[concepts/Routing vs Reasoning]] §"Sharpened floor"; [[concepts/Loop-Mode Emission]] §"Stacked diagnostic".
