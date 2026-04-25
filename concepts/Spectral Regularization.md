---
type: concept
title: "Spectral Regularization"
complexity: intermediate
domain: training
aliases:
  - "spectral norm regularization"
  - "singular-value constraint"
  - "orthogonality regularization"
  - "Parseval regularization"
  - "dynamical isometry"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept
  - domain/training
  - domain/theory
  - stability-theory
  - technique
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The operational family of interventions (Parseval retraction, spectral-margin parameterization, orthogonal init) that implements the stability-theory criterion rho(J_f) < 1 at the weight level. Directly applicable to M-step latent rollout."
  - slug: "branch-b"
    relevance: primary
    why: "Spectral-constraint interventions are the stability-preserving alternative to V2 detach. Rather than cut the gradient chain, bound its amplification. Parseval retraction is particularly cheap."
  - slug: "branch-d"
    relevance: secondary
    why: "Stabilizing the latent step geometry complements CPF's content-anchor. Both fight feature collapse, from orthogonal directions."
related:
  - "[[Fixed-Point Iteration]]"
  - "[[Jacobian Constraint]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
  - "[[Feature Collapse]]"
last_reviewed: 2026-04-22
reviewed_by: autoreview
sources:
  - "[[Parseval Networks]]"
  - "[[Orthogonal Recurrent Networks]]"
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
---

# Spectral Regularization

## One-line definition
A family of training-time interventions that constrain the **singular-value spectrum** of network weight matrices (or the input-output Jacobian) to prevent exploding/vanishing gradients and control the Lipschitz constant.

## Taxonomy of approaches

| Technique | What's constrained | Hardness | Cost |
|-----------|-------------------|----------|------|
| **Spectral normalization** | Top singular value $\sigma_1 \leq 1$ | Soft via division | 1-2 power iterations per step |
| **Parseval retraction** | All $\sigma_i \approx 1$ | Retraction step after SGD | 1 extra matmul per weight |
| **Hard orthogonality** | Exact $W^\top W = I$ | Stiefel-manifold optimization | Manifold-SGD |
| **Spectral margin** | $\sigma_i \in [1-m, 1+m]$ | SVD parameterization | SVD on each step |
| **Jacobian Frobenius** | $\|J\|_F^2 \leq C$ | Auxiliary loss | Hutchinson JVPs |
| **Orthogonal init** | $\sigma_i = 1$ at init | Initialization only | Zero extra cost |

## The hierarchy of targets

What exactly are we controlling?

1. **Individual weight matrix $W$.** Easy to constrain; cheap. But doesn't directly control the composite Jacobian through transformer blocks.
2. **Layer Jacobian $J_{\text{layer}} = \partial y / \partial x$ for one block.** More faithful to stability theory, but involves attention patterns and nonlinearities.
3. **Full M-step Jacobian $J_{\text{total}} = J_M J_{M-1} \cdots J_1$.** The actually-desired quantity. But direct regularization is expensive.

Practical choice for our M-step rollout: **spectral-margin parameterization on the transformer block weights**, combined with **Hutchinson Jacobian-norm penalty on the effective per-step Jacobian**. Cheap + targets the right quantity.

## The core inequality that drives everything

For latent state perturbation $\delta$ at step 0, after M steps:
$$
\|\delta_M\| \leq \prod_{t=1}^{M} \|J_t\|_2 \cdot \|\delta_0\|
$$
If $\|J_t\|_2 \leq 1 + \epsilon$ per step, total amplification is bounded by $(1+\epsilon)^M$. For $M=8, \epsilon=0.05$: bound is 1.47 — safe. For $\epsilon=0.3$: bound is 8.2 — explains F6.

**Key inequality for narrow-basin widening:**
$$
\text{basin width} \propto \prod_{t=1}^{M} \|J_t\|_2^{-1}
$$
So spectral constraints *directly* widen the basin.

## Which technique for which problem

- **F6 narrow basin** → spectral norm $\leq 1$ per step. Parseval retraction is the cheapest way.
- **F3 template attractor (single-direction)** → Parseval (all singular values = 1), because one dominant direction requires one singular value >> others.
- **Gradient explosion in BPTT** → spectral margin $[1-m, 1+m]$.
- **Gradient vanishing in BPTT** → orthogonal init + spectral margin (don't let any $\sigma_i$ drop to 0).
- **Dynamical isometry for deep stacks** → orthogonal init + avoid ReLU (use GELU/SiLU, SwiGLU).

## Concrete contradictions in the literature

- [[Orthogonal Recurrent Networks]] says hard orthogonality hurts expressivity; soft margin is better.
- [[Parseval Networks]] says soft Parseval retraction gives matched clean accuracy; no tradeoff.
- The discrepancy: Vorontsov used LSTM/RNN settings where hard orthogonality collapses representational capacity; Cisse used CNNs on CIFAR where the information bottleneck is elsewhere. **Implication for us:** try both; we have more data than either.

## Recommended application stack (most to least cheap)

1. **Orthogonal initialization** of recurrent block weights. Zero cost.
2. **Parseval retraction** with $\beta = 10^{-3}$ on recurrent weights. ~1 extra matmul per step.
3. **Noise injection** $\sigma \sim 0.1$ on latent states during training ([[Noisy Recurrent Neural Networks]]). Free, implicit Jacobian penalty.
4. **Hutchinson-estimated Jacobian-Frobenius penalty** ([[Robust Learning with Jacobian Regularization]], [[Stabilizing Equilibrium Models by Jacobian Regularization]]). ~15% compute overhead.
5. **Spectral margin parameterization** ([[Orthogonal Recurrent Networks]]). More expensive but direct.

Start with (1) + (3). These are the fastest to try and could directly address F6 without any architecture changes.

## Limits

- Spectral constraints control linearization, not global dynamics. Pair with Lyapunov-auxiliary for full attractor control.
- They don't address content-ablation failure (F5) — input dependence is a separate property.
- Attention blocks don't decompose into simple weight matrices; need to target the composite block Jacobian.
