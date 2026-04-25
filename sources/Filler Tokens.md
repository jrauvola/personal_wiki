---
type: source
title: "Let's Think Dot by Dot: Hidden Computation in Transformer Language Models (Pfau, Merrill, Bowman 2024)"
source_type: paper
arxiv_id: "2404.15758"
venue: "COLM 2024"
date_published: 2024-04-24
authors:
  - "Jacob Pfau"
  - "William Merrill"
  - "Samuel R. Bowman"
url: "https://arxiv.org/abs/2404.15758"
code_repo: "https://github.com/jacobpfau/fillertokens"
has_weights: false
status: read
confidence: high
key_claims:
  - "Meaningless filler tokens (e.g., sequences of '.......') can replace semantically meaningful chain-of-thought tokens on two hard algorithmic tasks (3SUM variant, quantifier-nested evaluations) while preserving accuracy."
  - "Theoretical characterization: filler tokens are useful when the target problem has a first-order-logic representation with non-trivial quantifier depth. Precisely: problems solvable by TC0 with filler tokens include those beyond what a constant-depth no-filler transformer can solve."
  - "Learning to use filler tokens requires specific, dense supervision — it is not naturally learnable from sparse end-task reward alone. This is the empirical caveat limiting practical deployment."
  - "Raises an interpretability concern: models may exploit extra token positions for 'hidden computation' unrelated to the visible tokens, meaning CoT faithfulness is fundamentally brittle."
  - "The result disentangles two hypotheses for CoT gain: (H1) semantic decomposition of the problem vs (H2) mere extra compute via extra token positions. The filler-token experiment supports H2 for the class of TC0-solvable problems identified."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Theoretical foundation for why CODI/COCONUT can work at all: extra token positions = extra TC0 compute. Essential for genealogy and for the writeup's 'why latent reasoning should be possible in principle' section."
  - slug: "branch-a"
    relevance: reference
    why: "Theoretical claim is architecture-dependent (constant-depth transformer); relevant as a framing for what Qwen3 can/cannot reason about."
  - slug: "branch-b"
    relevance: reference
    why: "Not a training-block intervention."
  - slug: "branch-c"
    relevance: secondary
    why: "Faithfulness concern directly bears on probe design: if filler tokens enable hidden computation, any probe of the 'visible' CoT tokens is missing the action."
  - slug: "branch-d"
    relevance: reference
    why: "Orthogonal to fusion axis; useful as context for why CPF anchoring might matter."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/theory
  - family/pause-filler-tokens
  - type/source
  - status/theoretical
related:
  - "[[Pause Tokens]]"
  - "[[Quiet-STaR]]"
  - "[[COCONUT]]"
  - "[[Beyond Semantics Reasonless Tokens]]"
sources: []
---

# Filler Tokens — Let's Think Dot by Dot (Pfau, Merrill, Bowman 2024)

## TL;DR

Meaningless dot-sequence tokens ('......') can replicate CoT performance on two hard algorithmic tasks. Theoretical characterization: useful for problems with first-order-logic formulas of non-trivial quantifier depth. Learning is brittle — requires dense supervision.

## Why this matters to our project

This paper is the **theoretical bedrock** for the entire latent-reasoning program. It answers the question "why should additional token positions give the model any reasoning advantage?" with a concrete complexity-theoretic argument:

- A constant-depth transformer lives in $TC^0$.
- $TC^0$ has known expressivity limits (cannot compute parity, etc.).
- Adding $n$ filler tokens gives the transformer $n$ more parallel computation slots per layer, effectively moving it to a strictly larger complexity class.

This justifies COCONUT's continuous thoughts, CODI's latent rollout, [[Pause Tokens]]' learnable blanks — all of them as particular instantiations of "expand computational budget via extra token positions."

## Method

**Tasks:**
- **3SUM variant** (decision version of well-known algorithmic problem).
- **Quantifier-nested boolean evaluation.**

**Filler sequence:** Fixed length, constant token ('.' or '+') or learnable special-token embedding (results similar).

**Training:**
- Requires **per-step supervision** (dense): the model is told what the filler-region "output" should be at each step. End-task-reward only does not work.
- This is the core practical limitation.

## Results

On the two hard tasks: transformer with filler tokens matches CoT-trained transformer. Without filler tokens (or without dense supervision), both fail.

## Theoretical result

Proposition (informal): There exist problems solvable by transformers with $n$ filler tokens in $TC^0$ that are **not** solvable by $n$-shorter transformers without filler tokens. The gap is characterized by quantifier depth in a first-order formula.

## Faithfulness concern

The paper raises an interpretability implication: if filler tokens can drive complex hidden computation, then CoT explanations output by LLMs are not necessarily faithful reflections of internal computation. This motivates [[Are LRMs Easily Interpretable]], [[Quora Faithfulness Probe]], and related mechanistic-interpretability threads.

## Relevance to CODI / COCONUT contrast

Filler Tokens gives the **abstract reason** COCONUT / CODI should work. COCONUT's key *additional* insight on top of filler tokens is that the continuous-thought's *content* matters, not just its presence — specifically, feeding the hidden state back allows the model to store and retrieve information across latent steps. COCONUT's ablation table shows this: pause-as-thought (matching this paper's setup) trails continuous-thought on GSM8k by 10+ points.

## Gap in our vault (now filled)

Before this ingest the vault had [[Beyond Semantics Reasonless Tokens]] (which extends Pfau 2024) but not Pfau 2024 itself. The Pfau theorem is *cited* in nearly every latent-reasoning paper since April 2024.

## Citation links to chase

- [[Pause Tokens]] (Goyal 2023) — sibling paper, learnable pause tokens at LLM scale.
- [[Beyond Semantics Reasonless Tokens]] (vault) — extends Pfau's setup.
- Merrill & Sabharwal 2023 "The Expressive Power of Transformers with Chain of Thought" — complementary theoretical framing.
