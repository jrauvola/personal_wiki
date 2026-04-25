---
type: entity
entity_type: person
title: "Shaojie Bai"
role: "First author, Deep Equilibrium Models; first author, Stabilizing DEQ by Jacobian Regularization"
first_mentioned: "[[Deep Equilibrium Models]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - entity
  - researcher
  - stability-theory
  - affiliation/CMU
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Primary architect of Deep Equilibrium Models — the most relevant research program for stabilizing recurrent latent reasoning. All Bai papers directly relevant to our routing-lock and basin-width problems."
  - slug: "branch-b"
    relevance: primary
    why: "DEQ + Jacobian regularization directly replaces V2/V3/V4 detach interventions with principled fixed-point alternative. Bai's work is the engineering recipe."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[J. Zico Kolter]]"
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
  - "[[Deep Equilibrium Model (DEQ)]]"
sources:
  - "[[Deep Equilibrium Models]]"
  - "[[Stabilizing Equilibrium Models by Jacobian Regularization]]"
---

# Shaojie Bai

## Position
Researcher at CMU (PhD with J. Zico Kolter, subsequent academic appointments). Also collaborator with Vladlen Koltun.

## Core contribution
Invented the Deep Equilibrium Model (DEQ) framework ([[Deep Equilibrium Models]], NeurIPS 2019 spotlight): neural networks defined by a fixed-point equation rather than a stack of layers, trained via implicit differentiation. Follow-up: Jacobian regularization as a first-class stability objective for DEQ training ([[Stabilizing Equilibrium Models by Jacobian Regularization]], ICML 2021).

## Cited in this vault
- [[Deep Equilibrium Models]] (first author)
- [[Stabilizing Equilibrium Models by Jacobian Regularization]] (first author)

## Why relevant to us
Our M-step latent rollout in CODI is a crude truncated DEQ. Bai's work — especially the Jacobian regularization paper — gives us the recipe for making the rollout stable as a fixed-point iteration rather than hoping BPTT through M steps doesn't blow up. The implicit-differentiation machinery also gives us a principled alternative to V2/V3/V4 detach. Bai's body of work is the single largest body of actionable stability-theory relevant to Branch B.

## See also
- [[J. Zico Kolter]] — longtime collaborator, co-author on both DEQ papers.
- [[Deep Equilibrium Model (DEQ)]] — the concept page.
- [[Jacobian Constraint]] — the concept page for Bai's 2021 contribution.
