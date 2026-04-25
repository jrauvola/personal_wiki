---
type: source
title: "LatentChem — From Textual CoT to Latent Thinking in Chemical Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/chemistry
  - type/source
  - method/emergent-latent
  - method/task-success-only
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
sources:
  - "[[.raw/papers/2602.07075-latentchem]]"
source_type: paper
arxiv_id: "2602.07075"
venue: "arXiv"
date_published: 2026-02-06
authors:
  - "Xinwu Ye"
  - "Yicheng Mao"
  - "Jia Zhang"
  - "Yimeng Liu"
  - "Li Hao"
  - "Fang Wu"
  - "Zhiwei Li"
  - "Yuxuan Liao"
  - "Zehong Wang"
  - "Yingcheng Wu"
  - "Zhiyuan Liu"
  - "Zhenfei Yin"
  - "Li Yuan"
  - "Philip Torr"
  - "Huan Sun"
  - "Xiangxiang Zeng"
  - "Mengdi Wang"
  - "Le Cong"
  - "Shenghua Gao"
  - "Xiangru Tang"
url: "https://arxiv.org/abs/2602.07075"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "When optimized solely for task success, models spontaneously internalize reasoning, progressively abandoning verbose textual derivations in favor of implicit latent computation."
  - "LatentChem decouples chemical computation from textual generation, enabling models to perform multi-step reasoning directly in continuous latent space while emitting language only for final outputs."
  - "LatentChem achieves a 59.88% non-tie win rate over strong CoT-based baselines on ChemCoTBench."
  - "LatentChem delivers a 10.84× average reduction in reasoning overhead."
  - "The shift from textual to latent reasoning is not merely stylistic but computationally advantageous — chemical reasoning is more naturally realized as continuous latent dynamics than as discretized linguistic trajectories."
projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Chemistry-domain applied paper; no Qwen3 scaling signal."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No grad-stability discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Emergent abandonment of textual derivations without curriculum is a counterpoint to LT-Tuning's view that explicit curriculum is load-bearing — worth noting, but domain-specific (chemistry structural reasoning) and unclear how it generalizes to math."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Provides a domain-specific 'emergent latent reasoning' data point for the SPAR writeup's taxonomy. 10.84× overhead reduction and 59.88% win rate are concrete numbers. Taxonomic value, not recipe value."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LatentChem — From Textual CoT to Latent Thinking in Chemical Reasoning

## TL;DR

Chemistry-domain latent-reasoning interface that decouples chemical computation from textual generation. Key empirical claim: **when optimized only for task success, models spontaneously internalize reasoning** — verbose textual derivations are progressively abandoned in favor of implicit latent computation. 59.88% non-tie win rate vs strong CoT baselines on ChemCoTBench, 10.84× average reasoning-overhead reduction.

## Method

- Latent reasoning interface: multi-step reasoning happens in continuous latent space; language only emitted for final output.
- No explicit curriculum or reasoning-data distillation needed (claimed); only task-success optimization.
- Base model architecture not specified in abstract.

## Recipe

- Task-success-only optimization (pure end-task loss).
- Emergent behavior: abandonment of text derivations.
- Training details in PDF.

## Results

- ChemCoTBench: 59.88% non-tie win rate vs CoT baselines.
- 10.84× average reduction in reasoning overhead.

## Relevance

- **Contra LT-Tuning** (weakly): suggests that in some domains, curriculum is not load-bearing and emergence suffices. But chemical reasoning has structural/continuous priors that math reasoning lacks — the generalization is not automatic.
- For SPAR writeup: interesting as a contrastive datapoint on "when does curriculum matter."

## Citations

- Discovered via SIM-CoT downstream citation graph.
- High-profile author list (Torr, Mengdi Wang, OSU, Stanford) — worth tracking.
