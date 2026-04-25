---
type: entity
title: "InternLM"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/organization
status: developing
entity_type: organization
role: "Hosts and releases SIM-CoT code and weights on GitHub and Hugging Face"
first_mentioned: "[[SIM-CoT]]"
related:
  - "[[SIM-CoT]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Source of SIM-CoT checkpoints that inform CPF fusion comparison."
  - slug: "branch-a"
    relevance: primary
    why: "Publisher of production-ready Llama 3.1 8B SIM-CoT weights central to Qwen3 scaling comparisons."
  - slug: "branch-b"
    relevance: reference
    why: "Source of strong-supervision baseline weights for detach ablation comparisons."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not involved in probe methodology debugging."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Major open-source contributor in the latent reasoning ecosystem."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# InternLM

GitHub and Hugging Face organization responsible for publishing SIM-CoT and associated latent reasoning checkpoints.

## Artifacts attributed

- Repo: [InternLM/SIM-CoT](https://github.com/InternLM/SIM-CoT)
- HF checkpoints:
  - `internlm/SIM_COT-GPT2-Coconut`
  - `internlm/SIM_COT-GPT2-CODI`
  - `internlm/SIM_COT-LLaMA3-CODI-1B`
  - `internlm/SIM_COT-LLaMA3-CODI-3B`
  - `internlm/SIM_COT-LLaMA3-CODI-8B`

## Sources referencing

- [[SIM-CoT]]
