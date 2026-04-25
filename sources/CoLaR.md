---
type: source
title: "CoLaR — Compressed Latent Reasoning"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/source
  - method/compression-first
status: read
related:
  - "[[Adaptive Latent RL]]"
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[SIM-CoT]]"
  - "[[Token Efficiency]]"
  - "[[GRPO]]"
  - "[[MARCOS]]"
  - "[[Latent-SFT]]"
  - "[[LEPO]]"
  - "[[SwiReasoning]]"
  - "[[Parallel TTS Latent]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[Weak vs Strong Supervision Study]]"
  - "[[LSTR]]"
  - "[[Capabilities and Limits of Latent CoT]]"
  - "[[Are LRMs Easily Interpretable]]"
  - "[[Gumbel-Softmax Latent]]"
  - "[[Shortcut Behavior]]"
  - "[[Exploration-Execution Trade-off]]"
sources:
  - "[[.raw/papers/2505.16552-colar]]"
source_type: paper
arxiv_id: "2505.16552"
venue: "arXiv (NeurIPS 2025 poster)"
date_published: 2025-05-22
authors:
  - "Wenhui Tan"
  - "Jiaze Li"
  - "Jianzhong Ju"
  - "Zhenbo Luo"
  - "Jian Luan"
  - "Ruihua Song"
url: "https://arxiv.org/abs/2505.16552"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "A probabilistic Latent Head predicts both mean and standard deviation of the next compressed embedding rather than a deterministic vector, enabling diverse reasoning pathways and amenability to GRPO."
  - "Sequential token embeddings are merged by summation scaled by 1/√c (compression factor c) rather than mean pooling; mean pooling distorts the near-zero-centered embedding distribution and causes a 3.4% accuracy drop."
  - "CoLaR-2 achieves 48.8% accuracy on grade-school math (only 4.8% below explicit CoT at 53.6%) while using 53% fewer reasoning steps."
  - "RL-enhanced CoLaR on DeepSeek-R1-Distill-Qwen-1.5B reaches 14.3% on MATH (+5.36% over SFT) with 82.8% reduction in reasoning chain length."
  - "CoLaR-8B on GPQA reaches 37.5%, exceeding its CoT teacher's 35.7% while reducing reasoning by 69% — a rare case of latent reasoning surpassing its explicit-CoT teacher."
  - "CoLaR cannot generalize beyond the maximum compression factor seen during training due to discrete tokenization constraints."
  - "Users dynamically modulate inference latency at runtime by prompting the system with a desired compression factor."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Compression-first paradigm orthogonal to LT-Tuning fusion; relevant as a secondary optimization layer but not the primary experiment."
  - slug: "branch-a"
    relevance: secondary
    why: "Compression mechanics useful for Qwen3 scaling throughput but not core to the architecture-dependence finding."
  - slug: "branch-b"
    relevance: reference
    why: "Tangential to detach/grad-stability ablations; compression is a separate axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No bearing on Qwen3 probe methodology or configuration debugging."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Important taxonomic entry (compression-first school) for the writeup but not a synthesis input for the north-star model."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# CoLaR — Compressed Latent Reasoning

**Full arXiv title:** "Think Silently, Think Fast: Dynamic Latent Compression of LLM Reasoning Chains" — [arXiv:2505.16552](https://arxiv.org/abs/2505.16552) (v1 May 22, 2025; v6 Feb 3, 2026). NeurIPS 2025 poster.

Paradigm shift toward compression-first optimization within the continuous space. Where earlier latent architectures enforce near-linear mapping between a single continuous vector and a single semantic thought step, CoLaR explicitly designs a mechanism to force individual latent variables to encapsulate multiple consecutive vocabulary tokens simultaneously.

## Core thesis

Extreme vector compression via a specialized **Latent Head** — a two-headed MLP operating in parallel with the standard autoregressive language head. This dual-headed architecture predicts highly compressed future states.

CoLaR integrates a non-deterministic sampling mechanism making it uniquely amenable to post-training RL. Applying policy gradients in the continuous space incentivizes the model to explore diverse, varying-length trajectories, ultimately exploiting the shortest most highly compressed vector path that yields a correct conclusion. Runtime: users dynamically modulate inference latency by prompting with a desired compression factor.

## Training pipeline

Bifurcated into two optimization phases.

### Phase 1 — Dynamic-compression SFT

- Compression factor $c$ is stochastically sampled from a predefined continuous range during each forward pass.
- Sequential embeddings of the reasoning tokens are partitioned into blocks.
- Blocks are fused into a single dense representation via summation scaled by $1/\sqrt{c}$ (preserving geometric distribution; mean pooling is a known failure mode).
- **Latent Head**: optimized via NLL to predict compressed block distributions.
- **Language Head**: trained via cross-entropy against a representative token stochastically sampled from within the block.

### Phase 2 — GRPO RL

- Multiple latent output trajectories sampled per query.
- Relative advantages computed via composite reward:
  - Heavy reinforcement of mathematical accuracy.
  - Penalty on total continuous reasoning chain length.
- Drives the policy toward maximum operational efficiency.

## Public artifacts

Transitional.

- NeurIPS 2025 poster; official codebase published.
- Authors note primary model weights **pending release**.
- Community reproductions:
  - `AlbertTan/CoLaR` (HF — DeepSeek-R1-Distill-Qwen-1.5B)
  - `dd101bb/latent-tts-colar`

## Empirical results

- +14.1% accuracy over weakly supervised latent baselines at identical compression ratios.
- RL on complex math: **-82.8% chain length** and **+5.4% accuracy** simultaneously.
- Strong internal supervision (SFT rigorously anchors compressed vectors to specific token blocks) makes CoLaR resistant to shortcut mapping.

## Integration notes

Project fit: medium-high. Requires a dedicated implementation slot (planned, `methodology.md:222`). Optimal target for integrating aggressive compression mechanics **once baselines are fully stabilized**.
