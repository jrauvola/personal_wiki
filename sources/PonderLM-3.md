---
type: source
title: "PonderLM-3 — Differentiable Token-Adaptive Depth"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/source
  - method/adaptive-compute
  - method/pretraining
status: read
related:
  - "[[Adaptive Latent RL]]"
  - "[[CODI]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2603.02023-ponderlm-3]]"
source_type: paper
arxiv_id: "2603.02023"
venue: "arXiv"
date_published: 2026-03-02
authors:
  - "He Li"
  - "Feichen Song"
  - "Boyi Zeng"
  - "Shixiang Song"
  - "Zhiqin John Xu"
  - "Ziwei He"
  - "Zhouhan Lin"
url: "https://arxiv.org/abs/2603.02023"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "PonderLM-3 injects a differentiable attention mask during pretraining and pairs it with a matching hard pruning rule at inference to learn token-wise adaptive pondering under purely self-supervised objectives."
  - "A lightweight router conditioned on step-0 hidden state predicts a step distribution s_{t,k}; the tail CDF w_{t,k} = Σ_{j=k}^K s_{t,j} parameterizes both training masking (log w added to attention logits) and inference hard stopping (K̂_t = max{k : w_{t,k} ≥ τ} with τ = 10^-4)."
  - "The final representation ĥ_t = Σ_k s_{t,k} · h_t^(k) avoids discrete-step instability during training while letting inference skip steps with negligible mass; augmented-matrix construction preserves FlashAttention-2 compatibility."
  - "At K_max=3, PonderLM-3 on 410M LLaMA attains 46.4 avg over 7 downstream benchmarks at 8.86 inference FLOPs, versus PonderLM-2's 46.0 at 9.84 FLOPs — comparable accuracy at lower compute."
  - "Learned halting tracks predictive entropy not static features: deterministic tokens ('the', 'of') average ≈2.3 pondering steps with 66-74% pruned; high-uncertainty tokens ('a') average ≈3.0 steps with 0.07% pruned; word boundaries allocate maximum depth 100% of the time."
  - "RMSE between training-iteration states and inference-time fixed point decays with effective contraction factor L ≈ 0.433 (R² ≈ 0.9959), empirically validating train-inference alignment through near-exponential convergence."
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Internal differentiable halting is orthogonal to CPF; relevant only as taxonomic neighbor."
  - slug: "branch-a"
    relevance: reference
    why: "Pretraining-phase adaptive depth is outside current Qwen3 scaling scope."
  - slug: "branch-b"
    relevance: reference
    why: "Token-adaptive depth gates touch grad flow but are not a detach/BPTT variant."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to Qwen3 probe methodology debugging."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Fills out the adaptive-compute taxonomy alongside Adaptive Latent RL in the writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# PonderLM-3 — Differentiable Token-Adaptive Depth

**Paper:** "PonderLM-3: Adaptive Token-Wise Pondering with Differentiable Masking" — He Li, Feichen Song, Boyi Zeng, Shixiang Song, Zhiqin John Xu, Ziwei He, Zhouhan Lin — [arXiv:2603.02023](https://arxiv.org/abs/2603.02023) (v1 Mar 2, 2026; v2 Mar 10, 2026). Built on the PonderLM-2 backbone (Jacobi-aligned latent-thought pretraining).

While post-training methods like [[Adaptive Latent RL]] use external value networks or GRPO to halt reasoning at the sequence level, PonderLM-3 attacks dynamic compute allocation purely internally during the pretraining phase.

## Core thesis

A **differentiable attention mask** functions as a highly granular, token-dependent routing gate. Rather than applying a fixed number of recurrent continuous steps uniformly across an entire sequence, PonderLM-3 evaluates the inherent complexity of each individual token during the forward pass. It learns an end-to-end differentiable halting mechanism that routes additional internal iterations — "pondering steps" — exclusively to mathematically or logically complex tokens, while allowing trivial tokens to bypass the recurrent loops entirely.

## Why it matters

This shifts inference compute from a rigid sequence-level tax into a highly fluid token-adaptive resource, yielding a significantly steeper and more favorable perplexity-compute Pareto frontier than standard fixed-step latent models.

## Public artifacts

No explicit public artifacts listed in the source survey.

## Integration notes

Relevant primarily as a taxonomic neighbor to [[Adaptive Latent RL]] — the pretraining-internal counterpart to post-training adaptive halting.
