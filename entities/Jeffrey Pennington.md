---
type: entity
entity_type: person
title: "Jeffrey Pennington"
role: "First author, Dynamical Isometry; research scientist at Google Brain"
first_mentioned: "[[Resurrecting the Sigmoid Dynamical Isometry]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - entity
  - researcher
  - stability-theory
  - affiliation/Google-Brain
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Lead author of the foundational dynamical-isometry / Jacobian-spectrum research line. Key theoretical framing for why spectral control of recurrent-block weights matters for deep / M-step latent stacks."
  - slug: "branch-b"
    relevance: secondary
    why: "Theoretical backing for orthogonal initialization and Jacobian-spectrum control in the recurrent-depth regime. Useful framing for Branch B spectral interventions."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
  - "[[Spectral Regularization]]"
  - "[[Jacobian Constraint]]"
sources:
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
---

# Jeffrey Pennington

## Position
Research scientist at Google Brain / Google Research.

## Core contributions (relevant to us)
- **Dynamical isometry theory** ([[Resurrecting the Sigmoid Dynamical Isometry]], NeurIPS 2017 with Schoenholz and Ganguli) — foundational statement that deep-network trainability requires Jacobian singular-value spectrum concentrated near 1.
- **Mean field theory of CNNs / 10,000-layer training** (Xiao, Bahri, Sohl-Dickstein, Novak, Pennington 2018) — practical initialization schemes that realize dynamical isometry.
- **Free probability for deep networks** — analytic tools for computing Jacobian spectra in deep nets.
- **GloVe word embeddings** — older work, not stability-relevant but canonical.

## Cited in this vault
- [[Resurrecting the Sigmoid Dynamical Isometry]] (first author)

## Why relevant to us
The dynamical-isometry framing is what makes "Jacobian spectrum matters" a first-principle rather than a heuristic. For an M-step latent rollout, compositional products of per-step Jacobians determine whether gradients survive and whether basins are well-conditioned. Pennington's work gives us the analytic tools for predicting what the composite Jacobian will look like without running the experiment.

Especially relevant: ReLU cannot achieve isometry. Qwen3-4B uses SiLU (smoother, but not orthogonal). This predicts inherent spectral pathology in our latent step that any stability-theory intervention must correct.

## See also
- [[Spectral Regularization]] — operational family descended from isometry framework.
- [[Jacobian Constraint]] — operational implementation of isometry-adjacent constraints.
