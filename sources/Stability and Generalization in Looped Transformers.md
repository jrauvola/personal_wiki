---
type: source
title: "Stability and Generalization in Looped Transformers"
source_type: paper
arxiv_id: "2604.15259"
venue: "arXiv"
date_published: 2026-04-16
authors:
  - "Asher Labovich"
url: "https://arxiv.org/abs/2604.15259"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "THEORY: Introduces a fixed-point-based framework for looped Transformers analyzed along three stability axes — reachability, input-dependence, geometry — characterizing when fixed-point iteration yields meaningful predictions."
  - "THEOREM: Looped networks WITHOUT recall have countable fixed points and cannot achieve strong input-dependence — formalizes why re-injecting the input (Huginn's 'e' fed back every step) is load-bearing for scaling with input-specific behavior."
  - "IMPLICATION: Architectural choices (recall / no recall, normalization, shortcut modulation) determine whether a looped model extrapolates to harder problems or merely memorizes training-depth-specific solutions."
  - "FRAMING: Places looped Transformers in the Deep Equilibrium Models (DEQ) tradition — stability → generalization link."
projects:
  - slug: "branch-b"
    relevance: secondary
    why: "Theoretical framework useful for reframing detach ablations as stability-preserving, but abstract-only paper with no code. Downgraded primary → secondary this sweep: framing support rather than an empirical input."
  - slug: "branch-a"
    relevance: secondary
    why: "Explains when a looped architecture will generalize across depths — useful grounding for our 'why recurrence helps at scale' narrative."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Theoretical scaffolding for the looped-Transformer family; taxonomic/framing value. Downgraded primary → secondary this sweep: abstract-only, not yet a canonical citation (Parcae + Formal CoT vs Latent + Reasoning by Superposition already cover the theory axis)."
  - slug: "branch-d"
    relevance: reference
    why: "Theory: non-recall ≡ no input re-injection. CPF's injection of context at each latent step is in the 'recall' regime; gives a theoretical reason why anchoring helps."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/theory
  - domain/latent-reasoning
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Parcae]]"
  - "[[Formal CoT vs Latent]]"
  - "[[From Growing to Looping]]"
sources:
  - "[[.raw/papers/2604.15259-stability-generalization-looped]]"
---

# Stability and Generalization in Looped Transformers

## TL;DR
A theoretical framework for looped transformer analysis along three fixed-point stability axes — reachability, input-dependence, geometry. Key theorem: looped nets WITHOUT recall (no input re-injection) have countable fixed points and cannot achieve strong input-dependence; formalizes why Huginn's re-injected prelude output is essential.

## Relevance
Provides the formal vocabulary (reachability, input-dependence, geometry) for explaining WHY depth-recurrence generalizes or fails to — useful when writing up Branch B ablations and when framing the Branch A scaling story. Only an arxiv abstract was accessible at crawl time (HTML v1 not yet indexed); full-text ingest pending.
