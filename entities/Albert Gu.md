---
type: entity
entity_type: person
title: "Albert Gu"
role: "Lead author of S4 (2022) and Mamba (2023); architect of the modern state-space-model research program"
first_mentioned: "[[Mamba]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/state-space-model
  - affiliation/cmu
  - affiliation/cartesia
status: developing
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Architect of the SSM lineage (HiPPO → S4 → Mamba) - the only modern architecture family that has scaled gated-recurrent ideas to LLM-class parameter counts. Direct underwriting of the LSTM analogy in Latent Scratchpad."
  - slug: "branch-d"
    relevance: primary
    why: "Mamba's selection mechanism is the closest published analog to W3.5 Latent Scratchpad's emission gate. Theorem 1 in the Mamba paper makes the LSTM-equivalence explicit."
  - slug: "branch-a"
    relevance: secondary
    why: "Mamba is the leading non-attention architecture for Qwen3-scale work."
  - slug: "branch-b"
    relevance: reference
    why: "Selective state-update is conceptually adjacent to detach policy."
  - slug: "branch-c"
    relevance: reference
    why: "Architectural probe transfer is non-trivial."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Mamba]]"
  - "[[Selective State-Space Model]]"
sources:
  - "[[Mamba]]"
---

# Albert Gu

## Position
Assistant Professor at CMU (Machine Learning Department); co-founder and Chief Scientist at Cartesia. PhD from Stanford (advised by Christopher Ré).

## Core contributions

- **HiPPO, 2020** (NeurIPS, with Dao et al.). Theory of optimal continuous-time function memorization — derives the A matrix structure that becomes the foundation of S4.

- **S4 (Structured State Space), 2022** (ICLR, with Goel, Re). First state-space model to be competitive with transformers on long-range arena. Diagonal-plus-low-rank A matrix factorization makes the SSM trainable and efficient.

- **Mamba, 2023** ([[Mamba]], with Tri Dao). Adds selection mechanism (input-dependent A, B, C, Δ) and hardware-aware parallel scan. Theorem 1 explicitly identifies discretization as the foundation of LSTM-style gating.

- **Mamba-2, 2024** (with Tri Dao). State-space duality framework; further improves SSM-transformer interop.

- **HiPPO / S4 / Mamba lineage** has produced ~30 papers at this point and constitutes the dominant non-attention architecture program.

## Co-author note

Co-author Tri Dao (Princeton + Together AI) is the FlashAttention author and the kernel-engineering specialist behind Mamba's hardware-aware parallel scan. Mamba's empirical wall-clock competitiveness with transformers depends on Dao's selective-scan kernel (analogous to FlashAttention for transformers). For the W3.5 LLM-scale grounding, Mamba and FlashAttention are both load-bearing infrastructure.

## Why relevant to this project

Gu's research program is the **strongest single thread of evidence** that input-dependent gating works at LLM scale. Mamba's 2.8B-parameter validation, combined with Theorem 1's explicit equivalence to LSTM gating, **directly underwrites the LSTM analogy** in the Latent Scratchpad page.

For W3.5: Mamba's `s_Δ(x) = Broadcast_D(Linear_1(x))` followed by softplus is the recommended parametrization for the emission gate (a learned input-dependent positive scalar that broadcasts to a Bernoulli decision).

## See also

- [[Mamba]] — primary source paper.
- [[Selective State-Space Model]] — concept page for Gu's selection mechanism.
