---
type: source
title: "Tiny Recursive Model (TRM)"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/architecture
  - source/paper
status: read
source_type: paper
arxiv_id: "2510.04871"
venue: "arXiv"
date_published: 2025-10-06
authors:
  - "Alexia Jolicoeur-Martineau"
url: "https://arxiv.org/abs/2510.04871"
code_repo: "https://github.com/SamsungSAILMontreal/TinyRecursiveModels"
has_weights: false
confidence: high
projects:
  - slug: spar-latent-reasoning
    relevance: secondary
    why: "Recursive-refinement latent reasoning with explicit y/z split — adjacent to COCONUT/CODI, user flagged as lead for 'scratchpad' precedence."
  - slug: branch-a
    relevance: reference
    why: "Tiny-scale recursive reasoning; not Qwen3-family, but scaling posture informs discussion."
  - slug: branch-b
    relevance: reference
    why: "Full-recursion backprop (no truncation) contrasts with V2/V3/V4 detach ablation direction."
  - slug: branch-c
    relevance: not-applicable
    why: "Not a probe-methodology or Qwen3-configuration paper."
  - slug: branch-d
    relevance: reference
    why: "Does not modify CODI or discrete-vocab anchor mechanism; recurrence-style only."
last_reviewed: 2026-04-22
reviewed_by: autoreview
key_claims:
  - "A single 2-layer network recursing n=6 inner steps per supervision step with T=3 supervision iterations outperforms HRM's two-network setup."
  - "The network updates latent reasoning feature z given (x, y, z), then refines answer y given (z, y); only the final y receives explicit loss."
  - "Only the last supervision iteration runs with gradients; first T-1 iterations run without gradients to refine y and z."
  - "Loss combines softmax CE on answer tokens with binary CE on a halting head trained to predict whether the current answer is correct."
  - "7M parameters achieves 45% ARC-AGI-1 and 8% ARC-AGI-2, beating DeepSeek R1, o3-mini, Gemini 2.5 Pro with <0.01% of their parameter counts."
  - "Latent z is never decoded or supervised at intermediate steps — it remains an internal reasoning representation. TRM has no discrete scratchpad side-channel."
related:
  - "[[Hierarchical Reasoning Model]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Deep Equilibrium Models]]"
  - "[[Alexia Jolicoeur-Martineau]]"
  - "[[Research - Latent Scratchpad Precedence]]"
sources: []
---

# Tiny Recursive Model (TRM)

**arXiv:** [2510.04871](https://arxiv.org/abs/2510.04871) | **Code:** [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels) | **Date:** 2025-10-06

## Abstract (verbatim)

"Hierarchical Reasoning Model (HRM) is a novel approach using two small neural networks recursing at different frequencies. This biologically inspired method beats Large Language models (LLMs) on hard puzzle tasks such as Sudoku, Maze, and ARC-AGI while trained with small models (27M parameters) on small data (around 1000 examples). HRM holds great promise for solving hard problems with small networks, but it is not yet well understood and may be suboptimal. We propose Tiny Recursive Model (TRM), a much simpler recursive reasoning approach that achieves significantly higher generalization than HRM, while using a single tiny network with only 2 layers. With only 7M parameters, TRM obtains 45% test-accuracy on ARC-AGI-1 and 8% on ARC-AGI-2, higher than most LLMs (e.g., Deepseek R1, o3-mini, Gemini 2.5 Pro) with less than 0.01% of the parameters."

## Method summary

Single network `f(x, y, z)` with two call patterns per supervision step:
1. **Update latent z:** repeatedly, `z ← f_z(x, y, z)` for `n = 6` inner iterations.
2. **Refine answer y:** once, `y ← f_y(z, y)`.

This `(6 × z-update + 1 × y-update)` block is a "supervision iteration." `T = 3` such iterations run per training step; iterations `1..T-1` run without gradients (improve y, z as a warm-up), iteration `T` runs with gradients for backprop.

**Loss:** softmax CE on final y + BCE on a halting head (predicts answer correctness).

## Relevance to Latent Scratchpad (W3.5)

TRM is **NOT a scratchpad architecture**. Latent z is never decoded to discrete tokens at intermediate steps. There is no gate, no discrete side-channel, no human-readable notes. The paper is adjacent because it is another latent-reasoning formulation (like COCONUT/CODI) with an internal latent that runs several update steps per outer step — but the internal state stays continuous throughout.

The user's `Latent Scratchpad` proposal — latent primary + sparse discrete interpretable notes via a learned gate — is **orthogonal to TRM's design axis** (recursion depth/count) and is not anticipated by TRM.

## Comparison to HRM

| Aspect | HRM | TRM |
|--------|-----|-----|
| Networks | Two (fL, fH) | One |
| Layers | 4 per network | 2 total |
| Parameters | 27M | 7M |
| Justification | Fixed-point theorem | Direct backprop through full recursion |
| Forward passes/supervision step | 2 | 1 |

## Code / weights

Code is released: [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels). No pretrained weights flagged in abstract / README excerpts observed; training is cheap enough that reproduction is the expected path.
