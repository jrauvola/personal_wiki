---
type: source
title: "Is Continuous CoT Better for Multilingual Reasoning?"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/cross-lingual
  - method/codi-application
status: read
related:
  - "[[CODI]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2603.08177-continuous-cot-multilingual]]"
source_type: paper
arxiv_id: "2603.08177"
venue: "arXiv"
date_published: 2026-03-09
authors:
  - "Ali Hamza Bashir"
  - "Behzad Shomali"
  - "Markus Frey"
  - "Mehdi Ali"
  - "Rafet Sifa"
  - "David Berghaus"
url: "https://arxiv.org/abs/2603.08177"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "We compare Continuous Chain-of-Thought (using the CODI framework) against standard supervised fine-tuning across five typologically diverse languages: English, Chinese, German, French, and Urdu."
  - "Continuous reasoning significantly outperforms explicit reasoning on low-resource languages, particularly in zero-shot settings where the target language was not seen during training."
  - "This approach achieves extreme efficiency, compressing reasoning traces by approximately 29× to 50×."
  - "Continuous latent representations naturally exhibit greater language invariance, offering a scalable solution for cross-lingual reasoning."
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Uses CODI but orthogonal to fusion mechanism; applied domain evaluation."
  - slug: "branch-a"
    relevance: reference
    why: "Not scaling-specific."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach / stability content."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "CODI-framework generalization datapoint (language-invariance); useful rhetorical support for the writeup but not a method or framing contribution."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Is Continuous CoT Better Suited for Multilingual Reasoning?

Bashir, Shomali, Frey, Ali, Sifa, Berghaus, [arXiv:2603.08177](https://arxiv.org/abs/2603.08177).

## TL;DR

Direct application of the **CODI framework** to multilingual reasoning. Compared against standard SFT on EN/ZH/DE/FR/UR over GSM8K and CommonsenseQA. Continuous CoT wins especially on low-resource zero-shot (target language unseen at training). 29×-50× compression of reasoning traces. Supports the thesis that continuous latent representations are more language-invariant than discrete token CoT.

## Results

- Low-resource, zero-shot: continuous CoT ≫ explicit.
- High-resource: comparable or better.
- 29× to 50× trace compression.

## Relevance

Mostly useful as a **CODI validation / generalization datapoint** — confirms that the single-point distillation recipe generalizes across typologically diverse languages. Not a methodology contribution for branch-d, but useful rhetorical support in the fellowship writeup. No probe or fusion mechanism content.

## Citation links to chase

- CODI (direct framework dependency).
