---
type: concept
title: "Deep Equilibrium Model (DEQ)"
complexity: advanced
domain: architecture
aliases:
  - "DEQ"
  - "implicit neural network"
  - "equilibrium network"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept
  - domain/architecture
  - family/equilibrium
  - stability-theory
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "DEQ is the formal framework for any recurrent latent-reasoning model trained via fixed-point iteration. North-star latent-reasoning architectures rolling out shared blocks M times are DEQs whether trained explicitly as such or via BPTT."
  - slug: "branch-b"
    relevance: primary
    why: "Implicit differentiation via DEQ replaces BPTT through M latent steps — directly obsoletes the V2/V3/V4 detach tradeoff. The one-matrix-solve gradient via (I - J_f)^{-1} is the principled version of detach."
  - slug: "branch-d"
    relevance: secondary
    why: "CPF at each step is equivalent to 'recall-mode' DEQ — input re-injection at every step. Gives theoretical cover for why CPF works vs naive M-step rollout."
related:
  - "[[Fixed-Point Iteration]]"
  - "[[Jacobian Constraint]]"
  - "[[Spectral Regularization]]"
last_reviewed: 2026-04-22
reviewed_by: autoreview
sources:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Stability and Generalization in Looped Transformers]]"
---

# Deep Equilibrium Model (DEQ)

## One-line definition
A neural network architecture in which the output is defined as the **fixed point of a single shared layer**: $z^\star = f_\theta(z^\star, x)$. Training uses implicit differentiation through the fixed point rather than BPTT.

## Why DEQ matters for our project

CODI's M-step latent rollout is effectively a *truncated* DEQ: we iterate $z_{t+1} = f(z_t, x, \text{KV})$ for a fixed M steps rather than running to convergence. This has all the drawbacks of DEQ (potential instability, vanishing gradients) without the main benefit (implicit-gradient memory efficiency, fixed-point regularity).

The key question: **what would happen if we ran CODI as a true DEQ?**

1. **Implicit-gradient** replaces the BPTT chain, removing the V2/V3/V4 detach tradeoff entirely.
2. **Convergence-to-fixed-point** is enforced as a training target; the template-attractor collapse (F3) is forbidden *in principle* because the fixed point must depend on $x$.
3. **Stability is first-class:** [[Stabilizing Equilibrium Models by Jacobian Regularization]] gives a recipe for bounding $\rho(J_f)$ directly.

## Core mechanics

**Forward pass.** Given input $x$, solve $z^\star = f_\theta(z^\star, x)$ via a root-finder:
- Broyden's method (quasi-Newton; DEQ's original choice).
- Anderson acceleration (faster in practice).
- Simple Picard iteration $z_{k+1} = f_\theta(z_k, x)$ (slow but always works if $\rho(J_f) < 1$).

**Backward pass.** By the implicit function theorem:
$$
\frac{\partial \ell}{\partial \theta} = -\frac{\partial \ell}{\partial z^\star}\left(I - \frac{\partial f}{\partial z^\star}\right)^{-1}\frac{\partial f}{\partial \theta}
$$
The $(I - J_f)^{-1}$ term is solved via a *second* root-finding procedure (or matrix-vector product iterations), not explicit inversion. Memory is **O(1) in effective depth** — no intermediate activations stored.

## Recall vs no-recall

[[Stability and Generalization in Looped Transformers]] proves a structural result:

- **No-recall DEQ:** $z^\star = f_\theta(z^\star)$, input enters only via initial $z_0$. Has countable fixed points; **cannot express strong input-dependence**.
- **Recall DEQ:** $z^\star = f_\theta(z^\star, x)$, input re-injected at every iterate. Full input-dependence possible.

Huginn's "e-to-be-re-injected" is recall-mode. CODI's base is no-recall (input enters only via KV-cache and decoded by the teacher-forced lens). CPF makes CODI recall-mode by injecting context at each step. The F3 / F5 results predict *exactly* what the no-recall theorem predicts: CODI's latents are nearly input-independent.

## Scaling status

- DEQ for image classification (ResNet-101 parity): mature.
- DEQ for language modeling (WikiText-103 parity): demonstrated [[Deep Equilibrium Models]] but compute overhead is 5x vs Transformer-XL.
- DEQ for LLM scale (>1B): not yet demonstrated cleanly. IIET (Iterative Implicit Euler Transformer, EMNLP 2025) is the closest — competitive at 1-3B with explicit stability objective.
- TorchDEQ (2023) is the most mature library.

## Limits & caveats

- **Expressivity ceiling.** A single fixed-point per input may not capture multi-step reasoning sequences. Mitigation: stack DEQs, or switch to [[Mixture of Recursions]]-style iterated-block architectures.
- **Compute cost.** Each forward solve needs ~10-30 Picard/Broyden iterations — worse than a fixed-depth transformer for comparable compute.
- **Jacobian conditioning.** The $(I - J_f)^{-1}$ term requires $J_f$ to not have eigenvalues near 1 — which coincides with the stability criterion. If training drifts $\rho(J_f) \to 1$, the gradient blows up. Jacobian regularization fixes this.

## For Branch B synthesis

A concrete research branch: **"CODI-as-DEQ."** Re-implement V2 such that the M-step rollout is replaced by a fixed-point solve. Use implicit gradients + Jacobian regularization. Compare F3/F5/F6 signatures to V2 baseline. This is the single cleanest way to test whether stability theory directly addresses our routing-lock problem.
