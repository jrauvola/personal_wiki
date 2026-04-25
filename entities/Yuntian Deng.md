---
type: entity
entity_type: person
title: "Yuntian Deng"
role: "First author, Implicit Chain of Thought Reasoning via Knowledge Distillation (2023); first author, Stepwise Internalization (2024). Direct predecessor work to COCONUT."
first_mentioned: "[[Implicit CoT via Knowledge Distillation]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/implicit-reasoning
  - affiliation/harvard
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Deng's 2023 iCoT-KD and 2024 Stepwise Internalization are the direct predecessors to both COCONUT and CODI — canonical for the 'compress CoT into hidden states' framing."
  - slug: "branch-a"
    relevance: reference
    why: "GPT-2 baseline results relevant as historical pre-Qwen data point."
  - slug: "branch-b"
    relevance: reference
    why: "Stepwise Internalization's removal schedule is a precursor to COCONUT's curriculum, orthogonal to detach axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology unrelated."
  - slug: "branch-d"
    relevance: secondary
    why: "iCoT-KD is a direct-supervision precursor to the LT-Tuning / KaVa distillation family; worth citing as historical root of the decoder-distillation axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
sources:
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
---

# Yuntian Deng

## Position
Assistant professor at the University of Waterloo (from 2024); prior postdoc with Alexander Rush at Harvard and PhD at Harvard with Stuart Shieber. Co-lead author with Stuart Shieber and Yejin Choi on the Implicit CoT research program at Microsoft Research.

## Core contributions

- **Implicit Chain of Thought Reasoning via Knowledge Distillation, 2023** ([[Implicit CoT via Knowledge Distillation]], arXiv:2311.01460). First paper to explicitly distill CoT reasoning into hidden states ("vertical reasoning across layers") rather than into token sequences. Teacher model trained on explicit CoT; emulator student reads teacher's hidden states layer-by-layer and learns to reproduce the final answer without emitting CoT tokens. Uses GPT-2 Small.

- **Stepwise Internalization / From Explicit CoT to Implicit CoT, 2024** ([[Stepwise Internalization]], arXiv:2405.14838). Simpler single-model variant: starts from explicit CoT training, gradually removes intermediate tokens (Δ=8 per epoch for multiplication, Δ=1 for GSM8K). Stability requires "removal smoothing" (random offsets) + optimizer reset on second-moment stats. Achieves 99% accuracy on 9×9 multiplication with GPT-2 Small; >50% on GSM8K with Mistral 7B.

## Why relevant to this project

The Deng research program is *the* direct predecessor to both [[COCONUT]] (curriculum-based replacement) and [[CODI]] (single-stage distillation). Deng's two papers correspond almost exactly to the two axes that later define the COCONUT/CODI fork:

- **iCoT-KD (2023)** = hidden-state distillation. Foreshadows CODI's self-distillation.
- **Stepwise Internalization (2024)** = curriculum-based CoT removal. Foreshadows COCONUT's stage-k truncation.

Both 2023 and 2024 methods feed **no continuous thoughts back as input embeddings** — the key innovation introduced by COCONUT that distinguishes it from Deng's lineage.

## See also
- [[Implicit CoT via Knowledge Distillation]] — 2023 source page.
- [[Stepwise Internalization]] — 2024 source page.
- [[COCONUT]] — 2024 Meta paper that extends this line with continuous-thought feedback.
