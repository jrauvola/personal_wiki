---
type: source
title: "Retrofitted Recurrence — Depth-Recurrent Conversion of Pretrained LMs"
source_type: paper
arxiv_id: "2511.07384"
venue: "arXiv"
date_published: 2025-11-10
authors:
  - "Sean McLeish"
  - "Ang Li"
  - "John Kirchenbauer"
  - "Dayal Singh Kalra"
  - "Brian R. Bartoldson"
  - "Bhavya Kailkhura"
  - "Avi Schwarzschild"
  - "Jonas Geiping"
  - "Tom Goldstein"
  - "Micah Goldblum"
url: "https://arxiv.org/abs/2511.07384"
code_repo: "https://github.com/mcleish7/retrofitting-recurrence"
has_weights: true
status: read
confidence: high
key_claims:
  - "RESULT: TinyLlama/OLMo-2-1B/Llama-3.2-1B can all be converted to depth-recurrent models via continued training; at matched training FLOPs the recurrent model beats the non-recurrent original on math benchmarks."
  - "RECIPE: A curriculum of recurrences that gradually increases effective depth (training recurrence k) over the course of conversion preserves base capabilities while adding test-time depth scaling — preserves accuracy AND reduces total compute."
  - "RECIPE: Muon optimizer > AdamW for training recurrent models (Section 4.3.1); truncated BPTT through last 8 passes of recurrent block R matches Huginn-style training and keeps memory O(1) in r."
  - "RESULT: Prelude parameters keep updating every step because the skip connection injects prelude output into every iteration — same as Huginn."
  - "RESULT: At inference, retrofitted recurrent models are competitive with fixed-depth baselines at k recurrences and outperform them when more iterations are spent (test-time compute scaling without new params)."
  - "RELEVANCE: 'Similar to how one would extend context length during late pretraining' — reframes depth-recurrence conversion as a late-stage pretraining recipe, not a from-scratch requirement."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Retrofit recipe lets us add depth-recurrence to Qwen3-4B without a 800B-token from-scratch run — directly applicable to our scaling branch. Pairs naturally with post-hoc latent-scaffolding (CODI/LT-Tuning) comparison."
  - slug: "branch-b"
    relevance: primary
    why: "k=8 truncated BPTT replicated here on different base models — strong external evidence for the minimum-sufficient detach story across TinyLlama / OLMo / Llama-3.2-1B. Multiple-model validation is what Branch B needs."
  - slug: "branch-d"
    relevance: secondary
    why: "An alternative retrofit path: pure depth recurrence + curriculum, no CPF anchor. Contrast for the LT-Tuning CPF writeup — 'how do you add latent depth without vocab-anchoring?'"
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Huginn follow-up from the same UMD lab — canonical conversion recipe for the recurrent-depth family. Pairs with [[Scaling Up TTC]]."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - domain/curriculum
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[From Growing to Looping]]"
  - "[[Ouro]]"
  - "[[Parcae]]"
  - "[[AdaPonderLM]]"
  - "[[Mixture of Recursions]]"
sources:
  - "[[.raw/papers/2511.07384-retrofitted-recurrence]]"
---

# Retrofitted Recurrence

## TL;DR
Convert an off-the-shelf pretrained non-recurrent LM (TinyLlama, OLMo-2-1B, Llama-3.2-1B) into a depth-recurrent model via continued training with a curriculum of increasing recurrence k. At matched training FLOPs the recurrent model beats the non-recurrent original on math; at inference it trades params for test-time compute.

## Method
- **Initialization**: duplicate/fold existing layers into a recurrent block R; prelude + coda wrap R exactly as in Huginn.
- **Curriculum of recurrences**: during conversion, gradually raise the Poisson-Lognormal distribution's mean k (train recurrence). Avoids the collapse that would occur if a non-recurrent model were forced immediately to train at high k.
- **Truncated BPTT**: backprop only through last 8 passes of R — matches Huginn recipe.
- **Optimizer**: Muon outperforms AdamW for recurrent training. Appears robust across base models.

## Results
- On math: matched-FLOP conversion to recurrent > continued non-recurrent post-training for all three base models.
- Language modeling benchmarks remain stable (no catastrophic loss of base capability).
- Test-time compute scaling recovers: accuracy climbs with inference recurrence count beyond training k.

## Relevance
- Branch A: adds an experimental axis — convert Qwen3-4B to depth-recurrent via curriculum, compare against our latent-scaffolding baselines at matched FLOPs.
- Branch B: cross-model confirmation that k=8 truncated BPTT is the load-bearing memory trick.
- SPAR: directly extends [[Scaling Up TTC]] with the missing "can we do this without a from-scratch Frontier run?" recipe.
