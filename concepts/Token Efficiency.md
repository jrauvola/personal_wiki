---
type: concept
title: "Token Efficiency"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/concept
  - optimization
status: developing
complexity: basic
domain: latent-reasoning
aliases:
  - "Compression Ratio"
  - "Inference Efficiency"
  - "Chain-Length Reduction"
related:
  - "[[CODI]]"
  - "[[SIM-CoT]]"
  - "[[CoLaR]]"
  - "[[Adaptive Latent RL]]"
  - "[[PonderLM-3]]"
  - "[[LaSER]]"
  - "[[KV Compression]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Token efficiency gains are a secondary benefit of fusion recipes; not the primary CPF experiment target."
  - slug: "branch-a"
    relevance: secondary
    why: "Efficiency metrics accompany scaling findings."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach/grad-stability ablations."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology debugging."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "A primary axis along which latent reasoning improves over explicit CoT; essential for the writeup framing."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Token Efficiency

A shared axis along which latent reasoning methods are evaluated: the ratio of inference tokens / reasoning chain length / forward passes required relative to explicit text CoT baselines.

## Representative numbers from the survey

| Method | Claim |
|---|---|
| [[CODI]] | 3.1x compression rate while matching explicit text reasoning on GSM8K at GPT-2 scale. |
| [[SIM-CoT]] | 2.3x token efficiency advantage while exceeding explicit reasoning baselines by 2.1%. |
| [[CoLaR]] | RL on complex math: -82.8% chain length with +5.4% accuracy. User-tunable runtime compression factor. |
| [[Adaptive Latent RL]] | On GSM8K-Aug: -52.94% total reasoning tokens with +0.38% accuracy. |
| [[PonderLM-3]] | Steeper perplexity-compute Pareto frontier by routing pondering steps only to complex tokens. |
| [[LaSER]] | BRIGHT benchmark: matches explicit CoT deductive depth with a fraction of latent tokens. |

## Paradigms

- **Compression-first** — [[CoLaR]]: explicitly force one latent vector to encapsulate multiple consecutive vocabulary tokens.
- **Adaptive compute** — [[Adaptive Latent RL]], [[PonderLM-3]]: halt/continue based on query or token complexity.
- **Latent-native baseline** — [[CODI]], [[COCONUT]], [[SIM-CoT]]: efficiency emerges from bypassing vocabulary projection, not explicit compression.
- **KV compression** — see [[KV Compression]] for memory-side efficiency.

## Cross-references

Sources linking efficiency as a load-bearing claim: [[CODI]], [[SIM-CoT]], [[CoLaR]], [[Adaptive Latent RL]], [[PonderLM-3]], [[LaSER]].
