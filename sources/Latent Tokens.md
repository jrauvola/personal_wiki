---
type: source
title: "Latent Tokens — Enhancing Latent Computation in Transformers with Latent Tokens"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/architecture
  - type/source
  - method/learnable-tokens
  - method/prompt-tuning
status: read
related:
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2505.12629-latent-tokens]]"
source_type: paper
arxiv_id: "2505.12629"
venue: "arXiv"
date_published: 2025-05-19
authors:
  - "Yuchang Sun"
  - "Yanxi Chen"
  - "Yaliang Li"
  - "Bolin Ding"
url: "https://arxiv.org/abs/2505.12629"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Latent tokens are lightweight auxiliary dummy tokens (non-interpretable in natural language) that steer autoregressive decoding via the attention mechanism without producing extra verbal outputs; they integrate into any decoder-only Transformer."
  - "Periodic insertion (e.g., one latent token before each comma — Comma_m) outperforms prompt-tuning-style start/end insertion (Start_m, End_m), especially in OOD generation length settings."
  - "On a synthetic Generation task with Llama-3.2-1B, Comma_2 achieves a 23% relative improvement over Start_2/End_2 in extreme OOD settings."
  - "On a Summation information-retrieval task, periodic 8_2 insertion achieves 127% relative improvement over Start_2 in extreme OOD."
  - "Function specialization (one latent token at start + one before each comma, Comma_1 w/ FS) achieves 220% relative improvement on Repetition task over best baseline in extreme OOD — evidence that different latent-token roles can be specialized via position."
  - "Performance gains do not come from increased computation alone: baselines matched for token count (23/20/7 extra tokens) still underperform latent tokens in OOD settings."
projects:
  - slug: "branch-a"
    relevance: reference
    why: "Llama-3.2-1B backbone; too small to test architecture-dependence thesis directly."
  - slug: "branch-b"
    relevance: reference
    why: "Prompt-tuning axis orthogonal to detach/fp32."
  - slug: "branch-c"
    relevance: reference
    why: "Unrelated to probe validation."
  - slug: "branch-d"
    relevance: secondary
    why: "Periodic latent-token insertion is an alternative anti-collapse mechanism to CPF — keeps the model re-anchored to verbal context at regular intervals rather than interpolating at token level. Attention-map analysis showing latent tokens receive 6-subsequent-token attention is relevant evidence for how anchor mechanisms work."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Lightweight auxiliary-token paradigm (Pause Token / filler-token family); taxonomic reference for the 'non-trained-from-scratch lightweight augmentation' branch."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Latent Tokens

## TL;DR

Lightweight decoder-only Transformer augmentation: introduce m learnable "latent tokens" (non-verbal) inserted at specific positions (periodic before commas, or function-specialized at start+comma). These steer attention-mechanism computation without producing extra verbal tokens. Three synthetic tasks (Generation / Summation / Repetition) on Llama-3.2-1B show 23%/127%/220% OOD relative improvements over prompt-tuning-style Start/End baselines.

## Method

**Design principles:**
- **General applicability:** integrates into any decoder-only Transformer.
- **Latent computation:** latent tokens help next-token prediction via attention but are not decoded themselves.
- **Minimal disturbance:** introduce with minimal impact on verbal-token distribution.

**Architecture:**
- m learnable vectors z_i ∈ R^d; each is a "latent token" u_i outside the original vocabulary.
- Inserted into query and generated response at specified positions.
- Positional encoding for latent tokens: design choices explored in Appendix A.1.
- Loss: next-token CE on verbal tokens only; latent tokens do not emit targets.

**Insertion strategies:**
- Start_m: m latent tokens at start of query (prompt-tuning analog).
- End_m: m latent tokens at end of query.
- **Comma_m:** m latent tokens before each comma (periodic, context-aware).
- k_m: m latent tokens every k verbal tokens (periodic, context-free).
- **Comma_1 with function specialization (Comma_1 w/ FS):** one latent token at start (instruction-memory role) + one before each comma (local-context role).

## Recipe

- Backbone: Llama-3.2-1B.
- Three synthetic diagnostic tasks:
  - **Generation:** learn a 4-digit operation rule + generate chain of equations. ID: match training; OOD: longer chains.
  - **Summation:** given a list of Var=value lines, answer Var_i + Var_j. ID: 5-15 variables; OOD: >15 variables.
  - **Repetition:** repeat a given equation n times. ID: n-s_1 ∈ [1,5]; OOD: >5.
- Train with frozen backbone + learnable latent tokens (prompt-tuning-like).

## Results

**Generation (ID / OOD):**
- Comma_1, Comma_2 outperform all baselines at equal trainable params.
- Extreme OOD: 23% relative improvement over best baseline.
- Attention-map inspection: pattern repeats every 8 tokens (6 verbal + 2 latent); each latent group heavily attended by next 6 tokens.

**Summation:**
- Periodic 8_2 insertion achieves 127% OOD relative improvement over Start_2.
- Latent tokens as "anchors" to locate information in input.

**Repetition:**
- Base Llama-3.2-1B cannot finish this task without fine-tuning.
- Comma_1 w/ FS: 220% OOD relative improvement over best baseline.
- Function specialization: start token memorizes instruction; comma tokens track current status.

**Ablation:**
- Token-count-matched baselines (23/20/7 extra tokens to match average sequence length) still underperform.
- Gains stem from position/function design, not raw extra computation.

## Relevance to our project

**Secondary for Branch D.** Periodic latent-token insertion is a mild anti-collapse / anchoring mechanism: the model re-grounds attention to specific position markers regularly. This is a distinct mechanism from CPF (which anchors at the embedding level, not the positional level). Attention-map observation that Comma_m latent tokens are heavily attended by the subsequent 6 verbal tokens is concrete evidence for how "anchor" tokens operate mechanistically — potentially useful for interpreting [[Latent Thoughts Tuning]]'s CPF. **Secondary for spar-latent-reasoning:** belongs to the "lightweight learnable-token augmentation" branch of the taxonomy (Pause Token, CCoT contemplation tokens, filler tokens) — worth including in the writeup as a contrasting design philosophy where heavy latent reasoning (COCONUT, LT-Tuning) is not required. **Caveat:** Llama-3.2-1B scale means conclusions may not transfer to 8B+ where the embedding decoupling problem kicks in.

## Citation links to chase

- Pause Token (Goyal et al. 2023) — closely related augmentation.
- CCoT contemplation tokens (Cheng & Durme 2024).
- Filler tokens (Pfau et al. 2024).
- Prompt tuning (Lester et al. 2021) — baseline paradigm.
