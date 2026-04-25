---
type: entity
entity_type: person
title: "J. Zico Kolter"
role: "Co-author, Deep Equilibrium Models; advisor on DEQ research program"
first_mentioned: "[[Deep Equilibrium Models]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - entity
  - researcher
  - stability-theory
  - affiliation/CMU
  - affiliation/Bosch
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Academic lead of the DEQ research program. Kolter's lab at CMU consistently produces the most actionable stability-theory-for-neural-nets work relevant to recurrent latent reasoning."
  - slug: "branch-b"
    relevance: primary
    why: "Primary source of both DEQ framework and Jacobian-regularization recipes that directly address our M-step rollout stability concerns."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Shaojie Bai]]"
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[TorchDEQ]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
sources:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
---

# J. Zico Kolter

## Position
Professor at Carnegie Mellon University; Chief Scientist at Bosch Center for AI. Anthropic board member.

## Core contributions (relevant to us)
- **Deep Equilibrium Models** ([[Deep Equilibrium Models]], NeurIPS 2019 with Shaojie Bai, Vladlen Koltun) — neural networks as fixed-point equations.
- **DEQ stabilization via Jacobian regularization** ([[Stabilizing Equilibrium Models by Jacobian Regularization]], ICML 2021) — canonical recipe for making DEQ training robust.
- **TorchDEQ** (2023, with Zhengyang Geng) — the mature library for DEQ research.

Also: provable adversarial robustness (randomized smoothing), constraint-based learning, broader implicit-layer research.

## Cited in this vault
- [[Deep Equilibrium Models]] (co-author)
- [[Stabilizing Equilibrium Models by Jacobian Regularization]] (co-author)
- (TorchDEQ referenced in Deep Equilibrium Models; no standalone page yet.)

## Why relevant to us
The Kolter lab is the center of actionable stability-theory for deep nets that can be plugged into real ML systems. Every technique in the stability toolkit that we might want for CODI-as-DEQ (Jacobian reg, Broyden/Anderson root-finding, implicit differentiation in PyTorch) traces back to Kolter's lab. For Branch B synthesis (V2 detach + fixed-point structure), his recipes are the default starting point.

## See also
- [[Shaojie Bai]] — primary DEQ collaborator.
- [[Deep Equilibrium Model (DEQ)]] — concept page.
- [[Jacobian Constraint]] — the concept Kolter's 2021 paper operationalizes.
