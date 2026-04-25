---
type: source
title: "Think before you speak: Training Language Models With Pause Tokens (Goyal et al. 2023)"
source_type: paper
arxiv_id: "2310.02226"
venue: "ICLR 2024"
date_published: 2023-10-03
authors:
  - "Sachin Goyal"
  - "Ziwei Ji"
  - "Ankit Singh Rawat"
  - "Aditya Krishna Menon"
  - "Sanjiv Kumar"
  - "Vaishnavh Nagarajan"
url: "https://arxiv.org/abs/2310.02226"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Append M (typically 10) learnable `<pause>` tokens to the input; delay output extraction until after the last pause. Pause token is a single learnable embedding (≈1024 extra parameters at 1B scale, 10⁻⁶ fraction)."
  - "Gains require BOTH pause-pretraining AND pause-finetuning (PausePT_PauseFT). Pause-finetuning on a standard-pretrained model yields minimal or negative gains. This is the paper's central empirical finding."
  - "Decoder-only 1B and 130M models trained with causal LM on C4. 9-task evaluation suite: reasoning, QA, general understanding, fact recall."
  - "1B model with PausePT_PauseFT: +18% SQuAD EM, +8% CommonsenseQA, +1% GSM8K — outperforms no-pause baseline on 8 of 9 downstream tasks."
  - "Mechanistic framing: pause tokens expand 'computational width' — K+M hidden-vector slots per layer instead of K — rather than depth. Frames latent reasoning as a horizontal (width) rather than vertical (depth) intervention."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "First LLM-scale demonstration that 'insert blank tokens → let the model use the extra compute' works. Canonical precursor to COCONUT's <bot>/<eot> special-token design and to Quiet-STaR's <start-thought>/<end-thought> tokens. Essential for genealogy."
  - slug: "branch-a"
    relevance: reference
    why: "Pause mechanism is a minimal baseline; 1B-scale results are taxonomic reference point pre-Qwen."
  - slug: "branch-b"
    relevance: reference
    why: "Not a BPTT/detach axis intervention."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Pause tokens are a null-content intervention; CPF introduces non-null content fusion. Useful contrast."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - family/pause-filler-tokens
  - type/source
  - status/historical
related:
  - "[[Filler Tokens]]"
  - "[[Quiet-STaR]]"
  - "[[COCONUT]]"
  - "[[Stepwise Internalization]]"
sources: []
---

# Pause Tokens — Think Before You Speak (Goyal et al. 2023)

## TL;DR

First LLM-scale demonstration of "insert M learnable blank tokens, delay output extraction, let the model use the extra forward-pass compute." 1B decoder with PausePT_PauseFT: +18% SQuAD, +8% CommonsenseQA. Central finding: pause-pretraining is *required* — finetuning alone doesn't work.

## Why this matters to our project

Pause Tokens is the most important pre-COCONUT latent-reasoning precursor at LLM scale. The core question it asks — "does extra non-linguistic compute at inference help reasoning?" — is exactly COCONUT's question one year earlier, with a much simpler intervention (null tokens instead of hidden-state feedback). COCONUT's ablation table directly compares to a Pause Token baseline and shows continuous-thought feedback clearly dominates (GSM8k 34.1% vs 16.4%), but pause tokens establish the *feasibility* of the entire line.

Two direct descendant design patterns:
1. **`<bot>` / `<eot>` special tokens** in COCONUT and CODI — directly inherit from the pause-token idea of "dedicated special tokens mark the latent-compute region."
2. **`<start-thought>` / `<end-thought>` in Quiet-STaR** — same design pattern, learnable delimiter pair.

## Method

**Pause-pretraining.**
- During causal LM pretraining on C4, append $M_{\text{PT}}$ pause tokens at random locations with probability $p_{\text{PT}}$.
- Mask the loss on pause tokens (so they don't contribute to cross-entropy).
- Single learnable `<pause>` embedding in vocabulary.

**Pause-finetuning.**
- For downstream tasks, append $M_{\text{FT}} = 10$ pause tokens to the prompt.
- Model's output is read *after* the last pause token.
- Fine-tune with task-specific loss.

**Inference.**
- Same: append $M=10$ pauses, extract output after the last pause.

## Results

**1B decoder, PausePT_PauseFT:**

| Task | Baseline | PausePT_PauseFT |
|------|----------|-----------------|
| SQuAD (EM) | — | +18% |
| CommonsenseQA | — | +8% |
| GSM8k | 7.5% | 8.5% |

Gains on 8 of 9 tasks. 130M model shows smaller but consistent improvements.

**Ablation — pause-pretraining is load-bearing:**
- PauseFT alone: minimal or *negative* gains.
- PausePT alone (pause only at pretraining): some gain but less than combined.
- PausePT_PauseFT: full gain.

## Framing: width, not depth

Goyal et al. explicitly frame pause tokens as expanding **computational width** — adding $M$ extra hidden-vector slots per layer, giving the model "finer distribution of attention across various parts of the supporting context." This is a subtly different framing from COCONUT's **depth**/recurrence framing (where continuous thoughts are fed back through the stack).

This framing is historically important because it establishes that *both* axes — width (pause/filler tokens) and depth (continuous-thought recycling) — are legitimate dimensions of latent compute expansion.

## Relevance to CODI / COCONUT contrast

Pause tokens are the **minimal** latent reasoning intervention. COCONUT adds: (i) feedback of hidden states instead of blank tokens, (ii) curriculum for progressive replacement of language steps. Comparing Pause Tokens to COCONUT on the same benchmark is the cleanest ablation of "does hidden-state content matter vs mere extra compute?" — COCONUT's answer is yes.

But Pause Tokens' pretraining-requirement finding is **under-explored** in COCONUT and CODI: neither paper pretrains the LLM with continuous-thought mode, they only fine-tune. Goyal's result predicts this is suboptimal; the COCONUT paper even mentions pretraining as a future direction. **This is a possible gap we could exploit.**

## Citation links to chase

- [[Filler Tokens]] (Pfau, Merrill, Bowman 2024) — companion paper; meaningless filler tokens can replicate CoT gains under specific conditions.
- [[Quiet-STaR]] (Zelikman 2024) — per-token rationale generation with similar special-token machinery.
- [[COCONUT]] — compares directly to Pause Token baseline.
