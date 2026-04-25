---
type: concept
title: "Dynamic Switching Protocol"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/latent-reasoning
  - mechanism/adaptive-compute
status: seed
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Confidence-Threshold Switching"
  - "Confidence-Gated Latent Insertion"
related:
  - "[[Latent Thoughts Tuning]]"
  - "[[Adaptive Latent RL]]"
  - "[[Adaptive Exit Gate]]"
  - "[[PonderLM-3]]"
  - "[[Token Efficiency]]"
sources:
  - "[[Latent Thoughts Tuning]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Adaptive-compute gating is an extension beyond core CPF; worth understanding but not the Branch D implementation target."
  - slug: "branch-a"
    relevance: reference
    why: "Not specific to Qwen3 scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Orthogonal to detach/BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Part of the adaptive-compute taxonomy; taxonomic placeholder."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Dynamic Switching Protocol

Mechanism from [[Latent Thoughts Tuning]] that gates between discrete-token generation and latent `<thinking>` phases based on prediction confidence.

## Mechanism

At each step, the model evaluates the confidence of its next-token prediction (e.g., max softmax probability). If confidence is below threshold τ, the model inserts a `<thinking>` latent token instead of emitting a discrete token. The latent state then reasons continuously until confidence recovers, at which point the model emits a discrete token again.

## Effect

Adaptive allocation of compute:
- **Easy problems:** high confidence throughout → few or no latent tokens → near-instant response.
- **Hard problems:** low-confidence positions trigger latent phases → model spends more compute on difficult sub-steps.

Empirically: LT-Tuning allocates more latent tokens to harder problems without external halting networks.

## Comparison to other adaptive-compute methods

| Method | Gating signal | Training |
|---|---|---|
| Dynamic switching (this page) | Prediction confidence | Part of LT-Tuning Stage 2 curriculum |
| [[Adaptive Latent RL]] | Binary halting head | RL post-training (GRPO) |
| [[Adaptive Exit Gate]] (Ouro) | Per-step exit probability | Joint with main training |
| [[PonderLM-3]] | Differentiable token-dependent attention mask | Pretraining-time |

Dynamic switching is distinctive in using *intrinsic* prediction confidence (no added parameters) vs. the others which add a halting network or gate.

## Open questions

- How is τ chosen — fixed, learned, or annealed through the curriculum?
- Does confidence-based gating correlate with actual problem difficulty or just with training-distribution frequency?
- Stability when combined with CPF: does CPF's fusion with vocabulary prior make confidence less informative?
