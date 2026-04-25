---
type: concept
title: "Lyapunov Stability"
complexity: advanced
domain: stability-theory
aliases:
  - "Lyapunov function"
  - "Lyapunov criterion"
  - "V-function"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept
  - domain/theory
  - stability-theory
  - foundational
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Lyapunov criterion is the continuous-time / auxiliary-loss analog of the Banach fixed-point criterion. A Lyapunov-function auxiliary loss forces the latent dynamics toward a well-defined attractor during training, potentially curing the narrow-basin pathology."
  - slug: "branch-b"
    relevance: secondary
    why: "For V2 treated as a discrete-time dynamical system, Lyapunov discrete-decrease condition V(z_{t+1}) < V(z_t) would provide a stronger convergence guarantee than Jacobian-norm bounds. Could be an auxiliary loss."
  - slug: "branch-d"
    relevance: secondary
    why: "If CPF is viewed as steering latents toward a 'target manifold' (the vocab submanifold), a Lyapunov function on distance-to-manifold is a natural auxiliary loss to complement the cross-entropy teacher forcing."
related:
  - "[[Fixed-Point Iteration]]"
  - "[[Jacobian Constraint]]"
  - "[[Spectral Regularization]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
last_reviewed: 2026-04-22
reviewed_by: autoreview
sources:
  - "[[Lyapunov-stable Neural-Network Control]]"
  - "[[Noisy Recurrent Neural Networks]]"
---

# Lyapunov Stability

## One-line definition
A dynamical system $\dot{z} = f(z)$ is **Lyapunov-stable** at $z^\star$ if there exists a scalar function $V: X \to \mathbb{R}_{\geq 0}$ (the Lyapunov function) such that $V(z^\star) = 0$, $V(z) > 0$ for $z \neq z^\star$, and $\dot{V}(z) = \nabla V(z)^\top f(z) \leq 0$ along trajectories.

## Why it matters for latent reasoning

The Lyapunov criterion is the **continuous-time analog** of the Banach fixed-point contraction criterion. Where Banach gives "iterate $\to z^\star$ if $\rho(J_f) < 1$," Lyapunov gives "trajectory $\to z^\star$ if there exists a decreasing function along flow." Advantage: doesn't require differentiability, gives you a **certificate function** as bonus.

For latent-reasoning nets, the value: **you can train a Lyapunov function as an auxiliary network**, using the decrease condition as a loss. This gives you:

1. **Provable convergence to a well-defined attractor**, not just "hopefully stable."
2. **Basin of attraction estimate**: the sublevel set $\{z : V(z) \leq c\}$ where the decrease condition holds is a certified basin.
3. **Diagnostic**: $V$ is an *interpretable* scalar measuring how far we are from the attractor.

## Discrete-time Lyapunov (most relevant for us)

For a discrete iteration $z_{t+1} = f(z_t)$, the Lyapunov criterion becomes
$$
V(f(z)) - V(z) \leq -\alpha(\|z - z^\star\|)
$$
for some class-$\mathcal{K}$ function $\alpha$. This is *strictly stronger* than the spectral-radius criterion — it tracks the full dynamic, not just the linearization.

## Lyapunov function as auxiliary loss

Concrete recipe (from [[Lyapunov-stable Neural-Network Control]] and its followups):

1. Parameterize $V: \mathbb{R}^d \to \mathbb{R}_{\geq 0}$ as a small ReLU network — say 2 hidden layers.
2. Add to training loss the **Lyapunov decrease violation**:
$$
\mathcal{L}_{\text{lyap}} = \sum_{t=1}^{M} \max(0, V(z_{t+1}) - V(z_t) + \alpha \|z_t - z^\star\|^2)
$$
where $z^\star$ is a moving target (e.g. the M-th latent state, or a learned "attractor embedding").
3. Train jointly: $\mathcal{L} = \mathcal{L}_{\text{task}} + \lambda_V \mathcal{L}_{\text{lyap}}$.
4. Outcome: latent trajectories are forced to have a decreasing scalar — so they converge to *something*, with the something being learned jointly.

## For the routing-lock / template-attractor problem

This is the most interesting untried angle. CODI's template attractor is a poor fixed point — it's a **global attractor for all inputs** (F3). A Lyapunov function that is **input-conditional** — $V(z; x)$ — would explicitly require trajectories to converge to an input-dependent target, breaking the one-template-fits-all pathology.

Concretely:
$$
V(z; x) = \|z - g_\phi(x)\|_2^2
$$
where $g_\phi$ is a learned per-input attractor. The training signal says "converge to the right attractor for *this* $x$." This is conceptually close to [[Context-Prediction-Fusion]] but with an explicit convergence certificate.

## Limits & caveats

- **Lyapunov function is hard to parameterize.** Must be positive-definite; easy choice (quadratic) limits expressivity; ReLU-net versions need verification ([[Lyapunov-stable Neural-Network Control]] uses MIP to verify decrease condition).
- **No free lunch.** The Lyapunov loss is an *auxiliary signal*, not a replacement for spectral/Jacobian constraints. Usually combined.
- **Continuous-time theory is cleaner than discrete-time.** For us (discrete M-step rollout) the decrease condition is the right form but less explored in ML.

## See also
- [[Fixed-Point Iteration]] — related but weaker criterion (linearization-based).
- [[Jacobian Constraint]] — implies Lyapunov stability under a quadratic $V(z) = \|z - z^\star\|^2$.
- [[Spectral Regularization]] — operational way to meet Lyapunov criterion via $\rho(J_f) < 1$.
