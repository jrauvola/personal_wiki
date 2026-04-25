---
type: source
title: "Adaptive Latent Reasoning via Reinforcement Learning"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/source
  - method/post-training-rl
  - method/adaptive-compute
status: read
related:
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[SIM-CoT]]"
  - "[[CoLaR]]"
  - "[[PonderLM-3]]"
  - "[[GRPO]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2511.21581-adaptive-latent-reasoning]]"
source_type: paper
arxiv_id: "2511.21581"
venue: "arXiv"
date_published: 2025-11-26
authors:
  - "Alex Ning"
  - "Yen-Ling Kuo"
  - "Gabe Gomes"
url: "https://arxiv.org/abs/2511.21581"
code_repo: "https://github.com/apning/adaptive-latent-reasoning"
has_weights: true
status: read
confidence: high
key_claims:
  - "Latent reasoning directly passes the information-rich previous final latent state into the next sequence, removing the restriction to human-language tokens as the medium for reasoning."
  - "A simple linear binary classification head appended to the model learns when to stop, converting fixed-length latent reasoning into an adaptive-length variable."
  - "During variable-length SFT, the target latent step count is set via the clamp min(n_max, max(n_min, c·k + b)) where k is the number of reasoning steps in the training CoT."
  - "The GRPO reward combines correctness, a format penalty, and a length component that applies a length penalty when p_correct ≥ p_cutoff (trivial problem) and a length reward when p_correct < p_cutoff (complex problem), with λ_penalty = 0.0001, λ_reward = 0.1, p_cutoff = 1.0."
  - "On GSM8K-Aug with Llama 3.2 1B, Latent-6 + RL reduces avg reasoning tokens from 8 to 3.76 (−52.94%) while accuracy slightly improves from 49.73% to 50.11%."
  - "The model learns through SFT and RL to allocate more reasoning tokens to harder problems: the proportion of incorrect answers increases with reasoning length."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Post-training add-on that could layer on top of LT-Tuning-CPF-on-CODI but isn't the branch's core scientific question."
  - slug: "branch-a"
    relevance: secondary
    why: "Throughput optimization for scaled Qwen3 runs; secondary to the architecture-dependence finding itself."
  - slug: "branch-b"
    relevance: reference
    why: "Adaptive halting is orthogonal to detach/grad-stability ablations."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No relevance to Qwen3 probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Definitive secondary optimization stage for the north-star workable model; layered on top of a strong-supervision base."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Adaptive Latent Reasoning via Reinforcement Learning

**Paper:** "Learning When to Stop: Adaptive Latent Reasoning via Reinforcement Learning" — Alex Ning, Yen-Ling Kuo, Gabe Gomes, [arXiv:2511.21581](https://arxiv.org/abs/2511.21581) (Nov 26, 2025). Code: [apning/adaptive-latent-reasoning](https://github.com/apning/adaptive-latent-reasoning). HF org: `Lapisbird` (hosts all released checkpoints).

Resolves a persistent architectural flaw across intrinsic latent reasoning models — reliance on a static, predetermined allocation of continuous thought vectors. Simple arithmetic queries waste cycles; complex problems exhaust the budget before convergence.

## Core thesis

Transform the reasoning horizon into a fully dynamic, token-adaptive variable. Augment the standard latent transformer stack with a lightweight, linear binary classification head. At every discrete step in the continuous space, the head evaluates the current cognitive state and emits a halt/continue signal. This dynamic halting mechanism can be optimized entirely through post-training RL — no external value networks, no human-annotated stopping datasets.

## Training pipeline

Two-stage post-training add-on.

### Stage 1 — Variable-length SFT

Base latent model initialized via standard distillation or curriculum SFT. The final phase of SFT introduces variability: target latent step count per sample is

$$n_{target} = \min(n_{max}, \max(n_{min}, c \cdot k + b))$$

where $k$ = original explicit CoT length. Ensures internal representations remain stable across varying temporal horizons.

### Stage 2 — GRPO

Composite reward:

- **Length penalty $\lambda_{penalty}$** applied when a batch of sampled outputs achieves uniform mathematical correctness (trivial problem → truncate reasoning).
- **Length reward $\lambda_{reward}$** applied when accuracy in the batch is mixed/poor (complex problem → allocate deeper exploration).

## Public artifacts

Exemplary.

- Official codebase published.
- HF weights (Llama 3.2 1B):
  - `Lapisbird/Llama-adaLR-model-latent-6-by-1` (SFT)
  - `Lapisbird/Llama-adaLR-model-latent-6_rl` (RL)
  - `Lapisbird/Llama-adaLR-model-latent-6-by-1_rl` (RL)

## Empirical results

- On GSM8K-Aug: **-52.94%** total reasoning tokens, **+0.38%** absolute accuracy vs base latent model.
- Granular analysis confirms the algorithm maps cognitive effort to task complexity — near-instantaneous for basic arithmetic, deep vector chains for multi-step logic.

## Integration notes

Premier post-training optimization layer for continuous reasoning systems. Not a foundational implementation — the **definitive secondary optimization stage** to layer on top of stabilized CODI, COCONUT, or SIM-CoT.
