---
type: source
title: "Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking (Zelikman et al. 2024)"
source_type: paper
arxiv_id: "2403.09629"
venue: "COLM 2024"
date_published: 2024-03-14
authors:
  - "Eric Zelikman"
  - "Georges Harik"
  - "Yijia Shao"
  - "Varuna Jayasiri"
  - "Nick Haber"
  - "Noah D. Goodman"
url: "https://arxiv.org/abs/2403.09629"
code_repo: "https://github.com/ezelikman/quiet-star"
has_weights: true
status: read
confidence: high
key_claims:
  - "Quiet-STaR generates a short rationale (internal 'thought') at EVERY token during pretraining, not only at explicit question-answer boundaries. The rationale is produced between learnable `<start-thought>` and `<end-thought>` tokens."
  - "Tokenwise-parallel sampling: generate a rationale for each token in parallel via batched inference, then mix the rationale-prediction with the base-model next-token prediction via a learnable mixing head."
  - "REINFORCE-based learning: rationales are rewarded when their presence raises the likelihood of the subsequent ground-truth token. No external verifier or teacher needed — pure self-supervised."
  - "Base model Mistral-7B. After continued pretraining on internet text with Quiet-STaR: zero-shot GSM8K 5.9% → 10.9%, CommonsenseQA 36.3% → 47.2%. Zero fine-tuning on these tasks."
  - "Rationales disproportionately help difficult-to-predict tokens (high-entropy transitions); confirms 'spend compute where it's needed' intuition from ACT."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical 'implicit thought during pretraining' precursor; learnable <start-thought>/<end-thought> is the direct ancestor of COCONUT's <bot>/<eot>. Load-bearing genealogy node and arguably the paper that *proves* latent-reasoning pretraining is feasible."
  - slug: "branch-a"
    relevance: secondary
    why: "Mistral-7B base model + zero-shot transfer to GSM8K; scaling-relevant data point for the Qwen scaling writeup."
  - slug: "branch-b"
    relevance: reference
    why: "No BPTT/detach axis; tokenwise-parallel sampling is a different axis of concern."
  - slug: "branch-c"
    relevance: secondary
    why: "Per-token rationale mixing is a probe-relevant signal: each token has an associated latent thought that can be inspected."
  - slug: "branch-d"
    relevance: reference
    why: "Mixing-head is conceptually adjacent to CPF's fusion; worth citing."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - family/thought-tokens
  - method/reinforce
  - method/pretraining
  - type/source
related:
  - "[[Pause Tokens]]"
  - "[[COCONUT]]"
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[Filler Tokens]]"
sources: []
---

# Quiet-STaR (Zelikman et al. 2024)

## TL;DR

Self-supervised pretraining recipe that teaches a base LM to generate internal rationales at every token, rewarded via REINFORCE when the rationale increases next-token likelihood. Mistral-7B: GSM8K 5.9% → 10.9% (zero-shot, no task fine-tuning).

## Why this matters to our project

Quiet-STaR is the *pretraining-scale* latent-reasoning precursor to COCONUT. It establishes three patterns COCONUT inherits almost verbatim:

1. **Learnable thought-delimiter tokens.** `<start-thought>` and `<end-thought>` are the direct inspiration for COCONUT's `<bot>` and `<eot>`.
2. **Latent thoughts during pretraining.** Quiet-STaR trains thoughts at pretraining; COCONUT (Dec 2024) mentions pretraining with continuous thoughts as future work (which is still open — [[Adaptive Latent CoT Pretraining]] is the first to try it). Quiet-STaR *already does* it with discrete thoughts.
3. **Per-token thought.** Quiet-STaR generates a rationale at every token; most 2024-2026 latent-reasoning methods (COCONUT, CODI, LT-Tuning, KaVa) use *per-question* (one latent block per prompt). Quiet-STaR's per-token granularity is a road *not* taken in the COCONUT descendants.

## Method

**Structure.**
```
[context] <start-thought> [rationale tokens] <end-thought> [continues]
```

**Training loop.**
1. Sample token position $t$.
2. Generate rationale $r_t$ of length $T$ conditioned on $x_{\leq t}$.
3. Compute $P_{\text{mixed}}(x_{t+1}) = m \cdot P_{\text{base}}(x_{t+1} | x_{\leq t}) + (1 - m) \cdot P_{\text{rationale}}(x_{t+1} | x_{\leq t}, r_t)$ with learnable mixing weight $m$.
4. Compute reward = $\log P_{\text{mixed}}(x_{t+1}^{\text{true}}) - \log P_{\text{base}}(x_{t+1}^{\text{true}})$.
5. REINFORCE gradient on rationale, backprop through mixing head.

**Tokenwise-parallel sampling.** Key engineering trick: generate rationales for *all* positions in parallel by batching with appropriate attention masks. Without this, per-token rationale generation is prohibitive.

## Results

**Mistral-7B base, post-Quiet-STaR continued pretraining on internet text:**
- GSM8K zero-shot: 5.9% → 10.9% (+5.0).
- CommonsenseQA zero-shot: 36.3% → 47.2% (+10.9).
- Perplexity improvement concentrated on high-entropy natural tokens.

**No fine-tuning on these tasks.** The gain comes entirely from the Quiet-STaR pretraining extension.

## Relevance to CODI / COCONUT contrast

- **Thoughts per-token vs per-question.** Quiet-STaR is per-token; COCONUT is per-question (one `<bot>`...`<eot>` block per prompt). This is a *fundamental architecture choice* that has not been systematically ablated.
- **Discrete thoughts vs continuous thoughts.** Quiet-STaR uses discrete text tokens; COCONUT uses continuous hidden states. Continuous is arguably more expressive (encodes superposition of next steps, per COCONUT's BFS claim); discrete is interpretable.
- **Training regime.** Quiet-STaR is REINFORCE-based self-supervised pretraining; COCONUT is staged curriculum distillation. Both are fundamentally different from CODI's single-stage self-distillation.

Quiet-STaR suggests an obvious direction: *combine per-token latent thought with continuous feedback*. This is an open design not yet tried at scale.

## Citation links to chase

- STaR (Zelikman 2022) — parent paper; rationale-bootstrapping for single QA.
- [[Pause Tokens]] (Goyal 2023) — width-based precursor.
- [[COCONUT]] — curriculum-based descendant.
- [[CODI]] — self-distillation descendant.
