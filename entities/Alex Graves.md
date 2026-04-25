---
type: entity
entity_type: person
title: "Alex Graves"
role: "Inventor of Adaptive Computation Time (ACT, 2016) and Neural Turing Machines (2014); key architect of differentiable memory-augmented networks"
first_mentioned: "[[Adaptive Computation Time]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/recurrent
  - affiliation/deepmind
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Historical root of adaptive-depth / variable-compute neural networks. ACT (2016) is the direct ancestor of PonderNet, Universal Transformers, HRM's halting head, and modern looped-depth transformers. Taxonomically essential for the field-trajectory framing."
  - slug: "branch-a"
    relevance: reference
    why: "Depth-adaptive computation is orthogonal to Qwen3 scaling but is the ancestor of HRM / Ouro / Mixture of Recursions that sit adjacent to the scaling question."
  - slug: "branch-b"
    relevance: reference
    why: "ACT's 'ponder cost' regularizer foreshadows BPTT-through-variable-depth trade-offs but not directly applicable to CODI's fixed-M rollout."
  - slug: "branch-d"
    relevance: reference
    why: "Orthogonal axis (halting) to CPF's fusion axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Adaptive Computation Time]]"
  - "[[Neural Turing Machines]]"
  - "[[Universal Transformers]]"
  - "[[PonderNet]]"
sources:
  - "[[Adaptive Computation Time]]"
  - "[[Neural Turing Machines]]"
---

# Alex Graves

## Position
Research scientist; long tenure at DeepMind (since 2012), prior PhD with Juergen Schmidhuber at IDSIA. Core contributor to the pre-Transformer recurrent-network research program that established the conceptual vocabulary of modern latent reasoning.

## Core contributions

- **Adaptive Computation Time (ACT), 2016** ([[Adaptive Computation Time]], arXiv:1603.08983). First fully differentiable mechanism for variable-depth computation in RNNs — the network learns a halting probability per step, regularized by a "ponder cost." This is the *origin* of the halting-head lineage running through [[PonderNet]] → [[Universal Transformers]] → [[Hierarchical Reasoning Model]] → [[Ouro]] / [[Mixture of Recursions]].

- **Neural Turing Machine (NTM), 2014** ([[Neural Turing Machines]], arXiv:1410.5401, with Greg Wayne & Ivo Danihelka). First neural architecture with differentiable external memory and content/location-based addressing. Precursor to all attention-over-memory systems; historically adjacent to latent reasoning because the controller's iterations over memory constitute non-linguistic, step-wise reasoning.

- **Differentiable Neural Computer (DNC), 2016** (*Nature* 538, 471–476, with Wayne et al.). Evolution of NTM with dynamic memory allocation and temporal attention; demonstrated graph reasoning and shortest-path inference.

- **Connectionist Temporal Classification (CTC), 2006** and deep bidirectional LSTM for speech recognition. Historically load-bearing but orthogonal to latent reasoning.

## Why relevant to this project

Graves introduced the core axioms that later latent-reasoning work operationalizes:

1. **Depth is learnable.** ACT dissolves the "fixed number of layers" assumption.
2. **Reasoning can happen in iterations of a shared block.** NTM's controller + memory is a loop, not a feed-forward stack — this is the pattern reused in every modern recurrent-depth latent reasoner.
3. **Differentiability end-to-end is sufficient.** No explicit programs; gradient-descent-learnable halting.

Every "fundamentally different training block" in modern latent reasoning inherits from one of these three ideas.

## See also

- [[Adaptive Computation Time]] — the canonical ACT paper.
- [[Neural Turing Machines]] — memory-augmented reasoning precursor.
- [[Mostafa Dehghani]] — Universal Transformers author who brought ACT into the Transformer era.
- [[Andrea Banino]] — PonderNet author; rigorous probabilistic reformulation of ACT.
