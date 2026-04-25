---
type: source
title: "Encode-Think-Decode (ETD) — Recursive Latent Thoughts Mid-Training"
source_type: paper
arxiv_id: "2510.07358"
venue: "arXiv"
date_published: 2025-10-08
authors:
  - "Yeskendir Koishekenov"
  - "Aldo Lipani"
  - "Nicola Cancedda"
url: "https://arxiv.org/abs/2510.07358"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "RESULT: ETD gives +28.4% relative accuracy on reasoning benchmarks across 17 tasks without changing parameter count, hyperparameters, or training data composition."
  - "RECIPE: Partition a base model into latent-encoder E / thinking-block T / latent-decoder D; during mid-training iterate only the small T subset of reasoning-relevant layers (not the whole model)."
  - "RECIPE: Iterate T at inference for adaptive test-time compute — same core block is reused recursively, similar to Huginn/Ouro but retrofitted into an existing architecture."
  - "OBSERVATION: T is identified via interpretability studies showing that the crucial reasoning computation is concentrated in a small band of middle layers — iterating them amplifies reasoning without disrupting surrounding capability."
  - "AFFILIATION: FAIR at Meta + UCL — lends credibility to the method; provides a production-scale retrofit path distinct from from-scratch recurrent pretraining."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "ETD partitions model into E/T/D and iterates only T — directly compatible with Qwen3 scaling: retrofit depth recurrence on a middle-layer subset rather than the whole stack. Cheaper than full conversion."
  - slug: "branch-d"
    relevance: secondary
    why: "E/T/D partition is independently-derived Prelude/Core/Coda structure — informs where CPF alignment signals could live, but the recipe iterates a middle-layer subset without CPF-style vocab anchoring. Downgraded primary → secondary this sweep: related methodology rather than CPF implementation target."
  - slug: "branch-b"
    relevance: secondary
    why: "Iterating only a subset of middle layers naturally localizes detach boundaries; suggests a smaller effective BPTT depth."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Middle-layer recurrence as a canonical retrofit primitive; complements [[From Growing to Looping]] (which finds similar middle-block looping behavior)."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Retrofitted Recurrence]]"
  - "[[From Growing to Looping]]"
  - "[[Mixture of Recursions]]"
sources:
  - "[[.raw/papers/2510.07358-encode-think-decode]]"
---

# Encode-Think-Decode (ETD)

## TL;DR
Add latent reasoning to a pretrained model by identifying a small subset of "reasoning-relevant" middle layers (the "thinking block" T), then iterate only those during mid-training. The rest of the architecture (encoder E, decoder D) stays fixed. At inference, iterate T more for extra test-time compute. +28.4% relative on 17 reasoning benchmarks.

## Method
- **E / T / D partition**: E embeds inputs and retrieves entity info; T is the iterated core (small subset of original layers); D unembeds and holds the prediction head.
- **Mid-training**: iterate T for k steps, backprop through the whole unroll. Preserves architecture / parameter count / hyperparameters / data.
- **Inference**: choose iteration count adaptively.

## Results
- 17 benchmarks across 6 categories (factual, reading, commonsense, math, multi-disciplinary, reasoning-intensive).
- Strongest gains on math (GSM8K, MATH) — mirrors Huginn's task-dependent saturation pattern.

## Relevance
ETD is the minimum-invasive conversion recipe — no full retraining, no data changes, no architecture surgery. Likely the cheapest prototype path for Qwen3 retrofits.
