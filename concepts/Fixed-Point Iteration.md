---
type: concept
title: "Fixed-Point Iteration"
complexity: intermediate
domain: stability-theory
aliases:
  - "Picard iteration"
  - "Banach fixed point"
  - "contraction mapping"
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
    why: "Foundational framing for all recurrent latent-reasoning models: each latent step is one Picard iterate. Banach contraction criterion rho(J) < 1 is the single condition that keeps the iteration stable."
  - slug: "branch-b"
    relevance: primary
    why: "V2/V3/V4 detach ablations are the crude implementation of implicit-function-theorem gradient. Fixed-point framing is what lets us reinterpret them cleanly."
  - slug: "branch-d"
    relevance: secondary
    why: "CPF anchors each iterate to the vocab manifold — this is 'recall-mode' fixed-point iteration in Labovich's terminology. Gives a theoretical handle on why CPF breaks template attractors."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling recurrent depth at 9B is a fixed-point problem by design."
related:
  - "[[Deep Equilibrium Model (DEQ)]]"
  - "[[Spectral Regularization]]"
  - "[[Jacobian Constraint]]"
  - "[[Lyapunov Stability]]"
last_reviewed: 2026-04-22
reviewed_by: autoreview
sources:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Stability and Generalization in Looped Transformers]]"
  - "[[Orthogonal Recurrent Networks]]"
---

# Fixed-Point Iteration

## One-line definition
The iterative process $z_{k+1} = f(z_k)$ starting from $z_0$, seeking a point $z^\star$ such that $f(z^\star) = z^\star$. Stability of the process is governed by the **spectral radius** of the Jacobian $J_f$ at $z^\star$.

## The Banach contraction-mapping theorem

**Statement.** Let $(X, d)$ be a complete metric space and $f: X \to X$ be a **contraction**, meaning there exists $L < 1$ such that $d(f(x), f(y)) \leq L \cdot d(x, y)$ for all $x, y$. Then:

1. $f$ has a **unique** fixed point $z^\star$.
2. For any $z_0$, the sequence $z_{k+1} = f(z_k)$ converges to $z^\star$.
3. Convergence rate is **geometric**: $d(z_k, z^\star) \leq L^k \cdot d(z_0, z^\star)$.

For a differentiable $f: \mathbb{R}^d \to \mathbb{R}^d$, Taylor expansion at the fixed point gives $L \approx \rho(J_f(z^\star))$, the spectral radius. So: **$\rho(J_f) < 1$ $\iff$ $f$ is a contraction near $z^\star$ $\iff$ Picard iteration converges.**

## Why it matters for latent reasoning

CODI's latent rollout $z_{t+1} = \text{TransformerBlock}(z_t, x, \text{KV})$ is a Picard iteration. Three regimes:

| Regime | $\rho(J_f)$ | Consequence |
|--------|-------------|-------------|
| Contractive | $< 1$ | Iterates converge; *all* inputs → fixed point. Can collapse to template attractor if the basin is one. |
| Marginally stable | $= 1$ | Iterates preserve norm. Dynamical isometry regime ([[Resurrecting the Sigmoid Dynamical Isometry]]). |
| Expansive | $> 1$ | Iterates diverge or chaos. Gradients explode through BPTT. |

The **F3 template attractor** in our project is the pathological case of regime 1: the iteration has one *strong* attractor (the template) that swallows most inputs. The F6 narrow basin is tied to regime 3 along non-template directions: a contractive direction near the fixed point but expansive on perturbations off the basin (sharp basin walls).

**The stability-theory remedy:** force $\rho(J_f) < 1$ *uniformly* — every direction contractive — so no single template direction dominates. This is what [[Spectral Regularization]] and [[Jacobian Constraint]] operationalize.

## Implicit-function theorem for gradients

If $z^\star$ solves $z^\star = f_\theta(z^\star, x)$, then differentiating both sides:
$$
\frac{\partial z^\star}{\partial \theta} = (I - J_f)^{-1} \frac{\partial f}{\partial \theta}
$$
This gives a **one-step gradient** w.r.t. $\theta$ without backpropagating through the entire iteration. This is the foundation of [[Deep Equilibrium Model (DEQ)]] training.

For our project: V2's detach is a crude approximation of this. Instead of $(I - J_f)^{-1}$, V2 just uses $I$ at the detach point — correct only when $J_f \approx 0$, which is the "content-inert" regime F5 documents. The IFT formula is what we'd use to properly differentiate through a latent fixed point.

## Reachability, input-dependence, geometry

[[Stability and Generalization in Looped Transformers]] decomposes fixed-point stability into three axes:

- **Reachability.** Does the iteration actually converge from typical inputs, or does it diverge / oscillate?
- **Input-dependence.** Does $z^\star$ depend on $x$, or is it a constant regardless of input? *This is F5's diagnostic.*
- **Geometry.** What is the basin shape around $z^\star$? Narrow basins → fragile; wide basins → robust. *This is F6's diagnostic.*

**F3 (template attractor)** is an input-dependence failure: the fixed point is nearly constant across inputs. **F6 (narrow basin)** is a geometry failure. **F5 (swap-null)** is an input-dependence failure probed via a different route.

## See also
- [[Deep Equilibrium Model (DEQ)]] — trained fixed-point iteration.
- [[Spectral Regularization]] — enforcing $\rho(J_f) < 1$ during training.
- [[Jacobian Constraint]] — the operational form of the spectral criterion.
- [[Lyapunov Stability]] — the smooth / continuous-time version of fixed-point stability.
