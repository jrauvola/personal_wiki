---
type: source
title: "VICReg: Variance-Invariance-Covariance Regularization"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/self-supervised
  - domain/anti-collapse
  - domain/regularization
status: triaged
source_type: paper
arxiv_id: "2105.04906"
venue: "ICLR 2022"
date_published: 2021-05-11
authors:
  - "Adrien Bardes"
  - "Jean Ponce"
  - "Yann LeCun"
url: "https://arxiv.org/abs/2105.04906"
code_repo: "https://github.com/facebookresearch/vicreg"
has_weights: true
confidence: high
key_claims:
  - "VICReg loss L = λ·s(Z,Z′) + μ·[v(Z)+v(Z′)] + ν·[c(Z)+c(Z′)] with invariance s = MSE(Z,Z′), variance v = (1/d)·Σ max(0, γ − √(Var(z^j)+ε)) hinge, covariance c = (1/d)·Σ_{i≠j} C_{ij}²."
  - "Variance hinge with γ=1 prevents dimensional collapse without normalising layers, stop-gradients, or momentum encoders."
  - "Default coefficients λ=25, μ=25, ν=1; embedding dim 8192; batch 2048. Robust to batches as small as 256."
  - "VICReg matches Barlow Twins, SimCLR, BYOL on ImageNet linear-probe while avoiding Barlow Twins' cross-correlation-matrix identity constraint."
related:
  - "[[Barlow Twins]]"
  - "[[SeLaR]]"
  - "[[Feature Collapse]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/2105.04906"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "VICReg's variance-hinge term v(Z) is exactly what F6 (narrow basin) needs: force per-dimension std ≥ γ across the batch, which broadens the latent distribution. Zero assumptions about the prior; plug-in regularizer."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Non-variational anti-collapse mechanism — pure feature-space regularizer. Directly applicable to CODI's KV cache without touching the encoder distribution."
  - slug: "branch-b"
    relevance: secondary
    why: "Works per-batch, per-step, with no gradient flow assumption — compatible with detach regimes."
  - slug: "branch-a"
    relevance: secondary
    why: "Provides a simple diagnostic: per-dimension std of latent KV across batch. If many dims have σ<<γ, collapse is dimensional."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe method."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# VICReg: Variance-Invariance-Covariance Regularization

Bardes, Ponce & LeCun (ICLR 2022). A self-supervised learning method that explicitly regularizes the **variance**, **invariance**, and **covariance** of learned representations. VICReg's contribution is showing that dimensional collapse can be prevented by a simple per-dimension variance hinge, without any of the architectural tricks BYOL/SimSiam need (momentum encoders, stop-gradients).

## Core equations

**Full loss:**
$$
\ell(Z, Z') = \lambda \cdot s(Z, Z') + \mu \cdot [v(Z) + v(Z')] + \nu \cdot [c(Z) + c(Z')]
$$

**Invariance (MSE between two augmented views):**
$$
s(Z, Z') = \frac{1}{n} \sum_i \|z_i - z'_i\|_2^2
$$

**Variance (hinge function on per-dimension std):**
$$
v(Z) = \frac{1}{d} \sum_{j=1}^d \max\!\left(0,\ \gamma - \sqrt{\mathrm{Var}(z^j) + \epsilon}\right)
$$

where $z^j$ is the $j$-th coordinate across the batch. Pushes every dimension to have std at least $\gamma$ (set to 1 in the paper).

**Covariance (off-diagonal Gram-matrix squared):**
$$
c(Z) = \frac{1}{d} \sum_{i \neq j} [C(Z)]_{i,j}^2
$$

where $C(Z) = \frac{1}{n-1} \sum_i (z_i - \bar{z})(z_i - \bar{z})^T$ is the empirical covariance matrix.

**Default hyperparameters:** $\lambda = 25$, $\mu = 25$, $\nu = 1$. The condition $\lambda = \mu > 1$ and $\nu$ small is required for stability. Batch size 2048, embedding dim 8192.

## Why the variance term prevents collapse

The hinge $\max(0, \gamma - \sigma_j)$ is zero when std ≥ γ and linear below. It provides a **lower bound on entropy per dimension** without a prior. The paper contrasts this with Barlow Twins' cross-correlation identity constraint, which conflates invariance and decorrelation; VICReg separates them cleanly.

## VICReg as a drop-in for CODI

**Proposed loss add-on:**
$$
\mathcal{L}_\text{CODI-VIC} = \mathcal{L}_\text{CODI-CE} + \mu \cdot v(KV_t) + \nu \cdot c(KV_t)
$$

computed per latent step $t$, pooling across the batch dim. Note: no invariance term — we don't have two views. (Alternatively: use dropout-pairs as the two views, re-introducing `s`.)

Critically, the variance term $v(KV_t)$ requires no two-view augmentation and can be added stand-alone as a **F6-basin-widening regularizer**.

**Expected effect:**
- **F3 template lock** (7/8 positions <0.4 bits): covariance term $c(KV_t)$ forces decorrelation across latent dimensions within a step; variance term forces per-dimension activity.
- **F6 narrow basin** (σ=0.5 → <3%): variance term directly widens per-dimension spread, by construction.
- **F5 swap-null** (0% change): only indirectly; covariance increases *between-example* differentiability, which helps F5 if the per-example signal exists but is being funnelled into a low-rank subspace.

## Canonical citation form

Bardes, A., Ponce, J., & LeCun, Y. (2022). VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning. ICLR 2022. arXiv:2105.04906.
