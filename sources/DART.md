---
type: source
title: "DART — Distilling Autoregressive Reasoning to Silent Thought"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/self-distillation
  - method/non-autoregressive
status: read
related:
  - "[[CODI]]"
  - "[[SIM-CoT]]"
  - "[[Self-Distillation]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2506.11752-dart]]"
source_type: paper
arxiv_id: "2506.11752"
venue: "arXiv"
date_published: 2025-06-13
authors:
  - "Nan Jiang"
  - "Ziming Wu"
  - "De-Chuan Zhan"
  - "Fuming Lai"
  - "Shaobing Lian"
url: "https://arxiv.org/abs/2506.11752"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "DART is a self-distillation framework that enables LLMs to replace autoregressive CoT with non-autoregressive Silent Thought (ST)."
  - "DART introduces two training pathways: the CoT pathway for traditional reasoning and the ST pathway for generating answers directly from a few ST tokens."
  - "The ST pathway utilizes a lightweight Reasoning Evolvement Module (REM) to align its hidden states with the CoT pathway, enabling the ST tokens to evolve into informative embeddings."
  - "During inference, only the ST pathway is activated, leveraging evolving ST tokens to deliver the answer directly."
  - "DART offers significant performance gains compared with existing non-autoregressive baselines without extra inference latency."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Closely parallel to CODI's self-distillation recipe but with a Reasoning Evolvement Module — a candidate fusion-style mechanism in the CPF family worth comparing on LT-Tuning stack."
  - slug: "branch-a"
    relevance: reference
    why: "Non-autoregressive ST is orthogonal to Qwen3 scaling; useful context only."
  - slug: "branch-b"
    relevance: reference
    why: "Detach ablation operates on CODI's autoregressive continuous rollout; non-autoregressive ST is a different design axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe-methodology content."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Same self-distillation family as CODI/SIM-CoT; useful data point in the north-star synthesis."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# DART — Distilling Autoregressive Reasoning to Silent Thought

Jiang, Wu, Zhan, Lai, Lian, [arXiv:2506.11752](https://arxiv.org/abs/2506.11752).

## TL;DR

A close cousin of CODI in the self-distillation family. Dual training pathways — autoregressive CoT + non-autoregressive "Silent Thought" (ST) — with a lightweight **Reasoning Evolvement Module (REM)** that aligns ST hidden states to the CoT pathway. At inference, only the ST pathway runs; answers come directly from a few ST tokens with no autoregressive decoding step. Claims performance gains over prior non-autoregressive baselines at zero extra latency.

## Method

- **CoT pathway.** Standard autoregressive reasoning (teacher-like).
- **ST pathway.** Non-autoregressive answer generation from a few Silent Thought tokens.
- **Reasoning Evolvement Module (REM).** Lightweight module on the ST pathway; aligns ST hidden states to the CoT pathway.
- **Inference.** Only the ST pathway is activated.

## Recipe

Self-distillation, similar to CODI but:
- Distillation target = CoT-pathway hidden states (multi-point, via REM), not a single pre-answer state.
- ST pathway is non-autoregressive — structurally different from CODI's autoregressive continuous rollout.
- REM evolves ST tokens iteratively (parallel).

## Results

- "Significant gains over non-autoregressive baselines without extra inference latency." Specific numbers not in abstract.

## Relevance

DART's REM is a concrete, published example of a **learned evolution module on the student pathway** that could be benchmarked against LT-Tuning's CPF fusion on the CODI stack. Same design philosophy — add a cheap module to shape implicit representations — with a different architectural inductive bias (non-autoregressive). Worth holding as a backup recipe for branch-d.

## Citation links to chase

- CODI self-distillation (base method).
- SIM-CoT auxiliary-decoder supervision (complementary family).
