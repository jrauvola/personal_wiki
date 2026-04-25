---
type: synthesis
title: "Research: Stability Theory for Latent Recurrence"
question: "What mathematical principles and AI techniques from stability theory could break routing-lock / template-attractor failures in latent reasoning models?"
answer_quality: solid
created: 2026-04-22
updated: 2026-04-22
tags:
  - research
  - stability-theory
  - synthesis
  - latent-reasoning
status: developing
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Primary north-star input. Directly addresses the F1-F6 routing-lock failure modes with a concrete math-backed intervention menu."
  - slug: "branch-b"
    relevance: primary
    why: "Provides the stability-theoretic foundation for V2 detach and names principled alternatives (Jacobian regularization, implicit differentiation, Parseval, noise injection). Branch-B design decisions should flow from this page."
  - slug: "branch-d"
    relevance: secondary
    why: "Frames CPF as a 'recall-mode' DEQ anchor and gives spectral-stability scaffolding that complements CPF's content-anchor mechanism."
  - slug: "branch-a"
    relevance: reference
    why: "Stability theory informs scaling narrative for recurrent latent reasoning at 9B — without bounded-Lipschitz guarantees, M-step rollout at larger scale is gambling."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
  - "[[Parseval Networks]]"
  - "[[Orthogonal Recurrent Networks]]"
  - "[[Noisy Recurrent Neural Networks]]"
  - "[[Robust Learning with Jacobian Regularization]]"
  - "[[Fixed-Point Iteration]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
  - "[[Lyapunov Stability]]"
  - "[[Spectral Regularization]]"
  - "[[Jacobian Constraint]]"
  - "[[Shaojie Bai]]"
  - "[[J. Zico Kolter]]"
  - "[[Jeffrey Pennington]]"
  - "[[Stability and Generalization in Looped Transformers]]"
sources:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Resurrecting the Sigmoid Dynamical Isometry]]"
  - "[[Parseval Networks]]"
  - "[[Orthogonal Recurrent Networks]]"
  - "[[Noisy Recurrent Neural Networks]]"
  - "[[Robust Learning with Jacobian Regularization]]"
  - "[[Stability and Generalization in Looped Transformers]]"
---

# Research: Stability Theory for Latent Recurrence

## Overview

This is the mathematical scaffold for our F1-F6 failure findings. CODI's M-step latent rollout is a **truncated, untrained fixed-point iteration** where the iteration map $f_\theta$ has no stability objective. The core findings of F3 (template attractor), F5 (swap-null / input-inertness), and F6 (narrow basin collapse) are precisely the pathologies that 2017-2025 stability theory predicts and gives *actionable* interventions for — Jacobian regularization, Parseval retraction, implicit differentiation, noise injection, Lyapunov-auxiliary losses. This page synthesizes the menu.

**The core diagnosis:**

$$
\text{CODI-V2 at 4B} = \text{Picard iteration without contraction guarantee}
$$

Our template-routing attractor (F3) + narrow basin (F6) + input-inertness (F5) are the three standard pathologies when $\rho(J_f)$ is uncontrolled, the Jacobian is rank-collapsed toward one dominant direction, and input enters only via initial state rather than recall-mode.

## Key Findings

Seven findings, each equation-level, each linking to one or more sources.

**F-ST1. CODI's M-step rollout IS a truncated DEQ, and stability theory forbids the template attractor if trained as one.** (Source: [[Deep Equilibrium Models]], [[Stability and Generalization in Looped Transformers]].)

For a fixed-point formulation $z^\star = f_\theta(z^\star, x)$, the fixed point is forced to depend on $x$. No-recall (input enters only via $z_0$) fixed points are **countable** — they cannot achieve strong input dependence (Labovich 2026 theorem). CODI's base rollout is no-recall (input via initial KV-cache but the iteration proper is not input-fed). CPF makes it recall-mode by injecting context at each step. **Mathematical prediction:** any non-recall-mode M-step rollout will degenerate toward a small finite set of attractors. Empirical: F3 finds a single-template attractor. **These agree.**

**F-ST2. Spectral radius $\rho(J_f) < 1$ is the Banach-contraction criterion for F6 basin width.** (Source: [[Stabilizing Equilibrium Models by Jacobian Regularization]], [[Robust Learning with Jacobian Regularization]].)

A perturbation $\delta$ at step 0 evolves as $\|\delta_M\| \leq \prod_t \|J_t\|_2 \cdot \|\delta_0\|$. For CODI's M=8 and F6's observation that $\sigma=0.5$ collapses accuracy, we infer local Lipschitz $L \geq 1.3$ per step (giving 8x amplification through the stack). Jacobian regularization via Hutchinson estimator reduces this to $L \leq 1$ per step, giving bounded basin. **Implementation cost:** ~15% compute overhead, 1-2 days engineering.

**F-ST3. Noise injection during training is equivalent to Jacobian-Frobenius regularization in the small-noise limit.** (Source: [[Noisy Recurrent Neural Networks]].)

For hidden-state noise $z_t \leftarrow z_t + \sigma \epsilon$, the implicit regularizer is $\frac{\sigma^2}{2} \mathbb{E}[\|J_f\|_F^2] + O(\sigma^4)$. Lim et al. 2021 prove this rigorously via SDE-limit theorems. **This unifies** [[Stochastic Soft Thinking]], [[Multiplex Thinking]], and [[Stabilizing Equilibrium Models by Jacobian Regularization]] — they're the same mechanism. **Implementation cost:** zero compute overhead, afternoon engineering.

**F-ST4. Parseval retraction $W \leftarrow (1+\beta)W - \beta W W^\top W$ directly eliminates the template-direction singularity.** (Source: [[Parseval Networks]], [[Orthogonal Recurrent Networks]].)

Template-attractor = rank-1 Jacobian. Parseval forces $W W^\top = I$ (all singular values $\approx 1$). A rank-1 dominant direction is *impossible* under Parseval — there's no preferred eigendirection. **Cost:** one extra matmul per recurrent weight per SGD step. **Engineering:** half a day.

**F-ST5. Implicit differentiation via the implicit function theorem replaces V2/V3/V4 detach cleanly.** (Source: [[Deep Equilibrium Models]], [[Deep Equilibrium Model (DEQ)]].)

The IFT gradient $\frac{\partial \ell}{\partial \theta} = -\frac{\partial \ell}{\partial z^\star}(I - J_f)^{-1}\frac{\partial f}{\partial \theta}$ is the principled version of "cut the chain." V2's detach at the M-th step is a crude approximation that assumes $J_f \approx 0$; IFT uses the actual Jacobian. **Implication for Branch B:** the detach-vs-no-detach sweep is a symptom-level investigation; the correct answer is "neither — solve the fixed point implicitly."

**F-ST6. Lyapunov-auxiliary loss adds input-conditional attractor shaping.** (Source: [[Lyapunov Stability]], Dai et al. 2021.)

A learned input-conditional Lyapunov function $V(z; x) = \|z - g_\phi(x)\|^2$ with decrease-condition loss $\max(0, V(z_{t+1}) - V(z_t) + \alpha \|z_t - g_\phi(x)\|^2)$ forces the trajectory to converge to a *per-input* target. **This is an orthogonal intervention from CPF** — CPF anchors via content; Lyapunov anchors via convergence. Can combine. **Engineering:** ~3 days.

**F-ST7. Dynamical isometry + SiLU nonlinearity predicts inherent Jacobian-spectrum pathology.** (Source: [[Resurrecting the Sigmoid Dynamical Isometry]].)

Pennington-Schoenholz-Ganguli 2017 prove ReLU nets cannot achieve dynamical isometry — at least half of singular-value mass is killed per layer. Qwen3-4B uses SiLU (smoother than ReLU but not orthogonal). Compositional Jacobian over 8 latent steps will therefore have a long tail of near-zero singular values + a few dominant ones. **This exactly matches** our F3 template-attractor signature. Mitigation: orthogonal init + Parseval retraction of recurrent weights.

## The five interventions ranked by cost and expected impact

| # | Intervention | Compute cost | Eng. time | Addresses | Expected impact on F3/F5/F6 |
|---|---|---|---|---|---|
| 1 | Noise injection at each latent step ($\sigma \sim 0.1$) | 0% | 0.5 day | F6 basin | F6: widens basin; expected σ=0.5 retention >50% |
| 2 | Orthogonal initialization of recurrent-block weights | 0% | 0.5 day | F3, F6 | F3: reduced template dominance; F6: initial well-conditioning |
| 3 | Parseval retraction $\beta=10^{-3}$ on recurrent weights | ~1% | 1 day | F3, F6 | F3: eliminates rank-1 eigendirection; F6: basin widened |
| 4 | Hutchinson Jacobian-Frobenius penalty $\lambda=10^{-3}$ | ~15% | 2 days | F3, F6 | F3: stable-rank rises; F6: formal margin guarantee |
| 5 | Full DEQ reformulation with Anderson root-finding | ~50% | 2 weeks | F3, F5, F6 | Complete stability-theoretic resolution but high engineering cost |

Recommend running (1)+(2) first as a zero-cost sanity check. If insufficient, add (3). Only reach for (4) if needed. (5) is the "north-star" long-term research arc.

## Top 5 findings linking stability theory → our routing-lock problem

**These are the five bullets the parent research-branch generation should pick up:**

1. **"F6 narrow basin = Jacobian norm >> 1 per step" is formally provable.** The basin width is $\propto \prod_t \|J_t\|_2^{-1}$. Our measured F6 σ=0.5 collapse implies per-step Lipschitz ≥ 1.3. Fixing this to ≤ 1 via any spectral constraint (Parseval, Jacobian-Frobenius, or noise injection) mechanically widens the basin.

2. **"F3 template attractor = rank-collapsed Jacobian"** — the single dominant singular direction in $J_f$ corresponds to the template-routing vector. Stable-rank regularization $\|J\|_F^2 / \|J\|_2^2$ directly fights this by enforcing that multiple singular values participate. This is arguably the single most specific technical intervention for the template-attractor problem.

3. **"V2 detach is truncated implicit-function-theorem gradient."** The principled version is solving the fixed point and using $(I - J_f)^{-1}$ for the gradient. Branch B should consider the V2-detach-vs-no-detach question as a proxy for "should we run this as a DEQ?" The IFT answers the question cleanly.

4. **"No-recall fixed points are countable → cannot be input-dependent"** (Labovich 2026 theorem, [[Stability and Generalization in Looped Transformers]]). This is the cleanest formal explanation of F5 swap-null. CODI is no-recall; CPF is recall. The theorem *predicts* F5 and *predicts* CPF will cure it. We can actually test this.

5. **"Noise injection is free Jacobian regularization"** (SDE-limit theorem, [[Noisy Recurrent Neural Networks]]). Injecting $\mathcal{N}(0, \sigma^2)$ noise into latents during training is equivalent to adding $\lambda \|J\|_F^2$ with $\lambda = \sigma^2/2$. Zero compute cost, afternoon engineering. This is the highest-value-per-effort intervention to try.

## Most applicable concepts to our project

- **[[Jacobian Constraint]]** — the single most portable intervention menu. Includes Frobenius, nuclear, stable-rank, and spectral norm penalties, each addressing a different failure-mode signature.
- **[[Spectral Regularization]]** — the weight-level implementation family (Parseval, orthogonal init, spectral margin). These compose with [[Jacobian Constraint]] and address the compositional M-step amplification directly.
- **[[Fixed-Point Iteration]]** — the framing that lets us reinterpret V2/V3/V4 detach as (crude) implicit differentiation, and makes F3/F5/F6 diagnostically cleaner via the reachability / input-dependence / geometry axes.
- **[[Deep Equilibrium Model (DEQ)]]** — the architectural target for "CODI done right." Replaces BPTT + detach tradeoffs with IFT gradients, forces convergence to input-dependent fixed point, enables Jacobian regularization as a first-class objective.
- **[[Lyapunov Stability]]** — the strongest mathematical framework for attractor shaping; most expressive intervention but highest engineering cost.

## Key Entities

- **[[Shaojie Bai]]** — primary architect of DEQ + Jacobian-regularization recipes. Papers directly replace V2/V3/V4 detach with principled alternatives.
- **[[J. Zico Kolter]]** — PI of the DEQ program, co-author on all key stability-theory-for-neural-nets papers relevant here.
- **[[Jeffrey Pennington]]** — foundational dynamical-isometry theory; backs spectral-constraint interventions.

## Contradictions

**Hard orthogonality: beneficial (Cisse 2017) vs harmful (Vorontsov 2017).** [[Parseval Networks]] reports Parseval (all $\sigma_i = 1$) matches SOTA accuracy on CIFAR while being more robust. [[Orthogonal Recurrent Networks]] reports hard orthogonality hurts RNN expressivity; soft margin is better. **Resolution:** domain-specific. CNNs on CIFAR are information-rich; RNN long-dependency tasks are information-bottlenecked. For our case (M=8 steps, reasoning task, Qwen3 base): try soft spectral margin first ($m \in \{0.01, 0.05, 0.1\}$), fall back to exact Parseval only if margin doesn't suffice.

**DEQ compute vs Transformer compute.** [[Deep Equilibrium Models]] reports 5x compute penalty to match Transformer-XL on WikiText-103. Newer work (IIET, TorchDEQ) closes this somewhat. **Resolution:** DEQ is not yet a practical drop-in replacement for LLM training at 4B scale; Jacobian regularization applied to a truncated M-step rollout is the current cost-effective compromise.

**Noise-as-regularization: helpful (Lim 2021) vs mode-collapse-inducing (common training wisdom).** Adding too much noise during training kills content ([[Stochastic Soft Thinking]] exploration-exploitation result). **Resolution:** scheduled noise — start high ($\sigma \sim 0.3$), anneal to near-zero. This matches what works for [[Multiplex Thinking]].

## Open Questions (next autoresearch pass)

1. **How do attention blocks' effective Jacobians relate to underlying weight spectra?** Spectral regularization targeting $W_Q, W_K, W_V, W_O$ individually is easy; targeting the composite block Jacobian $\partial \text{Attn} / \partial z$ is less explored. A second-pass autoresearch on "attention Jacobian analysis 2024-2025" would fill this.

2. **What is the scaling law for $\rho(J_f)$ in recurrent-depth models?** Huginn / Ouro / [[Mixture of Recursions]] all have reported instability at large iteration counts. Is there empirical data on how $\rho$ drifts with depth and model scale? A second pass on "recurrent-depth Jacobian dynamics" could resolve.

3. **Does implicit-function-theorem gradient help with discrete-step-count rollouts (not true DEQ)?** Our M-step rollout is not a solved equilibrium. Is there a "partial IFT" variant that's less compute-heavy than full DEQ but more principled than V2 detach? Pritt and Kolter's "Phantom Gradients" (follow-up to DEQ) hints at this; a second pass would verify.

4. **How does Lyapunov-auxiliary loss interact with teacher forcing?** If we add $\mathcal{L}_{\text{lyap}}$, does it fight or complement the cross-entropy loss pulling latents toward vocab-space targets (SIM-CoT style)? Untested.

5. **F6 at σ=0.5 — is this already past the linearization regime?** Our stability theory (Jacobian-based) works in the small-noise limit. σ=0.5 may be past that regime. Do we need the full Lyapunov machinery rather than Jacobian regularization alone?

6. **Parseval on attention's output projection vs QKV projections — which matters?** Empirical. Would need a dedicated ablation.

## Sources

- [[Deep Equilibrium Models]] — Bai, Kolter, Koltun 2019 (NeurIPS spotlight) — DEQ framework.
- [[Stabilizing Equilibrium Models by Jacobian Regularization]] — Bai, Koltun, Kolter 2021 (ICML) — Jacobian-reg for DEQ stability.
- [[Resurrecting the Sigmoid Dynamical Isometry]] — Pennington, Schoenholz, Ganguli 2017 (NeurIPS) — dynamical isometry theory.
- [[Parseval Networks]] — Cisse, Bojanowski, Grave, Dauphin, Usunier 2017 (ICML) — Parseval tight frame constraint.
- [[Orthogonal Recurrent Networks]] — Vorontsov, Trabelsi, Kadoury, Pal 2017 (ICML) — spectral margin parameterization.
- [[Noisy Recurrent Neural Networks]] — Lim, Erichson, Hodgkinson, Mahoney 2021 (NeurIPS) — noise ≡ Jacobian regularization.
- [[Robust Learning with Jacobian Regularization]] — Hoffman, Roberts, Yaida 2019 — margin = 1/Lipschitz theorem.
- [[Stability and Generalization in Looped Transformers]] — Labovich 2026 (prior ingest) — reachability / input-dependence / geometry axes.
