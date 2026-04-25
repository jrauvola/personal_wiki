---
type: source
title: "Barlow Twins: Self-Supervised Learning via Redundancy Reduction"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/self-supervised
  - domain/anti-collapse
  - domain/regularization
status: triaged
source_type: paper
arxiv_id: "2103.03230"
venue: "ICML 2021"
date_published: 2021-03-04
authors:
  - "Jure Zbontar"
  - "Li Jing"
  - "Ishan Misra"
  - "Yann LeCun"
  - "Stéphane Deny"
url: "https://arxiv.org/abs/2103.03230"
code_repo: "https://github.com/facebookresearch/barlowtwins"
has_weights: true
confidence: high
key_claims:
  - "Barlow Twins loss L_BT = Σ_i (1−C_ii)² + λ·Σ_{i≠j} C_ij² where C = cross-correlation matrix between batch-normalised embeddings of two augmented views."
  - "λ = 5×10⁻³ optimal; batch-size robust (works at 256); projector 3 layers × 8192 units."
  - "No stop-gradient, no momentum encoder, no predictor needed — avoids collapse by construction via the diagonal-identity objective."
  - "Matches or exceeds SimCLR / BYOL / MoCo on ImageNet linear probe."
related:
  - "[[VICReg]]"
  - "[[SeLaR]]"
  - "[[Feature Collapse]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/2103.03230"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Redundancy-reduction is exactly the F3 anti-template-lock mechanic: force latent dimensions to be decorrelated across the batch and each dim to be useful (C_ii → 1). Direct fix for 'all positions emit the same template'."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational anti-collapse recipe; needs to be cited in the regularization chapter."
  - slug: "branch-b"
    relevance: secondary
    why: "Compatible with detach-style training; loss is per-batch, no end-to-end gradient assumption."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling-neutral method."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not diagnostic."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Barlow Twins: Self-Supervised Learning via Redundancy Reduction

Zbontar, Jing, Misra, LeCun & Deny (ICML 2021). A self-supervised method that prevents collapse by making the **cross-correlation matrix** between two augmented views' embeddings close to the identity — forcing each dimension to be informative (diagonal = 1) and dimensions to be decorrelated (off-diagonals = 0).

Named after Horace Barlow's "redundancy reduction" principle (1961).

## Core equation

$$
\mathcal{L}_\text{BT} = \sum_i (1 - C_{ii})^2 + \lambda \sum_i \sum_{j \neq i} C_{ij}^2
$$

where the **cross-correlation matrix** is:
$$
C_{ij} = \frac{\sum_b z^A_{b,i}\, z^B_{b,j}}{\sqrt{\sum_b (z^A_{b,i})^2}\, \sqrt{\sum_b (z^B_{b,j})^2}}
$$

computed across the batch dimension $b$, between two augmented views $A, B$ of each sample.

## Hyperparameters

| Parameter | Value |
|-----------|-------|
| λ (off-diagonal weight) | 5 × 10⁻³ |
| Batch size | 2048 (robust down to 256) |
| Projector | 3-layer MLP, 8192 units each |
| Optimizer | LARS, lr=0.2, cosine decay |
| Epochs | 1000 (ImageNet) |

## Anti-collapse by construction

Two complementary forces:
- **Invariance (diagonal):** $(1 - C_{ii})^2$ drives $C_{ii} \to 1$ — the two views must give similar values for each dimension.
- **Redundancy reduction (off-diagonal):** $C_{ij}^2$ drives $C_{ij} \to 0$ — different dimensions must carry different information.

Together they make representations **whitening-like** without explicitly whitening, which forbids the trivial constant solution.

## Mapping to CODI F1-F6

Direct route for **F3 template lock** (7/8 positions emit the same template):

**Proposed CODI-Barlow loss on latent KVs:**
$$
\mathcal{L}_\text{KV-BT} = \sum_i (1 - C^{tt}_{ii})^2 + \lambda \sum_{i \neq j} (C^{tt}_{ij})^2
$$

where $C^{tt}$ is the cross-correlation between latent KV at step $t$ from two stochastic forward passes (e.g. with dropout as augmentation). Forces:
- Each KV dimension carries some signal ($C_{ii}=1$)
- Different dimensions are decorrelated ($C_{ij}=0$)

A **cross-position** variant $C^{t,t'}$ with $t \ne t'$ would additionally force the per-position latents to be differentiated — directly attacking the "all positions collapse to the same template" failure.

## Comparison to VICReg

Both are "anti-collapse without tricks" methods. Differences:

| Axis | Barlow Twins | VICReg |
|---|---|---|
| Anti-collapse via | identity cross-correlation | variance hinge + explicit covariance |
| Needs 2 views | Yes | Yes (but v-term alone works standalone) |
| Normalisation | batch-normalised embeddings | unnormalised |
| Separates invariance from decorrelation | No (coupled) | Yes (clean) |
| Preferred in our context | F3 (template lock, cross-position) | F6 (basin width, variance floor) |

## Canonical citation form

Zbontar, J., Jing, L., Misra, I., LeCun, Y., & Deny, S. (2021). Barlow Twins: Self-Supervised Learning via Redundancy Reduction. ICML 2021. arXiv:2103.03230.
