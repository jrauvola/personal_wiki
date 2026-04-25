---
type: source
title: "Parallel TTS Latent — Parallel Test-Time Scaling for Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/test-time-scaling
  - domain/stochastic-latent
  - type/source
  - method/reward-model
status: read
source_type: paper
arxiv_id: "2510.07745"
venue: "ACL 2026 Main Conference"
date_published: 2025-10-09
authors:
  - "Runyang You"
  - "Yongqi Li"
  - "Meng Liu"
  - "Wenjie Wang"
  - "Liqiang Nie"
  - "Wenjie Li"
url: "https://arxiv.org/abs/2510.07745"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "First method to enable parallel test-time scaling for latent reasoning models; previous parallel-TTS assumes discrete token sampling incompatible with continuous latent state."
  - "Two continuous-space sampling strategies — MC Dropout and Additive Gaussian Noise — both scale effectively with compute but exhibit distinct exploration dynamics."
  - "Latent Reward Model (LatentRM) trained with step-wise contrastive objective enables effective trajectory selection without decoding to text."
  - "Opens a new direction for scalable inference in continuous spaces, complementing serial compression approaches (CoLaR) with parallel diversity."
related:
  - "[[CoLaR]]"
  - "[[COCONUT]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2510.07745-parallel-tts-latent]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Inference-time parallel scaling complements but does not replace CPF; useful add-on for evaluation, not implementation target."
  - slug: "branch-a"
    relevance: secondary
    why: "Scaling test-time compute is scaling-relevant; stochastic sampling strategies are cheap to validate on Qwen3."
  - slug: "branch-b"
    relevance: reference
    why: "Parallel TTS orthogonal to detach/grad-stability."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Datapoint that latent reasoning supports parallel TTS — writeup needs this axis, but not a central synthesis input."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Parallel TTS Latent — Parallel Test-Time Scaling for Latent Reasoning

You, Li, Liu, Wang, Nie, Li — [arXiv:2510.07745](https://arxiv.org/abs/2510.07745) — ACL 2026 Main.

## Core thesis

Parallel test-time scaling (TTS) — sampling multiple CoT trajectories and aggregating by voting or search — is a standard recipe for token-based reasoning. Latent reasoning models can't use it directly: discrete-token sampling methods don't apply when reasoning lives in continuous vector space. This paper introduces **continuous-space parallel TTS**: stochastic latent sampling + a latent-space reward model for aggregation.

## Method

### Continuous-space sampling strategies

| Strategy | Mechanism | Exploration dynamics |
|---|---|---|
| **MC Dropout** | Activate dropout at inference | Structurally varied trajectories |
| **Additive Gaussian Noise** | Add N(0, σ²) to latent state per step | More dispersed exploration |

Both produce multiple distinct latent trajectories from one input. User picks σ or dropout rate as a compute/diversity knob.

### LatentRM aggregation

Reward model trained with step-wise contrastive objective. Given N candidate latent trajectories, LatentRM scores each *without decoding to text*, picks the winner for final-answer emission. Contrast with token-space reward models that require full decoding.

## Recipe

- **Architecture:** any latent-reasoning base model (COCONUT / CoLaR class).
- **Training:** LatentRM trained separately via step-wise contrastive loss on (good-trajectory, bad-trajectory) pairs.
- **Inference:** sample N latent trajectories, LatentRM scores, decode winner.

## Results

Both sampling strategies scale effectively with inference compute. LatentRM enables effective trajectory selection. Concrete numbers not in available excerpt — need raw PDF read for full results.

## Relevance to our project

- **Secondary for branch-d.** If CPF-on-CODI works, parallel TTS is a cheap evaluation add-on — show accuracy lift from N-trajectory voting.
- **Secondary for spar-latent-reasoning.** Writeup needs to note latent reasoning is compatible with parallel TTS — one datapoint among many.

## Citation links to chase

- Upstream: [[COCONUT]], [[CoLaR]]
- Related test-time scaling: LatentEvolve (2509.24771)

## Artifacts

- **Paper:** [arXiv:2510.07745](https://arxiv.org/abs/2510.07745) (ACL 2026)
- **Code:** GitHub repo linked by authors (URL not captured at crawl time).
- **Raw source:** [[.raw/papers/2510.07745-parallel-tts-latent]]
