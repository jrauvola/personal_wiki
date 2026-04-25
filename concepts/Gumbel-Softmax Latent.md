---
type: concept
title: "Gumbel-Softmax Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/stochastic-latent
  - method/gumbel-softmax
status: developing
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Gumbel-Softmax continuous reasoning"
  - "Stochastic latent sampling"
related:
  - "[[Latent-SFT]]"
  - "[[LEPO]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[MARCOS]]"
  - "[[CoLaR]]"
  - "[[Feature Collapse]]"
  - "[[Multiplex Thinking]]"
  - "[[LaDi-RL]]"
  - "[[SeLaR]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Alternative mechanism to CPF for anti-collapse; Gumbel-Softmax injects diversity at the sampling level while CPF anchors at the embedding level."
  - slug: "branch-a"
    relevance: reference
    why: "Stochasticity layer; applicable at inference or training but not architecture-core."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Unifying mechanism across four independently-invented recipes — central concept for the writeup's taxonomy."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Gumbel-Softmax Latent Reasoning

Unifying mechanism for stochastic continuous reasoning. Multiple independently-invented recipes use Gumbel-Softmax (or closely equivalent reparameterization) to inject controlled randomness into the latent reasoning trajectory:

| Paper | Use |
|---|---|
| [[Stochastic Soft Thinking]] (2508.03440) | Inference-time: breaks the Greedy Pitfall in soft-thinking |
| [[Latent-SFT]] (2510.15522) | Training-time: learns superposition of reasoning paths during SFT |
| [[LEPO]] (2604.17892) | RL-time: maintains diversity across rollout for policy gradient |
| [[MARCOS]] (2509.25020) | Generative: variational transitions in a Markov chain (related but not identical) |
| [[Multiplex Thinking]] (2601.08808) | RL-time: K-sample aggregation in vocab embedding space; self-adaptive width |
| [[LaDi-RL]] (2602.01705) | RL-time: latent-diffusion multi-step denoising distributes stochasticity |

[[CoLaR]] uses a *Gaussian* latent head rather than Gumbel-Softmax, but serves the same anti-collapse role. [[SeLaR]] and [[LEAD]] use entropy-gated soft embeddings (closely related — probability-weighted aggregation + contrastive push-away from top-1).

## Why it works

Deterministic latent inference suffers [[Feature Collapse]] and/or the Greedy Pitfall (see [[Stochastic Soft Thinking]]): top-1 tokens dominate successive steps, suppressing alternative paths. Gumbel-Softmax with temperature τ samples categorically from the softmax distribution while remaining differentiable (straight-through estimator). Setting τ > 0 injects exploration noise; τ → 0 recovers deterministic argmax.

## Equation (schematic)

Given logits `ℓ`, Gumbel noise `g_i ~ Gumbel(0, 1)`:

`y_i = softmax((ℓ_i + g_i) / τ)`

Straight-through: forward uses argmax(y), backward uses the softmax gradient.

## Relation to CPF

[[Context-Prediction-Fusion]] (LT-Tuning) and Gumbel-Softmax latent are **two independent solutions** to feature collapse:
- CPF anchors: `e_fusion = α · h_ctx + (1 − α) · e_pred` — anchor latent to vocabulary manifold.
- Gumbel: inject sampling noise, break the greedy feedback loop.

Neither supersedes the other; they could in principle stack.

## Sources

- [[Stochastic Soft Thinking]] — mechanism analysis + inference-time fix.
- [[Latent-SFT]] — SFT-phase use with Latent-Vocab constraint.
- [[LEPO]] — RL-phase use with unified gradient estimator.
- [[MARCOS]] — variational analogue.
- [[CoLaR]] — Gaussian sampling (sibling mechanism).
- [[Multiplex Thinking]] — top-K sampling into multiplex token; self-adaptive width.
- [[LaDi-RL]] — latent-diffusion RL; distributes stochasticity across denoising trajectory.
- [[SeLaR]] — entropy-gated soft + contrastive anti-collapse (training-free).
