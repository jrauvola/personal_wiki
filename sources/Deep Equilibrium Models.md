---
type: source
title: "Deep Equilibrium Models"
source_type: paper
arxiv_id: "1909.01377"
venue: "NeurIPS 2019"
date_published: 2019-09-03
authors:
  - "Shaojie Bai"
  - "J. Zico Kolter"
  - "Vladlen Koltun"
url: "https://arxiv.org/abs/1909.01377"
code_repo: "https://github.com/locuslab/deq"
has_weights: true
status: read
confidence: high
key_claims:
  - "A DEQ directly finds the fixed point z* = f_theta(z*, x) of a single parameterized layer rather than stacking L explicit layers."
  - "Backward pass is computed by implicit differentiation through the equilibrium, eliminating the need to store intermediate activations — training memory is O(1) in effective depth."
  - "Forward pass is solved by a root-finding routine (Broyden / Anderson acceleration) rather than L explicit forward passes."
  - "DEQ matches or beats Transformer-XL and trellis networks on WikiText-103 with up to 88% memory reduction and comparable compute."
  - "The fixed-point formulation makes the trained network's stability directly characterized by the Jacobian J_f at the equilibrium point — exposing stability as a first-class training concern (follow-up work)."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "DEQ formalism is the cleanest existing framework for recurrent/iterative latent reasoning. North-star latent-reasoning models that iterate a shared block over M steps sit inside the DEQ family; implicit differentiation breaks the BPTT / detach tradeoffs that define Branch B."
  - slug: "branch-b"
    relevance: primary
    why: "Implicit differentiation is a principled alternative to V2/V3/V4 detach ablations — gradients come from the fixed-point condition, not from BPTT through M latent steps. Addresses exactly the training-instability problem the detach branch is navigating."
  - slug: "branch-d"
    relevance: secondary
    why: "CPF injects context at each latent step (non-trivial input map), which is a 'recall-style' fixed-point system in DEQ terms; gives formal scaffold for why CPF can improve stability."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling narrative for recurrent latent reasoning cites DEQ as the memory-efficient training regime."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/theory
  - domain/architecture
  - family/equilibrium
  - stability-theory
related:
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[TorchDEQ]]"
  - "[[Stability and Generalization in Looped Transformers]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
  - "[[Fixed-Point Iteration]]"
sources: []
---

# Deep Equilibrium Models (Bai, Kolter, Koltun 2019)

## TL;DR
A DEQ replaces an L-layer feedforward stack with the **fixed-point equation** $z^\star = f_\theta(z^\star, x)$, trained via implicit differentiation. Training memory is O(1) in effective depth — gradients at equilibrium come from the implicit-function theorem rather than BPTT through L layers. On WikiText-103, DEQ matches or beats Transformer-XL with 88% less training memory.

## Why this matters to our project

CODI-at-4B rolls out M latent steps and backprops through all of them (with V2/V3/V4 controlling how/where gradients flow). The F1-F6 test battery shows this training regime produces **routing-lock** (F3 template attractor) and **narrow basin** (F6 σ=0.5 collapses to <3%) — classic signatures of an under-constrained iterative map with no stability objective. DEQ is the principled alternative:

1. **Implicit gradients replace BPTT chain.** For latent step function $f_\theta$, the DEQ gradient is
$$\frac{\partial \ell}{\partial \theta} = -\frac{\partial \ell}{\partial z^\star}\left(I - \frac{\partial f}{\partial z^\star}\right)^{-1}\frac{\partial f}{\partial \theta}$$
so the chain of M BPTT Jacobians never accumulates. Whatever is killing gradient signal through V2 detach could simply... not be a gradient path at all.

2. **Fixed-point as an explicit training target.** The model must *converge* to a solution of $z^\star = f(z^\star, x)$. This is a much stronger requirement than "the M-th latent happens to help the decoder" and directly forbids the template-attractor degeneracy: the fixed point depends on $x$, so it cannot be a constant key.

3. **Structural necessity of input re-injection.** [[Stability and Generalization in Looped Transformers]] proves: looped networks without recall (no input re-injection) have countable fixed points → cannot be input-dependent. CODI's latent rollout feeds $x$ only at step 0; CPF (and SIM-CoT) inject context at each step = recall. DEQ theory explains *why* this matters at the level of expressivity.

## Core mechanism

Forward pass — instead of computing $z_{L} = f^{(L)} \circ ... \circ f^{(1)}(x)$:
1. Pick initial $z_0$.
2. Run root-finder (Broyden / Anderson) until $\|z_{k+1} - z_k\| < \epsilon$.
3. Return $z^\star$.

Backward pass — implicit differentiation via the implicit function theorem:
- The derivative of $z^\star$ w.r.t. $\theta$ only requires solving a *linear* system in $J_f = \partial f / \partial z^\star$.
- No activations to store; memory is constant in effective depth.

## Limits & caveats
- **Convergence is not free.** Without stabilization, DEQ iteration counts grow during training and can diverge ([[Stabilizing Equilibrium Models by Jacobian Regularization]]).
- **Not yet scaled for LLMs.** TorchDEQ (2023) is the largest library but no >1B LLM DEQ exists. Recent IIET (2025) uses implicit-Euler transformer blocks with stability guarantees and competitive LM perplexity.
- **Expressivity lower than explicit depth** — a single fixed-point has countable modes; [[Mixture of Recursions]] family and Huginn handle this by iterating blocks rather than solving equilibria.

## For Branch-B / V2 detach
The key insight: V2's `detach_lat` at step M is a *crude, structural* form of implicit differentiation — it cuts the gradient chain. DEQ provides the principled version: cut the chain *and replace it with the implicit-function-theorem gradient*. This could be the "composable synthesis" the north-star is looking for.
