---
type: source
title: "Stabilizing Equilibrium Models by Jacobian Regularization"
source_type: paper
arxiv_id: "2106.14342"
venue: "ICML 2021"
date_published: 2021-06-28
authors:
  - "Shaojie Bai"
  - "Vladlen Koltun"
  - "J. Zico Kolter"
url: "https://arxiv.org/abs/2106.14342"
code_repo: "https://github.com/locuslab/deq"
has_weights: false
status: read
confidence: high
key_claims:
  - "DEQ stability is directly characterized by the spectral radius rho(J_f) of the Jacobian at the fixed point; rho < 1 is the contraction-mapping criterion guaranteeing convergence."
  - "Without explicit regularization, rho(J_f) grows during training and DEQ iteration counts blow up, indicating drift toward instability."
  - "The proposed regularizer penalizes a stochastic Hutchinson estimate of the Frobenius norm of J_f (upper bound on spectral norm), adding only a small per-step cost."
  - "Regularized DEQs converge to fixed points 2-3x faster in both forward and backward passes and scale to WikiText-103 LM and ImageNet classification."
  - "The technique is a first-class stability objective during training — stability is optimized, not just hoped for."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Directly operationalizes rho(J_f) < 1 as an auxiliary training loss — the most portable stability intervention we could graft onto CODI's M-step latent rollout without switching to full DEQ."
  - slug: "branch-b"
    relevance: primary
    why: "Jacobian regularization is the canonical drop-in for M-step recurrence — pair it with (or instead of) V2 detach. Frobenius-norm bound bounds BPTT chain amplification by design."
  - slug: "branch-d"
    relevance: secondary
    why: "CPF + Jacobian-reg is a natural combination: CPF anchors trajectory to vocab manifold, Jacobian-reg stabilizes trajectory geometry. Both address basin-width problem (F6) from orthogonal angles."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling recurrent latents to 9B with stability objective instead of brittle hand-tuning."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/theory
  - domain/training
  - family/equilibrium
  - stability-theory
  - technique/jacobian-regularization
related:
  - "[[Deep Equilibrium Models]]"
  - "[[Robust Learning with Jacobian Regularization]]"
  - "[[Fixed-Point Iteration]]"
  - "[[Jacobian Constraint]]"
  - "[[Spectral Regularization]]"
sources: []
---

# Stabilizing Equilibrium Models by Jacobian Regularization (Bai, Koltun, Kolter 2021)

## TL;DR
DEQ training drifts toward **instability** — iteration counts grow over training, gradients through the implicit solve explode. Fix: add an **auxiliary loss on the Jacobian of the fixed-point map**, using a stochastic Hutchinson trace estimator of $\|J_f\|_F^2$. Regularized DEQs are 2-3x faster, converge reliably, and scale to ImageNet + WikiText-103. This is the canonical "spectral radius < 1" contraction criterion enforced as a training objective.

## The core idea (with equations)

The Banach contraction-mapping theorem says: if $\rho(J_f) < 1$ (spectral radius of Jacobian), $f$ has a unique fixed point and Picard iteration converges geometrically. For neural $f_\theta$, this is not automatic — training is free to drive $\rho$ above 1.

The regularizer (stochastic Frobenius bound):
$$
\mathcal{L}_{\text{jac}}(\theta) = \mathbb{E}_{\epsilon \sim \mathcal{N}(0, I)}\left[\|J_f \epsilon\|_2^2\right] \approx \|J_f\|_F^2 \geq \|J_f\|_2^2 = \rho(J_f)^2
$$

Bounding Frobenius bounds spectral (cheap upper bound), avoiding any explicit SVD. The Hutchinson trace estimator needs only one extra JVP per step — adds ~15% training cost.

Total loss: $\mathcal{L}_{\text{task}} + \lambda \mathcal{L}_{\text{jac}}$, with $\lambda \sim 10^{-3}$.

## Why this is the highest-leverage finding for our routing-lock problem

The **F6 narrow-basin** result (σ=0.5 collapses V2 to <3% accuracy) is *exactly* the pathology Bai-Koltun-Kolter characterize. A narrow basin means high local sensitivity, i.e. a large Jacobian norm at the fixed point. Regularizing $\|J_f\|_F$ down **directly widens the basin by bounding local expansion**:

For a Picard iterate $z_{k+1} = f(z_k, x)$, noise $\delta$ propagates as $\delta_{k+1} \approx J_f \delta_k$, so after $M$ steps the perturbation scales by $\|J_f\|_2^M$. If $\|J_f\|_2 < 1$, perturbations *contract* — the basin is an attractor. If $\|J_f\|_2 \approx 1$, marginal stability. If $\|J_f\|_2 > 1$ (today's CODI regime), noise blows up — we see exactly this in F6.

For the M=8 rollout in V2, $\|J_f\|_2 = 1.3$ at each step implies an 8.2x amplification of perturbations — explaining the σ=0.5 collapse without further mystery.

## Application recipe for V2/V3/V4

1. Compute $\|J_f^{(t)}\|_F^2$ approximation per latent step using one Hutchinson sample.
2. Penalty: $\lambda \sum_{t=1}^{M} \|J_f^{(t)} \epsilon_t\|_2^2$, $\epsilon_t \sim \mathcal{N}$.
3. $\lambda$ starts at $10^{-3}$; anneal if basin widens too much (accuracy drops; monitor F6 at σ=0.1, 0.5).
4. Diagnostic: track rolling mean of $\|J_f\|_F$ during training — if ever >1, something is wrong.

Training-cost delta: ~15% per step. Engineering time: 1-2 days.

## Limits & caveats
- Hutchinson is stochastic; gradient variance bumps up. Not catastrophic but needs a slightly lower LR.
- Works well at the DEQ fixed point. For an explicit M-step rollout (not a solved equilibrium), the target is every step's Jacobian, not just the final.
- Does not address content-ablation (F5) — that's an *input-dependence* problem, orthogonal to the stability-of-map problem this technique addresses.
