---
type: experiment
title: "F3 — Per-latent-position trace variance (logit lens)"
slug: f3-trace-variance
status: success
started: 2026-04-22
finished: 2026-04-22
hypothesis: "If latents propagate per-example computation across iteration steps, top-1 logit-lens token should vary across examples at every step. Low entropy = template-only."
parent: "[[phase-1-v2-bf16-training]]"
artifacts:
  - research_findings/inert_latent_hypothesis_tests.md
  - research_findings/f1_f2_f3_inert_latent_tests.md
  - research_findings/inert_latent_F1_F2_F3.json
  - research_findings/latent_traces/qwen3_4b_codi_bf16_kv_latent_detach_last_2/gsm8k/numlatent_8/
updated: 2026-04-25
---

# F3 — Per-latent-position trace variance

## Parent context

Third local test in the F1-F6 battery, branched off [[phase-1-v2-bf16-training]]. The dumped latent traces (from the Phase 1 eval extension that captured logit-lens top-10 per latent step) make this analysis local-only.

## Hypothesis

If V2's 8 latent positions encode iterative reasoning, the top-1 token at each position should vary across examples (high entropy). Low entropy at most positions = template-only decoded output, refuting the iterative-reasoning framing at the logit-lens layer.

## Method

- Variant: V2 bf16, num_latent=8, GSM8k (1319 dumped traces).
- For each latent step (0-7), tabulate the top-1 token id across examples; compute Shannon entropy in bits, top-1 fraction, unique top-1 count, top-5.

## Result

| Step | unique top-1 | entropy (bits) | dominant token | dominant fraction |
|---|---|---|---|---|
| 0 | 3 | **0.018** | `The` | 99.85% |
| 1 | 3 | **0.052** | `0` | 99.47% |
| 2 | 2 | **0.299** | `0` | 94.69% |
| 3 | 5 | **1.493** | `0` | 54.28% |
| 4 | 3 | **0.389** | `.` | 93.40% |
| 5 | 2 | **0.009** | `.` | 99.92% |
| 6 | 1 | **0.000** | `.` | 100.00% |
| 7 | 1 | **0.000** | `.` | 100.00% |

Decoded template (top-1 per position): `The → 0 → 0 → 0/1/. → . → . → . → .`

Only step 3 has non-trivial cross-example variation (1.49 bits, three-way mix of `0`, `1`, `.`); steps 0, 5, 6, 7 effectively deterministic; steps 1, 2, 4 dominated by a single token at ≥93%.

## Verdict

**Success — 7 of 8 latent positions are template-only at the final-layer logit-lens.** The latent rollout is not propagating per-example computation through multiple iteration steps; at most one step (index 3) shows any cross-example signal, and that signal is a three-way digit branch, not a continuous reasoning trace. F3 is the strongest single piece of evidence for the template-routing characterization. *Caveat:* this is a final-layer readout; mid-stack content was the open question that motivated [[branch-1-layer-asymmetric-probe]] (which CONFIRMed the readout-artifact framing).

## Revert info

- Pure analysis. Reversible by deleting `research_findings/inert_latent_F1_F2_F3.json` and the F3 sections in the synthesis md files.
- The latent-trace dumps (`research_findings/latent_traces/.../numlatent_8/trace_*.jsonl`) are also used by [[branch-2-quora-faithfulness-probe]] and [[f3-layer-wise-step3]] — do not delete unless those follow-ups are also being reverted.
- Script: `latent_eval_training_harness/scripts/f1_f2_f3_inert_latent_tests.py`.

## Follow-ups / branch-offs

- [[f3-layer-wise-step3]] — deferred per-layer entropy analysis (needs GPU re-dump of `outputs.hidden_states[l]` for all 36 layers).
- [[branch-1-layer-asymmetric-probe]] — geometric-dispersion probe at all 37 layers; CONFIRMed F3 is a final-layer readout artifact.
- [[branch-2-quora-faithfulness-probe]] — token-level Quora probe constrained to F3's same logit-lens channel; data-starved.
