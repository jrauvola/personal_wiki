---
type: source
title: "Representation Learning with Contrastive Predictive Coding (InfoNCE)"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/contrastive
  - domain/information-theory
  - foundational
status: triaged
source_type: paper
arxiv_id: "1807.03748"
venue: "arXiv (widely cited, NeurIPS 2018 workshops)"
date_published: 2018-07-10
authors:
  - "Aaron van den Oord"
  - "Yazhe Li"
  - "Oriol Vinyals"
url: "https://arxiv.org/abs/1807.03748"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "InfoNCE: L_N = −E[log f_k(x_{t+k},c_t) / Σ_j f_k(x_j,c_t)]; minimizing this lower-bounds MI: I(x_{t+k};c_t) ≥ log(N) − L_N."
  - "Critic f_k(x,c) = exp(z^T W_k c) is density-ratio-proportional at optimum: f_k ∝ p(x|c)/p(x)."
  - "Bound becomes tighter as N (number of negatives) grows; saturates at log(N) at optimum."
  - "N-way softmax over 1 positive + (N−1) negatives; noise-contrastive estimation view."
related:
  - "[[VICReg]]"
  - "[[Barlow Twins]]"
  - "[[SeLaR]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/1807.03748"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "InfoNCE over (example_A latent, example_A answer) vs (example_B latent, example_A answer) pairs is the *exact* training-time signal that F5 swap-null tests at eval time. Zero accuracy change under swap = zero mutual info = InfoNCE at log(N) floor. Direct objective for making latents carry per-example info."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Standard MI lower bound; pair primitive for designing anti-swap losses. Will anchor the per-example-information section of the writeup."
  - slug: "branch-b"
    relevance: reference
    why: "Compatible with detach; purely batch-level loss."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling-neutral."
  - slug: "branch-c"
    relevance: reference
    why: "InfoNCE could probe per-example info at eval — but trivially derivable without this paper."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Representation Learning with Contrastive Predictive Coding

van den Oord, Li & Vinyals (2018). Introduces **Contrastive Predictive Coding (CPC)** and the **InfoNCE loss**. InfoNCE is now the canonical contrastive objective — SimCLR, MoCo, CLIP, and most modern SSL methods descend from it.

## Core equations

**InfoNCE loss:**
$$
\mathcal{L}_N = -\mathbb{E}_X\!\left[\log \frac{f_k(x_{t+k}, c_t)}{\sum_{x_j \in X} f_k(x_j, c_t)}\right]
$$

with $X$ containing 1 positive sample $x_{t+k}$ and $N-1$ negatives drawn from $p(x_j)$.

**Scoring function (log-bilinear):**
$$
f_k(x_{t+k}, c_t) = \exp(z_{t+k}^T W_k c_t)
$$

At optimum: $f_k(x, c) \propto p(x \mid c) / p(x)$ — the density ratio.

**Mutual information lower bound:**
$$
I(x_{t+k}; c_t) \ge \log(N) - \mathcal{L}_N
$$

Bound gets tighter as $N$ (# negatives) grows. At perfect critic + $\mathcal{L}_N = 0$, the estimate saturates at $\log N$.

## Why this directly matches the F5 swap-null failure

Our F5 experiment: swap example A's latent KV with example B's latent KV on the same question, measure accuracy delta. Zero accuracy delta means:
$$
I(KV;\ Y \mid \text{question}) \approx 0
$$
— the latent carries no per-example info used by the decoder.

**Contrastive framing of F5 as a training signal.** Let
- $c$ = question embedding
- $z^+$ = KV computed from the matching example's rollout
- $z^-_1, ..., z^-_{N-1}$ = KVs from $N-1$ other in-batch examples

Define a critic $f(z, c) = \exp(z^T W c)$ and train with InfoNCE:
$$
\mathcal{L}_\text{anti-F5} = -\log \frac{\exp(z^{+T} W c)}{\exp(z^{+T} W c) + \sum_{j} \exp(z^{-T}_j W c)}
$$

This **literally** forces $I(KV; y | \text{question}) > 0$, and the measured F5 swap-null should reduce from 0% to something positive.

## Mapping the three F5 variants to InfoNCE

| F5 variant | InfoNCE setup |
|---|---|
| Same question, swap latent | c = question, z⁺ = own-KV, z⁻ = other-KV |
| Same latent, swap question | c = latent, z⁺ = own-question, z⁻ = other-question |
| Cross-example at step t | multi-step InfoNCE, one loss per step |

All three give a signed, batch-local gradient that flows straight into the detached KV's *producing* hidden state — no special architecture needed, and completely compatible with detach regimes because the gradient enters through the question embedding side.

## Caveats

- InfoNCE gives a **loose** MI lower bound; recent work (f-MICL, Wu et al. 2022) has better estimators.
- **N-dependence:** with batch size 2, InfoNCE gives a max MI of log(2) = 0.69 bits, which is below the information content of a GSM8K question. Need large batches or cross-batch negatives (MoCo-style queue).
- Related paper (Oct 2025) "Contrastive Predictive Coding Done Right for Mutual Information Estimation" (arXiv:2510.25983) — worth following up.

## Canonical citation form

van den Oord, A., Li, Y., & Vinyals, O. (2018). Representation Learning with Contrastive Predictive Coding. arXiv:1807.03748.
