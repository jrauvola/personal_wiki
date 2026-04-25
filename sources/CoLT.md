---
type: source
title: "CoLT — Reasoning with Chain of Latent Tool Calls"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/auxiliary-decoder
  - method/tool-calling
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/2602.04246-colt]]"
source_type: paper
arxiv_id: "2602.04246"
venue: "arXiv"
date_published: 2026-02-04
authors:
  - "Fangwei Zhu"
  - "Zhifang Sui"
url: "https://arxiv.org/abs/2602.04246"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "CoLT implements latent reasoning as 'tool calls': main model reasons in explicit token space and emits seed tokens; a smaller external model takes hidden states of seed tokens and unpacks them back to a full reasoning step."
  - "Existing latent reasoning methods generally require model structure augmentation and exhaustive training, limiting their broader applicability — CoLT avoids both."
  - "CoLT achieves higher accuracy and shorter reasoning length than baseline latent models on four mathematical datasets."
  - "CoLT is compatible with reinforcement learning algorithms and different decoder structures."
projects:
  - slug: "branch-a"
    relevance: reference
    why: "Tool-calling latent formulation is orthogonal to Qwen3 scaling architecture-dependence question."
  - slug: "branch-b"
    relevance: reference
    why: "Method replaces latent-reasoning mechanism entirely rather than addressing detach/fp32 gradient-stability axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No bearing on Qwen3 probe methodology debugging."
  - slug: "branch-d"
    relevance: secondary
    why: "Inverts SIM-CoT's auxiliary-decoder-at-training-only design into auxiliary-decoder-at-inference (tool-call unpacker). Relevant contrast point for LT-Tuning CPF framing as anchor-to-vocab-space. Not directly portable as a recipe — main model still reasons in token space, which defeats latent-computation goals we care about."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Notable alternative latent-reasoning paradigm (tool-call decomposition) for SPAR writeup taxonomy. Marked isInfluential=true in SIM-CoT citation graph — a cited-by signal."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# CoLT — Reasoning with Chain of Latent Tool Calls

## TL;DR

CoLT reframes latent reasoning as external tool invocation: the main LLM reasons in explicit token space and emits **seed tokens**; when a "latent tool call" triggers, a smaller external decoder receives the hidden states of those seed tokens and **unpacks** them back into a full reasoning step. The main model's token-space reasoning ability is preserved (no structural modification, no exhaustive retraining), and the framework is compatible with RL algorithms and different decoder architectures.

## Method

- **Seed tokens** — short, compressed tokens emitted by the main LLM that encode information from a reasoning step.
- **Latent tool call trigger** — a marker causes an external (smaller) model to read the hidden states of those seed tokens as input.
- **Unpacker** — the external model produces the full reasoning step text from the seed-token hidden states.
- Main LLM's reasoning remains in explicit token space throughout; the latent behavior lives in the unpacking subroutine rather than in the primary reasoning trajectory.

Inverts the SIM-CoT training-only auxiliary-decoder pattern into an **inference-time** external decoder.

## Recipe

- Training-recipe numerics not available in abstract; PDF required for reproduction details.
- Compatible with RL fine-tuning (claimed).
- Decoder-agnostic (claimed).

## Results

- Four mathematical datasets (names not in abstract); higher accuracy and shorter reasoning length than baseline latent models.
- No public code in abstract.

## Relevance

- **SIM-CoT ↔ CoLT contrast**: SIM-CoT uses aux decoder to supervise implicit latents during training and discards at inference. CoLT keeps the aux decoder at inference as a tool-call target. Interesting axis for the SPAR writeup when discussing "where does the explicit supervision signal live — training or inference."
- For Branch D (LT-Tuning CPF): reinforces that CPF's niche is anchoring a **single-model** latent trajectory to vocab space, vs CoLT's multi-model decomposition.

## Citations

- Seed arXiv listing only; no full body fetched.
- Discovered via SIM-CoT downstream citation graph (isInfluential=true).
