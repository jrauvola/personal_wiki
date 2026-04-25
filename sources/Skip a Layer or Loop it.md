---
type: source
title: "Skip a Layer or Loop it? (CoLa) — Test-Time Depth Adaptation"
source_type: paper
arxiv_id: "2507.07996"
venue: "arXiv"
date_published: 2025-07-10
authors:
  - "Ziyue Li"
  - "Yang Li"
  - "Tianyi Zhou"
url: "https://arxiv.org/abs/2507.07996"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "FINDING: Layers of a pretrained LLM can be treated as independent modules — skipped (fast thinking), repeated as RNNs (slow thinking), or combined — to build a sample-specific shallower/deeper architecture WITHOUT finetuning."
  - "METHOD (CoLa = Chain-of-Layers): Monte Carlo Tree Search (MCTS) per sample to find the optimal skip/loop sequence; no parameter updates required."
  - "RESULT: For >75% of samples the MCTS-optimized CoLa differs from the vanilla static architecture — shows that per-sample depth adaptation is broadly beneficial."
  - "RESULT: CoLa generalizes across math and commonsense reasoning benchmarks; works on multiple pretrained LLM backbones without fine-tuning."
  - "FRAMING: Unifies layer-skipping (early exit) and layer-looping (depth recurrence) under a single test-time architectural-search lens."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "CoLa is a zero-training per-sample depth adapter — a cheap upper-bound on what inference-time recurrence could achieve on Qwen3. If Qwen3 + CoLa matches Qwen3 + trained recurrence, retrofitting isn't needed."
  - slug: "branch-d"
    relevance: secondary
    why: "CoLa shows that the capability is partially latent — argues for lightweight trained refinement (CPF, LoRA) rather than full conversion."
  - slug: "branch-b"
    relevance: secondary
    why: "MCTS search over skip/loop is an ablation tool: measure which layers benefit from looping — informs detach boundary placement."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Complements [[Inner Loop Inference]] as the other canonical train-free recurrence-extraction method. Pairs with [[From Growing to Looping]] (retrofit via middle-block looping on trained models)."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/inference-time
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Inner Loop Inference]]"
  - "[[From Growing to Looping]]"
  - "[[Mixture of Recursions]]"
sources:
  - "[[.raw/papers/2507.07996-skip-or-loop]]"
---

# Skip a Layer or Loop it? (CoLa)

## TL;DR
Treat each layer of a pretrained LLM as an independent module that can be skipped (fast thinking), looped (slow thinking), or stacked in a sample-specific sequence. Use MCTS to search the Chain-of-Layers (CoLa) per sample. No fine-tuning. For >75% of samples the optimal CoLa differs from the vanilla static architecture, and CoLa beats static on math and commonsense reasoning across backbones.

## Relevance
Establishes that capability for variable-depth reasoning is already latent in pretrained LLMs. Combined with [[Inner Loop Inference]] and [[From Growing to Looping]], forms the "recurrent capability is present before training" case against mandatory from-scratch recurrent pretraining.
