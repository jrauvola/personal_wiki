---
type: source
title: "InfoVAE: Information Maximizing Variational Autoencoders"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/information-theory
  - domain/regularization
  - domain/posterior-collapse
status: triaged
source_type: paper
arxiv_id: "1706.02262"
venue: "AAAI 2019"
date_published: 2017-06-07
authors:
  - "Shengjia Zhao"
  - "Jiaming Song"
  - "Stefano Ermon"
url: "https://arxiv.org/abs/1706.02262"
code_repo: "https://github.com/ermongroup/lagvae"
has_weights: false
confidence: high
key_claims:
  - "InfoVAE objective: L = E[log p(x|z)] − (1−α)·KL(q(z|x)‖p(z)) − (α+λ−1)·D(q(z)‖p(z)); independent control of inference accuracy (α) and info preservation (λ)."
  - "MMD-VAE (D = Maximum Mean Discrepancy) is the most stable instantiation; outperforms adversarial JS and Stein VGD."
  - "λ controls the X vs Z loss-scale imbalance; recommended to set λ so that L_X ≈ L_Z at initialisation (λ=1000 on MNIST)."
  - "At α+λ−1 = 0 reduces to β-VAE; otherwise allows disentangling posterior regularization from aggregated-posterior regularization."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/1706.02262"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "InfoVAE is the canonical answer to 'β-VAE causes posterior collapse' — directly maps to our F3 (template lock = posterior-collapsed latent) and F5 (swap-null = low I(x;z)). MMD divergence on aggregated posterior is drop-in into CODI."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Posterior-collapse-mitigation canonical reference; writeup needs the MMD vs KL story."
  - slug: "branch-b"
    relevance: reference
    why: "MMD divergence is batch-local, compatible with detach."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling-neutral."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a diagnostic."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# InfoVAE: Information Maximizing Variational Autoencoders

Zhao, Song & Ermon (AAAI 2019). Generalises β-VAE to a 2-parameter family that **independently** controls the posterior-fit term and the information-maximisation term. MMD-VAE (the preferred instantiation) replaces the KL divergence on aggregated posterior with a kernel MMD, avoiding the pathological ignore-latent solution of standard VAEs.

## Core objective

$$
\mathcal{L}_\text{InfoVAE} = \mathbb{E}[\log p_\theta(x \mid z)] - (1 - \alpha) \cdot \mathbb{E}[\mathrm{KL}(q_\phi(z|x) \,\|\, p(z))] - (\alpha + \lambda - 1) \cdot D(q_\phi(z) \,\|\, p(z))
$$

where:
- $q_\phi(z|x)$ = encoder
- $q_\phi(z) = \int q_\phi(z|x) p(x) dx$ = **aggregated posterior**
- $D$ = any divergence (KL, JS, Stein, MMD)
- $\alpha \in [-\infty, 1]$ controls posterior-fit
- $\lambda > 0$ controls info-preservation strength

**Recovery of β-VAE:** setting $\alpha + \lambda - 1 = 0$ and $D = \mathrm{KL}$ gives β-VAE with $\beta = 1 - \alpha$.

## The three divergence choices

| Divergence | Implementation | Stability |
|---|---|---|
| Jensen-Shannon | adversarial discriminator | unstable |
| Stein VGD | kernel gradient | moderate |
| **MMD** | kernel two-sample test | stable, preferred |

**MMD** form (batch estimator):
$$
\widehat{\mathrm{MMD}}^2(q, p) = \mathbb{E}_{z,z' \sim q}[k(z, z')] - 2\mathbb{E}_{z \sim q, z'' \sim p}[k(z, z'')] + \mathbb{E}_{z'', z''' \sim p}[k(z'', z''')]
$$

with Gaussian kernel $k(z, z') = \exp(-\|z - z'\|^2 / 2\sigma^2)$.

## Why this is the direct answer to F3

**F3 diagnosis:** 7/8 latent positions emit a fixed template with entropy <0.4 bits. This is canonical posterior collapse: $q(z|x) \to p(z)$, latent ignored by decoder.

**InfoVAE fix.** Replace KL with MMD on the aggregated posterior:
- MMD matches *moments* of $q(z)$ to the prior, not pointwise per-example
- Allows individual $q(z|x_i)$ to be sharp and example-specific while still keeping $\mathbb{E}_x[q(z|x)] \approx p(z)$
- Breaks the KL-driven incentive to collapse $q(z|x) \to p(z)$

## Proposed CODI-InfoVAE loss

$$
\mathcal{L}_\text{CODI-IV} = \mathcal{L}_\text{CE}(y) + \mu \cdot \widehat{\mathrm{MMD}}^2(q(KV_t), r(KV_t))
$$

where $r$ is a fixed reference distribution (e.g. batch-mean empirical). No KL between $q(KV_t | x)$ and $r$ — so individual examples can stay sharp.

## Caveats

- **Kernel bandwidth selection** is notoriously fiddly; median-heuristic works tolerably.
- **Not a tight MI bound** — MMD indirectly proxies info via divergence to the aggregated posterior.
- **Scaling to high-dim latents:** MMD estimation variance grows with dim. For our KV cache dim 3584 (Qwen3-4B), may need sliced MMD or random projections.

## Canonical citation form

Zhao, S., Song, J., & Ermon, S. (2019). InfoVAE: Information Maximizing Variational Autoencoders. AAAI 2019. arXiv:1706.02262.
