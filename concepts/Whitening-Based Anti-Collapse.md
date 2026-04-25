---
type: concept
title: "Whitening-Based Anti-Collapse"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/self-supervised
  - domain/regularization
  - domain/anti-collapse
  - type/concept
status: developing
complexity: intermediate
domain: representation-learning
aliases:
  - "Decorrelation Regularization"
  - "Variance-Covariance Regularization"
  - "Redundancy Reduction"
related:
  - "[[Barlow Twins]]"
  - "[[VICReg]]"
  - "[[Contrastive Predictive Coding]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "[[Barlow Twins]]"
  - "[[VICReg]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Direct tool for F3 (force per-position, per-dimension KV diversity) and F6 (variance-hinge floors per-dim std). Plug-in add-on to CODI — no architecture change."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Non-variational, non-contrastive anti-collapse family — foundational alternative to VIB/IB for the writeup."
  - slug: "branch-b"
    relevance: secondary
    why: "Works per-batch, compatible with detach (no gradient flow assumption through the KV sequence needed)."
  - slug: "branch-a"
    relevance: secondary
    why: "Per-dim std and cross-position decorrelation are simple scaling-neutral diagnostics."
  - slug: "branch-c"
    relevance: secondary
    why: "The diagnostic form (per-dim std + off-diagonal correlation) is exactly the F-battery probe that extends F3."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Whitening-Based Anti-Collapse

A family of self-supervised regularizers that prevent representation collapse by **directly constraining the statistics of the embedding distribution** — specifically, forcing per-dimension variance to be non-zero and cross-dimension covariance to be small.

Distinct from VIB (which uses a generative prior) and from InfoNCE (which uses explicit negatives). Whitening methods are pure post-hoc statistical regularizers.

## Core mechanism: force $\mathrm{Cov}(z) \approx I$

The name comes from "whitening" a random variable — making its covariance matrix the identity. In practice, we use two soft proxies:

**Variance:** force $\mathrm{Var}(z_j) \geq \gamma^2$ for each dimension $j$.
**Decorrelation:** force $\mathrm{Cov}(z_i, z_j) \approx 0$ for $i \neq j$.

These together mean every dimension is active and carries independent information — the geometric opposite of collapse.

## Two canonical implementations

### Barlow Twins ([[Barlow Twins]])

Cross-correlation matrix between two views:
$$
\mathcal{L}_\text{BT} = \sum_i (1 - C_{ii})^2 + \lambda \sum_{i \neq j} C_{ij}^2
$$

$C_{ii}=1$ forces invariance across views + per-dim activity; $C_{ij}=0$ forces decorrelation. Both conditions together = identity cross-correlation matrix.

### VICReg ([[VICReg]])

Three separable terms:
$$
\ell = \lambda\, s(Z,Z') + \mu[v(Z) + v(Z')] + \nu[c(Z) + c(Z')]
$$

- $s$: invariance (MSE between views)
- $v$: variance hinge $\max(0, \gamma - \mathrm{std}(z_j))$
- $c$: off-diagonal covariance $\sum_{i \neq j} C_{ij}^2$

**Key difference from Barlow Twins:** VICReg decouples the three terms — can apply the variance or covariance term *standalone* without needing two views.

## Why this family matters for our setting

1. **No prior assumption.** VIB needs a well-chosen r(z); whitening only constrains moments.
2. **Detach-compatible.** Loss is batch-local; no gradient-through-encoder assumption.
3. **Cheap.** Per-batch Gram matrix computation: $O(B \cdot d^2)$ — trivial vs attention.
4. **Drop-in.** Add as auxiliary loss with a small weight; no architecture change.

## Direct mapping to F1-F6

| Failure | Whitening prescription |
|---|---|
| **F3 template lock** (7/8 pos <0.4 bits) | Cross-position Barlow: $\mathcal{L}_\text{pos-BT} = \sum_i (1 - C^{tt}_{ii})^2 + \lambda \sum_{i \neq j} (C^{t,t'}_{ij})^2$ where $C^{t,t'}$ is batch-cross-correlation of KV at positions $t, t'$. Forces positions to carry decorrelated information. |
| **F6 narrow basin** (σ=0.5 → <3%) | VICReg variance hinge $v(KV) = (1/d)\sum_j \max(0, \gamma - \mathrm{std}(KV_{\cdot,j}))$. Directly widens the per-dim spread. |
| **F5 swap-null** (0% Δ under swap) | Indirect: forcing decorrelation across examples increases the functional range of the latent, which *enables* per-example differentiation but doesn't *force* it. Pair with InfoNCE. |

## Typical hyperparameters (literature)

| Paper | λ | μ | ν | γ | Batch | Dim |
|---|---|---|---|---|---|---|
| Barlow Twins | 5e-3 | - | - | - | 2048 | 8192 |
| VICReg | 25 | 25 | 1 | 1 | 2048 | 8192 |

Note: these are calibrated for 2048-dim image embeddings. Our CODI KV dim is 3584 (Qwen3-4B). Scaling γ and μ to match signal strength of next-token CE loss is an open calibration question.

## Caveats

- **Batch-size sensitive.** Covariance estimate has variance $\propto 1/B$. With B<256 the covariance term can be noisy.
- **Does not prevent *functional* collapse.** Latents can be statistically diverse (pass whitening) while being functionally ignored (F5 null). Need to pair with InfoNCE-style contrastive or VIB-style predictive signal.
- **Requires care with normalised embeddings.** If LayerNorm comes after the whitening regularizer, its effect is mostly removed.
