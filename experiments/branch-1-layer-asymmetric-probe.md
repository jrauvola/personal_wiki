---
type: experiment
title: "Branch 1 — Layer-asymmetric probe (V2 bf16, step 3, 500 GSM8k × 37 layers)"
slug: branch-1-layer-asymmetric-probe
status: success
started: 2026-04-24
finished: 2026-04-24
hypothesis: "F3's template-lock is a final-layer readout artifact; mid-stack preserves per-example geometric variation."
parent: "[[f3-trace-variance]]"
artifacts:
  - research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md
  - research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.json
  - research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe.png
  - research_findings/layer_probe/v2_bf16_step3/analyze.py
  - research_findings/layer_probe/v2_bf16_step3/hidden_all_layers/
updated: 2026-04-25
---

# Branch 1 — Layer-asymmetric probe

## Parent context

Direct child of [[f3-trace-variance]]. F3 found 7/8 latent positions are template-only at the *final-layer* logit lens (top-1 entropy ≤0.5 bits). Open question: is this template lock a property of the model's internal state (template all the way down), or only the final-layer readout (mid-stack carries content that gets compressed before the unembed)?

## Hypothesis

- **H1 (readout artifact, CONFIRM):** mid-stack layer exhibits meaningfully higher cross-example variation than final layer → template lock is readout-only.
- **H0 (template all the way down, KILL):** per-layer geometric dispersion monotone-decreases from input to final → no mid-stack asymmetry.

## Method

- Variant: V2 bf16, num_latent=8, step 3 (the one F3 position with non-trivial entropy).
- 500 GSM8k examples dumped on GH200 via per-layer `outputs.hidden_states[l][:, -1:, :]` capture; pulled to local fp16 `(37, 2560)` arrays.
- All 500 stacked into `H ∈ ℝ^{500×37×2560}` (fp32 for analysis; fp16 mid-stack norms overflow).
- Per-layer geometric metrics: median pairwise cosine, top-1 PC variance fraction, RMS-over-centroid, 95%-PC count.
- Logit-lens-per-layer entropy NOT computed: Qwen3-4B-Instruct-2507 uses tied embeddings; only shard 3/3 is locally cached (missing `model.embed_tokens.weight` in shard 1). Geometric diagnostics suffice for the kill-vs-confirm question. Logit lens is the designated follow-up.

## Result

Four independent geometric-dispersion metrics over all 500 examples × 37 layers all trace a clean U: dispersion grows through the stack, peaks around **L22-L30**, then **re-collapses** over the last 5 layers. Final L36 is a local max of template collapse, not the tail of monotone decay.

| Metric | Final L36 | Mid-stack peak/trough | Layer | Ratio |
|---|---|---|---|---|
| Median pairwise cos | **0.9888** | 0.9662 (trough) | L28 | Δ = 0.023 |
| Top-1 PC variance frac | **0.310** | 0.137 (trough) | L30 | final = 2.27× trough |
| RMS / centroid | **0.120** | 0.194 (peak) | L28 | — |
| 95%-PC count | **82** | 213 (peak) | L22 | final = 38.5% of peak |

Eval summary alongside the dump: 500/500 examples completed at 18.6% accuracy (matches V2 bf16 num_latent=8 baseline at this slice).

## Verdict

**Success — CONFIRM.** The mid-stack carries per-example geometric content; the last 6 layers compress that content into the routing template before it is written to KV cache. F5's swap-null is therefore mechanistically explained — swapping final-layer KV swaps two copies of the template. The "template" characterization (F3) belongs to the decoder-facing readout, not the model's internal state. **V3 implication:** middle-layer [[concepts/Context-Prediction-Fusion]] is on the table — anchor target `h_{t-1, L≈28-30}`, placed *before* the L31→L36 re-collapse (L35 already half-collapsed at top-1 PC = 0.160). Resolves the deferred F3 layer-wise item from 2026-04-23.

## Revert info

- Pure analysis on local data. Reversible by deleting:
  - `research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md` + `.json` + `.png`
  - `research_findings/layer_probe/v2_bf16_step3/analyze.py`
  - `research_findings/layer_probe/v2_bf16_step3/hidden_all_layers/` (500 raw fp16 dumps, ~190 MB)
- GPU dump was a one-shot: code patch in `latent_tap.py` to capture `hidden_states[l]` for all 36 layers at step 3 was applied during the 500-example sub-eval, not committed to main. No upstream code change to revert.
- The eval summary at `research_findings/layer_probe/v2_bf16_step3/eval/` is also deletable.

## Follow-ups / branch-offs

- Logit-lens-per-layer entropy: deferred follow-up. Required: download Qwen3-4B shard 1/3 (~8 GB) for `embed_tokens.weight`, then project per-layer hidden state through tied lm_head. Designated as next-step.
- Wiki refs: [[concepts/Routing vs Reasoning]] §"Layer-asymmetric refinement", [[concepts/Feature Collapse]] §"Branch-1 layer-wise result", [[concepts/Context-Prediction-Fusion]] §"Middle-layer anchoring candidate".
- Resolves [[f3-layer-wise-step3]] (the deferred logit-lens-per-layer experiment) at the geometric level. The full logit-lens version remains deferred.
