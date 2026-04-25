---
type: concept
title: "Context-Prediction-Fusion"
created: 2026-04-22
updated: 2026-04-24
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/anti-collapse
  - mechanism/fusion
status: developing
complexity: advanced
domain: latent-reasoning
aliases:
  - "CPF"
  - "Context Prediction Fusion"
related:
  - "[[Feature Collapse]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Dynamic Switching Protocol]]"
  - "[[Curriculum Distillation]]"
  - "[[HRPO]]"
  - "[[ThinkRouter]]"
  - "[[Mull-Tokens]]"
sources:
  - "[[Latent Thoughts Tuning]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "The mechanism Branch D is designed to implement on CODI."
  - slug: "branch-a"
    relevance: secondary
    why: "Anti-collapse mechanism worth understanding when analyzing Qwen3 scaling behavior."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach/BPTT axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No bearing on Qwen3 probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Core anti-collapse mechanism for the writeup's synthesis roadmap."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Context-Prediction-Fusion

Mechanism from [[Latent Thoughts Tuning]] that interpolates recurrent context hidden states with vocabulary-prior embeddings, anchoring latent trajectories to the discrete token manifold.

## Formula

```
e_fusion = α · h_{t−1, I} + (1 − α) · e_pred

where  e_pred = ∑_{w ∈ V} P̂(w) · E(w)
```

- `h_{t−1, I}` — hidden state from layer I at previous step (the "context")
- `e_pred` — probability-weighted sum of vocabulary embeddings (the "prediction anchor")
- `α` — tunable coefficient; LT-Tuning uses intermediate α

## Intuition

**Without fusion:** raw hidden states `h` recur back into the input layer. If the input/output embeddings are untied, `h` lives in a different geometric space than the embedding table expects → geometric distribution mismatch → [[Feature Collapse]].

**With fusion:** `e_pred` is computed as a weighted average of *actual* embedding vectors — so it's guaranteed to live inside the embedding manifold. Mixing a fraction of `e_pred` into every recurrent input pulls the trajectory back toward vocabulary-space each step, preventing drift.

## Curriculum position

CPF is introduced in **Stage 3** of LT-Tuning's three-stage curriculum — not from step 1. Stages 1 and 2 establish baseline step-decomposition and acclimate attention to recurrent inputs respectively. Stage 3 swaps raw `h` for `e_fusion` and is load-bearing: ablation shows **23.5% accuracy degradation at 8B** if Stage 3 is removed.

## Comparison to other anti-collapse mechanisms

| Mechanism | Source | Where it acts |
|---|---|---|
| CPF (this page) | [[Latent Thoughts Tuning]] | Input embedding (fusion with vocab prior) |
| Auxiliary decoder | [[SIM-CoT]] | Training-only loss on latent states |
| KV-cache distillation | [[KaVa]] | Key-value supervision across layers |
| Cross-modal regularization | [[ReGuLaR]] | Variational prior from rendered-CoT images |

CPF is distinctive in being (a) inference-time active (not training-only), (b) embedding-space rather than loss-space, (c) parameter-free additional supervision.

## Open questions

- Does CPF help below 8B? Paper shows gains but the *collapse-prevention* framing is scale-dependent.
- How does α interact with embedding tying? LT-Tuning tested on Llama (untied); behavior on tied-embedding architectures (Gemma-3) is untested.
- Can CPF compose with SIM-CoT's auxiliary decoder or KaVa's KV distillation? No published composition.

## Branch D notes

See [[meta/projects/branch-d]] for implementation plans on CODI. Primary open questions for our implementation:
- α schedule: fixed or learned?
- Layer index I for extracting `h_{t−1, I}`: final layer or intermediate?
- Interaction with existing CODI V2 KV/latent detach strategies.

## Related hybrid/fusion mechanisms (downstream literature)

Crawl 2026-04-23 (HRPO downstream) identified two additional data points in the fusion design space:

- **[[HRPO]]** — `e_fusion = g(ctx) · h_hidden + (1 − g(ctx)) · e_token`, where `g` is LEARNED and context-dependent (vs CPF's fixed/scheduled α), trained by RL with a progressive token→hidden curriculum. Independently rediscovers the same functional form as CPF.
- **[[ThinkRouter]]** — not a fusion; a BINARY route between soft-embedding and discrete-token sampling based on `p_t^max < τ`. Inference-time, training-free. Exposes a distinct failure mode of the `e_pred` primitive (noise accumulation from low-confidence aggregation) that CPF's α-interpolation may or may not mitigate — open question for branch-d.
- **[[Mull-Tokens]]** — three-stage curriculum with dual-modality anchoring (LM-head for text / frozen encoder for image) at warm-up stage; RL refinement at stage 3. Validates the curriculum family beyond text.

These independently convergent discoveries strengthen the case that fusion of a context signal with a vocabulary-anchored / target-anchored prediction signal is a robust inductive bias for latent reasoning.

## Motivating evidence from SPAR F-tests (2026-04-23)

The SPAR F1-F6 inert-latent battery on CODI V2 bf16 (Qwen3-4B-Instruct-2507, `num_latent=8`) provides direct motivation for CPF-style anchoring. F3's per-latent-position logit-lens analysis over 1319 GSM8k dumped traces shows that 7 of 8 latent positions decode to a fixed template `The → 0 → 0 → ? → . → . → . → .` with <0.4 bits of cross-example entropy — the latent rollout is emitting a position-invariant template rather than per-step computation. This is precisely the failure mode CPF is designed to prevent: without fusion back into the vocabulary manifold, the latent trajectory drifts into a content-free routing role (see [[Routing vs Reasoning]]).

CPF's `e_fusion = α · h_ctx + (1 − α) · e_pred` anchors each latent step against the embedding layer, so that drift toward a fixed-template attractor imposes measurable fidelity cost. The 5-way convergence of CPF-adjacent fusion mechanisms — LT-Tuning's α-interpolation, [[HRPO]]'s learned gate, [[Mull-Tokens]]' dual-modality anchor, [[ThinkRouter]]'s binary route, and [[SIM-CoT]]'s auxiliary decoder — suggests a shared inductive bias: latent-reasoning architectures need an anchor back to a discrete or vocabulary-space signal to avoid collapsing into a routing-only regime. See `research_findings/inert_latent_hypothesis_tests.md` for the full battery and `PROJECT_STATE.md` entries for the 5-way convergence.

## Middle-layer anchoring candidate (2026-04-24)

Branch 1's layer-asymmetric probe (`research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md`, 500 GSM8k × 37 layers, V2 bf16 Qwen3-4B step 3) identifies a viable **middle-layer CPF anchor target**. Per-layer geometric dispersion peaks at L22-L30 — median pair cos 0.966 at L28, top-1 PC variance 0.137 at L30, 95%-PC count 213 at L22 — before re-collapsing at L31-L36 to the final-layer template (L36: pair cos 0.989, top-1 PC 0.310, 95%-PC count 82). The mid-stack carries per-example reasoning content the last 6 layers compress away. Implication for the LT-Tuning [[Context-Prediction-Fusion]] formula `e_fusion = α · h_{t-1, I} + (1 − α) · e_pred`: layer index `I ≈ 28-30` is the empirical sweet-spot for V3 — chosen *before* the L31→L36 re-collapse (L35 already half-collapsed at top-1 PC 0.160), and well above the LT-Tuning paper's default of final-layer hidden. Cross-references [[Routing vs Reasoning]] § Layer-asymmetric refinement and [[meta/projects/branch-d]]. Open-question 2 ("layer index I") in the Branch-d implementation list now has a candidate answer pending logit-lens / linear-probe confirmation.
