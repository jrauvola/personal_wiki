---
type: entity
entity_type: person
title: "Bo Peng"
role: "First author of RWKV (2023); founder of the RWKV open-source project"
first_mentioned: "[[RWKV]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/linear-attention
  - domain/rnn-revival
  - affiliation/independent
status: developing
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Lead architect of RWKV, the largest dense RNN ever trained (14B params). Second flagship validation - alongside Mamba - that LSTM-style gating mechanisms scale to LLM-class parameter counts."
  - slug: "branch-d"
    relevance: secondary
    why: "RWKV's σ(r_t) output gate at 14B is a direct analog of what Latent Scratchpad's emission gate has to do. Different placement (in-stream vs side-channel) but same gating mechanism family."
  - slug: "branch-a"
    relevance: secondary
    why: "Alternative to attention for Qwen3-scale; demonstrates RNN-like architectures can compete at scale."
  - slug: "branch-b"
    relevance: reference
    why: "Different recurrence pattern."
  - slug: "branch-c"
    relevance: reference
    why: "Architecture difference complicates direct probe transfer."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[RWKV]]"
  - "[[Selective State-Space Model]]"
sources:
  - "[[RWKV]]"
---

# Bo Peng

## Position
Independent researcher and open-source community founder. The RWKV project is largely community-driven and hosted on GitHub (`BlinkDL/RWKV-LM`), with a Discord community of contributors. EleutherAI and others have collaborated on the published RWKV papers.

## Core contributions

- **RWKV-1 through RWKV-6, 2021-2024** ([[RWKV]] is the v1-3 paper; subsequent versions extend it). Linear-attention RNN with explicit per-channel exponential time decay and sigmoid output gates. Designed for parallel training (transformer-style) and recurrent inference (RNN-style).

- **RWKV-LM open-source ecosystem.** Models from 169M to 14B params released on Hugging Face, all trained on the Pile. Largest dense RNN ever trained. Active community of fine-tuners and quantization implementations.

- **Q-RWKV, RWKV-fitness (community).** Evaluation harnesses and ablation studies driven by the community.

## Why relevant to this project

Peng's RWKV is **the empirical proof** (alongside Mamba) that **gated linear models scale**. The 14B RWKV is the largest published dense RNN, and its `σ(r_t) ⊙ wkv_t` output gate is a per-channel sigmoid gate operating at 14-billion-parameter scale.

This directly underwrites the LSTM analogy in [[Latent Scratchpad]]: gates are not artifacts of small-scale recurrent models from 1997; they survive scaling and remain the dominant mechanism in non-attention LLM architectures.

For W3.5: RWKV's depth-dependent time-decay initialization recipe `w_i = -5 + 8·(i/(d-1))^{0.7 + 1.3·l/(L-1)}` is a sophisticated init that the W3.5 emission-gate could borrow conceptually — early latent positions biased toward low emission, late positions biased toward higher emission.

## See also

- [[RWKV]] — primary source paper.
- [[Selective State-Space Model]] — sibling concept (RWKV and Mamba are kin).
