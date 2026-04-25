---
type: entity
entity_type: person
title: "Eric Zelikman"
role: "First author, STaR (NeurIPS 2022) and Quiet-STaR (COLM 2024). Originator of rationale self-bootstrapping and per-token latent-thought pretraining."
first_mentioned: "[[Quiet-STaR]]"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/entity
  - entity/person
  - domain/latent-reasoning
  - domain/reasoning
  - affiliation/stanford
  - affiliation/xai
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Quiet-STaR is a load-bearing genealogy node: learnable `<start-thought>`/`<end-thought>` delimiters are the direct ancestor of COCONUT's `<bot>`/`<eot>`; per-token rationale pretraining is still a road not taken by COCONUT descendants."
  - slug: "branch-a"
    relevance: secondary
    why: "Mistral-7B scaling result for implicit reasoning during pretraining is a useful Qwen3 baseline reference."
  - slug: "branch-b"
    relevance: reference
    why: "REINFORCE training of rationales is a different gradient-estimator axis than CODI's L1 self-distillation."
  - slug: "branch-c"
    relevance: secondary
    why: "Per-token rationales are an interpretability-adjacent signal: each token has an associated latent thought that can be probed independently."
  - slug: "branch-d"
    relevance: reference
    why: "Quiet-STaR's mixing head is conceptually adjacent to CPF's fusion gate."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Quiet-STaR]]"
  - "[[COCONUT]]"
  - "[[Pause Tokens]]"
sources:
  - "[[Quiet-STaR]]"
---

# Eric Zelikman

## Position
Research scientist at xAI (from 2024). Previously PhD at Stanford (with Noah Goodman). Prior to that, BS + Stanford Symbolic Systems.

## Core contributions

- **STaR: Self-Taught Reasoner, 2022** (NeurIPS 2022, with Yuhuai Wu, Jesse Mu, Noah Goodman). Bootstraps CoT rationales from a base LM: generate rationale + answer, keep only rationales that produce correct answers, fine-tune on this self-generated dataset. Establishes the "rationale filtering + fine-tuning" recipe reused by RFT and many 2023-2024 reasoning methods.

- **Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking, 2024** ([[Quiet-STaR]], arXiv:2403.09629, COLM 2024). Extends STaR to pretraining: generate a short rationale at *every* token, reward it via REINFORCE when its presence increases the likelihood of the ground-truth next token. Base Mistral-7B: zero-shot GSM8K 5.9% → 10.9%; CommonsenseQA 36.3% → 47.2%. Introduces learnable `<start-thought>` / `<end-thought>` delimiters.

## Why relevant to this project

Quiet-STaR provides three patterns that COCONUT (Dec 2024) adopted:

1. **Learnable thought-delimiter tokens.** `<bot>` / `<eot>` is a verbatim descendant of `<start-thought>` / `<end-thought>`.
2. **Internal rationales during pretraining.** Quiet-STaR actually did this with discrete thoughts; COCONUT only mentions continuous-thought pretraining as future work (which [[Adaptive Latent CoT Pretraining]] is the first to attempt).
3. **Per-token granularity.** Quiet-STaR generates a rationale at every token; every COCONUT descendant uses one latent block per prompt. Per-token latent thinking is an open design direction that Quiet-STaR already validated with discrete thoughts.

## See also
- [[Quiet-STaR]] — canonical source page.
- [[Pause Tokens]] — orthogonal "insert blank tokens" approach.
- [[COCONUT]] — continuous-thought descendant.
- STaR (Zelikman 2022, NeurIPS) — parent paper; not ingested as separate source but referenced throughout.
