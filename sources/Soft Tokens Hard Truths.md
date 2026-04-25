---
type: source
title: "Soft Tokens, Hard Truths — RL for Continuous CoT"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/reinforcement-learning
  - method/scaling
status: read
related:
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[Adaptive Latent RL]]"
sources:
  - "[[.raw/papers/2509.19170-soft-tokens-hard-truths]]"
source_type: paper
arxiv_id: "2509.19170"
venue: "arXiv"
date_published: 2025-09-23
authors:
  - "Natasha Butt"
  - "Ariel Kwiatkowski"
  - "Ismail Labiad"
  - "Julia Kempe"
  - "Yann Ollivier"
url: "https://arxiv.org/abs/2509.19170"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "This is the first work introducing a scalable method to learn continuous CoTs via reinforcement learning (RL), without distilling from reference discrete CoTs."
  - "We use 'soft' tokens: mixtures of tokens together with noise on the input embedding to provide RL exploration. Computational overhead is minimal, enabling us to learn continuous CoTs with hundreds of tokens."
  - "On math reasoning benchmarks with Llama and Qwen models up to 8B, training with continuous CoTs match discrete-token CoTs for pass@1 and surpass them for pass@32, showing greater CoT diversity."
  - "In systematic comparisons, the best-performing scenario is to train with continuous CoT tokens then use discrete tokens for inference."
  - "Continuous CoT RL training better preserves the predictions of the base model on out-of-domain tasks, thus providing a softer touch to the base model."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Alternative training signal (RL, no distillation) at the same 8B scale target as LT-Tuning; relevant context for branch-d's supervision-mechanism choice."
  - slug: "branch-a"
    relevance: primary
    why: "Explicitly tests Llama and Qwen up to 8B — direct data on Qwen-family continuous-CoT scaling behavior, and claims better OOD preservation which is load-bearing for the Qwen3 architecture-dependence thesis."
  - slug: "branch-b"
    relevance: secondary
    why: "Reports stability under scale without distillation; orthogonal to but informs the detach/fp32 ablation framing."
  - slug: "branch-c"
    relevance: reference
    why: "Not probe-methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "First RL-trained scalable continuous CoT — a distinct synthesis input alongside V2 / SIM-CoT / LT-Tuning."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Soft Tokens, Hard Truths

> [!contradiction] No-curriculum RL vs [[Capabilities and Limits of Latent CoT]] + [[ALiCoT]]
> This paper trains continuous CoT via RL alone, no curriculum, scaling to 8B with pass@1 matching discrete CoT. [[Capabilities and Limits of Latent CoT]] proves curriculum is theoretically necessary to traverse Exploration-Execution trade-off; [[ALiCoT]] (round-2 crawl) proves Order-r alignment is also theoretically necessary for irreducible problems. Tension: either the two theoretical claims are regime-specific (distillation-only), or RL exploration substitutes for curriculum/alignment traversal. [[Token Assorted]] makes the sibling argument for discrete latent tokens. Three-way cluster; unresolved.

Butt, Kwiatkowski, Labiad, Kempe, Ollivier, [arXiv:2509.19170](https://arxiv.org/abs/2509.19170).

## TL;DR

Claims the **first scalable method to learn continuous CoTs via RL** — no distillation from discrete traces. Uses "soft tokens" (mixtures of discrete tokens + noise on input embeddings) for exploration. Scales to hundreds of continuous tokens, Llama + Qwen up to 8B. Train-soft / infer-discrete is the best configuration; pass@1 matches discrete, pass@32 surpasses it (more diversity). OOD predictions are better preserved than discrete fine-tuning.

## Method

- **Soft tokens** = convex mixtures of discrete token embeddings + additive noise on input embedding.
- **RL training** (details not in abstract; no distillation target).
- **Scale:** hundreds of continuous tokens. Llama, Qwen ≤ 8B.
- **Inference trick:** train with continuous, deploy with discrete.

## Results

- pass@1: matches discrete-token CoT.
- pass@32: exceeds discrete-token CoT — greater CoT diversity.
- Better OOD preservation of base-model predictions vs discrete fine-tuning.

## Relevance

Directly hits branch-a's Qwen-family scaling concern — 8B Qwen with continuous CoT, without distillation, successful. That's a significant comparison point for the Qwen3 architecture-dependence thesis. For branch-d, it's an **alternative supervision regime** to LT-Tuning's CPF + 3-stage curriculum — worth tracking whether CPF + RL hybrid is viable.

## Citation links to chase

- CODI, COCONUT (continuous CoT predecessors).
- Adaptive Latent RL (different RL framing).
