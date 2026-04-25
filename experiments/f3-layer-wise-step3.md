---
type: experiment
title: "F3 layer-wise — step-3 entropy across layers 0-31 (deferred)"
slug: f3-layer-wise-step3
status: planned
started: 2026-04-23
finished: pending
hypothesis: "Earlier-layer hidden state at latent step 3 carries more per-example variation than the final layer's 1.49 bits."
parent: "[[f3-trace-variance]]"
artifacts:
  - research_findings/f3_layerwise_step3.md
  - research_findings/f3_layerwise_step3.json
updated: 2026-04-25
---

# F3 layer-wise — step 3 across layers

## Parent context

Direct child of [[f3-trace-variance]]. F3's final-layer logit lens found 1.49 bits at step 3, ≤0.4 bits at the other 7 positions. Open question: is the final-layer template a property of the model's internal computation, or only the readout? A logit-lens entropy curve `layer → entropy(top-1 distribution at step 3)` would directly answer this.

## Hypothesis

- **H1 (layer-wise template commit):** early layers (0-15) show materially higher cross-example entropy than final layer's 1.49 bits, dropping monotonically through the stack as template compression takes over. Routing key is assembled mid-stack, not end-to-end template.
- **H0 (template all the way down):** entropy is low at every layer, or rises only at the very last layers. Routing key is template from embedding stage onward.

## Method (planned)

For each of 1319 V2 bf16 num_latent=8 GSM8k examples at latent step 3:
1. Load per-layer hidden state at the final latent-position token, all 36 transformer layers.
2. Logit-lens project each layer through tied `lm_head` (= `embed_tokens.weight`, bf16, [151936, 2560]).
3. Per layer, tabulate top-1 token distribution, top-1 fraction, unique top-1 count, Shannon entropy in bits.
4. Report layer-wise curve.

## Result

**Deferred — local data insufficient.**

- `latent_tap.py` captures only `outputs.hidden_states[-1]` (final layer); no per-layer dump for any of the 1319 traces.
- KV dumps in `research_findings/kv_pca/` are `final_layer_only=True` and only 200 examples.
- Qwen3-4B-Instruct-2507 HF cache has only shard 3/3 — no `embed_tokens` / tied `lm_head`.

Final-layer anchor re-verified across all 1319 examples (matches published F3 exactly): step 3 entropy **1.493 bits**, top-1 `0` at 54.3%, top-5 `0/1/./2/=` = 716/322/273/7/1.

[[branch-1-layer-asymmetric-probe]] resolved the underlying question at the *geometric* level (mid-stack carries content, last 6 layers re-collapse) — the logit-lens-per-layer extension would add a redundant token-level confirmation and a per-layer top-1 token table.

## Verdict

**Deferred / not run.** Geometric resolution from Branch 1 is sufficient to answer the kill-vs-confirm of the underlying H1 vs H0. The logit-lens version is now nice-to-have. Spec for the GPU dump is in the deliverable: one-line patch to `latent_tap.py` saving `outputs.hidden_states[l][:, -1:, :]` for all 36 layers, ~361 MB fp16, <10% eval wall-clock overhead. Plus shard 1/3 download (~8 GB) for `embed_tokens`.

## Revert info

- Reversible by deleting `research_findings/f3_layerwise_step3.md` + `.json`. Documents only — no code changes, no compute spent.

## Follow-ups / branch-offs

- Bundled with [[branch-1-layer-asymmetric-probe]]'s deferred logit-lens extension. The same GPU dump (per-layer hidden states at step 3) feeds both.
- Resolves the "what does mid-stack look like under logit lens" question once dumped.
