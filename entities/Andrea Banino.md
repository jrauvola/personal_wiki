---
type: entity
entity_type: person
title: "Andrea Banino"
role: "First author, PonderNet (ICML 2021); probabilistic halting for adaptive compute"
first_mentioned: "[[PonderNet]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/adaptive-compute
  - affiliation/deepmind
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "PonderNet is the cleanest probabilistic reformulation of ACT and a direct ancestor of every halting-head in modern latent reasoning (HRM, AdaPonderLM, Mixture of Recursions halting gates)."
  - slug: "branch-a"
    relevance: reference
    why: "Adaptive compute not primary concern for Qwen3 scaling."
  - slug: "branch-b"
    relevance: reference
    why: "Halting is orthogonal to detach axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
  - slug: "branch-d"
    relevance: not-applicable
    why: "Fusion/anchor axis unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[PonderNet]]"
  - "[[Adaptive Computation Time]]"
  - "[[Alex Graves]]"
sources:
  - "[[PonderNet]]"
---

# Andrea Banino

## Position
Research scientist at DeepMind.

## Core contribution
First author of PonderNet (Banino, Balaguer, Blundell; arXiv:2107.05407, ICML 2021 workshop / NeurIPS 2021). Introduces probabilistic halting: at step n the network emits a Bernoulli halt probability $\lambda_n \in [0, 1]$, and the unconditional halting distribution is $p_n = \lambda_n \prod_{i<n}(1-\lambda_i)$ (geometric in $\lambda$). Training regularizes this distribution via KL divergence to a geometric prior $p^G(\lambda_p)$, giving a principled hyperparameter (expected number of ponder steps) that replaces ACT's brittle "ponder cost."

## Why relevant
PonderNet fixes the two most notorious ACT pathologies: (i) the ponder-cost regularizer's scale-sensitivity, and (ii) its biased gradient estimator. PonderNet is the reference point for every clean halting-head design in modern depth-recurrent latent reasoning — [[Hierarchical Reasoning Model]]'s Q-learning halt gate, [[AdaPonderLM]]'s Gumbel-softmax halt gate, and the halting path in [[Mixture of Recursions]] all cite this lineage.

## See also
- [[PonderNet]] — canonical source page.
- [[Alex Graves]] — ACT is PonderNet's precursor.
