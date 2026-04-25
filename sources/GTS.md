---
type: source
title: "GTS — Gaussian Thought Sampler for Latent Inference-Time Scaling"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/inference-time-scaling
  - method/grpo
status: read
related:
  - "[[CODI]]"
  - "[[GRPO]]"
sources:
  - "[[.raw/papers/2602.14077-gts]]"
source_type: paper
arxiv_id: "2602.14077"
venue: "arXiv"
date_published: 2026-02-15
authors:
  - "Minghan Wang"
  - "Ye Bai"
  - "Thuy-Trang Vu"
  - "Ehsan Shareghi"
  - "Gholamreza Haffari"
url: "https://arxiv.org/abs/2602.14077"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Inference-time scaling (ITS) in latent reasoning models typically relies on heuristic perturbations, such as dropout or fixed Gaussian noise, to generate diverse candidate trajectories."
  - "Stronger perturbations do not necessarily yield better sampling quality: they often induce larger distribution shifts without producing more useful reasoning paths or better final decisions."
  - "GTS is a lightweight module that reformulates latent exploration as sampling from a learned conditional distribution over continuous reasoning states."
  - "GTS predicts context-dependent perturbation distributions and is trained with GRPO-style policy optimization while keeping the backbone frozen, turning heuristic perturbation into an explicit probabilistic sampling policy."
  - "GTS yields more reliable inference-time scaling than heuristic baselines, suggesting that effective latent ITS requires better-controlled and optimizable sampling rather than simply amplifying stochasticity."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Post-hoc ITS module; composes with CODI / CPF at inference without retraining. Useful for evaluation-time throughput/quality knob."
  - slug: "branch-a"
    relevance: reference
    why: "Not specifically scaling-related."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Orthogonal to detach ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Latent ITS as an explicit subject of study; useful survey datapoint."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# GTS — Gaussian Thought Sampler

Wang, Bai, Vu, Shareghi, Haffari, [arXiv:2602.14077](https://arxiv.org/abs/2602.14077).

## TL;DR

Latent reasoning ITS usually uses heuristic noise (dropout / fixed Gaussian). GTS replaces this with a **learned conditional distribution** over continuous reasoning states, trained via GRPO with frozen backbone. Claim: controlled, optimizable sampling > amplified stochasticity. Two latent architectures tested (unnamed in abstract).

## Method

- Lightweight GTS module predicts context-dependent perturbation distribution.
- GRPO-style policy optimization; backbone frozen.
- Replaces heuristic perturbation with explicit sampling policy.

## Relevance

A post-hoc, backbone-frozen ITS module that could be plugged into CODI/CPF at inference time. Relevance is secondary but real: if CPF anchors intermediate latents to vocab geometry, GTS gives a principled way to explore around that trajectory. Related to Soft Thinking / Single-Threaded Reasoners by attacking the same phenomenon (heuristic noise is bad) from a different angle.

## Citation links to chase

- Soft Thinking (single-threaded reasoner finding motivates learned noise).
- GRPO (training method).
