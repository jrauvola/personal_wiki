---
type: source
title: "PCCoT — Parallel Continuous Chain-of-Thought with Jacobi Iteration"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/parallel-decoding
  - method/jacobi-iteration
status: read
related:
  - "[[CODI]]"
  - "[[KaVa]]"
  - "[[COCONUT]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2506.18582-pccot]]"
source_type: paper
arxiv_id: "2506.18582"
venue: "arXiv"
date_published: 2025-06-23
authors:
  - "Haoyi Wu"
  - "Zhihao Teng"
  - "Kewei Tu"
url: "https://arxiv.org/abs/2506.18582"
code_repo: "https://github.com/whyNLP/PCCoT"
has_weights: false
confidence: high
key_claims:
  - "The sequential dependencies between latent thought tokens spoil parallel training, leading to long training time."
  - "PCCoT performs Jacobi iteration on the latent thought tokens, updating them iteratively in parallel instead of sequentially."
  - "By choosing the proper number of iterations, we are able to achieve comparable or even better performance while saving nearly 50% of the training and inference time."
  - "PCCoT shows better stability and robustness in the training process."
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Jacobi parallel updates are directly compatible with CODI's continuous rollout and with LT-Tuning's CPF curriculum — a candidate efficiency/stability improvement on the CPF+CODI stack."
  - slug: "branch-a"
    relevance: secondary
    why: "~50% training/inference savings and improved training stability are directly relevant to Qwen3 scaling throughput."
  - slug: "branch-b"
    relevance: primary
    why: "Jacobi iteration is the stabilization knob at the heart of KaVa; detach ablation on CODI V2/V3/V4 should include Jacobi variants and KaVa-style truncated BPTT."
  - slug: "branch-c"
    relevance: reference
    why: "Not methodology-probe-relevant."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Substantive efficiency and stability recipe in the latent-CoT canon; useful synthesis data point."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# PCCoT — Parallel Continuous Chain-of-Thought with Jacobi Iteration

Wu, Teng, Tu, [arXiv:2506.18582](https://arxiv.org/abs/2506.18582). Code: [whyNLP/PCCoT](https://github.com/whyNLP/PCCoT).

## TL;DR

The sequential dependencies in autoregressive continuous CoT (COCONUT / CODI) spoil parallel training. PCCoT replaces sequential generation of latent thought tokens with Jacobi iteration: all latents are initialized and iteratively updated in parallel. At the right number of iterations, PCCoT matches or exceeds sequential baselines while cutting ~50% of both training and inference time, and shows markedly better training stability.

## Method

- Initialize all latent thought tokens simultaneously.
- Apply Jacobi update rule iteratively for K steps; each iteration updates every latent token in parallel using the previous iteration's values.
- K trades quality for compute.

## Recipe

Drop-in replacement for sequential rollout in any continuous-CoT framework (COCONUT, CODI, etc.).

## Results

- ~50% reduction in training time.
- ~50% reduction in inference time.
- Performance matched or exceeded baseline with proper K.
- Improved training stability and robustness.

## Relevance

PCCoT is one of the more **mechanically consequential** citing works on CODI: removing sequential dependencies is a first-order efficiency win, and the stability improvement is directly relevant to branch-b's detach/fp32 stability agenda. Natural question for branch-d: does CPF fusion compose with Jacobi parallel updates, or does it require the sequential rollout to anchor the trajectory?

## Citation links to chase

- KaVa — Jacobi-stabilized KV-cache distillation at 7B; parallel formulation is in the same family.
- COCONUT — sequential continuous rollout baseline.
- CODI — self-distilled sequential continuous rollout baseline.
