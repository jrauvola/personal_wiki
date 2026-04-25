---
type: experiment
title: "Branch 2 — Quora faithfulness probe (V2 bf16, step-k → y_final)"
slug: branch-2-quora-faithfulness-probe
status: partial
started: 2026-04-23
finished: 2026-04-23
hypothesis: "F5's swap-null is post-hoc commitment: a probe trained step-k → y_final should hit ≥0.90 agreement at k=0 if the model commits early, or rise monotonically if iterative."
parent: "[[f5-cross-example-kv-swap]]"
artifacts:
  - research_findings/quora_faithfulness_probe_v2_bf16.md
  - research_findings/quora_faithfulness_probe_v2_bf16.json
  - research_findings/quora_faithfulness_agreement_matrix.png
  - "script: scripts/quora_faithfulness/run_probe.py"
updated: 2026-04-25
---

# Branch 2 — Quora faithfulness probe

## Parent context

Direct child of [[f5-cross-example-kv-swap]]. F5's swap-null leaves three competing interpretations:
1. **Inert** — latents carry no answer-relevant content.
2. **Post-hoc** — the model commits to its answer at position 0 and the rest is rationalization (Ouro §7.2 framing on Qwen3-4B-Thinking shows step-0 probe AUC ≈ 0.99 = post-hoc).
3. **Iterative** — answer is computed across steps (Ouro §7.2: step 2 ↔ step 4 agreement 36% = iterative).

A position-wise probe `P_k : step-k features → y_final` should disambiguate via the agreement matrix `A_{ij}`.

## Hypothesis

If V2 bf16 is post-hoc, agreement-with-y_final ≥ 0.90 at k=0 with `A_{ij}` uniformly high. If iterative, agreement rises monotonically with k. If inert, agreement at chance for every k.

## Method

- **Constraint discovered:** local latent traces contain only logit-lens top-10 token ids/probs per step — no raw `h_{k, L}` hidden states (re-confirmed by F3 layer-wise agent: `latent_tap.py` only saves `outputs.hidden_states[-1]`). Fall back to a **token-level probe**.
- Features per position k: one-hot over observed top-1 token id at step k + raw top-10 token ids (10 floats) + top-10 probabilities (10 floats).
- Target y_final: first character of parsed predicted numeric answer (11 classes).
- Probe: `sklearn.linear_model.LogisticRegression(penalty='l2', C=1.0)`, stratified 5-fold CV, 1319 examples.
- SIM-CoT GPT-2 comparison: no local checkpoint / traces — skipped.

## Result

| k | macro-AUC (y_final) | agreement w/ y_final | binary-correct AUC | probe modal prediction |
|---|---|---|---|---|
| 0 | 0.5186 | 0.470 | 0.505 | `1` |
| 1 | 0.4888 | 0.470 | 0.599 | `1` |
| 3 | 0.4995 | 0.469 | 0.580 | `1` |
| 7 | 0.5317 | 0.470 | 0.627 | `1` |

`A_{ij}` mean off-diagonal = **0.999**, min 0.996. Looks post-hoc, but mechanically degenerate: **probe outputs constant `1` for every example**.

Reason — top-1 token takes ≤3 distinct values at 7/8 steps and 5 values only at step 3 (matches F3). y_final majority class (`1`) is 620/1319 = 47%; probes collapse to predicting `1`. Macro-AUC 0.49-0.53 (chance for 11-way). Binary-correct AUC 0.50-0.64 — small non-trivial signal at steps 2, 6, 7.

## Verdict

**Partial — data-starved, not diagnostic.** The logit-lens channel is template-only at every step (matches F3), so answer identity (if present) lives in the residual that `lm_head` dampens at non-terminal positions. F5's swap-null cannot be adjudicated from this token-level data. The literal `A_{ij} ≈ 1.0` is mechanical (constant predictions), not content agreement. To close: need a GPU re-dump of `outputs.hidden_states[-1][:, -1:, :]` at each latent step — 1319 × 8 × 2560 bf16 ≈ 54 MB, one-line `latent_tap.py` patch.

## Revert info

- Pure local analysis. Reversible by deleting:
  - `research_findings/quora_faithfulness_probe_v2_bf16.md` + `.json`
  - `research_findings/quora_faithfulness_agreement_matrix.png`
  - `scripts/quora_faithfulness/run_probe.py`
- The upstream latent-trace files are shared; do not delete.
- Once raw HS dump exists, the same script can be re-pointed at the new features.

## Follow-ups / branch-offs

- **Trivial re-dump** — persist `outputs.hidden_states[-1][:, -1:, :]` at each latent step. Spec is in the deliverable. Enables the proper Quora probe (post-hoc expects macro-AUC ≈ 0.99 at k=0; iterative expects monotone rise; inert expects chance).
- Once dumped, re-running the probe is local and cheap. Currently the rate-limiting step on disambiguating "post-hoc vs iterative vs inert" interpretation of the swap-null.
- Mechanistic explanation now mostly comes from [[branch-1-layer-asymmetric-probe]] — final-layer KV is template, mid-stack carries content.
