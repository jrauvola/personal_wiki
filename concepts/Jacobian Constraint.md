---
type: concept
title: "Jacobian Constraint"
complexity: advanced
domain: stability-theory
aliases:
  - "Jacobian regularization"
  - "Jacobian-norm penalty"
  - "input-output Jacobian constraint"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept
  - domain/theory
  - domain/training
  - stability-theory
  - technique
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The single most portable intervention for enforcing latent-trajectory stability. Adding lambda * ||J||_F^2 to the loss directly addresses F6 narrow basin and F3 template attractor at a shared mechanism level (bounded Lipschitz)."
  - slug: "branch-b"
    relevance: primary
    why: "Drop-in alternative to V2 detach: regularize the Jacobian instead of cutting it. Hutchinson estimator is cheap. Provides formal basin-width guarantee."
  - slug: "branch-d"
    relevance: secondary
    why: "Combines with CPF: CPF for content anchor, Jacobian-reg for geometric stability. Both attack feature collapse at different scales."
related:
  - "[[Spectral Regularization]]"
  - "[[Fixed-Point Iteration]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
  - "[[Lyapunov Stability]]"
last_reviewed: 2026-04-22
reviewed_by: autoreview
sources:
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Robust Learning with Jacobian Regularization]]"
  - "[[Noisy Recurrent Neural Networks]]"
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
---

# Jacobian Constraint

## One-line definition
An auxiliary training loss (or architectural constraint) that penalizes the norm of the **Jacobian** of a neural network map — either the input-output Jacobian or the state-to-state Jacobian in a recurrent setting. Bounds Lipschitz constant → controls margin, basin width, and gradient amplification.

## The three distinct Jacobians we care about

For a recurrent latent rollout $z_{t+1} = f_\theta(z_t, x)$:

1. **State-to-state Jacobian** $J_f^{(t)} = \partial z_{t+1} / \partial z_t$. Controls stability of the iteration. $\rho(J_f) < 1 \Rightarrow$ contraction.
2. **State-to-input Jacobian** $G_f = \partial z_{t+1} / \partial x$. Controls input-dependence of the fixed point. $G_f \neq 0$ required for non-degenerate behavior.
3. **Input-output Jacobian of the full model** $J_{\text{total}} = \partial y / \partial x$. Controls margin and perturbation robustness.

For our project:
- **F3 template attractor** suggests $G_f \approx 0$ (no input dependence of fixed point).
- **F6 narrow basin** suggests $\|J_{\text{total}}\|_2 >> 1$ (large amplification near basin edges).
- **F5 swap-null** is the strongest evidence of $G_f \approx 0$ on the latent-content dimension.

## The core penalty forms

### Frobenius norm penalty (upper bound on spectral)
$$
\mathcal{L}_{\text{jac}} = \lambda \|J\|_F^2 = \lambda \sum_{i,j} J_{ij}^2 = \lambda \cdot \text{tr}(J^\top J)
$$
Hutchinson estimator: $\|J\|_F^2 = \mathbb{E}_v [\|Jv\|_2^2]$ with one random $v$ per gradient step. Cost: one extra JVP.

### Nuclear norm penalty (low-rank structure)
$$
\mathcal{L}_{\text{jac}} = \lambda \|J\|_* = \lambda \sum_i \sigma_i(J)
$$
Encourages *low-rank* Jacobian — the map is effectively low-dim. Intractable for high-d; use denoising-style approximation (Nuclear Norm Regularization for Deep Learning, 2024).

### Spectral norm penalty (direct Lipschitz bound)
$$
\mathcal{L}_{\text{jac}} = \lambda \sigma_1(J)^2
$$
Most direct target but needs SVD or power iteration per step.

### Stable rank
$$
\text{srank}(J) = \|J\|_F^2 / \|J\|_2^2
$$
Ratio of Frobenius to spectral — a soft count of "how many effective dimensions the map uses." Stable-rank regularization encourages the map to use many directions equally → anti-template-attractor. ([[Stable Rank Normalization]], ICLR 2020.)

## Why Jacobian constraint addresses routing-lock

**The template attractor (F3) corresponds to a low-rank Jacobian where one singular direction dominates.** If the latent step function $f$ has $J_f$ with $\sigma_1 >> \sigma_2 \geq ... \geq \sigma_d$, every input gets projected onto the top singular vector → fixed template.

**Stable-rank regularization** directly fights this: pushing $\text{srank}(J_f)$ up forces all singular values to contribute, making the projection "richer" and input-dependent.

**Spectral-norm regularization** (soft $\sigma_1 \leq 1$) caps the top singular value but doesn't force the others to be non-zero. Insufficient for attractor-breaking on its own.

**Parseval retraction** forces *all* $\sigma_i = 1$. Strongest form; most direct attack on template attractors.

## Implementation priority for our project

1. **Phase A (1 day):** Add Hutchinson-Frobenius penalty to V2 rollout, $\lambda = 10^{-3}$. Re-run F3, F5, F6. Expected: basin widening (F6 σ=0.5 tolerable), reduced template dominance (F3 template probability down from 0.95 to ~0.7).

2. **Phase B (2 days):** Add stable-rank regularizer. Expected: template attractor breaks further; F3 entropy rises above 1 bit on most positions.

3. **Phase C (3 days):** Compose with CPF. Expected: full resolution of F3, F5, F6 to baseline levels.

## Limits

- Works at the level of per-step Jacobian; does not control the global phase-space structure.
- Frobenius bound can over-regularize: restrict low-$\sigma_i$ along with high-$\sigma_i$. Stable rank is better at preserving structure.
- Hutchinson variance: one-sample estimator has 2x target variance; can need 2-3 samples per step in practice.
- Attention blocks are not smooth in the standard sense; computing $J_f$ through attention requires either softmax-smoothed variants or effective-Jacobian approximation.

## See also
- [[Spectral Regularization]] — the weight-level implementation family.
- [[Fixed-Point Iteration]] — what the Jacobian constraint governs.
- [[Deep Equilibrium Model (DEQ)]] — the architectural framework where $(I - J_f)^{-1}$ appears in gradients.
- [[Lyapunov Stability]] — stronger global stability criterion.
