---
type: entity
title: "Alexia Jolicoeur-Martineau"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
status: mature
entity_type: person
role: "Research scientist, Samsung SAIL Montreal; first author of TRM (Tiny Recursive Model); formerly known for Relativistic GANs."
first_mentioned: "[[Tiny Recursive Model]]"
projects:
  - slug: spar-latent-reasoning
    relevance: secondary
    why: "TRM adjacent to latent-reasoning taxonomy; not a CODI/COCONUT variant but same problem space."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Tiny Recursive Model]]"
  - "[[Hierarchical Reasoning Model]]"
---

# Alexia Jolicoeur-Martineau

Research scientist at **Samsung SAIL Montreal** (Samsung AI Lab, formerly SAIT Montreal). Previously known for Relativistic GANs. Current research focus as of 2025: recursive reasoning with small networks.

## Known work relevant to this vault

- **Tiny Recursive Model (TRM)** — arXiv:2510.04871 (Oct 2025). 7M-param 2-layer network that beats DeepSeek R1 / o3-mini / Gemini 2.5 Pro on ARC-AGI with simpler recipe than HRM.
- Repo: [SamsungSAILMontreal/TinyRecursiveModels](https://github.com/SamsungSAILMontreal/TinyRecursiveModels)
- Twitter: [@jm_alexia](https://x.com/jm_alexia)

## Relevance to user's Latent Scratchpad proposal

**TRM does NOT have a scratchpad or discrete side-channel** — its latent z is purely internal. User's recollection of "Alexia tiny reasoning models doing something similar" is **accurate about the model existing**, but the architectural overlap is "recursive latent reasoning on tiny models" (adjacent to COCONUT/CODI), not "discrete scratchpad side-channel." The closest-prior-art credit goes elsewhere (Latent Sketchpad, Token Assorted, HRPO).
