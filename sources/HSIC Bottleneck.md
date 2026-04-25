---
type: source
title: "The HSIC Bottleneck"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/information-theory
  - domain/regularization
status: triaged
source_type: paper
arxiv_id: "1908.01580"
venue: "AAAI 2020"
date_published: 2019-08-05
authors:
  - "Wan-Duo Kurt Ma"
  - "J.P. Lewis"
  - "W. Bastiaan Kleijn"
url: "https://arxiv.org/abs/1908.01580"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Replace IB mutual-information terms with kernel-based HSIC: Z_i* = argmin nHSIC(Z_i, X) − β·nHSIC(Z_i, Y); per-layer, no backprop needed."
  - "Gaussian kernel k(x,y) ~ exp(−‖x−y‖²/(2σ²·d)) with d = data dimensionality; nHSIC is the normalised Hilbert-Schmidt independence criterion using Gram matrix trace."
  - "β=500 and σ=5 used in CIFAR experiments; per-layer optimization avoids vanishing/exploding gradients and does not require symmetric feedback."
  - "Matches backprop accuracy on MNIST/CIFAR with zero gradient flow between layers; biologically plausible."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/1908.01580"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "HSIC is tractable (no variational bound needed) and gives a *per-layer* anti-collapse signal — natural fit for detach-regime training where the KV has no gradient flow but we still want per-layer diversity constraints."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Non-MI bottleneck alternative worth mentioning in the regularization chapter; useful when the variational-bound machinery (stochastic encoder) is infeasible."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach ablation kills gradient flow through KV; HSIC can provide a local per-layer regularization signal that doesn't need end-to-end gradient."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Not scaling-specific."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a diagnostic."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# The HSIC Bottleneck

Ma, Lewis & Kleijn (AAAI 2020) replace the mutual-information terms of the Information Bottleneck with **Hilbert–Schmidt Independence Criterion (HSIC)** — a tractable kernel-based measure of (in)dependence that doesn't require density estimation or a variational bound.

## Core equations

Per-layer objective:
$$
Z_i^* = \arg\min_{Z_i}\ \mathrm{nHSIC}(Z_i, X) - \beta \cdot \mathrm{nHSIC}(Z_i, Y)
$$

where nHSIC is computed as:
$$
\mathrm{nHSIC}(\mathcal{D}, \mathcal{H}, \mathcal{G}) = \mathrm{tr}(\tilde{K}_X \tilde{K}_Y)
$$

with Gaussian-kernel Gram matrices:
$$
k(\mathbf{x}, \mathbf{y}) \sim \exp\!\left(-\frac{\|\mathbf{x} - \mathbf{y}\|^2}{2\sigma^2 d}\right)
$$

Hyperparameters used in the paper: $\beta = 500$, $\sigma = 5$, $d$ = data dimensionality.

## Why HSIC over MI

1. **Tractable:** closed form over a minibatch; no variational encoder/decoder needed.
2. **No backprop required:** per-layer block coordinate descent works; gives the "deep learning without backprop" claim.
3. **Differentiable:** despite the optimizer flexibility, HSIC is smooth in the layer parameters, so SGD works fine.
4. **Biologically plausible:** ties to three-factor Hebbian learning (see Pogodin & Latham 2020).

## Relevance to CODI branch-d / branch-b

Branch-b's **minimum-sufficient detach** variant kills gradient flow through the KV cache. That means the standard IB/VIB objective, which requires gradients through the encoder `q(z|x)`, cannot be applied end-to-end.

HSIC provides an alternative: a **per-step, local** regularization signal:
$$
\mathcal{L}_\text{HSIC} = \mathrm{nHSIC}(KV_t, X) - \beta \cdot \mathrm{nHSIC}(KV_t, Y)
$$

applied at each latent step $t$ independently. Because HSIC only needs the minibatch Gram matrices, it works even when the KV path has stopped gradients.

**Caveat:** the original paper's β=500 is calibrated for feed-forward nets on CIFAR; for transformers with very high-dim hidden states, both β and σ likely need retuning. Cost: one extra $(B \times B)$ Gram matrix computation per batch per step — trivial vs attention cost.

## Canonical citation form

Ma, W.-D. K., Lewis, J. P., & Kleijn, W. B. (2020). The HSIC Bottleneck: Deep Learning without Back-Propagation. AAAI 2020. arXiv:1908.01580.
