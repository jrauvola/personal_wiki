---
type: entity
title: "Fan Yin"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
status: seed
related:
  - "[[Ouro]]"
  - "[[ByteDance Seed]]"
sources:
  - "[[Ouro]]"

entity_type: person
role: "First author, Ouro / LoopLM; wrote custom vLLM/SGLang PRs for LoopLM inference"
first_mentioned: "[[Ouro]]"

projects:
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "First author on Ouro — primary contact point for questions about checkpoint release, loop-aware inference infra, and RLVR failure modes."
  - slug: "branch-a"
    relevance: not-applicable
    why: "No direct overlap with Qwen3 scaling branch."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No direct overlap with detach-ablation branch."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No direct overlap with Qwen3 convergence debugging."
  - slug: "branch-d"
    relevance: not-applicable
    why: "Ouro architecture incompatible with LT-Tuning CPF."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Fan Yin

First author of [[Ouro]] (LoopLM). Affiliation inferred ByteDance Seed / academic collaborator (full affil not extracted in notes).

## Work relevant to this vault

- **Ouro / LoopLM** — pretrained-from-scratch looped language models, 1.4B / 2.6B + Thinking variants.
- **Custom vLLM / SGLang PRs** — loop-aware inference runtime for variable-depth execution paths (per paper, §RL attempts).

## Why tracked

Principal contact for:
- Exact HF checkpoint locations for Ouro base + Thinking releases.
- Custom rollout infra supporting dynamic depth (relevant to any RLVR-on-latent-reasoning attempt).
- Interpretability gap — the paper self-identifies a sparse interp section that our tuned-lens pipeline could directly fill.
