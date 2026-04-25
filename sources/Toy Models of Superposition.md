---
type: source
source_type: paper
title: "Toy Models of Superposition"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/source
status: triaged
arxiv_id: "2209.10652"
venue: "Transformer Circuits Thread (Anthropic)"
date_published: 2022-09-14
authors:
  - "Nelson Elhage"
  - "Tristan Hume"
  - "Catherine Olsson"
  - "Nicholas Schiefer"
  - "Tom Henighan"
  - "Shauna Kravec"
  - "Zac Hatfield-Dodds"
  - "Robert Lasenby"
  - "Dawn Drain"
  - "Carol Chen"
  - "Roger Grosse"
  - "Sam McCandlish"
  - "Jared Kaplan"
  - "Dario Amodei"
  - "Martin Wattenberg"
  - "Christopher Olah"
url: "https://transformer-circuits.pub/2022/toy_model/index.html"
code_repo: "https://github.com/zroe1/toy-models-of-superposition"
has_weights: false
confidence: high
key_claims:
  - "Neural networks represent more features than they have dimensions by packing features into non-orthogonal directions — superposition."
  - "Superposition arises when features are sparse, of unequal importance, and the network can nonlinearly filter interference."
  - "A sharp phase change separates clean-basis (one feature per direction) and superposition regimes — the transition is abrupt, not gradual."
  - "In superposition, feature vectors organize as uniform polytopes in the activation space (digons, triangles, tetrahedra, pentagons…) minimizing interference."
  - "Polysemanticity in real networks is explained by superposition — many features share one neuron/direction."
  - "Nonlinearity is required to recover superposed features; pure linear networks cannot."
related:
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "[[.raw/external/toy-models-of-superposition-2022]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational framework for interpreting F3 template collapse — 7/8 latent positions sharing one direction is a canonical superposition/polysemanticity artifact."
  - slug: "branch-c"
    relevance: primary
    why: "Probe-typology contest is exactly the problem Toy Models formalizes — linear probes see superposed features incoherently; anti-superposition directions give a principled basis."
  - slug: "branch-d"
    relevance: secondary
    why: "Motivates anti-superposition losses as CPF alternative/supplement; the phase-change finding informs when such a loss would bind."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling context — superposition pressure grows with feature count per dimension."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach/fp32 concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Toy Models of Superposition

Foundational Anthropic/Harvard paper formalizing the superposition hypothesis: neural networks represent more features than they have dimensions by packing features into non-orthogonal directions, producing polysemantic neurons.

## Core mechanism

A network with `m` features and `n < m` hidden dimensions can represent all features simultaneously when:

1. **Sparsity** — at most a few features active per example.
2. **Unequal importance** — loss weighting lets less-important features tolerate interference.
3. **Nonlinearity** — ReLU / similar filtering step removes small cross-feature noise on the way out.

Toy model loss (schematic):
```
L = Σ_i I_i · E[(x_i - x̂_i)²]
x̂ = ReLU(W^T W x + b)
```
with features `x ∈ R^m`, projection `W ∈ R^{n×m}`, importance weights `I_i`, and sparsity controlled by feature activation density `p`.

Interference between features is measured by the inner-product matrix `W^T W` minus the identity; off-diagonal entries quantify "how much feature i leaks into feature j".

## Phase change

As sparsity increases past a threshold, the model abruptly transitions from a clean basis (one feature per direction, zero interference) to a superposition regime (features share directions, interference is tolerated). The boundary is a geometric constraint — how many unit vectors one can pack in `R^n` at bounded inner product.

## Geometry

In the superposition regime, feature vectors form **uniform polytopes**: regular simplices, antipodal pairs, tetrahedra, pentagons, 600-cells. The geometry is exactly the sphere-packing / spherical-code optimum for a given feature count and interference budget.

## Implications for latent reasoning

The F3 finding in the CODI V2 run — 7 of 8 latent positions decode to the same template token string — is structurally consistent with superposition at the position-level:

- Many "features" (one per example-position pair) share a single direction (the template attractor).
- The remaining position (step 3 in F3) carries the per-example content and shows low-template/high-variance decoding.
- This is the geometric collapse predicted by Toy Models when sparsity is high and task-importance is concentrated on one position.

## Anti-superposition interventions discussed in the paper

- **Dimension expansion** — more neurons per feature.
- **Orthogonality penalty** — add `||W^T W − I||²` to the loss.
- **Feature-sparsity penalty** on activations — force each feature to fire rarely (but not to zero).
- **Ablation / targeted knockout** to verify interference structure.

## Cross-references

- [[Towards Monosemanticity]] — the SAE follow-up that extracts the superposed features empirically.
- [[Sparse Autoencoder]] — the tool this paper motivates.
- [[Feature Collapse]] — our project's failure mode; superposition is its representational underpinning.
- [[Routing vs Reasoning]] — F3/F5 battery reads naturally as a superposition artifact at position-granularity.
