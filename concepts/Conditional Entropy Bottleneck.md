---
type: concept
title: "Conditional Entropy Bottleneck (concept)"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/information-theory
  - domain/regularization
  - type/concept
status: developing
complexity: advanced
domain: information-theory
aliases:
  - "CEB"
  - "Fischer Bottleneck"
  - "Minimum Necessary Information"
related:
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Context-Prediction-Fusion]]"
sources:
  - "[[Conditional Entropy Bottleneck]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CEB's backward encoder b(z|y) is structurally analogous to CPF's e_pred (both are 'latent reconstructed from predicted target'). CEB gives the learnable γ replacement for CPF's hand-tuned α mixing coefficient."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Tighter-bound IB variant; principled MNI target; writeup needs this framing."
  - slug: "branch-b"
    relevance: secondary
    why: "MNI point provides a principled stopping criterion: stop scaling up compression when I(Z;Y) ≈ I(X;Y)."
  - slug: "branch-a"
    relevance: reference
    why: "Not scaling-specific."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a diagnostic tool."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Conditional Entropy Bottleneck (concept)

A reformulation of the Information Bottleneck that uses the **conditional** mutual information $I(X;Z|Y)$ — which is always $\geq 0$ — instead of VIB's unconditional $I(X;Z)$. Invented by Ian Fischer (2020, see [[Conditional Entropy Bottleneck]]).

## Why conditional MI matters

VIB's $I(X;Z)$ term is "all X information in Z, including the part that is Y" — which means VIB is simultaneously pushing I(X;Z) down and I(Y;Z) up, and those two terms share content. This creates an adversarial dynamic that makes β hard to schedule.

CEB's $I(X;Z|Y)$ is the residual X information that Y does not explain. Minimizing it only removes nuisance, never predictive signal. This is an absolute, non-negative quantity — gives a principled stopping criterion.

## Primal and variational forms

Primal:
$$
\text{CEB} \equiv \min_Z\, I(X; Z \mid Y) - \gamma \cdot I(Y; Z)
$$

Variational (trainable):
$$
\text{VCEB} \equiv \min_{e, b, c}\, \langle \log e(z|x) \rangle - \langle \log b(z|y) \rangle - \gamma \cdot \langle \log c(y|z) \rangle
$$

## Minimum Necessary Information (MNI)

The unique Z satisfying:
$$
I(X;Y) = I(X;Z) = I(Y;Z)
$$

At MNI:
- Z captures everything Y contains about X (sufficiency)
- Z contains no X-specific information beyond Y (minimality)

γ=1 reaches MNI on deterministic datasets. No analogous "principled target" exists in VIB — VIB needs a β sweep to find a Pareto-optimal point.

## CPF = CEB in structural analogy

CPF's fusion:
$$
e_\text{fusion} = \alpha \cdot h_\text{ctx} + (1-\alpha) \cdot e_\text{pred}
$$

- $h_\text{ctx}$ carries full context info, including X-nuisance → "$e(z|x)$ forward encoder side"
- $e_\text{pred} = \sum_v p(v|\cdot) \cdot W_E[v]$ is a Y-conditional vocab-simplex projection → "$b(z|y)$ backward encoder side"
- α controls the mix

**Proposed CODI-CEB loss** (replaces hand-tuned α):
$$
\mathcal{L}_\text{CODI-CEB} = \mathcal{L}_\text{CE}(y) + \lambda_1 \cdot \|h_\text{ctx} - \mathrm{sg}(e_\text{pred})\|_2^2 + \gamma \cdot \mathrm{KL}\!\left[p(z|x) \,\|\, \mathrm{sg}(b(z|y))\right]
$$

with γ scheduled to approach 1 across training.

## Advantages over VIB for our setting

1. **Absolute scale.** MNI point is a target, not a pareto tradeoff.
2. **No adversarial dynamic.** The two terms I(X;Z|Y) and I(Y;Z) are not in direct tension.
3. **Matches CPF's structure naturally.** CPF already has the 2-encoder shape that CEB formalises.

## Open questions

- Does MNI exist for stochastic (non-deterministic) reasoning datasets? Paper claims γ=1 reaches MNI only deterministically.
- Empirical γ schedule for language-model reasoning has not been studied (paper benchmarks on image classification).
- Does MNI correspond empirically to a "sweet spot" in the F1-F6 battery — i.e. non-collapsed F3 AND non-null F5?
