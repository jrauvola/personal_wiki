---
type: source
title: "Noisy Recurrent Neural Networks"
source_type: paper
arxiv_id: "2102.04877"
venue: "NeurIPS 2021"
date_published: 2021-02-09
authors:
  - "Soon Hoe Lim"
  - "N. Benjamin Erichson"
  - "Liam Hodgkinson"
  - "Michael W. Mahoney"
url: "https://arxiv.org/abs/2102.04877"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Noise injection in RNN hidden states is formally equivalent to implicit regularization against the state-to-state Jacobian norm — noise IS a Jacobian penalty."
  - "Noisy RNNs are biased toward flatter loss minima, mathematically equivalent to Hessian-penalty regularization at the small-noise limit."
  - "Stability bias: noise-trained RNNs have smaller state-Jacobian norms by design, making them less sensitive to input perturbations."
  - "Classification margin is provably increased: noisy RNNs favor decision boundaries with larger margin (proof via SDE-limit analysis)."
  - "Empirical: noisy-RNN training improves robustness to various input perturbations without hurting clean-data accuracy."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Provides a principled alternative route to spectral constraints: simply inject noise into latent states during training, which implicitly regularizes Jacobian norms. Cheap, drop-in, and has already been shown to widen margins. F6's narrow basin is exactly the pathology this addresses."
  - slug: "branch-b"
    relevance: primary
    why: "Noise-as-Jacobian-penalty is a cheaper alternative to Hutchinson-Jacobian-regularization for the M-step rollout. Can be combined with V2 detach."
  - slug: "branch-d"
    relevance: secondary
    why: "Stochastic Soft Thinking already does noise injection; this paper provides the theoretical backing explaining WHY it helps (implicit Jacobian regularization, not just exploration)."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/theory
  - domain/training
  - stability-theory
  - technique/noise-injection
related:
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Robust Learning with Jacobian Regularization]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[Jacobian Constraint]]"
  - "[[Spectral Regularization]]"
sources: []
---

# Noisy Recurrent Neural Networks (Lim, Erichson, Hodgkinson, Mahoney 2021)

## TL;DR
Treat RNNs as **discretizations of stochastic differential equations**. Under this framing, injecting noise into hidden states is **mathematically equivalent** to regularizing the state-to-state Jacobian norm — noise acts as an implicit Jacobian penalty. Result: flatter minima, smaller Jacobian norms, larger classification margin, better robustness. All backed by SDE-limit theorems, not just empirics.

## Why this matters for routing-lock

This paper unifies two previously separate interventions: (a) noise injection ([[Stochastic Soft Thinking]], [[Multiplex Thinking]]) and (b) Jacobian regularization ([[Stabilizing Equilibrium Models by Jacobian Regularization]]). They're the same thing in the small-noise limit.

Formally: in the SDE limit, noisy RNN dynamics satisfy
$$
dz_t = f_\theta(z_t, x) dt + \sigma dW_t
$$
Integrating gives implicit regularization on the Jacobian:
$$
\mathcal{L}_{\text{eff}} = \mathcal{L}_{\text{task}} + \frac{\sigma^2}{2} \mathbb{E}\left[\|J_f\|_F^2\right] + O(\sigma^4)
$$
(Equation 9 in the paper, small-σ expansion.) This is **exactly** the Hutchinson-estimator penalty in Bai-Koltun-Kolter (2021), but obtained for free via SGD with noise.

## Concrete implication for CODI

F6 finds CODI's narrow basin: σ=0.5 additive noise on latents collapses accuracy from 16% to <3%. Lim et al. predict: **training with noise σ ≈ 0.1-0.3** would have widened the basin to accommodate test-time noise σ=0.5.

This is a one-line training-code change: after each latent step, add $\mathcal{N}(0, \sigma^2 I)$ to $z_t$. The theorem says it's equivalent to adding $\lambda \|J_f\|_F^2$ to the loss with $\lambda = \sigma^2 / 2$.

## Why this is so much cheaper than explicit Jacobian regularization

- **No Hutchinson trace estimator** (no extra JVP per step).
- **No auxiliary loss** (no new gradient path).
- **Works with any architecture** (including attention; no need to reason about block Jacobians).
- **One hyperparameter** ($\sigma$).

Cost: zero compute overhead. Engineering time: an afternoon.

## Recipe

1. During training of M-step rollout, inject $z_t \leftarrow z_t + \sigma \epsilon_t$, $\epsilon_t \sim \mathcal{N}(0, I)$ at each latent step.
2. Start $\sigma \in \{0.05, 0.1, 0.3\}$; sweep.
3. Measure F6 post-training: does σ=0.5 test-time noise still collapse accuracy?
4. Cross-validate against V2 baseline (no noise injection) and Jacobian-regularization baseline.

## Limits & caveats
- Noise injection is equivalent to Jacobian regularization only in the *small noise limit*. Large σ has different dynamics.
- Does not address *input dependence* (F5). Noise doesn't force content to matter.
- Training loss becomes stochastic; slightly noisier gradients.
- The SDE-limit analysis is rigorous in continuous time; the discrete step size (latent step) is finite, so the theorem is approximate.
