---
type: source
title: "Depth-Recurrent Attention Mixtures (Dreamer)"
source_type: paper
arxiv_id: "2601.21582"
venue: "arXiv"
date_published: 2026-01-29
authors:
  - "Jonas Knupp"
  - "Jan Hendrik Metzen"
  - "Jeremias Bohn"
  - "Georg Groh"
  - "Kristian Kersting"
url: "https://arxiv.org/abs/2601.21582"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "CRITIQUE: Prior depth-recurrent work (including Huginn) uses partially fixed layer stacks, lacks matched baselines (combined FLOP-, parameter-, AND memory-matched), and ignores the bottleneck of constant hidden size — which restricts many-step latent reasoning."
  - "METHOD (Dreamer): Combines three attention variants — sequence attention, depth attention, sparse expert attention — in a modular depth-recurrent framework. Depth attention provides attention ALONG the iteration axis, alleviating the hidden-size bottleneck."
  - "DESIGN: Decouples scaling dimensions so depth-recurrent models scale efficiently and effectively — width, depth, and sparsity become independently tunable."
  - "RESULT: Outperforms matched baselines on language reasoning benchmarks — explicit depth-attention + expert attention unlocks gains that plain depth-recurrence leaves on the table."
  - "IMPLICATION: Constant hidden size is a real bottleneck for many-step latent reasoning — iterating a single fixed-width block loses information that depth-attention recovers."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Critique + solution for the hidden-size bottleneck is directly relevant to Qwen3 scaling — Qwen3-4B's 2048 hidden may limit recurrence depth; Dreamer gives a principled fix via depth attention."
  - slug: "branch-b"
    relevance: secondary
    why: "Matched-baseline discipline (combined FLOP + param + memory) is the evaluation methodology we should adopt for detach/fp32 ablations."
  - slug: "branch-d"
    relevance: secondary
    why: "Depth attention is an alternative to CPF for getting information flow across iterations — structurally comparable. Worth cross-reference in CPF writeup."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Architectural critique of the recurrent-depth family — essential methodology note. Pairs with [[Stability and Generalization in Looped Transformers]]."
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
  - "[[Stability and Generalization in Looped Transformers]]"
sources:
  - "[[.raw/papers/2601.21582-depth-recurrent-attention-mixtures]]"
---

# Depth-Recurrent Attention Mixtures (Dreamer)

## TL;DR
Critiques prior depth-recurrent work for (1) partially fixed layer stacks, (2) lack of combined FLOP/param/memory-matched baselines, (3) ignoring the constant-hidden-size bottleneck. Proposes Dreamer: a modular framework combining sequence attention + depth attention + sparse expert attention. Depth attention (attending along the iteration axis) alleviates the hidden-size bottleneck. Outperforms matched baselines on reasoning.

## Relevance
Methodological discipline + an architectural fix. If our Qwen3 retrofits saturate at moderate depths, the hidden-size bottleneck is a likely cause — Dreamer gives a principled lever.
