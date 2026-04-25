---
type: source
title: "Step-resolved data attribution for looped transformers (SDI)"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/interpretability
  - type/source
  - method/data-attribution
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
sources:
  - "[[.raw/papers/2602.10097-step-resolved-attribution]]"

source_type: paper
arxiv_id: "2602.10097"
venue: "arXiv"
date_published: 2026-02-10
authors:
  - "Georgios Kaissis"
  - "David Mildenberger"
  - "Juan Felipe Gomez"
  - "Martin J. Menten"
  - "Eleni Triantafillou"
url: "https://arxiv.org/abs/2602.10097"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "Standard training-data-influence estimators (TracIn) aggregate over recurrent iterations and cannot tell *when* during a looped forward pass a training example matters."
  - "Step-Decomposed Influence (SDI) unrolls the recurrent computation graph and attributes influence to specific loop iterations, producing a length-τ influence trajectory per training example."
  - "A TensorSketch implementation of SDI never materialises per-example gradients — practical at transformer scale."
  - "On looped GPT-style models + algorithmic reasoning tasks, SDI matches full-gradient baselines with low error."
  - "SDI supports per-step insights into latent reasoning, opening step-resolved data attribution for looped LMs."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Data attribution is orthogonal to Qwen3 architecture-dependent scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a gradient-stability or detach tool."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool."
  - slug: "branch-d"
    relevance: reference
    why: "Attribution per loop iteration is a future companion to tuned-lens — both unpack per-step latent computation — but TracIn-style influence is not on Branch D's critical path."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Step-resolved influence is a powerful complement to our planned tuned-lens / activation-oracle pipeline on Ouro — same interpretability target (per-loop latent computation), different method (data attribution vs probes); directly reusable once we need to ask *which training examples* shape a given loop step."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Step-resolved data attribution for looped transformers (SDI)

## TL;DR

TracIn gives one scalar for training-example influence across the whole forward pass; that aggregates over τ loop iterations for a looped transformer. **Step-Decomposed Influence (SDI)** unrolls the recurrent computation graph and produces a length-τ *influence trajectory* per training example, letting you localise when during the recurrence an example matters. A **TensorSketch** implementation avoids per-example gradient materialisation.

## Method

- Unroll the τ-loop computation graph.
- Attribute TracIn components to the specific loop step in the unrolling.
- Output: for each training example `z_train` and each test instance `z_test`, a vector of length τ giving per-step influence.
- TensorSketch projection replaces explicit per-example gradient tensors — enables scale.

## Results

- On looped GPT-style models with algorithmic reasoning tasks:
  - SDI scales to transformer-scale models.
  - Matches full-gradient baselines with low error.
- Supports per-step interpretability + data attribution tasks.

## Relevance

- **Natural companion to tuned-lens** for per-loop mechanistic analysis of [[Ouro]]. Tuned lens answers "what does the model 'think' at step t?"; SDI answers "which training data shaped that belief at step t?".
- Open question: does Ouro's reasoning-stage specialization (T=1 → T=4 gains on reasoning MMLU categories, not retrieval — see [[Manipulation vs Capacity]]) show up as training-example influence concentrated in reasoning data at later steps? SDI could test this directly.
- Orthogonal to our Branch D LT-Tuning experiments, but very relevant for the Ouro-interpretability pipeline in the SPAR writeup.

## Cross-links

- [[Ouro]] — primary testbed for this tool in our vault.
- [[LoopLM]] — the model class SDI is designed for.
