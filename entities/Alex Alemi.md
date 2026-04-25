---
type: entity
title: "Alex Alemi"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/entity
  - type/person
  - domain/information-theory
entity_type: person
role: "Research scientist at Google; lead author on VIB (ICLR 2017) and collaborator on CEB-related work. Primary expositor of information-bottleneck methods in deep learning."
first_mentioned: "[[Deep Variational Information Bottleneck]]"
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Foundational author for our information-theoretic regularization chapter. Not an active collaborator."
  - slug: "branch-d"
    relevance: reference
    why: "VIB is the ancestor of the CPF-as-IB reading in branch-d."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Alex Alemi

Research scientist at Google Research. Lead author on the Deep Variational Information Bottleneck (ICLR 2017) with Ian Fischer, Josh Dillon, and Kevin Murphy — the foundational paper that brought IB into the deep-learning mainstream.

## Contributions referenced in this vault

- **Deep Variational Information Bottleneck** ([[Deep Variational Information Bottleneck]], ICLR 2017): introduces $\beta \cdot \mathrm{KL}(p(z|x) \| r(z))$ as a tractable variational bound on $I(Z;X)$ for supervised deep nets.

## Peripheral but relevant

- Collaborator with Ian Fischer (author of [[Conditional Entropy Bottleneck]]) on information-theoretic generalization work.
- Active in the information-geometry and Bayesian deep-learning communities.

## Why tracked

We cite VIB across multiple branches (branch-d CPF-as-IB framing, branch-b detach-as-compression, spar writeup). Alemi is the primary node to retrieve if additional Google-Research IB work needs to be pulled.
