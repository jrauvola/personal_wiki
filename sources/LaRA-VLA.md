---
type: source
title: "LaRA-VLA — Latent Reasoning VLA"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/robotics
  - type/source
  - method/curriculum
  - method/vla
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[OneVL]]"
  - "[[DualCoT-VLA]]"
sources:
  - "[[.raw/papers/2602.01166-lara-vla]]"
source_type: paper
arxiv_id: "2602.01166"
venue: "arXiv"
date_published: 2026-02-01
authors:
  - "Shuanghao Bai"
  - "Jing Lyu"
  - "Wanqi Zhou"
  - "Zhe Li"
  - "Dakai Wang"
  - "Lei Xing"
  - "Xiaoguang Zhao"
  - "Pengwei Wang"
  - "Zhongyuan Wang"
  - "Cheng Chi"
  - "Badong Chen"
  - "Shanghang Zhang"
url: "https://arxiv.org/abs/2602.01166"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "LaRA-VLA internalizes multi-modal CoT reasoning into continuous latent representations for embodied action, performing unified reasoning and prediction in latent space and eliminating explicit CoT generation at inference time."
  - "The curriculum-based training paradigm progressively transitions from explicit textual and visual CoT supervision to latent reasoning, and finally adapts latent reasoning dynamics to condition action generation."
  - "LaRA-VLA consistently outperforms state-of-the-art VLA methods while reducing inference latency by up to 90% compared to explicit CoT-based approaches."
  - "The authors construct two structured CoT datasets for simulation and long-horizon real-robot manipulation evaluation."
projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "VLA domain; no bearing on Qwen3 architecture-dependence scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach/fp32 backward-chain discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to Qwen3 probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Three-stage curriculum (explicit→latent→action) parallels LT-Tuning's three-stage CPF curriculum — reference only since action-conditioning final stage is domain-specific to VLA."
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "One of three parallel 2026 VLA latent-CoT extensions of SIM-CoT (with OneVL, DualCoT-VLA) — taxonomic footnote for the SPAR writeup's 'latent reasoning beyond math' section."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LaRA-VLA — Latent Reasoning VLA

## TL;DR

Unified VLA framework that internalizes multi-modal (visual + linguistic) CoT into continuous latent representations used for embodied action. Three-stage curriculum: explicit textual+visual CoT supervision → latent reasoning → action-conditioned latent dynamics. Up to 90% inference-latency reduction vs explicit CoT VLA baselines.

## Method

Latent reasoning space shared across perception, planning, and action prediction. Explicit CoT is eliminated at inference — only the final action output is emitted. Architecture details not in abstract.

## Recipe

- **Curriculum (3 stages):**
  1. Explicit textual + visual CoT supervision.
  2. Transition to latent reasoning.
  3. Adapt latent reasoning dynamics to condition action generation.
- Two structured CoT datasets constructed for training (names not in abstract).
- Base backbone not specified.

## Results

- Outperforms SOTA VLA methods on simulation benchmarks and long-horizon real-robot manipulation (benchmark names not in abstract).
- Up to 90% inference latency reduction vs explicit CoT VLA baselines.

## Relevance

- **Curriculum shape is familiar**: mirrors the CODI/SIM-CoT/LT-Tuning three-stage pattern.
- Taxonomic relevance only: applied-domain extension rather than a novel recipe for math/code latent reasoning.

## Citations

- Project page: https://loveju1y.github.io/Latent-Reasoning-VLA/
- Discovered via SIM-CoT downstream citation graph.
