---
type: entity
entity_type: person
title: "Sainbayar Sukhbaatar"
role: "First author of End-to-End Memory Networks (2015); long-tenured Meta FAIR researcher in memory-augmented and long-context architectures"
first_mentioned: "[[End-to-End Memory Networks]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/external-memory
  - affiliation/meta-fair
status: developing
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Founding architect of end-to-end soft-attention over discrete memory - the conceptual ancestor of every modern attention-over-side-channel mechanism, including Latent Scratchpad."
  - slug: "branch-d"
    relevance: secondary
    why: "MemN2N's 'Linear-Start' training trick directly maps to the gate-init phase of W3.5 Latent Scratchpad. Sukhbaatar has continued working on long-context memory (Adaptive Span, etc.)."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-LLM era; not in scaling debate."
  - slug: "branch-b"
    relevance: reference
    why: "Memory-attention concepts adjacent to detach mechanisms."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[End-to-End Memory Networks]]"
  - "[[Jason Weston]]"
sources:
  - "[[End-to-End Memory Networks]]"
---

# Sainbayar Sukhbaatar

## Position
Research scientist at Meta FAIR (formerly Facebook AI Research). PhD from NYU (Courant, advised by Rob Fergus).

## Core contributions

- **End-to-End Memory Networks, 2015** ([[End-to-End Memory Networks]], NeurIPS 2015, arXiv:1503.08895, with Szlam, Weston, Fergus). First end-to-end-trainable soft-attention model over a discrete memory bank. Replaced the strong-supervision per-hop loss of original Memory Networks (Weston 2014) with backprop-only training. Introduced the Linear-Start training trick.

- **Adaptive Attention Span**, 2019 (ACL). Per-head learnable attention span — a soft mask that lets each attention head learn its own context length. Direct ancestor of modern long-context fine-tuning recipes.

- **Augmenting Self-Attention with Persistent Memory**, 2019 (with Bojanowski, Joulin). Adds learnable persistent vectors to self-attention; conceptual prior for prefix-tuning.

- **Branch-Train-Merge / Branch-Train-Mix**, 2022-23. Modular LM training via specialist domains then merging.

## Why relevant to this project

Sukhbaatar's MemN2N established the founding pattern that **soft-attention over discrete memory is end-to-end trainable**. This is the gradient-flow property W3.5 Latent Scratchpad inherits when subsequent latent positions attend over emitted notes via standard self-attention.

The Linear-Start trick (start with linear, then re-add nonlinearities) is structurally identical to the Stage-A → Stage-B curriculum in W3.5: start with a soft / mostly-off gate, then sharpen.

## See also

- [[End-to-End Memory Networks]] — primary source page.
- [[Jason Weston]] — co-author, MemN2N + original Memory Networks (2014).
