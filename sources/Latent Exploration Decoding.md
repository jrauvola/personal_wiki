---
type: source
title: "LED — Latent Exploration Decoding"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/decoding
  - type/source
  - method/inference-time
  - method/depth-conditioned
status: read
source_type: paper
arxiv_id: "2602.01698"
venue: "arXiv"
date_published: 2026-02-02
authors:
  - "Wenhui Tan"
  - "Fiorenzo Parascandolo"
  - "Enver Sangineto"
  - "Jianzhong Ju"
  - "Zhenbo Luo"
  - "Qian Cao"
  - "Rita Cucchiara"
  - "Ruihua Song"
  - "Jian Luan"
url: "https://arxiv.org/abs/2602.01698"
code_repo: "https://github.com/AlbertTan404/Latent-Exploration-Decoding"
has_weights: false
confidence: high
key_claims:
  - "Modern reasoning post-training induces an unintended exploration collapse: temperature-based sampling no longer increases pass@n accuracy."
  - "The final-layer posterior of post-trained LRMs exhibit sharply reduced entropy, while the entropy of intermediate layers remains relatively high."
  - "LED aggregates intermediate posteriors via cumulative sum and selects depth configurations with maximal entropy as exploration candidates."
  - "Without additional training or parameters, LED consistently improves pass@1 and pass@16 accuracy by 0.61 and 1.03 percentage points across multiple reasoning benchmarks and models."
related:
  - "[[Stochastic Soft Thinking]]"
  - "[[Soft Thinking]]"
  - "[[Gumbel-Softmax Latent]]"
  - "[[Shortcut Behavior]]"
sources:
  - "[[.raw/papers/2602.01698-led]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Diagnoses exploration collapse via final-vs-intermediate-layer entropy asymmetry — empirical support for CPF's premise, but the fix (depth-conditioned decoding) is a different mechanism."
  - slug: "branch-a"
    relevance: secondary
    why: "Entropy-asymmetry diagnostic is a cheap probe applicable to Qwen3 latent baselines — could indicate whether a baseline is RL-collapsed without retraining."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Inference-time decoding; orthogonal to training stability."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology for Qwen3 config."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Third independent diagnosis of exploration collapse after SST (Greedy Pitfall) and LaDi-RL (mode elicitation) — adds depth-direction axis to the failure taxonomy."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LED — Latent Exploration Decoding

> [!note] Layer-asymmetric entropy collapse refines aggregate [[Feature Collapse]] framing
> LED's key diagnostic is that post-RL LRMs collapse entropy ONLY at the final layer while intermediate layers remain high-entropy. Our existing [[Feature Collapse]] concept has been framed as aggregate collapse of the latent trajectory. Not a contradiction, but a refinement: feature collapse is layer-asymmetric, not uniform. The entropy reservoir in intermediate layers is why decoding-time interventions (LED, SeLaR, ThinkRouter) can recover diversity without retraining. Related refinement from [[Latent Thinking Optimization]]: Huginn latent trajectories encode a process-reward signal invisible to logit lens but visible to a reward classifier — same pattern: the information is elsewhere in the stack.

Tan, Parascandolo, Sangineto et al., [arXiv:2602.01698](https://arxiv.org/abs/2602.01698), Feb 2026. Marked `isInfluential=True` in S2's citation graph from [[Stochastic Soft Thinking]].

## TL;DR

RL post-training collapses final-layer entropy of LRMs — temperature sampling fails to raise pass@n. But **intermediate layers keep high entropy**. LED exploits this asymmetry: aggregate intermediate-layer posteriors via cumulative-sum and decode from the depth config with maximal entropy. Training-free, parameter-free. +0.61 pp pass@1 / +1.03 pp pass@16 across multiple benchmarks and models.

## Method

### Entropy asymmetry diagnosis

Post-RL LRMs exhibit collapsed final-layer entropy (the "confident collapse" after RL). But hidden layers retain high entropy. LED uses intermediate layers as a *reservoir of preserved diversity*.

### LED algorithm

- Compute posteriors at each intermediate layer.
- Aggregate via cumulative-sum across depth.
- Select depth configurations with maximal entropy as exploration candidates.
- Decode with these high-entropy depth configurations.

### No training, no new parameters

Pure decoding-time modification.

## Results

- +0.61 pp pass@1.
- +1.03 pp pass@16.
- Across multiple reasoning benchmarks and model families.

## Relevance

- **Reference for branch-d.** Independent evidence that RL/SFT collapse is real but partial — final-layer only. CPF's mechanism targets earlier-in-stack collapse via vocabulary anchor, so not directly comparable, but same disease.
- **Secondary for branch-a.** The intermediate-layer entropy probe is a cheap diagnostic — could test whether our Qwen3 latent baselines exhibit the asymmetry or not.

## Citation links

- [[Stochastic Soft Thinking]] — Greedy Pitfall (final-layer collapse via autoregression).
- [[Shortcut Behavior]] — another collapse diagnosis.
- Tuned lens / logit lens literature (not cited) — related intermediate-layer decoding techniques.

## Artifacts

- **Paper:** [arXiv:2602.01698](https://arxiv.org/abs/2602.01698)
- **Code:** https://github.com/AlbertTan404/Latent-Exploration-Decoding
- **Raw source:** [[.raw/papers/2602.01698-led]]
