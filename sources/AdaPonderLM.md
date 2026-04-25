---
type: source
title: "AdaPonderLM — Gated Pondering with Token-Wise Adaptive Depth"
source_type: paper
arxiv_id: "2603.01914"
venue: "arXiv"
date_published: 2026-03-02
authors:
  - "Shixiang Song"
  - "He Li"
  - "Zitong Wang"
  - "Boyi Zeng"
  - "Feichen Song"
  - "Yixuan Wang"
  - "Zhiqin John Xu"
  - "Ziwei He"
  - "Zhouhan Lin"
url: "https://arxiv.org/abs/2603.01914"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "RECIPE: iteration-specific MLP gates produce per-token halting probabilities over a monotonic halting mask — each token decides when to stop recurring, learned self-supervised during pretraining, no manual per-token/per-layer pruning ratios."
  - "RECIPE: KV-reuse mechanism: halted tokens' cached K/V states are reused in subsequent iterations, giving train-inference consistency (no off-distribution gap when some tokens stop early)."
  - "RESULT: Scales from Pythia-70M to Pythia-2.8B; reduces inference compute by ~10% at matched perplexity / competitive downstream accuracy."
  - "RELATIONSHIP: Extends ACT (Adaptive Computation Time) and Early Exit — but operates at the recurrent-iteration level rather than per-layer in a fixed stack."
  - "DESIGN: Monotonic mask ensures once a token halts it stays halted — simplifies KV cache management and keeps halting decisions stable."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Token-wise adaptive depth is the missing inference-efficiency piece for Qwen3 scaling: lets us report 'avg iterations per token' instead of worst-case full-depth compute."
  - slug: "branch-d"
    relevance: secondary
    why: "Gating mechanism has structural similarity to HRPO's learnable hidden-state/token fusion — adds a halting dimension to the gate. Worth cross-referencing in CPF design."
  - slug: "branch-b"
    relevance: secondary
    why: "Monotonic mask + KV reuse is a clean test-train consistency story that informs detach-boundary design (halted tokens don't need gradients past halt step)."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Self-supervised halting is the canonical efficiency add-on for any recurrent-depth model in the umbrella taxonomy."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Mixture of Recursions]]"
  - "[[Adaptive Loops and Memory]]"
  - "[[PonderLM-3]]"
sources:
  - "[[.raw/papers/2603.01914-adaponderlm]]"
---

# AdaPonderLM

## TL;DR
A recurrent LM that learns token-wise halting during pretraining. Iteration-specific MLP gates produce halting probabilities; a monotonic halting mask ensures once a token halts it stays halted; halted tokens reuse cached KV states, giving train-inference consistency. 10% inference compute reduction on Pythia 70M-2.8B at matched perplexity.

## Method
- **Gate**: at iteration i, an MLP_i reads the current hidden state and outputs gate probability p_i ∈ [0,1].
- **Monotonic mask**: persistent mask m^i = m^(i-1) · (1 - halt_i); tokens can only transition from "recurring" to "halted" — no oscillation.
- **KV reuse**: halted tokens use cached K/V from the iteration at which they halted — keeps attention consistent without gradient through further iterations.
- **Self-supervised**: halting is learned jointly with LM loss during pretraining.

## Results
- Scales 70M → 2.8B (continued pretraining on Pythia backbones).
- ~10% inference FLOP reduction at matched PPL.
- Token-wise halting distributions concentrate on content tokens (analysis shows gates learn difficulty).

## Relevance
Adaptive depth is the obvious efficiency lever for recurrent LMs. AdaPonderLM's monotonic-mask + KV-reuse design is clean and self-contained — likely the reference implementation to cite when our recurrent runs report per-token variable depth.
