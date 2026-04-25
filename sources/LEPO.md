---
type: source
title: "LEPO — Latent Reasoning Policy Optimization"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/reinforcement-learning
  - domain/stochastic-latent
  - type/source
  - method/gumbel-softmax
status: read
source_type: paper
arxiv_id: "2604.17892"
venue: "arXiv"
date_published: 2026-04-20
authors:
  - "Yuyan Zhou"
  - "Jiarui Yu"
  - "Hande Dong"
  - "Zhezheng Hao"
  - "Hong Wang"
  - "Jianqing Zhang"
  - "Qiang Lin"
url: "https://arxiv.org/abs/2604.17892"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Latent reasoning without stochastic sampling collapses to deterministic inference, foreclosing the exploration benefit that RL provides."
  - "LEPO injects controllable randomness via Gumbel-Softmax, maintaining stochasticity throughout trajectory sampling (not just first step)."
  - "A unified gradient estimator propagates through both continuous latent transitions (straight-through Gumbel) and discrete token emissions (standard policy gradient), avoiding separate RL pipelines for latent vs token heads."
  - "LEPO significantly outperforms existing RL methods for both discrete and latent reasoning."
related:
  - "[[CoLaR]]"
  - "[[GRPO]]"
  - "[[Latent-SFT]]"
  - "[[MARCOS]]"
sources:
  - "[[.raw/papers/2604.17892-lepo]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "RL-on-latent complements but does not replace CPF; relevant for post-SFT fine-tuning once base CPF model trained."
  - slug: "branch-a"
    relevance: reference
    why: "RL on top of a scaled model; not core to architecture-dependence finding."
  - slug: "branch-b"
    relevance: reference
    why: "Stochastic-latent mechanism orthogonal to detach/BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "One of multiple RL-on-latent approaches (alongside CoLaR-GRPO, MARCOS-variational); writeup cites as a recipe variant."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LEPO — Latent Reasoning Policy Optimization

Zhou, Yu, Dong, Hao, Wang, Zhang, Lin — [arXiv:2604.17892](https://arxiv.org/abs/2604.17892) (2026-04-20).

## Core thesis

RL post-training for latent reasoning is bottlenecked by *deterministic collapse*: without explicit randomness, latent inference produces a single trajectory, so policy-gradient rollouts are identical and RL degenerates. LEPO fixes this via Gumbel-Softmax-injected randomness, maintained across the trajectory (not just step 1), with a unified gradient path through both latent and token heads.

## Method

### Gumbel-Softmax stochasticity

At each latent step, softmax-sample via Gumbel trick. Straight-through estimator for gradients. Result: same input → multiple distinct latent trajectories.

### Rollout-phase diversity

Random sampling maintained throughout each rollout (not only at trajectory start) — so tree-of-trajectories is genuinely diverse, enabling meaningful reward-based updates.

### Unified gradient estimator

Single gradient pipeline covers:
- Continuous latent transitions (straight-through Gumbel).
- Discrete token emissions (REINFORCE-style policy gradient).

Avoids the two-pipeline complexity of naive RL over latent + token architectures.

## Recipe

- **Base model:** latent reasoning LLM (COCONUT / CoLaR-class).
- **RL objective:** standard reward maximization (correctness, length penalty — unspecified in excerpt).
- **Sampling:** Gumbel-Softmax throughout rollout.

## Results

Claims significant outperformance vs existing RL methods for both discrete and latent reasoning. Specific numbers not in available excerpt.

## Relevance to our project

- **Secondary for branch-d.** After CPF-on-CODI SFT is stable, LEPO-style Gumbel-RL is a natural next step. Not the Days 3-7 target.
- **Secondary for spar-latent-reasoning.** One of three concurrent stochastic-latent-RL recipes (with CoLaR-GRPO and MARCOS-variational). The writeup needs to triangulate these approaches.

## Citation links to chase

- Upstream: [[CoLaR]] (GRPO-RL), [[COCONUT]]
- Sibling Gumbel-latent work: [[Latent-SFT]] (Gumbel for SFT instead of RL), Stochastic Soft Thinking (2508.03440)

## Artifacts

- **Paper:** [arXiv:2604.17892](https://arxiv.org/abs/2604.17892)
- **Code:** none released at crawl time.
- **Raw source:** [[.raw/papers/2604.17892-lepo]]
