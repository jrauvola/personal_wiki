---
type: concept
title: "Variational Information Bottleneck"
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
  - "VIB"
  - "Deep VIB"
  - "Information Bottleneck (variational)"
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck (concept)]]"
  - "[[InfoVAE]]"
  - "[[HSIC Bottleneck]]"
  - "[[Continuous Autoregressive Language Models]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
  - "[[Context-Prediction-Fusion]]"
sources:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Emergence of Invariance and Disentanglement]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CPF is an implicit VIB (convex mix of info-rich h_ctx and vocab-simplex-compressed e_pred); VIB gives the principled loss to learn the mixing coefficient."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational concept for the writeup's regularization chapter; links to posterior-collapse and mode-collapse failure modes across the literature."
  - slug: "branch-b"
    relevance: secondary
    why: "Minimum-sufficient detach = VIB at β→∞; VIB gives a graded version of what detach does by brute force."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling-neutral regularization tool."
  - slug: "branch-c"
    relevance: reference
    why: "Probe-side: per-dim KL diagnostic (CALM) comes directly from this framework."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Variational Information Bottleneck

A family of information-theoretic regularization objectives whose common structure is: **maximise predictive information $I(Z;Y)$ while minimising nuisance information $I(Z;X)$**, via a tractable variational bound.

## The objective family

Primal IB Lagrangian:
$$
\mathcal{R}_\text{IB} = I(Z;Y) - \beta \cdot I(Z;X)
$$

Neural networks cannot directly compute MI, so the field has produced a sequence of variational *upper bounds* on $I(Z;X)$ and lower bounds on $I(Z;Y)$:

| Method | Source | Bound form | Key innovation |
|---|---|---|---|
| VIB | [[Deep Variational Information Bottleneck]] | $\mathrm{KL}(q(z|x) \| r(z))$, fixed spherical-Gaussian prior | Parameterisation of IB via reparameterised Gaussian encoder |
| β-VAE | Higgins et al. 2017 | Same as VIB, Y=X | Unsupervised IB for disentanglement |
| InfoVAE | [[InfoVAE]] | MMD on aggregated posterior instead of KL | Independent control of posterior-fit and info-preservation |
| CEB | [[Conditional Entropy Bottleneck]] | $I(X;Z|Y)$ via backward encoder $b(z|y)$ | Absolute-scale compression metric; tighter bound |
| HSIC-IB | [[HSIC Bottleneck]] | Kernel HSIC replaces MI | Tractable, per-layer, no backprop needed |
| CLUB | Cheng et al. 2020 | Contrastive *upper* bound on MI | Tighter compression |
| CALM KL-clip | [[Continuous Autoregressive Language Models]] | max(λ, KL_i) per-dim | Prevents per-dimension collapse |

## Failure modes

VIB's canonical pathology: **posterior collapse.** When β is too high relative to the Y-signal strength, the encoder's easiest gradient descent path is $q(z|x) \to r(z)$, driving KL to zero. The decoder then ignores $z$ (since it's just noise) and the network ignores the latent entirely.

Diagnostic: for every example $x_i$, measure $\mathrm{KL}(q(z|x_i) \| r(z))$. If the distribution of these KLs is concentrated near zero, collapse has occurred. CALM's fix: clip per-dim KL to a floor $\lambda$ (see [[Continuous Autoregressive Language Models]]).

## Relevance to the F1-F6 battery on CODI V2

See [[Routing vs Reasoning]] for the detailed F-battery. Summary:

| Failure | IB interpretation | Fix family |
|---|---|---|
| F3 template lock (7/8 pos, <0.4 bits) | posterior collapse: $q(z\|x) \to r(z)$ position-wise | CALM KL-clip per-position; InfoVAE MMD; CEB |
| F5 swap-null (0% Δ under A↔B swap) | $I(Z;Y \| \text{question}) \approx 0$ | InfoNCE ([[Contrastive Predictive Coding]]) directly targets this |
| F6 narrow basin (σ=0.5 → <3%) | deterministic encoder: $f_\Sigma(x) \to 0$ | VIB KL term bounds $f_\Sigma$ away from zero; VICReg variance hinge |

## When VIB *hurts*

- On problems where $I(X;Y)$ is very small (e.g. RL with sparse rewards), the $\beta I(Z;X)$ term dominates and causes collapse. Fix: schedule β to be very small, or switch to CEB where $\gamma=1$ is scale-invariant.
- On tasks where the "nuisance" information is actually useful downstream (e.g. rare but predictive features), VIB compresses them away. Mitigations: use CEB's conditional form, or task-specific $\beta$ scheduling.

## Related but distinct concepts

- **[[Feature Collapse]]** — the failure mode; VIB is one *prescription* for preventing it.
- **[[Routing vs Reasoning]]** — functional diagnosis of CODI's failure; VIB is one *mechanism* for shifting routing into reasoning.
- **[[Context-Prediction-Fusion]]** — CPF is interpretable as an implicit VIB; this concept page gives the bridge.
