---
type: source
title: "Neural Ordinary Differential Equations (Chen, Rubanova, Bettencourt, Duvenaud 2018)"
source_type: paper
arxiv_id: "1806.07366"
venue: "NeurIPS 2018 (Best Paper)"
date_published: 2018-06-19
authors:
  - "Ricky T. Q. Chen"
  - "Yulia Rubanova"
  - "Jesse Bettencourt"
  - "David K. Duvenaud"
url: "https://arxiv.org/abs/1806.07366"
code_repo: "https://github.com/rtqichen/torchdiffeq"
has_weights: false
status: read
confidence: high
key_claims:
  - "A Neural ODE replaces the discrete sequence of residual blocks h_{n+1} = h_n + f(h_n, θ) with a continuous-time ODE dh(t)/dt = f(h(t), t, θ); the output is obtained by integrating from t=0 to t=T with an off-the-shelf adaptive ODE solver."
  - "The adjoint sensitivity method backpropagates through an ODE solve in O(1) memory — the gradient is computed by integrating a second (augmented) ODE backwards in time, never storing intermediate forward-pass activations."
  - "Evaluation cost adapts to input difficulty: the solver takes more function evaluations where the trajectory is stiff and fewer where it is easy; this is continuous-depth analogue of ACT adaptive compute."
  - "Introduces Continuous Normalizing Flows: bypasses the discrete permutation/partition requirements of RealNVP-style normalizing flows because the change-of-variables formula for an ODE is tr(∂f/∂h) which is cheap regardless of f's structure."
  - "Continuous-time latent-variable models for irregularly sampled time series — latent dynamics z(t) = ODESolve(f, z_0, t) with a VAE encoder/decoder — the originating trick for 'latent state evolving in continuous time'."
  - "Won NeurIPS 2018 Best Paper Award; authored at University of Toronto / Vector Institute."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Taxonomic root of continuous-depth latent computation. Latent reasoning models that iterate a shared block M times sit between discrete Universal Transformers and continuous Neural ODEs; both are specializations of 'learn a vector field, integrate it.' Required genealogy node."
  - slug: "branch-a"
    relevance: reference
    why: "Continuous-depth scaling is a conceptual alternative to discrete-depth scaling; relevant framing context for the writeup."
  - slug: "branch-b"
    relevance: secondary
    why: "Adjoint-sensitivity method is the continuous analogue of DEQ's implicit differentiation and sits in the same 'O(1)-memory gradient' family as V2 detach — a principled alternative to CODI's M-step BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probing methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Orthogonal to CPF fusion axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/continuous-depth
  - method/adjoint-sensitivity
  - type/source
  - status/historical
related:
  - "[[Deep Equilibrium Models]]"
  - "[[Universal Transformers]]"
  - "[[Adaptive Computation Time]]"
  - "[[Ricky T.Q. Chen]]"
sources: []
---

# Neural Ordinary Differential Equations (Chen et al. 2018)

## TL;DR

Generalize ResNet's residual block $h_{n+1} = h_n + f(h_n)$ to a continuous-time ODE $\dot h(t) = f(h(t), t; \theta)$. Evaluate with any black-box ODE solver; backprop via the adjoint method in O(1) memory. NeurIPS 2018 Best Paper.

## Why this matters to our project

Neural ODEs is the **taxonomic bookend** to Universal Transformers on the "latent reasoning = iterated computation" axis:

| Axis | Discrete | Continuous |
|------|----------|-----------|
| Explicit depth | Stacked ResNet / Transformer | — |
| Shared-block recurrence | Universal Transformer, Ouro, HRM | Neural ODE |
| Fixed-point | (N/A) | Deep Equilibrium Model |

The three right-column entries are variants of "learn a vector field / iterator, evaluate it until some condition holds." Latent reasoning models (CODI, COCONUT, Huginn) sit in the **discrete shared-block** cell — but the math (O(1)-memory gradients via adjoint or IFT) has been available since 2018. The field mostly ignored it.

## Method

**Forward.** Given initial state $h(0) = x$, compute
$$
h(T) = h(0) + \int_0^T f(h(t), t; \theta)\,dt
$$
with an adaptive solver (Runge-Kutta, Dopri5, etc.). The solver chooses step sizes based on local error; harder inputs → more function evaluations.

**Backward (adjoint).** Define the adjoint $a(t) = \partial L / \partial h(t)$. Then
$$
\frac{da(t)}{dt} = -a(t)^\top \frac{\partial f}{\partial h},\qquad
\frac{dL}{d\theta} = -\int_T^0 a(t)^\top \frac{\partial f}{\partial \theta}\,dt
$$
Solve these two backward-in-time ODEs jointly; no forward activations need to be stored.

**Memory.** Forward: only $h(T)$ (and optionally a log for solver error estimation). Backward: a single augmented ODE. Memory cost is O(1) in effective depth — independent of the number of solver steps.

## Results

- **MNIST / CIFAR:** Neural ODE with comparable parameter count matches ResNet accuracy with 1/3 the memory footprint.
- **Continuous-time latent models:** outperform RNN-VAE on physical-simulation time-series (irregularly sampled) by handling irregular time gaps natively.
- **Continuous Normalizing Flows (CNF):** generative modeling with tractable likelihood; avoids RealNVP's forced partitioning.

## Relationship to other latent-reasoning precursors

- **Adaptive Computation Time** (Graves 2016): discrete variable-depth with halting head; Neural ODE's adaptive solver is the continuous version — both allocate more compute to harder inputs.
- **Deep Equilibrium Models** (Bai 2019): the DEQ fixed-point $z^\star = f(z^\star, x)$ is the $t \to \infty$ limit of a stable Neural ODE; IFT gradients are the DEQ analogue of the adjoint method.
- **Universal Transformers** (Dehghani 2019): discrete shared-block iteration; "Euler-discretize a Neural ODE with step size 1" → UT.

## Relevance to CODI / COCONUT contrast

Neural ODEs are **not** a latent-reasoning training block in themselves (the paper is about continuous models, not CoT compression). But as a conceptual anchor they enable the entire "iterate a learned vector field M times and backprop via IFT/adjoint" frame that CODI's V2 detach ablation is crudely approximating. A north-star latent reasoner that replaces CODI's M-step BPTT with either DEQ-style IFT or Neural-ODE-style adjoint gradients would fit naturally into this lineage — and likely be the first to actually use this machinery at LLM scale.

## Citation links to chase

- [[Deep Equilibrium Models]] (Bai 2019) — fixed-point specialization.
- [[Universal Transformers]] — discrete shared-block sibling.
- torchdiffeq — official PyTorch library (still maintained).
- FFJORD (2019) — follow-up on continuous normalizing flows.
