---
type: source
title: "LEAD — Latent Entropy-Aware Decoding for MLRMs"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/multimodal
  - type/source
  - method/inference-time
  - method/entropy-gated
status: read
source_type: paper
arxiv_id: "2603.13366"
venue: "arXiv"
date_published: 2026-03-09
authors:
  - "Zhongxing Xu"
  - "Zhonghua Wang"
  - "Zhe Qian"
  - "Dachuan Shi"
  - "Feilong Tang"
  - "Ming Hu"
  - "Shiyan Su"
  - "Xiaocheng Zou"
  - "Wei Feng"
  - "Dwarikanath Mahapatra"
  - "Yifan Peng"
  - "Mingquan Lin"
  - "Zongyuan Ge"
url: "https://arxiv.org/abs/2603.13366"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Transition words (e.g., because, however, and wait) are closely associated with hallucinations and tend to exhibit high-entropy states."
  - "Adequate contextual reasoning information can be directly extracted from the token probability distribution."
  - "Reliance on discrete textual inputs may drive the model toward sequential explicit reasoning, underutilizing dense contextual cues during high-entropy reasoning stages."
  - "The model employs probability-weighted continuous embeddings under high-entropy states and transitions back to discrete token embeddings as entropy decreases."
  - "LEAD effectively mitigates hallucinations across various MLRMs on multiple benchmarks."
related:
  - "[[SeLaR]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[Soft Thinking]]"
  - "[[Reasoning by Superposition]]"
sources:
  - "[[.raw/papers/2603.13366-lead]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Multimodal (not text-only) application of entropy-gated soft embedding — same mechanism as SeLaR but on MLRMs. Off-axis from CODI harness."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Multimodal reasoning; not Qwen3 text-only scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Inference-time only."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Transition-words-are-hallucinations finding is cute but narrow (multimodal hallucination); not central to the latent reasoning writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LEAD — Latent Entropy-Aware Decoding for MLRMs

Xu, Wang, Qian et al., [arXiv:2603.13366](https://arxiv.org/abs/2603.13366), Mar 2026.

## TL;DR

Entropy-gated soft-embedding decoding for **multimodal** reasoning models (MLRMs). Key observation: transition words (because, however, wait) are high-entropy states that correlate with hallucinations. Fix: at high-entropy steps, emit **probability-weighted continuous embeddings**; switch back to discrete when entropy drops. Plus **visual anchor injection** (prior-guided attention bias toward visual tokens). Training-free, plug-and-play. Mitigates hallucinations across various MLRMs on multiple benchmarks.

## Method

Same structural recipe as [[SeLaR]] (also 2026) applied to MLRMs:

### Entropy-aware mode switching

- High-entropy step → probability-weighted soft embedding (continuous).
- Low-entropy step → discrete token embedding.

### Visual anchor injection

Prior-guided attention-bias toward visual tokens during high-entropy states. Multimodal-specific; grounds uncertain reasoning in visual evidence.

### Training-free

Inference-time plug-and-play.

## Results

- Hallucination mitigation across various MLRMs on multiple benchmarks (specifics not enumerated in abstract).

## Relevance

- **Reference for all branches.** Multimodal-specific; off-axis from our text-only CODI/Qwen3 scope.
- For the SPAR writeup, useful only as an "entropy-gated soft embedding is a recurring recipe across modalities" data point.

## Citation links

- [[SeLaR]] — text-only twin; same entropy-gated recipe.
- [[Stochastic Soft Thinking]] — Greedy Pitfall motivation.
- [[Reasoning by Superposition]] — cited by LEAD as theoretical inspiration for multi-candidate semantics.

## Artifacts

- **Paper:** [arXiv:2603.13366](https://arxiv.org/abs/2603.13366)
- **Code:** none.
- **Raw source:** [[.raw/papers/2603.13366-lead]]
