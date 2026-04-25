---
type: source
title: "BFS-PO — Best-First Search for Large Reasoning Models"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/reasoning
  - type/source
  - method/reinforcement-learning
  - method/search
status: read
source_type: paper
arxiv_id: "2602.14917"
venue: "arXiv"
date_published: 2026-02-16
authors:
  - "Fiorenzo Parascandolo"
  - "Wenhui Tan"
  - "Enver Sangineto"
  - "Ruihua Song"
  - "Rita Cucchiara"
url: "https://arxiv.org/abs/2602.14917"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Overthinking is often exacerbated by Reinforcement Learning (RL) algorithms such as GRPO/DAPO."
  - "BFS-PO looks for the shortest correct answer using a backtracking mechanism based on maximum entropy nodes."
  - "By generating progressively shorter responses during training, BFS-PO learns to produce concise reasoning chains."
  - "BFS-PO can simultaneously increase the LRM accuracy and shorten its answers."
related:
  - "[[Latent Exploration Decoding]]"
  - "[[Stochastic Soft Thinking]]"
sources:
  - "[[.raw/papers/2602.14917-bfs-po]]"
projects:
  - slug: "branch-d"
    relevance: not-applicable
    why: "Discrete RL search — no latent reasoning component."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Discrete reasoning only."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not relevant to detach/BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Adjacent entropy-based RL work — max-entropy nodes as backtracking anchors is parallel to LED's max-entropy depth config. Not a central writeup citation but same author cluster (Parascandolo, Tan, Sangineto, Song, Cucchiara) as LED."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# BFS-PO — Best-First Search for Large Reasoning Models

Parascandolo, Tan, Sangineto, Song, Cucchiara, [arXiv:2602.14917](https://arxiv.org/abs/2602.14917), Feb 2026. Same author cluster as [[Latent Exploration Decoding]].

## TL;DR

RL algorithm to **reduce overthinking** in LRMs (o1 / DeepSeek-R1). Uses Best-First Search with backtracking anchored at **maximum-entropy nodes** → shortest correct path. Simultaneously raises accuracy and cuts length. **Discrete only** — no latent reasoning; included here because it's a downstream citation of SST and uses the same entropy-node framing as LED.

## Method

- **BFS exploration + policy optimization.**
- **Backtrack at max-entropy nodes:** nodes where the model is most uncertain are the best branching points.
- **Shortest-path objective:** RL reward shapes toward concise reasoning chains.

## Results

- Simultaneous accuracy ↑ + answer length ↓ across multiple benchmarks and base LRMs.

## Relevance

- **Reference for spar-latent-reasoning.** Adjacent but off-axis — entropy-based RL node selection (related to LED's entropy-depth selection). Not a primary writeup citation.
- **Not-applicable for branch-d / branch-a / branch-b.** No latent component.

## Citation links

- [[Latent Exploration Decoding]] — same author cluster, entropy-based framing applied in decoding (LED) vs RL (BFS-PO).
- GRPO / DAPO — the RL baselines BFS-PO improves over.

## Artifacts

- **Paper:** [arXiv:2602.14917](https://arxiv.org/abs/2602.14917)
- **Code:** none.
- **Raw source:** [[.raw/papers/2602.14917-bfs-po]]
