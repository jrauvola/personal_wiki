---
type: source
title: "SynAdapt — Synthetic Continuous CoT with Adaptive Re-think"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/synthetic-supervision
  - method/adaptive-compute
status: read
related:
  - "[[CODI]]"
  - "[[Adaptive Latent RL]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2508.00574-synadapt]]"
source_type: paper
arxiv_id: "2508.00574"
venue: "arXiv"
date_published: 2025-08-01
authors:
  - "Jianwei Wang"
  - "Ziming Wu"
  - "Fuming Lai"
  - "Shaobing Lian"
  - "Ziqian Zeng"
url: "https://arxiv.org/abs/2508.00574"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Existing CCoT methods are hampered by indirect fine-tuning, limited alignment, or inconsistent targets."
  - "SynAdapt generates the synthetic CCoT to serve as a precise and effective alignment target for LLMs."
  - "Relying solely on CCoT is insufficient for solving hard questions; SynAdapt integrates a difficulty classifier that leverages both question context and CCoT to identify hard questions."
  - "CCoT can effectively help identify hard questions after some brief reasoning; we then adaptively prompt the LLM to re-think these hard questions for improved performance."
  - "Extensive experimental results across various benchmarks from different difficulty levels strongly demonstrate the effectiveness of our method, achieving the best accuracy-efficiency trade-off."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Synthetic-CCoT target is an alternative to LT-Tuning's per-step fusion / CODI's hidden-state distillation — a different framing of the alignment target that might compose with or substitute for CPF."
  - slug: "branch-a"
    relevance: reference
    why: "Not specifically about scaling."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Adaptive re-think after brief CCoT is in the same family as Adaptive Latent RL's dynamic stopping — useful synthesis data point."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# SynAdapt — Synthetic Continuous CoT with Adaptive Re-think

Wang, Wu, Lai, Lian, Zeng, [arXiv:2508.00574](https://arxiv.org/abs/2508.00574).

## TL;DR

Two complaints about existing continuous CoT: indirect fine-tuning, limited alignment, inconsistent targets. SynAdapt's fix: (1) generate a **synthetic CCoT** as an explicit alignment target rather than using hidden states as a dynamic target; (2) add a difficulty classifier that uses context + a brief CCoT pass to decide whether a hard-question re-think is needed. Claims best accuracy-efficiency trade-off across mixed-difficulty benchmarks.

## Method

- **Synthetic CCoT target.** Precomputed continuous trajectory that serves as alignment target for LLM during training.
- **Difficulty classifier.** Uses question context + early CCoT to predict hardness.
- **Adaptive re-think.** On hard questions, prompt the LLM to re-reason after the initial brief CCoT.

## Relevance

SynAdapt contributes two orthogonal ideas: (a) explicit synthetic target vs dynamic teacher-hidden-state target; (b) adaptive-compute on top of latent reasoning (difficulty classifier → re-think). The latter is methodologically adjacent to Adaptive Latent RL (2511.21581). Secondary for branch-d's CPF work because CPF is a fusion-at-every-step mechanism, not a target-design mechanism.

## Citation links to chase

- CODI (alignment target as hidden state).
- Adaptive Latent RL (dynamic compute allocation).
