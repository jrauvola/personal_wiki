---
type: concept
title: "Curriculum Distillation"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/concept
  - method/training
status: developing
complexity: intermediate
domain: curriculum
aliases:
  - "Multi-stage Curriculum"
  - "Progressive Text-to-Latent Replacement"
related:
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[SIM-CoT]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "LT-Tuning mandates a three-stage curriculum; understanding curriculum distillation is required for CPF-on-CODI."
  - slug: "branch-a"
    relevance: secondary
    why: "Curriculum stability is a component of scaling Qwen3 runs."
  - slug: "branch-b"
    relevance: secondary
    why: "Curriculum recipes affect detach/grad-stability behavior."
  - slug: "branch-c"
    relevance: reference
    why: "General method context."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Curriculum-based vs distillation-based vs fusion-based is a primary taxonomic axis of the writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Curriculum Distillation

The family of training recipes that transition a language model from explicit text CoT into a continuous latent reasoning mode via phased replacement of text with continuous vectors.

## Canonical design (COCONUT)

- **Stage 0** — SFT on complete explicit reasoning chains.
- **Subsequent stages** — progressively truncate explicit textual reasoning steps from training targets; insert recycled hidden states as continuous thoughts.
- **Expansion hyperparameter** — number of continuous vectors inserted per explicit step removed.
- **Anti-forgetting sampling** — uniform-probability interleaving of earlier-stage data into later optimization phases preserves the vocabulary mapping.

## Known pathologies

- **Destabilization in intermediate stages** — computationally expensive; prone to destabilization if intermediate stages lose their mapping to the final answer. This is the motivating critique that [[CODI]] addresses by collapsing the curriculum into a single-stage self-distillation recipe.
- **Weak supervision** — the continuous trajectory is only weakly anchored, leaving intermediate latent states unconstrained and vulnerable to feature collapse and shortcut mapping.

## Strong-supervision alternatives

- [[SIM-CoT]] — plug-and-play auxiliary decoder translates implicit tokens back to the reasoning vocabulary during training, anchoring each step.
- [[CODI]] — single-stage self-distillation with a terminal $L_1$ anchor; not a curriculum, but a distillation-family cousin.

## Cross-references

Sources that implement or critique curriculum distillation: [[COCONUT]], [[CODI]], [[SIM-CoT]].
