---
type: source
title: "Soft Thinking"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/training-free
  - method/continuous-concepts
status: read
related:
  - "[[COCONUT]]"
  - "[[SoftCoT++]]"
  - "[[Soft Thinking Mechanism]]"
  - "[[Latent Reasoning as Chain of Superposition]]"
  - "[[Feature Collapse]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2505.15778-soft-thinking]]"
source_type: paper
arxiv_id: "2505.15778"
venue: "arXiv"
date_published: 2025-05-21
authors:
  - "Zhen Zhang"
  - "Xuehai He"
  - "Weixiang Yan"
  - "Ao Shen"
  - "Chenyang Zhao"
  - "Shuohang Wang"
  - "Yelong Shen"
  - "Xin Eric Wang"
url: "https://arxiv.org/abs/2505.15778"
code_repo: "https://github.com/eric-ai-lab/Soft-Thinking"
has_weights: false
status: read
confidence: high
key_claims:
  - "Soft Thinking is a training-free method that replaces discrete token sampling at each CoT step with a 'concept token' = probability-weighted mixture of all vocabulary embeddings."
  - "Soft Thinking improves pass@1 by up to 2.48 points (QwQ-32B on math suite) and reduces token usage by up to 22.4% (DeepSeek-R1-Distill-Qwen-32B) vs standard CoT."
  - "Cold Stop mechanism monitors entropy of the concept-token distribution and terminates intermediate reasoning when entropy < τ for k consecutive steps, preventing OOD-induced generation collapse."
  - "In weight-tied ≤7B models, input and output embeddings align after training, enabling continuous-space reasoning; in >7B decoupled models, hidden states and input embeddings reside in different spaces, causing representational mismatch that extensive retraining cannot fix — motivating the training-free vocabulary-distribution bridge."
  - "Soft Thinking approximates the exact exponential path-summation over CoT trajectories via first-order linearization at the concept-token expectation, collapsing sampling into a single forward pass."
  - "On AIME 2024 the QwQ-32B improvement is 6.45 pass@1 points — the largest observed gain."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Training-free alternative to Qwen3 SFT; useful baseline if architecture-dependence finding holds."
  - slug: "branch-b"
    relevance: reference
    why: "Not a gradient/detach study."
  - slug: "branch-c"
    relevance: reference
    why: "Probe-methodology reference only."
  - slug: "branch-d"
    relevance: primary
    why: "Directly relevant to LT-Tuning's embedding-geometry thesis — Soft Thinking explicitly identifies the decoupled-embedding mismatch at >7B that LT-Tuning's CPF is designed to fix. This paper corroborates the core Branch D hypothesis."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical training-free continuous-space reasoning recipe; essential writeup reference."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Soft Thinking

## TL;DR

Training-free continuous-space CoT. At each reasoning step, replace the sampled discrete token with a probability-weighted mixture of all vocabulary embeddings (a "concept token"), preserving the full next-step distribution as a superposition. A Cold Stop entropy trigger terminates intermediate reasoning to prevent OOD-induced collapse. Gains on QwQ-32B / DeepSeek-R1-Distill: up to +2.48 pass@1 and -22.4% tokens on math; +6.45 pass@1 on AIME 2024.

## Method

- **Concept token:** at intermediate step t, the concept token is the LLM's full softmax output p ∈ Δ^|V|-1 (not sampled).
- **Continuous concept space:** the convex combination E^T p of all token embeddings via the weights p. Plug this mixture embedding as the next input.
- **Cold Stop:** compute entropy H(p) at each step; increment low-entropy counter if H(p) < τ, else reset. When counter reaches k consecutive steps, inject `</think>` and switch to discrete answer generation.
- **Reuse existing embedding matrix** — no new parameters, no training.
- **Efficiency:** top-k top-p filter on the vocabulary before the mixture, O(nd) per step where n = top-n size.

## Recipe

- Models: QwQ-32B, DeepSeek-R1-Distill-Qwen-32B, DeepSeek-R1-Distill-Llama-70B.
- Max generation length 32,768; temperature 0.6; top-k=30; top-p=0.95.
- Concept-token top-n ∈ {5, 10, 15, 20, 30}; best n=15 for QwQ-32B, n=10 for DeepSeek-R1.
- Cold Stop τ ∈ {0.01, 0.05, 0.1, 0.2}; k ∈ {128, 256, 512, 1024}.
- SGLang inference backend; 8× H100 80GB.

## Results

Math (Math500, AIME 2024, GSM8K, GPQA-Diamond):
- QwQ-32B avg pass@1: 83.84% → 86.32% (+2.48), tokens -11.6%.
- AIME 2024 specifically: +6.45 pass@1.
- DeepSeek-R1-Distill-Qwen-32B: +1.71 pass@1, tokens -22.4%.
- DeepSeek-R1-Distill-Llama-70B: +1.11 pass@1, tokens -17.9%.

Code (HumanEval, MBPP, LiveCodeBench):
- QwQ-32B: +0.48 pass@1, -16.1% tokens.
- DeepSeek-R1-Distill-Qwen-32B: +0.90 pass@1, -19.1% tokens.
- DeepSeek-R1-Distill-Llama-70B: +0.70 pass@1, -16.3% tokens.

## Relevance to our project

**Load-bearing for Branch D / spar-latent-reasoning.** This paper explicitly articulates the weight-tied-vs-decoupled embedding problem at the 7B scale boundary — the same mechanism [[Latent Thoughts Tuning]] identifies as driving feature collapse. Soft Thinking's solution (route through the softmax / vocabulary distribution) is structurally similar to LT-Tuning's CPF interpolation: both anchor the latent trajectory to the discrete token manifold rather than the hidden-state manifold. Corroborating evidence that decoupled embeddings at ≥7B are the dominant failure mode for continuous-latent reasoning. Also: Cold Stop's entropy-triggered halting is a training-free analog of [[Adaptive Exit Gate]] / ACT Q-head patterns in [[Ouro]] / [[Hierarchical Reasoning Model]] / [[Adaptive Latent RL]].

## Citation links to chase

- [[COCONUT]] — compared as failing at >7B due to decoupled embeddings.
- [[Latent Thoughts Tuning]] — same diagnosis, different solution.
- [[Soft Thinking Mechanism]] (2508.03440) — critical follow-up showing vanilla Soft Thinking is actually greedy in practice.
- SoftCoT (Xu et al. 2025) — learned-assistant variant.
- [[SoftCoT++]] (2505.11484) — TTS extension.
