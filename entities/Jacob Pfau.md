---
type: entity
entity_type: person
title: "Jacob Pfau"
role: "First author, Let's Think Dot by Dot / Filler Tokens (COLM 2024). Provides the complexity-theoretic foundation for why latent reasoning can work."
first_mentioned: "[[Filler Tokens]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/theory
  - affiliation/nyu
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Filler Tokens is the theoretical bedrock for why latent reasoning works at all: extra token positions expand the expressivity of a constant-depth transformer beyond TC^0 under mild conditions. Essential framing for the writeup."
  - slug: "branch-a"
    relevance: reference
    why: "Complexity-theoretic architecture dependence is the high-level framing for what Qwen3 can vs. cannot reason about."
  - slug: "branch-b"
    relevance: reference
    why: "Not a BPTT/detach intervention."
  - slug: "branch-c"
    relevance: secondary
    why: "Faithfulness concern directly bears on probing: visible CoT tokens may be mere cover for hidden computation."
  - slug: "branch-d"
    relevance: reference
    why: "Orthogonal to CPF fusion axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Filler Tokens]]"
  - "[[Pause Tokens]]"
  - "[[William Merrill]]"
  - "[[Sam Bowman]]"
sources:
  - "[[Filler Tokens]]"
---

# Jacob Pfau

## Position
PhD student at NYU Center for Data Science (with Sam Bowman). Prior research at MATS / Alignment Research Center.

## Core contribution

First author of "Let's Think Dot by Dot: Hidden Computation in Transformer Language Models" (Pfau, Merrill, Bowman; arXiv:2404.15758, COLM 2024). Shows that meaningless filler sequences (e.g., `'.......'`) can replace semantically meaningful CoT on two hard algorithmic tasks (3SUM variant, quantifier-nested boolean evaluation) while preserving accuracy. Provides the first theoretical characterization: problems solvable by transformers with $n$ filler tokens in $TC^0$ can exceed the expressivity of $n$-shorter transformers without filler tokens. Learning filler-token usage requires dense per-step supervision — sparse end-reward training fails.

## Why relevant to this project

Filler Tokens is the **theoretical foundation** that justifies the entire COCONUT / CODI / LT-Tuning program:

1. **Extra token positions = extra computation.** A constant-depth transformer lives in $TC^0$. Adding $n$ filler tokens gives $n$ additional parallel hidden-vector slots per layer, effectively moving the transformer into a strictly larger complexity class (under the paper's characterization).
2. **Faithfulness concern.** If filler tokens can drive complex hidden computation, visible CoT tokens in a standard model may be mere cover for invisible reasoning. This is the theoretical starting point for [[Are LRMs Easily Interpretable]] and related probing work.
3. **Dense supervision is load-bearing.** Sparse task rewards don't teach the model to use filler tokens; this is the empirical warning that propagates forward to [[Soft Tokens Hard Truths]] and the broader "weak supervision can fail" literature.

## See also
- [[Filler Tokens]] — canonical source page.
- [[Pause Tokens]] — companion / precursor at LLM scale (Goyal 2023).
- William Merrill — co-author, complexity theory of transformers.
- Sam Bowman — co-author, senior.
