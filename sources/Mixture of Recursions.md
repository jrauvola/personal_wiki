---
type: source
title: "Mixture-of-Recursions (MoR) — Token-Level Adaptive Recursion Depth"
source_type: paper
arxiv_id: "2507.10524"
venue: "arXiv"
date_published: 2025-07-14
authors:
  - "Sangmin Bae"
  - "Yujin Kim"
  - "Reza Bayat"
  - "Sungnyun Kim"
  - "Jiyoun Ha"
  - "Tal Schuster"
  - "Adam Fisch"
  - "Hrayr Harutyunyan"
  - "Ziwei Ji"
  - "Aaron Courville"
  - "Se-Young Yun"
url: "https://arxiv.org/abs/2507.10524"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "UNIFICATION: MoR combines parameter sharing (shared stack of layers reused across recursion steps — like Ouro/Huginn) AND adaptive computation (lightweight token-level routers assigning different recursion depths per token) in a single recursive transformer."
  - "METHOD: Router assigns each token a recursion depth at each step; quadratic attention compute is focused only where most useful — tokens with more assigned recursions get more attention iterations."
  - "RECIPE: Recursion-wise key-value caching — selectively stores K/V only for tokens designated for further recursion, eliminating redundant memory access across recursion steps."
  - "RESULT: Across pretraining runs from 135M → 1.7B parameters, MoR forms a new Pareto front over both plain recursive transformers (equal compute, better accuracy) and non-recursive baselines (fewer params, equal accuracy)."
  - "INFLUENTIAL: 8 influential-citations in 4 months — the current reference for token-level adaptive recursion depth; cited by Retrofitted Recurrence, AdaPonderLM, From Growing to Looping."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "MoR is the scaling-Pareto reference for recursive transformers — directly relevant to Qwen3 scaling. Matched pretraining runs 135M–1.7B give strong baseline curves."
  - slug: "branch-b"
    relevance: secondary
    why: "Recursion-wise KV caching is a related design axis for efficient-memory stories; useful background for the detach ablation framing. Downgraded primary → secondary this sweep: no released code, not a direct detach/fp32 ablation input."
  - slug: "branch-d"
    relevance: secondary
    why: "Token-level routing is an alternative to CPF's per-step vocab anchor — both are ways to make iteration behavior input-dependent. Compare in CPF writeup."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Most influential non-Huginn recursive-transformer paper in the umbrella. Pairs naturally with [[AdaPonderLM]] for the 'token-level adaptive depth' sub-family."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - domain/scaling
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[AdaPonderLM]]"
  - "[[Parcae]]"
  - "[[Retrofitted Recurrence]]"
  - "[[Ouro]]"
sources:
  - "[[.raw/papers/2507.10524-mixture-of-recursions]]"
---

# Mixture-of-Recursions (MoR)

## TL;DR
A unified recursive transformer that combines parameter sharing (reused layer stack) with token-level adaptive computation (lightweight routers per recursion step). Quadratic attention compute is focused only on tokens that need more iteration. A **recursion-wise KV cache** selectively stores K/V only for active tokens, eliminating redundant memory access. Pretraining runs 135M → 1.7B form a new Pareto front over plain recursive baselines.

## Method
- **Shared stack**: one block reused K_max times, like Huginn/Ouro.
- **Token-level router**: at each recursion step, a light router decides which tokens continue vs exit.
- **Recursion-wise KV cache**: K/V is stored only for still-active tokens — memory shrinks with the active set.

## Results
- Pareto front: at equal compute MoR beats plain recursive transformers; at equal accuracy it uses fewer params than non-recursive baselines.
- Validates token-level adaptive recursion as a primary scaling lever.

## Relevance
Most influential recursive-transformer paper outside Huginn/Ouro. Cited by Retrofitted Recurrence and AdaPonderLM — likely the reference implementation for token-level adaptive depth going forward.
