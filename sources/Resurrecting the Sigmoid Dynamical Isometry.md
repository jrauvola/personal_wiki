---
type: source
title: "Resurrecting the Sigmoid in Deep Learning Through Dynamical Isometry"
source_type: paper
arxiv_id: "1711.04735"
venue: "NeurIPS 2017"
date_published: 2017-11-13
authors:
  - "Jeffrey Pennington"
  - "Samuel S. Schoenholz"
  - "Surya Ganguli"
url: "https://arxiv.org/abs/1711.04735"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Dynamical isometry — all singular values of the end-to-end Jacobian concentrated near 1 — is both sufficient and necessary for stable deep-network training without vanishing/exploding gradients."
  - "ReLU networks CANNOT achieve dynamical isometry regardless of initialization: ReLU gates kill half the singular-value mass at every layer."
  - "Sigmoidal (and tanh) networks CAN achieve dynamical isometry, but only under orthogonal weight initialization — Gaussian init does not suffice."
  - "Free probability theory gives analytic predictions for the full Jacobian singular-value spectrum as a function of depth and nonlinearity."
  - "Networks at dynamical isometry learn orders of magnitude faster than networks whose Jacobian spectrum is pathological."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The most foundational statement of the Jacobian-spectrum-controls-training principle. Directly motivates the Jacobian-regularization / spectral-constraint interventions our F6 basin-collapse problem demands."
  - slug: "branch-b"
    relevance: secondary
    why: "Foundational theory backing spectral-regularization interventions for M-step latent rollout. SIlU/GELU activations in Qwen3 are ReLU-like — this is the paper that says we won't get isometry from standard init alone."
  - slug: "branch-d"
    relevance: reference
    why: "Frames why CPF's anchor-to-vocab-manifold step could be reinterpreted as a dynamical-isometry-preserving map."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/theory
  - foundational
  - stability-theory
  - technique/spectral-initialization
related:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Parseval Networks]]"
  - "[[Orthogonal Recurrent Networks]]"
  - "[[Jacobian Constraint]]"
  - "[[Spectral Regularization]]"
sources: []
---

# Dynamical Isometry (Pennington, Schoenholz, Ganguli 2017)

## TL;DR
Deep networks train fast if and only if all singular values of the end-to-end input-output Jacobian cluster around 1 — **dynamical isometry**. The authors derive this analytically using free probability theory and show: (1) ReLU nets cannot reach isometry; (2) sigmoid nets reach it under orthogonal init; (3) isometric nets train orders of magnitude faster.

## Why this matters to our project

This paper is the theoretical root for all downstream spectral-regularization work on recurrent nets. Its central lesson: **"mean squared singular value of J = O(1)" is not enough — the full spectrum must be isometric**. Subpopulations of near-zero or near-infinity singular values kill gradients and create narrow basins — which is exactly what F6 reports (σ=0.5 collapses).

For our M-step latent rollout, the composition Jacobian is
$$
J_{\text{total}} = J_f^{(M)} J_f^{(M-1)} \cdots J_f^{(1)}
$$
If each step's Jacobian has singular values sharply concentrated near 1 (isometry), the product stays well-conditioned after M=8 steps. If any singular value is >1 or <1, the product is exponentially ill-conditioned.

**Prediction:** measuring the singular value spectrum of $J_f$ at CODI's 4B latent step would reveal a long tail of near-zero values (ReLU/SiLU gates collapsing dimensions) and a small number of large singular values (the template-routing direction). Fixing this — e.g. Parseval-retraction or orthogonal re-init — might mechanically eliminate the template-routing eigendirection.

## Spectral criterion for Branch B / D

Instead of penalizing only Frobenius norm (upper bound on $\|J\|_2^2$, the top singular value), one can regularize the *entire* spectrum toward 1 using either:

- **Spectral normalization:** $W \leftarrow W / \sigma_1(W)$ each step (bounds top singular value).
- **Parseval retraction:** $W \leftarrow W - \alpha(WW^\top - I)W$ (pushes full spectrum toward 1).
- **Orthogonal parameterization:** $W = \exp(A - A^\top)$ (exact orthogonality).

Soft Parseval is usually the practical sweet spot: it preserves isometry without hurting expressivity like hard orthogonality does ([[Orthogonal Recurrent Networks]]).

## Limits
- Isometry is an *initialization* claim in this paper — maintaining isometry through training is the hard part that later work ([[Parseval Networks]], [[Orthogonal Recurrent Networks]]) addresses.
- ReLU-impossibility result is somewhat architecture-specific — GELU/SiLU used in Qwen3 are smoother and may partially recover isometry, but no guarantee.
- Depth >> width regime; for transformer width at our scale ($d_{model}=2560$ @ 4B), finite-width corrections matter.
