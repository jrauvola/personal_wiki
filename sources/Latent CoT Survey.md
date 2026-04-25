---
type: source
title: "Reasoning Beyond Language — Latent CoT Reasoning Survey"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - type/survey
  - method/taxonomy
status: read
source_type: paper
arxiv_id: "2505.16782"
venue: "arXiv"
date_published: 2025-05-22
authors:
  - "Xinghao Chen"
  - "Anhao Zhao"
  - "Heming Xia"
  - "Xuan Lu"
  - "Hanlin Wang"
  - "Yanjun Chen"
  - "Wei Zhang"
  - "Jian Wang"
  - "Wenjie Li"
  - "Xiaoyu Shen"
url: "https://arxiv.org/abs/2505.16782"
code_repo: "https://github.com/EIT-NLP/Awesome-Latent-CoT"
has_weights: false
confidence: high
key_claims:
  - "Conventional CoT relies on explicitly verbalized intermediate steps, which constrains its broader applicability, particularly in abstract reasoning tasks beyond language."
  - "Latent CoT reasoning, where the reasoning process is embedded within latent spaces, offers the promise of richer cognitive representations and facilitates more flexible, faster inference."
  - "We analyze recent advances in methods, categorizing them from token-wise horizontal approaches to layer-wise vertical strategies."
  - "Decoupling reasoning from explicit language generation is a shared design principle."
related:
  - "[[COCONUT]]"
  - "[[Stochastic Soft Thinking]]"
  - "[[Soft Thinking]]"
  - "[[Ouro]]"
  - "[[LoopLM]]"
sources:
  - "[[.raw/papers/2505.16782-latent-cot-survey]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Survey provides taxonomic framing but not specific CPF-family recipes; reference for writeup framing."
  - slug: "branch-a"
    relevance: reference
    why: "Taxonomy covers scaling dimensions but no Qwen-specific architectural insight."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach/BPTT content."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical taxonomy citation for the SPAR writeup. 'Token-wise horizontal vs layer-wise vertical' is the cleanest two-axis framing in the field — directly usable for structuring the writeup's background section."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Reasoning Beyond Language — Latent CoT Reasoning Survey

Chen, Zhao, Xia et al. (EIT-NLP), [arXiv:2505.16782](https://arxiv.org/abs/2505.16782), May 2025 (rev Nov 2025). **34 citations, 2 influential** — the canonical survey for this field.

## TL;DR

First comprehensive survey of **latent CoT reasoning**. Establishes the **token-wise horizontal vs layer-wise vertical** taxonomy:
- **Token-wise horizontal:** width-of-latent methods — COCONUT, CODI, Soft Thinking, Stochastic Soft Thinking, CoLaR, LT-Tuning, etc.
- **Layer-wise vertical:** depth-of-latent methods — Ouro, LoopLM, Parcae, recurrent-transformer methods.

Registry of tracked papers at github.com/EIT-NLP/Awesome-Latent-CoT is updated regularly.

## Taxonomy (as used in our vault)

**Horizontal (token-wise):**
- Sequential emission: COCONUT, CODI, Token Assorted, LT-Tuning.
- Parallel / soft: Soft Thinking, SST, CoLaR, Latent-SFT, LaDiR.
- Hybrid: HRPO, ThinkRouter, SwiReasoning, SeLaR.

**Vertical (layer-wise):**
- Pretraining: Ouro, Parcae.
- Adaptive: Think-at-Hard, Adaptive Loops and Memory.
- Iterative: Hierarchical Reasoning Model, LoopLM family.

## Relevance

- **Primary for spar-latent-reasoning.** Canonical taxonomy citation. Two-axis framing is the most parsimonious in the field and directly structures our writeup's background section.
- **Reference for other branches.** Not recipe-level — use for introduction / related-work framing only.

## Citation links

- Github registry: https://github.com/EIT-NLP/Awesome-Latent-CoT — tracks all new latent-CoT papers; useful cross-check against our vault.

## Artifacts

- **Paper:** [arXiv:2505.16782](https://arxiv.org/abs/2505.16782)
- **Registry:** github.com/EIT-NLP/Awesome-Latent-CoT
- **Raw source:** [[.raw/papers/2505.16782-latent-cot-survey]]
