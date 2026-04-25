---
type: concept
title: "Superposition"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/concept
status: developing
complexity: advanced
domain: interpretability
aliases:
  - "Polysemanticity"
  - "Feature Superposition"
related:
  - "[[Toy Models of Superposition]]"
  - "[[Sparse Autoencoder]]"
  - "[[Towards Monosemanticity]]"
  - "[[Feature Absorption and Splitting]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "[[Toy Models of Superposition]]"
  - "[[Towards Monosemanticity]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Superposition is the representational mechanism underlying F3 template-lock — many features share one direction in CODI's latent positions."
  - slug: "branch-c"
    relevance: primary
    why: "Explains why different linear probes see different things — a superposed basis has many equivalent readouts depending on which direction the probe lands on."
  - slug: "branch-d"
    relevance: secondary
    why: "Motivates explicit anti-superposition losses (orthogonality, feature diversity) as CPF complement."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling context — superposition pressure grows with feature count per dimension."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Superposition

Representational mechanism by which neural networks encode more features than they have dimensions, at the cost of polysemantic neurons (one neuron participates in many unrelated features) and requiring nonlinear activation to recover the separated features.

Introduced formally in [[Toy Models of Superposition]] (Elhage et al. 2022).

## Conditions

Superposition arises when:
1. **Features are sparse** — only a few active per example.
2. **Features have unequal importance** — loss weighting lets less-important features tolerate interference.
3. **Network is nonlinear** — ReLU / equivalent gates cross-feature noise.
4. **Capacity is constrained** — `#features > #dimensions`.

## Geometry

Feature directions form **uniform polytopes** in `R^n`: regular simplices, antipodal pairs, tetrahedra, pentagons, 600-cells. Each corresponds to a solution of the sphere-packing problem for the relevant feature-count / interference-budget combination.

## Phase change

Transition from clean-basis (one feature per direction) to superposition is **abrupt**: a small increase in feature count or sparsity triggers a sudden reorganization, not a gradual degradation. This matches the empirical observation that feature collapse in latent-reasoning models can appear late in training as a sudden change.

## Connection to F3 failure

F3 finding: 7 of 8 CODI latent positions decode to the same template token sequence, with only position 3 showing per-example content.

Superposition reading: the "feature" here is "position holds per-example content for problem X". Many such features (one per example-position pair) are packed into one direction (the template attractor). Decoding via logit-lens only reads out the shared direction; the per-example direction is orthogonal and invisible to logit-lens.

This generates a testable prediction: an SAE trained on CODI latent positions should recover two kinds of features —
- A "template feature" that fires at all 7 collapsed positions.
- Per-example features that fire at position 3 and are absent or near-zero at other positions.

## Diagnosing superposition

- **Non-orthogonal feature directions.** `W^T W − I` has large off-diagonal entries.
- **Polysemantic activation patterns.** A neuron fires for ostensibly unrelated concepts.
- **Interference under ablation.** Knocking out one feature changes unrelated features' readouts.

## Breaking superposition

- **Sparse autoencoders** — overcomplete `k ≫ d` dictionary, L1 sparsity penalty. Learns one direction per feature. See [[Sparse Autoencoder]].
- **Dimension expansion** — widen the underlying model.
- **Orthogonality penalty** — `||W^T W − I||²` directly.
- **Feature-activation sparsity** — penalize co-activation so each feature fires alone.
- **Causal invariance** — require representations to preserve ground-truth factors under intervention. See [[Causal Disentanglement]].

## Cross-references

- [[Feature Collapse]] — our project's failure-mode framing.
- [[Routing vs Reasoning]] — per-position functional-role framing.
- [[Sparse Autoencoder]] — the canonical anti-superposition tool.
