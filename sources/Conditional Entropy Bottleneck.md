---
type: source
title: "Conditional Entropy Bottleneck"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/information-theory
  - domain/regularization
  - foundational
status: triaged
source_type: paper
arxiv_id: "2002.05379"
venue: "Entropy (MDPI) / arXiv"
date_published: 2020-02-13
authors:
  - "Ian Fischer"
url: "https://arxiv.org/abs/2002.05379"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "CEB objective is min_Z I(X;Z|Y) − γ·I(Y;Z); variational form VCEB = ⟨log e(z|x)⟩ − ⟨log b(z|y)⟩ − γ·⟨log c(y|z)⟩ with forward encoder e, backward encoder b, classifier c."
  - "CEB is NOT a reparameterisation of VIB: VIB's marginal m(z) is replaced by a Y-conditional backward encoder b(z|y), giving a tighter bound on residual X-information and absolute compression metric I(X;Z|Y) ≥ 0."
  - "The Minimum Necessary Information point is the unique Z satisfying I(X;Y) = I(X;Z) = I(Y;Z); CEB reaches it at γ=1 on deterministic datasets."
  - "On ImageNet and CIFAR, CEB yields higher adversarial robustness and better OOD detection than VIB at matched clean accuracy."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Alex Alemi]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/2002.05379"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CEB's backward encoder b(z|y) = 'what latent best predicts y' is the right formalism for CPF — CPF already uses e_pred built from the predicted next-token distribution, which is a b(z|y_next) estimate. CEB reframes CPF as a principled VCEB objective with a learnable γ instead of a hand-tuned α."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Tighter-bound alternative to VIB, more principled definition of 'what the latent should carry'; writeup axis."
  - slug: "branch-b"
    relevance: secondary
    why: "MNI point gives a principled stopping criterion for detach schedules: stop scaling down gradients when I(Z;Y) ≈ I(X;Y)."
  - slug: "branch-a"
    relevance: reference
    why: "Regularization tool; architecture-agnostic."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Diagnostic probes don't use CEB."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Conditional Entropy Bottleneck

Ian Fischer's 2020 reformulation of the information bottleneck that replaces VIB's unconditional marginal $m(z)$ with a Y-conditional backward encoder $b(z|y)$. Gives a tighter variational bound, an absolute-scale compression metric, and the **Minimum Necessary Information (MNI)** criterion — the unique sufficient-and-compressed representation point.

## Core equations

Primal CEB:
$$
\text{CEB} \equiv \min_Z I(X; Z \mid Y) - \gamma \cdot I(Y; Z)
$$

Expanded form (Eq. 7 in paper):
$$
\min_Z -H(Z \mid X) + H(Z \mid Y) + \gamma \cdot H(Y \mid Z)
$$

Variational upper bound (VCEB) — the trainable objective:
$$
\text{VCEB} \equiv \min_{e, b, c}\ \langle \log e(z \mid x) \rangle - \langle \log b(z \mid y) \rangle - \gamma \cdot \langle \log c(y \mid z) \rangle
$$

where:
- $e(z|x)$ is the forward encoder (as in VIB)
- $b(z|y)$ is the **backward encoder** — maps labels back into latent space
- $c(y|z)$ is the classifier/decoder
- $\gamma > 0$; $\gamma = 1$ attains MNI on deterministic datasets

## Minimum Necessary Information (MNI)

The MNI point is the unique Z satisfying all three conditions:
1. **Informative:** Z has useful entropy
2. **Necessary:** $I(X;Y) \le I(Y;Z)$ (sufficient for Y)
3. **Minimal:** $I(X;Y) \ge I(X;Z)$ (no X-nuisance)

MNI point: $I(X;Y) = I(X;Z) = I(Y;Z)$. This is an *absolute* target, unlike VIB's β-sweep which only gives relative tradeoffs.

## Why CEB > VIB (author's claim)

VIB simultaneously minimizes *and* maximizes mutual information with Z (I(X;Z) down, I(Y;Z) up), which creates an adversarial dynamic. CEB replaces I(X;Z) with the strictly non-negative residual I(X;Z|Y), whose minimization is unambiguous — it measures exactly the X-information that is not explained by Y.

## Relevance to branch-d (CPF)

**Strong structural fit.** CPF's fusion equation is:
$$
e_\text{fusion} = \alpha \cdot h_\text{ctx} + (1-\alpha) \cdot e_\text{pred}
$$

where $e_\text{pred} = \sum_v p(v|\cdot) \cdot W_E[v]$ is a vocab-simplex prediction. This is effectively a *convex combination* of:
- $h_\text{ctx}$: hidden state carrying I(X;Z|Y) (reconstruction info)
- $e_\text{pred}$: vocab-anchor carrying I(Y;Z) (predictive info)

Recasting in CEB terms:
- $e(z|x) \leftrightarrow h_\text{ctx}$ (forward encoder output)
- $b(z|y) \leftrightarrow e_\text{pred}$ (backward encoder, anchored to the predicted token)
- $\alpha \leftrightarrow$ implicit mixing coefficient for the conditional vs predictive terms

**Proposed CODI-CEB loss** (draft):
$$
\mathcal{L}_\text{CODI-CEB} = \mathcal{L}_\text{CE}(y) + \lambda_1 \cdot \|h_\text{ctx} - \mathrm{sg}(e_\text{pred})\|_2^2 + \gamma \cdot \mathrm{KL}[p(z|x) \| \text{sg}(b(z|y))]
$$

where sg = stop-gradient. This replaces CPF's hand-tuned α with a CEB-principled γ schedule.

## Canonical citation form

Fischer, I. (2020). The Conditional Entropy Bottleneck. *Entropy*, 22(9), 999. arXiv:2002.05379.
