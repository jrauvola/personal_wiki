---
type: source
title: "HRPO — Hybrid Latent Reasoning via Reinforcement Learning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/reinforcement-learning
  - method/gated-fusion
status: read
related:
  - "[[CODI]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[Adaptive Latent RL]]"
  - "[[Soft Tokens Hard Truths]]"
sources:
  - "[[.raw/papers/2505.18454-hrpo]]"
source_type: paper
arxiv_id: "2505.18454"
venue: "arXiv"
date_published: 2025-05-24
authors:
  - "Zhenrui Yue"
  - "Bowen Jin"
  - "Huimin Zeng"
  - "Honglei Zhuang"
  - "Zhen Qin"
  - "Jinsung Yoon"
  - "Lanyu Shang"
  - "Jiawei Han"
  - "Dong Wang"
url: "https://arxiv.org/abs/2505.18454"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Latent reasoning approaches are often incompatible with LLMs, as their continuous paradigm conflicts with the discrete nature of autoregressive generation."
  - "Existing latent reasoning methods rely on CoT traces for training and thus fail to exploit the inherent reasoning patterns of LLMs."
  - "HRPO integrates prior hidden states into sampled tokens with a learnable gating mechanism."
  - "HRPO initializes training with predominantly token embeddings while progressively incorporating more hidden features."
  - "The hybrid HRPO introduces stochasticity into latent reasoning via token sampling, thereby enabling RL-based optimization without requiring CoT trajectories."
  - "HRPO outperforms prior methods in both knowledge- and reasoning-intensive tasks; HRPO-trained LLMs remain interpretable and exhibit intriguing behaviors like cross-lingual patterns and shorter completion lengths."
projects:
  - slug: "branch-d"
    relevance: primary
    why: "HRPO's learnable-gated fusion of hidden states + token embeddings (progressive curriculum from tokens to hidden) is structurally very close to LT-Tuning's CPF (α·h_ctx + (1−α)·e_pred); both can be viewed as fusion-of-context-and-prediction mechanisms. Direct comparison candidate for branch-d."
  - slug: "branch-a"
    relevance: reference
    why: "No direct Qwen3 scaling test; RL-without-CoT-traces framing is not the architecture-dependence story — reclassified reference."
  - slug: "branch-b"
    relevance: secondary
    why: "Progressive-feature curriculum is a stability technique relevant to the detach/fp32 scaling ablation."
  - slug: "branch-c"
    relevance: reference
    why: "Interpretability claim is high-level, not probe-methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "RL + hybrid fusion is a third synthesis input alongside V2 (distillation) / SIM-CoT (supervised) / LT-Tuning (CPF) — directly in scope for the north-star."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# HRPO — Hybrid Reasoning Policy Optimization

Yue, Jin, Zeng, Zhuang, Qin, Yoon, Shang, Han, Wang, [arXiv:2505.18454](https://arxiv.org/abs/2505.18454).

## TL;DR

Argues existing latent reasoning breaks autoregressive generation compatibility and ignores LLMs' native reasoning patterns. HRPO fixes both: (1) **learnable gating mechanism** integrates prior hidden states into sampled token embeddings; (2) **progressive curriculum** — start with mostly token embeddings, progressively incorporate more hidden features; (3) **RL** via token sampling stochasticity, no CoT trajectories required. Outperforms prior methods on knowledge + reasoning tasks; models remain interpretable, show cross-lingual patterns and shorter completions.

## Method

- Learnable gate `g(context)` mixes `h_hidden` into `e_token`.
- Training curriculum: initial gate is heavily biased to `e_token`, progressively allows more `h_hidden`.
- GRPO-like RL without CoT traces.

## Recipe

1. Initialize with token-embedding-dominant gate.
2. RL training on task reward (no CoT trace needed).
3. Progressively shift gate toward hidden-feature inclusion.

## Relation to LT-Tuning CPF

HRPO's gate mechanism is **the same functional form as CPF**:
- LT-Tuning CPF: `e_fusion = α·h_ctx + (1−α)·e_pred`.
- HRPO gate: `e_fusion = g·h_hidden + (1−g)·e_token`.

Key differences:
- LT-Tuning trains via distillation with a 3-stage curriculum; HRPO trains via RL with a gate curriculum.
- LT-Tuning's α is fixed or scheduled; HRPO's g is learnable and context-dependent.

## Relevance

**Primary for branch-d.** HRPO and LT-Tuning CPF independently discovered the same fusion form, implying it may be a fundamental inductive bias rather than an accident of one paper's design. Strong motivation for branch-d's CPF-on-CODI plan. Also raises the question: does making α **learnable** (HRPO-style) outperform fixed/scheduled (LT-Tuning-style) on the CODI stack?

## Citation links to chase

- Latent Thoughts Tuning (parallel fusion mechanism).
- Soft Tokens Hard Truths (alternative RL continuous CoT).
- CODI (base method).
