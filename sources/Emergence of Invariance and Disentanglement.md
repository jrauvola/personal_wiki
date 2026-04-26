---
type: source
title: "Emergence of Invariance and Disentanglement in Deep Representations"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/information-theory
  - foundational
status: triaged
source_type: paper
arxiv_id: "1706.01350"
venue: "JMLR 19 (2018)"
date_published: 2017-06-05
authors:
  - "Alessandro Achille"
  - "Stefano Soatto"
url: "https://arxiv.org/abs/1706.01350"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Invariance to nuisance factors is equivalent to information minimality of the representation: I(z; nuisance) ≤ I(weights; data) + const."
  - "Stacking layers + injecting noise during training naturally bias the network towards invariant representations without architectural enforcement."
  - "Introduces Information Bottleneck for weights (vs Tishby's IB for activations): I_θ(D;θ) = complexity term → PAC-Bayes bound."
  - "Invariance and disentanglement are bounded above and below by information in the weights; implicitly optimised during training."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck (concept)]]"
  - "[[Variational Information Bottleneck]]"
sources:
  - "https://jmlr.org/papers/v19/17-646.html"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Foundational theoretical framing — the 'CPF anchors via minimality' argument is exactly Achille-Soatto's invariance-as-minimality claim. Anchors our branch-d writeup theoretically."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical citation for the IB-in-deep-learning framing chapter; connects weights-side and activations-side IB."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach = infinite compression = invariance by Achille-Soatto's theorem. Gives theoretical justification for why minimum-sufficient variants can work."
  - slug: "branch-a"
    relevance: reference
    why: "Theory, not scaling."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not diagnostic."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Emergence of Invariance and Disentanglement in Deep Representations

Achille & Soatto (JMLR 2018). The theoretical paper showing that **invariance to nuisance factors is equivalent to minimality of the representation** — a foundational result linking the Information Bottleneck framework to the practical goals of representation learning.

## Key theorems

**Invariance-minimality duality:**
$$
I(z;\ n) \le I(\theta;\ \mathcal{D}) + \text{const}
$$

where $z$ = learned representation, $n$ = nuisance factors, $\theta$ = weights, $\mathcal{D}$ = dataset. Compressing the weights with respect to the data *automatically* makes $z$ nuisance-invariant.

**Weights IB (novel):**
$$
\mathcal{L}(\theta) = \mathbb{E}_\mathcal{D}[\mathcal{L}_\text{task}] + \beta \cdot I(\mathcal{D};\ \theta)
$$

Provides a PAC-Bayes-style bound on generalisation via mutual information in the weights — distinct from Tishby's IB over activations.

**Disentanglement via stacking noise:**
Injecting noise during training + stacking layers forces the network to build up invariance progressively; disentanglement of representations is bounded above and below by $I(\theta; \mathcal{D})$.

## Relevance to our latent-reasoning work

**"CPF forces invariance via anchoring"** is the natural Achille-Soatto reading of [[Context-Prediction-Fusion]]:
- CPF pins $e_\text{fusion}$ to the vocab simplex (via $e_\text{pred}$)
- This is an **explicit minimality constraint**: the latent cannot be richer than the vocab simplex can express
- By A-S duality, this *automatically* makes the latent invariant to non-predictive nuisance (random hidden-state fluctuations)

This framing gives a theoretical reason why CPF anti-collapse works — not just empirically observed but predicted by A-S Theorem 2.

## For branch-b (detach)

Branch-b's **minimum-sufficient detach** is also readable in A-S terms: `detach(KV) = stop_grad` is an **infinite-β limit** of the weights-IB. The gradient to the KV-producer is zero, so no information can flow back → the representation is maximally compressed w.r.t. downstream loss.

A-S's duality says this should maximise invariance. The question for branch-b is whether that invariance preserves the right Y-information — which is exactly what detach-ablation studies test.

## Canonical citation form

Achille, A., & Soatto, S. (2018). Emergence of Invariance and Disentanglement in Deep Representations. Journal of Machine Learning Research, 19(50), 1–34. arXiv:1706.01350.
