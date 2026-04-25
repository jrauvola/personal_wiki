---
type: source
title: "Visual Enhanced Depth Scaling for Multimodal Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/multimodal
  - type/source
  - method/gradient-dynamics
  - method/adaptive-depth
  - method/curriculum
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[Think-at-Hard]]"
  - "[[CODI]]"
  - "[[COCONUT]]"
sources:
  - "[[.raw/papers/2604.10500-visual-enhanced-depth-scaling]]"
source_type: paper
arxiv_id: "2604.10500"
venue: "arXiv"
date_published: 2026-04-12
authors:
  - "Yudong Han"
  - "Yong Wang"
  - "Zaiquan Yang"
  - "Zhen Qu"
  - "Liyuan Pan"
  - "Xiangxiang Chu"
url: "https://arxiv.org/abs/2604.10500"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "Visual tokens exhibit significantly higher and more volatile gradient norms than their textual counterparts due to inherent language bias, resulting in systematic visual under-optimization."
  - "Semantically simple tokens converge rapidly, whereas complex tokens exhibit persistent gradient instability constrained by fixed architectural depths."
  - "A visual replay module leverages causal self-attention to estimate token saliency, reinforcing fine-grained grounding through spatially-coherent constraints."
  - "Routing depth scaling adaptively allocates additional reasoning steps to complex tokens, enabling deeper contextual refinement."
  - "A curriculum strategy progressively internalizes explicit CoT into compact latent representations."
projects:
  - slug: "branch-a"
    relevance: reference
    why: "Adaptive-depth routing is adjacent to scaling discussion but multimodal framing limits direct transfer to text-only Qwen3."
  - slug: "branch-b"
    relevance: secondary
    why: "**Gradient-dynamics analysis during latent training is directly relevant to Branch B's grad-stability diagnostics.** Claims (1) volatile/high gradient norms on specific token classes and (2) persistent gradient instability for complex tokens under fixed architectural depth are the kind of phenomena our detach/fp32 ablation is trying to characterize on the text-only side. Worth reading for methodology (per-token gradient-norm instrumentation)."
  - slug: "branch-c"
    relevance: reference
    why: "Per-token gradient-norm instrumentation could inform Qwen3 probe methodology but is not a direct probe-validity check."
  - slug: "branch-d"
    relevance: reference
    why: "Curriculum + adaptive depth is a different axis than CPF; reference only."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Concrete gradient-dynamics observations (visual-token under-optimization, complex-token gradient instability bounded by fixed depth) are citable in the SPAR writeup's failure-modes / training-dynamics section. Complements our V2/V3/V4 detach work with an orthogonal finding."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Visual Enhanced Depth Scaling for Multimodal Latent Reasoning

## TL;DR

Analyzes **token-level gradient dynamics during latent training** in a multimodal setting and identifies two critical phenomena: (1) visual tokens have **higher and more volatile gradient norms** than text tokens → systematic visual under-optimization; (2) simple tokens converge fast while **complex tokens show persistent gradient instability** constrained by fixed depth. Proposes (a) **visual replay module** (causal self-attention for saliency-based grounding) and (b) **routing depth scaling** (adaptive extra reasoning steps for complex tokens). Paired with a standard curriculum that internalizes explicit CoT into compact latents.

## Method

### Gradient-dynamics observations (cross-cutting)

1. **Visual-token under-optimization**: systematically higher and more volatile gradient norms vs text tokens.
2. **Complex-token instability**: with fixed model depth, semantically complex tokens' gradient norms remain unstable throughout training.

### Modules

- **Visual replay** — uses causal self-attention to compute per-token saliency; adds spatially-coherent constraints to reinforce visual grounding.
- **Routing depth scaling** — adaptive additional reasoning iterations for complex tokens (analog to Think-at-Hard's per-token iteration gating).

### Curriculum

- Progressive internalization of explicit CoT into compact latent representations (standard CODI/SIM-CoT lineage).

## Recipe

- Base model + per-module hyperparameters in PDF.

## Results

- State-of-the-art across multimodal benchmarks (names not in abstract).
- Substantial inference speedup over explicit CoT baselines.

## Relevance

- **Methodology for Branch B**: per-token gradient-norm tracking during latent training is exactly the diagnostic we need. Worth porting to CODI/LT-Tuning runs.
- **Complex-token gradient instability bounded by fixed depth** is a precise statement of a phenomenon that our V2/V3/V4 detach ablations skirt around. Potential contradiction to track: if detach stabilizes gradients in text-only settings, does that imply a different mechanism than depth-boundedness?

## Citations

- Discovered via SIM-CoT downstream citation graph.
