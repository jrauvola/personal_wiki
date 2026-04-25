---
type: source
title: "JEPA-Reasoner — Decoupling Latent Reasoning from Token Generation"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/jepa
  - method/architecture
status: read
source_type: paper
arxiv_id: "2512.19171"
venue: "arXiv"
date_published: 2025-12-22
authors:
  - "Bingyang Kelvin Liu"
  - "Ziyu Patrick Chen"
  - "David P. Woodruff"
url: "https://arxiv.org/abs/2512.19171"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Current autoregressive language models couple high-level reasoning and low-level token generation into a single sequential process, making the reasoning trajectory vulnerable to compounding expression errors."
  - "JEPA-Reasoner decouples these tasks using a Joint-Embedding Predictive Architecture (JEPA) for pure latent-space reasoning and a separate Talker module for linguistic reconstruction."
  - "Error Containment: token-level failures cannot propagate into the latent reasoning chain."
  - "Representation of Uncertainty: the model maintains multiple hypotheses via mixed latent vectors."
  - "A 0.9B model achieves a 149.5% improvement in 8-shot GSM8K accuracy over a coupled Transformer baseline trained on identical data."
related:
  - "[[Stochastic Soft Thinking]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Hierarchical Reasoning Model]]"
  - "[[Shortcut Behavior]]"
sources:
  - "[[.raw/papers/2512.19171-jepa-reasoner]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Decoupled architecture is a paradigm-level alternative to CPF's fusion approach — different angle on the same problem (token-sampling noise propagates into reasoning). Not directly portable to CODI harness but informs the 'separate reasoner from talker' design space."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Architectural paradigm shift — too different from Qwen3 scaling target."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not relevant to detach/BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "JEPA + Talker decoupling is a distinct synthesis input — like SIM-CoT's auxiliary decoder but inverted (reasoner is the decoupled module). Useful for the writeup's architecture-taxonomy section. 149.5% GSM8K claim needs caveats (0.9B scale, controlled setting)."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# JEPA-Reasoner — Decoupling Latent Reasoning from Token Generation

Liu, Chen, Woodruff (David P. Woodruff — CMU, Algorithms), [arXiv:2512.19171](https://arxiv.org/abs/2512.19171), Dec 2025 / Jan 2026.

## TL;DR

Architectural paradigm: **decouple** reasoning (JEPA in pure latent space) from token generation (separate Talker module). Three claimed benefits: (1) Error Containment (token failures stay out of reasoning chain), (2) Continuous Guidance (generator sees entire lossless latent trajectory), (3) Uncertainty Representation (mixed latent vectors = multiple hypotheses). 0.9B model: +149.5% 8-shot GSM8K over coupled Transformer baseline on identical data.

## Method

### JEPA Reasoner

Pure latent-space reasoning — **no discrete token sampling in the reasoning chain**. Uses Joint-Embedding Predictive Architecture (LeCun-style). Trained to predict latent embeddings that encode the next reasoning state.

### Talker module

Separate linguistic-reconstruction network. Given the latent reasoning trajectory, the Talker produces tokens. Critically, the Talker runs *after* reasoning completes — so token-sampling errors cannot feed back into the reasoning chain.

### Mixed latent vectors for uncertainty

JEPA's latent can mix multiple hypotheses (superposition-like), preserved until the Talker collapses to tokens.

## Recipe

- **Scale:** 0.9B parameters.
- **Data:** 8-shot GSM8K eval.
- **Baseline:** coupled (standard autoregressive) Transformer trained on identical data.
- **Result:** +149.5% 8-shot GSM8K accuracy (read caveats: small scale, controlled experiments).

## Results

- **0.9B JEPA-Reasoner:** +149.5% 8-shot GSM8K over coupled baseline.
- Synthetic and natural language task gains.

## Relevance

- **Reference for branch-d.** Architectural alternative to CPF — both address the token-sampling-noise-in-reasoning problem, but JEPA decouples rather than anchors. Conceptually useful for framing.
- **Secondary for spar-latent-reasoning.** The decoupling philosophy is a distinct synthesis input alongside V2 / SIM-CoT / LT-Tuning. But claims at 0.9B scale need validation at larger scales before we'd build on them.

## Citation links

- JEPA literature (LeCun, V-JEPA, I-JEPA) — upstream.
- [[COCONUT]] / [[CODI]] — sequential-latent-reasoning contrast.
- [[SIM-CoT]] — auxiliary-decoder parallel (JEPA inverts: reasoner is decoupled, not decoder).

## Artifacts

- **Paper:** [arXiv:2512.19171](https://arxiv.org/abs/2512.19171)
- **Code:** none.
- **Raw source:** [[.raw/papers/2512.19171-jepa-reasoner]]
