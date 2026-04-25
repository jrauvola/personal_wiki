---
type: source
title: "Pretraining with Token-Level Adaptive Latent Chain-of-Thought"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/pretraining
  - type/source
  - method/adaptive-compute
  - method/token-level-halting
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[Think-at-Hard]]"
  - "[[Ouro]]"
  - "[[COCONUT]]"
sources:
  - "[[.raw/papers/2602.08220-adaptive-latent-cot-pretraining]]"
source_type: paper
arxiv_id: "2602.08220"
venue: "arXiv"
date_published: 2026-02-09
authors:
  - "Boyi Zeng"
  - "Yiqin Hao"
  - "He Li"
  - "Shixiang Song"
  - "Feichen Song"
  - "Zitong Wang"
  - "Siyuan Huang"
  - "Yi Xu"
  - "ZiWei He"
  - "Xinbing Wang"
  - "Zhouhan Lin"
url: "https://arxiv.org/abs/2602.08220"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "The model generates a variable-length latent CoT trajectory before emitting each token — allocating longer trajectories to difficult tokens and shorter (or even zero) trajectories to easy ones."
  - "This behavior emerges naturally from one-stage pretraining on general text and reduces computation in both training and inference via token-wise adaptive halting."
  - "Experiments with Llama architectures show that adaptive latent CoT consistently improves language modeling perplexity and broad downstream accuracy."
  - "Adaptive latent CoT improves PPL and downstream accuracy even with fewer training FLOPs than prior recurrent baselines."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Pretraining-scale latent-CoT recipe on Llama architectures is adjacent to the scaling question in Branch A; if the approach is architecture-dependent in the same way as COCONUT, this would be an independent data point. Secondary because Branch A is downstream (post-trained) scaling, not from-scratch pretraining."
  - slug: "branch-b"
    relevance: reference
    why: "Adaptive halting is orthogonal to the detach/fp32 ablation axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to Qwen3 probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Token-level adaptive depth is a different design axis than CPF's anchor-to-vocab; no direct recipe transfer."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Pretraining-embedded latent CoT is a distinct category from the post-training latent methods (CODI/SIM-CoT/LT-Tuning) we cover — worth one paragraph in the SPAR writeup taxonomy as the pretraining-scale analog."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Pretraining with Token-Level Adaptive Latent Chain-of-Thought

## TL;DR

Internalizes latent CoT into **pretraining itself**: before each token emission, the model generates a variable-length latent trajectory, allocating longer trajectories to difficult tokens and shorter (or zero) to easy ones. The adaptive-halting behavior **emerges naturally from one-stage pretraining on general text** — no curriculum, no SFT, no reasoning-data distillation. On Llama architectures, consistently improves PPL and downstream accuracy with fewer training FLOPs than prior recurrent baselines.

## Method

- Per-token variable-length latent CoT trajectory.
- Token-wise adaptive halting — reduces both training and inference compute.
- Single-stage pretraining on general text (no multi-stage curriculum).

## Recipe

- Llama architectures (scale unspecified in abstract).
- Compared against "prior recurrent baselines" (PonderNet family implied).
- Training-FLOP efficient (claimed).

## Results

- PPL: consistent improvements vs baselines.
- Downstream accuracy: broad improvements.
- Compute: fewer training FLOPs than prior recurrent baselines.
- No specific benchmark numbers in abstract.

## Relevance

- Pretraining-scale adaptive latent CoT is a complementary design axis to SIM-CoT / LT-Tuning (post-training) and Ouro/Think-at-Hard (fixed-loop adaptive). Emergence without curriculum is an important claim to verify.
- For SPAR writeup: fills a gap in the taxonomy — "latent CoT embedded at pretraining time" category.

## Citations

- Discovered via SIM-CoT downstream citation graph.
