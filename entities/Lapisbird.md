---
type: entity
title: "Lapisbird"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/entity
  - entity/organization
  - entity/hf-org
status: seed
entity_type: organization
role: "HF org hosting Adaptive Latent RL checkpoints"
first_mentioned: "[[Adaptive Latent RL]]"
related:
  - "[[Adaptive Latent RL]]"
  - "[[Alex Ning]]"
sources:
  - "[[Adaptive Latent RL]]"
projects: []
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Lapisbird (HuggingFace organization)

HuggingFace organization that hosts all released checkpoints for [[Adaptive Latent RL]]. Likely [[Alex Ning]]'s HF pseudonym — the GitHub repo `apning/adaptive-latent-reasoning` links to this org's models.

## Released models

- `Lapisbird/Llama-adaLR-model-latent-6-by-1`
- `Lapisbird/Llama-adaLR-model-latent-6-by-1_rl`
- `Lapisbird/Llama-adaLR-model-latent-6_rl`
- `Lapisbird/Llama-adaLR-model-cot_sft`
- `Lapisbird/Llama-adaLR-model-no_cot_sft`
- `Lapisbird/Llama-adaLR-appendix-model-codi[_intermediate]`
- `Lapisbird/Llama-adaLR-appendix-model-meaned[_intermediate|_codi]`

All are fine-tunes of `meta-llama/Llama-3.2-1B-Instruct` on `whynlp/gsm8k-aug`.
