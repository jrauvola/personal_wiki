---
type: source
title: "Deep Variational Information Bottleneck"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/information-theory
  - domain/regularization
  - foundational
status: triaged
source_type: paper
arxiv_id: "1612.00410"
venue: "ICLR 2017"
date_published: 2017-04-25
authors:
  - "Alexander A. Alemi"
  - "Ian Fischer"
  - "Joshua V. Dillon"
  - "Kevin Murphy"
url: "https://arxiv.org/abs/1612.00410"
code_repo: "https://github.com/alexalemi/vib_demo"
has_weights: false
confidence: high
key_claims:
  - "The IB Lagrangian R_IB = I(Z;Y) − β·I(Z;X) admits a tractable variational upper bound: J_IB = (1/N) Σ_n E_ε~p(ε)[−log q(y_n|f(x_n,ε))] + β·KL[p(Z|x_n) ‖ r(Z)] where r(z) is a fixed spherical Gaussian prior and f is the reparameterised encoder mean+diag-Σ MLP."
  - "VIB trained networks generalise better and are substantially more robust to adversarial perturbations than deterministic or L2-regularised baselines at matched accuracy."
  - "A Gaussian stochastic encoder p(z|x) = N(z | f_μ(x), f_Σ(x)) with reparameterisation ε ~ N(0,I) gives an unbiased Monte-Carlo estimate of the VIB gradient."
  - "β controls the compression/relevance tradeoff; VAE is the unsupervised special case at β=1 with q(y|z) a reconstruction of x."
related:
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Variational Information Bottleneck]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "https://ar5iv.labs.arxiv.org/html/1612.00410"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CPF α interpolation is an implicit IB: α·h_ctx + (1−α)·e_pred is the convex combination of reconstruction (h_ctx) and compression-to-prior (e_pred on the vocab simplex). VIB gives a principled objective for learning α per-step rather than hand-picking."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "VIB is the foundational anti-posterior-collapse formulation and the natural framing for the latent-reasoning regularization chapter of the writeup."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach ablations are an implicit information bottleneck (no-grad through KV = infinite β compression of the KV). A graded β schedule formalises what detach does by brute force."
  - slug: "branch-a"
    relevance: reference
    why: "Foundational regularization tool; not Qwen3-specific but applicable to any latent-reasoning scaling run."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology work; VIB is a training-time regularizer, not a diagnostic."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Deep Variational Information Bottleneck

Alemi et al.'s foundational paper introducing the **Variational Information Bottleneck (VIB)** — a tractable neural-network parameterization of the information-bottleneck principle (Tishby et al., 1999). VIB is the most widely adopted IB variant and the standard starting point for any "compress-to-prior plus predict-Y" latent-regularization scheme.

## Core equations

The IB Lagrangian:
$$
\mathcal{R}_{IB}(\theta) = I(Z;Y) - \beta \cdot I(Z;X)
$$

Variational upper bound (minimized during training):
$$
\mathcal{J}_{IB} = \frac{1}{N}\sum_{n=1}^N \mathbb{E}_{\epsilon \sim p(\epsilon)}\!\left[-\log q(y_n \mid f(x_n, \epsilon))\right] + \beta \cdot \mathrm{KL}\!\left[p(Z \mid x_n) \,\|\, r(Z)\right]
$$

where:
- $q(y|z)$ is a variational decoder (neural network)
- $r(z) = \mathcal{N}(z | 0, I)$ is a fixed spherical-Gaussian prior
- $p(z|x) = \mathcal{N}(z | f_\mu(x), f_\Sigma(x))$ with diagonal covariance
- reparameterisation: $z = f_\mu(x) + f_\Sigma(x)^{1/2} \odot \epsilon$

## Practical notes

- **β schedule matters.** Very small β (e.g. 10⁻³) behaves like standard dropout; large β (≥1) can induce collapse where the encoder outputs the prior. Typical sweet spot in the literature: β ∈ [1e-3, 1e-1].
- **Prior choice.** Spherical Gaussian is the textbook choice; in continuous-latent CoT where the "data" is already a distribution over intermediate hidden states, a learned mixture prior (GMM or VampPrior) is likely needed.
- **Stochastic encoder is load-bearing.** Deterministic encoders give vacuous KL terms and lose the robustness benefits.

## Relevance to our CODI failures

Direct mapping to the F1-F6 battery (see [[Routing vs Reasoning]]):

- **F3 template lock** (entropy <0.4 bits at 7/8 positions) is the classic VIB posterior-collapse signature with β set too high relative to the Y-reconstruction strength. Fix: lower effective β, or replace fixed spherical prior with a learned per-position mixture.
- **F5 swap-null** (0% accuracy change when A's KV is replaced with B's) is the F5-style empirical test for `I(Z;Y|question) = 0` — exactly what the VIB I(Z;Y) term is designed to prevent.
- **F6 narrow basin** (σ=0.5 noise → <3% accuracy) is consistent with a deterministic encoder collapsing f_Σ(x) → 0. VIB's minimum-KL constraint keeps f_Σ(x) bounded away from zero, widening the basin.

## Canonical citation form

Alemi, A. A., Fischer, I., Dillon, J. V., & Murphy, K. (2017). Deep Variational Information Bottleneck. ICLR 2017.
