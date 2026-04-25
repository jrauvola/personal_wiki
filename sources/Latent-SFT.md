---
type: source
title: "Latent-SFT — LLM Latent Reasoning as Chain of Superposition"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/stochastic-latent
  - domain/anti-collapse
  - type/source
  - method/gumbel-softmax
status: read
source_type: paper
arxiv_id: "2510.15522"
venue: "arXiv"
date_published: 2025-10-17
authors:
  - "Jingcheng Deng"
  - "Liang Pang"
  - "Zihao Wei"
  - "Shicheng Xu"
  - "Zenghao Duan"
  - "Kun Xu"
  - "Yang Song"
  - "Huawei Shen"
  - "Xueqi Cheng"
url: "https://arxiv.org/abs/2510.15522"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Latent reasoning should function as a superposition of multiple reasoning paths rather than a compressed single-path representation."
  - "Latent-Vocab token-level constraint anchors hidden states to vocabulary manifold, addressing distributional misalignment between latent states and input embedding space."
  - "Induction-Supervision Masking constructs semantically compact reasoning chains, resolving ambiguous chain definitions."
  - "Stochastic Gumbel-Softmax optimization yields diverse reasoning trajectories rather than collapsing to a single path."
  - "Latent-SFT outperforms explicit SFT across six mathematical benchmarks (GSM8K, AIME24, +4 others) with 2.7× to 5.5× reduction in reasoning length."
related:
  - "[[CoLaR]]"
  - "[[COCONUT]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[SIM-CoT]]"
  - "[[Feature Collapse]]"
  - "[[Context-Prediction-Fusion]]"
sources:
  - "[[.raw/papers/2510.15522-latent-sft-superposition]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Latent-Vocab constraint is functionally equivalent to LT-Tuning's CPF vocabulary anchor; superposition framing provides a second independent implementation of the same anti-collapse mechanism."
  - slug: "branch-a"
    relevance: secondary
    why: "2.7-5.5× reasoning length reduction at accuracy gain is a strong scaling-relevant datapoint."
  - slug: "branch-b"
    relevance: reference
    why: "Gumbel-Softmax is orthogonal to detach strategies."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Latent-Vocab ≡ CPF independent confirmation is an important writeup citation, and Gumbel-Softmax-for-SFT is a useful secondary recipe, but superposition framing is already primary-anchored by [[Reasoning by Superposition]]; reclassified secondary to keep signal density."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Latent-SFT — LLM Latent Reasoning as Chain of Superposition

Deng, Pang, Wei, Xu, Duan, K. Xu, Song, Shen, Cheng — [arXiv:2510.15522](https://arxiv.org/abs/2510.15522) (2025-10-17, revised 2026-01-30).

## Core thesis

Latent reasoning collapse has two causes: (1) **distributional misalignment** — hidden states drift from the input embedding space, (2) **ambiguous chain definitions** — a single continuous vector cannot cleanly encode multi-step discrete reasoning. Latent-SFT fixes both with a three-level framework (token, chain, learning) and reframes the output of a latent step as a **superposition of multiple discrete reasoning paths** rather than a compressed single path.

## Method

### Three-level framework

| Level | Mechanism | Fixes |
|---|---|---|
| Token | **Latent-Vocab**: constrain hidden states to vocabulary manifold | Distributional misalignment |
| Chain | **Induction-Supervision Masking**: semantically compact chains | Ambiguous chain definitions |
| Learning | **Stochastic Gumbel-Softmax optimization** | Single-path collapse |

### Latent-Vocab ↔ CPF

Latent-Vocab is essentially the same mechanism as LT-Tuning's Context-Prediction-Fusion: anchor the hidden state to the discrete vocabulary manifold by projecting through or fusing with the output-embedding matrix. Independently derived, confirming the anti-collapse mechanism is fundamental.

### Superposition interpretation

Each latent state is a probability distribution over discrete reasoning paths. Gumbel-Softmax samples a path per trajectory. At inference, multiple trajectories sampled and aggregated (paper doesn't specify aggregation — likely self-consistency voting).

## Results

| Metric | Latent-SFT | Explicit SFT |
|---|---|---|
| GSM8K / AIME24 / +4 math benchmarks | outperforms | baseline |
| Reasoning length reduction | 2.7× – 5.5× | 1× |

Analysis confirms captured trajectories are diverse, not collapsed onto one path.

## Relevance to our project

- **Primary for branch-d.** Latent-Vocab ≈ CPF confirms the anti-collapse mechanism is load-bearing across independent groups. Gumbel-Softmax gives a second implementation path if CPF-on-CODI hits blockers.
- **Primary for spar-latent-reasoning.** Superposition framing is a clean theoretical lens for the writeup — complements CoLaR's diverse-trajectory claim with a formal mechanism.

## Citation links to chase

- Upstream: [[COCONUT]], [[CoLaR]]
- Sibling Gumbel-Softmax latent work: LEPO (2604.17892), Stochastic Soft Thinking (2508.03440)
- Independent CPF-equivalent: [[Latent Thoughts Tuning]] (Latent-Vocab ≡ CPF anchor).

## Artifacts

- **Paper:** [arXiv:2510.15522](https://arxiv.org/abs/2510.15522)
- **Code:** none released at crawl time.
- **Raw source:** [[.raw/papers/2510.15522-latent-sft-superposition]]
