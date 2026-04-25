---
type: entity
entity_type: person
title: "Mostafa Dehghani"
role: "First author, Universal Transformers (ICLR 2019); key architect of depth-recurrent Transformer variants"
first_mentioned: "[[Universal Transformers]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/architecture
  - affiliation/google
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Universal Transformers is the direct ancestor of every modern depth-recurrent latent reasoner (Ouro, HRM, Mixture of Recursions, CODI's M-step rollout). Essential genealogy node."
  - slug: "branch-a"
    relevance: reference
    why: "UT's parameter-sharing across depth positions is the scalability precedent behind Ouro-style training."
  - slug: "branch-b"
    relevance: reference
    why: "UT's BPTT over T dynamic steps is the historical antecedent of CODI's M-step rollout with detach variants."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
  - slug: "branch-d"
    relevance: not-applicable
    why: "CPF/fusion axis unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Universal Transformers]]"
  - "[[Alex Graves]]"
sources:
  - "[[Universal Transformers]]"
---

# Mostafa Dehghani

## Position
Research scientist at Google Brain / Google DeepMind. Previously PhD at University of Amsterdam (with Maarten de Rijke on weak-supervision information retrieval).

## Core contribution
First author of Universal Transformers (Dehghani, Gouws, Vinyals, Uszkoreit, Kaiser; arXiv:1807.03819, ICLR 2019). The paper introduces depth-recurrent Transformers: a single transformer block is applied T times to each position, with a per-position dynamic halting mechanism inherited from Graves' ACT. Shown to be Turing-complete under certain assumptions, UT outperforms vanilla Transformers on algorithmic tasks and LAMBADA.

## Why relevant to this project

UT is the *first Transformer* with explicit variable-depth latent reasoning. Every modern recurrent-depth latent reasoner ([[Ouro]], [[Hierarchical Reasoning Model]], [[Mixture of Recursions]], [[LoopLM]]) is an architectural descendant of UT, and CODI's M-step hidden-state rollout inherits UT's "apply block T times" idea — with the difference that CODI does it in latent-thought mode, not in place of standard forward passes.

## See also
- [[Universal Transformers]] — canonical source page.
- [[Alex Graves]] — ACT author; UT halting mechanism builds on Graves 2016.
