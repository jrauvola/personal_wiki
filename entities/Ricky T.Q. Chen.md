---
type: entity
entity_type: person
title: "Ricky T. Q. Chen"
role: "First author, Neural Ordinary Differential Equations (NeurIPS 2018 Best Paper). Originator of adjoint-sensitivity training for continuous-depth networks."
first_mentioned: "[[Neural ODEs]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/architecture
  - affiliation/meta-fair
  - affiliation/u-toronto
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Neural ODEs is the taxonomic root of continuous-depth latent computation — the conceptual alternative to discrete Universal Transformers and the limiting case of Deep Equilibrium Models. Required genealogy node."
  - slug: "branch-a"
    relevance: reference
    why: "Continuous-depth scaling is orthogonal to discrete scaling but is a reference point for 'scale compute, not parameters' narratives."
  - slug: "branch-b"
    relevance: secondary
    why: "Adjoint sensitivity method is the conceptual ancestor of DEQ's IFT backward pass and belongs in the same O(1)-memory-gradient family as V2 detach."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
  - slug: "branch-d"
    relevance: not-applicable
    why: "CPF/fusion axis unrelated."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Neural ODEs]]"
  - "[[Deep Equilibrium Models]]"
  - "[[David Duvenaud]]"
sources:
  - "[[Neural ODEs]]"
---

# Ricky T. Q. Chen

## Position
Research scientist at Meta FAIR / Facebook AI Research (from ~2020). Previously PhD at University of Toronto / Vector Institute with David Duvenaud (co-advisor Roger Grosse).

## Core contribution
First author of Neural Ordinary Differential Equations (Chen, Rubanova, Bettencourt, Duvenaud; arXiv:1806.07366, NeurIPS 2018 Best Paper). Introduces continuous-depth neural networks by parameterizing the derivative $dh/dt = f(h, t; \theta)$ with a neural net, evaluated via off-the-shelf ODE solvers. The adjoint sensitivity method enables O(1) memory backpropagation — the gradient is a second ODE integrated backwards in time, never storing forward activations. Also introduces Continuous Normalizing Flows and continuous-time latent-variable models for irregularly sampled time series. Maintainer of the canonical PyTorch library `torchdiffeq`.

## Why relevant to this project

Neural ODEs establishes three patterns that surface (sometimes implicitly) in every modern recurrent-depth latent reasoner:

1. **Integrate a learned vector field.** The Universal Transformer / Ouro / HRM / Mixture-of-Recursions pattern of "apply block T times" is the Euler discretization of a Neural ODE with step size 1.
2. **O(1) memory gradient is available from day one.** Both the adjoint method and DEQ's implicit differentiation decouple the gradient chain from forward-pass depth. CODI's M-step BPTT is the baseline the field has *not* yet upgraded from.
3. **Adaptive compute = adaptive solver.** The continuous-depth analogue of ACT / PonderNet is "let the solver take smaller steps where the trajectory is stiff." This is an elegant direction that latent-reasoning LLMs have not explored.

## See also
- [[Neural ODEs]] — canonical source page.
- [[Deep Equilibrium Models]] — fixed-point specialization (DEQ = NODE at $t \to \infty$ if the dynamics are stable).
- [[Universal Transformers]] — discrete shared-block sibling.
