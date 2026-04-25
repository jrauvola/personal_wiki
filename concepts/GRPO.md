---
type: concept
title: "GRPO — Group Relative Policy Optimization"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/concept
  - method/reinforcement-learning
status: developing
complexity: advanced
domain: reinforcement-learning
aliases:
  - "Group Relative Policy Optimization"
related:
  - "[[CoLaR]]"
  - "[[Adaptive Latent RL]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "RL post-training is orthogonal to CPF fusion experiment."
  - slug: "branch-a"
    relevance: reference
    why: "RL optimization layer is separate from the architecture-dependence finding."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a grad-stability concern."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Recurring optimization mechanism across compression-first and adaptive-compute families; useful in the taxonomic writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# GRPO — Group Relative Policy Optimization

The reinforcement learning algorithm used across multiple latent reasoning post-training recipes to optimize policies in the continuous space without external value networks.

## Shared pattern across sources

A batch of sampled outputs per query is used to compute relative advantages against a group baseline, driving the policy toward operational efficiency using composite rewards that trade off task accuracy and reasoning-chain length.

### [[CoLaR]] usage

- Multiple latent output trajectories sampled per query.
- Relative advantages computed via composite reward: heavy reinforcement of mathematical accuracy plus penalty on total continuous reasoning chain length.
- Drives the policy toward maximum operational efficiency.

### [[Adaptive Latent RL]] usage

- Length penalty $\lambda_{penalty}$ applied when a batch achieves uniform mathematical correctness (trivial problem → truncate reasoning).
- Length reward $\lambda_{reward}$ applied when accuracy is mixed/poor (complex problem → allocate deeper exploration).
- Optimizes a halting-head classifier without requiring human-annotated stopping datasets.

## Cross-references

Sources that use GRPO: [[CoLaR]], [[Adaptive Latent RL]].
