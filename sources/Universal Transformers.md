---
type: source
title: "Universal Transformers (Dehghani et al. 2019)"
source_type: paper
arxiv_id: "1807.03819"
venue: "ICLR 2019"
date_published: 2018-07-10
authors:
  - "Mostafa Dehghani"
  - "Stephan Gouws"
  - "Oriol Vinyals"
  - "Jakob Uszkoreit"
  - "Łukasz Kaiser"
url: "https://arxiv.org/abs/1807.03819"
code_repo: "https://github.com/tensorflow/tensor2tensor"
has_weights: false
status: read
confidence: high
key_claims:
  - "Universal Transformer applies a single shared transformer block T times to each position, combining Transformer parallelism with the recurrent inductive bias of RNNs."
  - "Under certain assumptions Universal Transformers are Turing-complete; standard Transformers with finite depth are not."
  - "A per-position dynamic halting mechanism (ACT-based, Graves 2016) lets different tokens receive different amounts of computation — 'harder' positions ponder more."
  - "UTs outperform standard Transformers on algorithmic (copy, reverse, addition) and language-understanding tasks; achieve SOTA on LAMBADA and +0.9 BLEU on WMT14 En-De."
  - "The shared-block parameterization means UT has the same parameter count as a single Transformer layer regardless of iteration count T — depth is compute, not parameters."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Direct ancestor of every modern recurrent-depth latent reasoner (Ouro, HRM, Mixture of Recursions, LoopLM). Taxonomic cornerstone of the writeup's genealogy section."
  - slug: "branch-a"
    relevance: secondary
    why: "Parameter-tied depth recurrence is the scalability precedent behind Ouro and HRM; relevant when scaling story pushes toward depth-recurrent designs."
  - slug: "branch-b"
    relevance: secondary
    why: "UT's BPTT-through-T-steps is the ancestor pattern of CODI's M-step latent rollout; the detach/BPTT trade-offs are essentially the same problem."
  - slug: "branch-c"
    relevance: reference
    why: "Benchmark methodology unrelated."
  - slug: "branch-d"
    relevance: reference
    why: "UT has no fusion/anchor mechanism; orthogonal to CPF axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/recurrent-depth
  - method/act-halting
  - type/source
related:
  - "[[Adaptive Computation Time]]"
  - "[[PonderNet]]"
  - "[[Ouro]]"
  - "[[Hierarchical Reasoning Model]]"
  - "[[Mixture of Recursions]]"
  - "[[LoopLM]]"
  - "[[Mostafa Dehghani]]"
sources: []
---

# Universal Transformers (Dehghani 2019)

## TL;DR

Depth-recurrent Transformer: apply the same transformer block T times to each position, with a per-position ACT halting head. Same parameter count as a single layer; effective depth = T. Turing-complete under assumptions. First Transformer-era latent-reasoning architecture.

## Why this matters to our project

UT is the **architectural ancestor** of every modern depth-recurrent latent reasoner. The design pattern — "share one block's parameters, iterate T times, let each token halt when ready" — is reused nearly verbatim by:

- [[Ouro]] (Huggingface 2024) — loop LM that iterates a shared block; no ACT halting, uses fixed T.
- [[Hierarchical Reasoning Model]] (Wang 2025) — two-level recurrent modules with Q-learning halting head.
- [[Mixture of Recursions]] (Bae 2025) — routing variant that picks how many times to apply the block per token.
- [[LoopLM]] / [[AdaPonderLM]] / [[PonderLM-3]] — direct LM generalizations.

The **key innovation** that CODI inherits: "compute = apply the same transformer block multiple times" rather than "compute = stack more distinct layers." CODI's M-step latent rollout is essentially this — except CODI's block is the full LLM, not a shared-weight sub-block, and the iteration is gated by `<bot>` / `<eot>` rather than ACT halting.

## Method

1. **Shared block:** one transformer layer with multihead self-attention + position-wise FFN, parameters $\theta$.
2. **Recurrence over depth:** $h_t^{(m+1)} = \text{Block}(h^{(m)}; \theta)$ for $m = 0, 1, ..., T-1$.
3. **Per-position halting (ACT):** at each step $m$, each position $t$ emits a halt probability; when its cumulative halt $\geq 1-\epsilon$ that position is frozen. Iteration continues until all positions halt (or $T_{\max}$ reached).
4. **BPTT over T steps.** Gradient flows through entire trajectory.

## Results

- **bAbI, LAMBADA:** SOTA.
- **Copy / reverse / addition algorithmic tasks:** outperforms Transformer by wide margins.
- **WMT14 En-De:** +0.9 BLEU.

## Key theoretical claim

UT is Turing-complete under mild assumptions (arbitrary-precision arithmetic, unbounded T). Standard Transformers with fixed finite depth are not. This is the formal motivation for the entire "more compute at inference → better reasoning" line of thought that culminates in COCONUT, CODI, and o1-style reasoning models.

## Relevance to CODI / COCONUT contrast

UT shows that **depth-recurrent Transformers work** — but only with either (a) heavy synthetic-task curriculum, or (b) ACT halting to prevent collapse. COCONUT doesn't iterate a shared block; it iterates the full LLM in latent mode. CODI does the same. This is a departure from UT's parameter-sharing approach — modern latent reasoners use the *full pretrained LLM* as the recurrent block, leveraging the LLM's existing computational capacity rather than training a small shared block from scratch.

## Citation links to chase

- [[Adaptive Computation Time]] (Graves 2016) — source of UT's halting mechanism.
- Dehghani 2019 follow-up on depth-recurrent scaling.
- [[Ouro]] / [[LoopLM]] — modern heirs.
