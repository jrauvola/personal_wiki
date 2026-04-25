---
type: source
title: "LaDi-RL — Diversity-Preserving RL via Latent Diffusion Reasoner"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/diffusion
  - type/source
  - method/reinforcement-learning
  - method/latent-diffusion
status: read
source_type: paper
arxiv_id: "2602.01705"
venue: "arXiv"
date_published: 2026-02-02
authors:
  - "Haoqiang Kang"
  - "Yizhe Zhang"
  - "Nikki Lijing Kuang"
  - "Yi-An Ma"
  - "Lianhui Qin"
url: "https://arxiv.org/abs/2602.01705"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Exploration in token space often suffers from diversity collapse as policy entropy decreases due to mode elicitation behavior in discrete RL."
  - "By modeling exploration via guided diffusion, multi-step denoising distributes stochasticity and preserves multiple coexisting solution modes without mutual suppression."
  - "Latent diffusion-based optimization is more effective than text-space policy optimization alone, while a complementary text policy provides additional gains when combined with latent exploration."
  - "Absolute pass@1 gains of +9.4% on code generation and +5.7% on mathematical reasoning."
  - "Diffusion-based latent RL [is] a principled alternative to discrete token-level RL for reasoning."
related:
  - "[[LaDiR]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[Haoqiang Kang]]"
  - "[[Gumbel-Softmax Latent]]"
  - "[[Shortcut Behavior]]"
sources:
  - "[[.raw/papers/2602.01705-ladi-rl]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Latent-diffusion RL is a different paradigm from CPF's sequential latent emission; but the mode-elicitation-collapse failure mode is parallel to Greedy Pitfall and motivates CPF's anti-collapse design."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Diffusion paradigm orthogonal to Qwen3 sequential latent scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not relevant to detach/BPTT."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Extends LaDiR family to RL; diversity-preserving latent RL is a distinct synthesis input. 'Mode elicitation' framing parallels SST's Greedy Pitfall."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LaDi-RL — Diversity-Preserving RL via Latent Diffusion Reasoner

Kang, Zhang, Kuang, Ma, Qin, [arXiv:2602.01705](https://arxiv.org/abs/2602.01705), Feb 2026. Same lineage as [[LaDiR]] (Kang et al., UCSD + Apple).

## TL;DR

Discrete RL on CoT **collapses diversity** via **mode elicitation** — policy entropy falls, single mode dominates. LaDi-RL puts RL in a continuous latent space via guided diffusion: multi-step denoising distributes stochasticity across the trajectory, preserving multiple coexisting modes. Latent RL alone beats text-RL; latent + text RL combined is best. +9.4% pass@1 code, +5.7% pass@1 math.

## Method

### VAE-latent + latent-diffusion flow matching

Same backbone structure as [[LaDiR]] — VAE encodes CoT sentences to latent blocks; reasoning model is a flow-matching denoiser over latents.

### Guided diffusion exploration

RL exploration happens in the latent space via guided diffusion rather than in token space. Multi-step denoising distributes sampling noise across the trajectory, which avoids the single-point mode-elicitation failure of discrete RL.

### Decoupled latent + text policy

Two policies: latent policy does exploration (diffusion rollouts); text policy does fine-grained generation. Combining gives best pass@1 / pass@k.

## Results

- **Code generation:** +9.4% absolute pass@1 over discrete RL baselines.
- **Math reasoning:** +5.7% absolute pass@1 over discrete RL baselines.
- Consistent pass@k gains.

## Relevance

- **Secondary for spar-latent-reasoning.** Mode-elicitation framing is parallel to [[Stochastic Soft Thinking]]'s Greedy Pitfall at the RL-exploration scale. Pair the two for a "diversity collapse in latent vs token" pair in the writeup taxonomy.
- **Reference for branch-d.** Same disease, different cure; not directly portable to CODI harness.

## Citation links

- [[LaDiR]] — SFT version; LaDi-RL adds RL.
- [[Soft Tokens Hard Truths]] — token-space RL with soft perturbations as an alternative to latent-space diffusion RL.
- [[LEPO]] / [[HRPO]] / [[RLTT]] — latent-RL siblings via different mechanisms.
- [[Stochastic Soft Thinking]] — conceptual parallel: stochasticity-as-cure for mode collapse.

## Artifacts

- **Paper:** [arXiv:2602.01705](https://arxiv.org/abs/2602.01705)
- **Code:** none in abstract.
- **Raw source:** [[.raw/papers/2602.01705-ladi-rl]]
