---
type: source
title: "LoopFormer — Elastic-Depth Looped Transformers via Shortcut Modulation"
source_type: paper
arxiv_id: "2602.11451"
venue: "arXiv"
date_published: 2026-02-11
authors:
  - "Ahmadreza Jeddi"
  - "Marco Ciccone"
  - "Babak Taati"
url: "https://arxiv.org/abs/2602.11451"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "PROBLEM: Existing looped transformers train at a fixed number of unrolls. Representations collapse when evaluated at shorter or longer depths — off-distribution compute schedules fail."
  - "METHOD: LoopFormer adds shortcut modulation — a lightweight learned module that modulates the residual shortcut depending on iteration index, letting the shared block 'know which iteration it is' and adapt behavior."
  - "CLAIM: Shortcut modulation enables elastic-depth training — a single model trained once performs well across variable inference depths, unlike plain looped transformers."
  - "FRAMING: Positions looped transformers as having an inductive bias toward latent reasoning and algorithmic tasks; elastic-depth training makes that bias practically usable."
  - "IMPLICATION: Addresses a known failure mode of naive looped models — complements Huginn's solution (Poisson-Lognormal iteration sampling) with an architectural alternative."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Architectural alternative to Huginn's iteration sampling; worth considering as a Qwen3 retrofit component. Downgraded primary → secondary this sweep: no released code or weights, and LoopFormer's primary relevance is as a design option not an implementation input."
  - slug: "branch-b"
    relevance: secondary
    why: "Iteration-aware shortcut is a stability mechanism (tells the block what iteration it is) — cross-cuts with detach/fp32 for stable deep unrolls."
  - slug: "branch-d"
    relevance: secondary
    why: "Shortcut modulation + LT-Tuning CPF are structurally similar (both add an iteration-conditional signal). Worth comparison in CPF writeup."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Architectural variant in the looped-transformer family worth citing in the taxonomy section. Downgraded primary → secondary this sweep: no code/weights, conceptually similar to Huginn's iteration-randomization; taxonomic completeness rather than synthesis input."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Ouro]]"
  - "[[Parcae]]"
  - "[[Mixture of Recursions]]"
sources:
  - "[[.raw/papers/2602.11451-loopformer]]"
---

# LoopFormer

## TL;DR
Looped transformers trained with a fixed number of unrolls collapse when evaluated off-distribution (shorter or longer depths). LoopFormer fixes this by adding **shortcut modulation** — a lightweight module that modulates the residual shortcut conditional on iteration index, letting the shared block adapt behavior per iteration. Enables elastic-depth training from a single run.

## Relevance
Architectural alternative to Huginn's iteration-count randomization. Both solve the same off-distribution problem; LoopFormer via conditioning, Huginn via training-distribution diversity. Cross-cuts naturally with CPF (Branch D) — both inject an iteration-conditional signal into the shared block.
