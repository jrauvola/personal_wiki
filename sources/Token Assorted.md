---
type: source
title: "Token Assorted — Mixing Latent and Text Tokens for Improved Language Model Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/vq-vae
  - method/hybrid-tokens
  - method/cot-compression
status: read
related:
  - "[[COCONUT]]"
  - "[[CoLaR]]"
  - "[[KaVa]]"
  - "[[Token Efficiency]]"
  - "[[Curriculum Distillation]]"
sources:
  - "[[.raw/papers/2502.03275-token-assorted]]"
source_type: paper
arxiv_id: "2502.03275"
venue: "arXiv"
date_published: 2025-02-05
authors:
  - "DiJia Su"
  - "Hanlin Zhu"
  - "Yingchen Xu"
  - "Jiantao Jiao"
  - "Yuandong Tian"
  - "Qinqing Zheng"
url: "https://arxiv.org/abs/2502.03275"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Token Assorted compresses the prefix of a CoT trace into discrete latent tokens from a VQ-VAE codebook (codebook size 1024, compression r=16, chunk L=16) and leaves the suffix as text, extending the LLM vocabulary with unseen latent token IDs."
  - "Randomized replacement (varying m per sample, not a fixed curriculum) accelerates adaptation to new latent tokens and outperforms multi-stage curriculum (Coconut / iCoT style)."
  - "Llama-3.2-1B on MATH: +4.2% accuracy vs CoT baseline; Llama-3.2-3B on GSM8K: +4.1%; Llama-3.1-8B on Fresh-Gaokao-Math-2023: +13.3% — with a 17% average reduction in reasoning-trace length."
  - "Left-to-right (AR) replacement of the leftmost m CoT tokens outperforms subsampling tokens at different locations."
  - "Partial replacement with <boLatent> / <eoLatent> delimiters is critical; whole-sequence projection to latent space (as in prior planning works) underperforms."
  - "VQ-VAE is trained on the entire input sequence X = P ⊕ C ⊕ S but applied only to C during reasoning — training on the full context produces better latent codes than training only on CoT."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Discrete-latent alternative to continuous-CoT; Llama-3.1-8B result provides an 8B-scale data point for architecture-dependence comparisons."
  - slug: "branch-b"
    relevance: reference
    why: "VQ-VAE latent codes are not the BPTT/detach axis under study."
  - slug: "branch-c"
    relevance: reference
    why: "Probe methodology unrelated."
  - slug: "branch-d"
    relevance: secondary
    why: "Randomized-m single-stage training is a simpler alternative to the 3-stage LT-Tuning curriculum — worth citing as a contrast: does structured curriculum still help when latent tokens are discrete rather than continuous?"
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical hybrid latent+text reasoning method; taxonomic reference for 'discrete latent token' branch alongside COCONUT's 'continuous latent' branch."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Token Assorted

> [!contradiction] Randomized-m vs [[Capabilities and Limits of Latent CoT]] + [[ALiCoT]]
> This paper ablates and finds randomized-m single-stage training OUTPERFORMS multi-stage curriculum (Coconut/iCoT). [[Capabilities and Limits of Latent CoT]] proves curriculum is theoretically necessary to traverse Exploration-Execution trade-off; [[ALiCoT]] (round-2 crawl) proves Order-r alignment is also theoretically necessary for irreducible problems. Possible reconciliation: Token Assorted uses DISCRETE latent tokens (VQ-VAE codes); both theoretical necessity results may apply specifically to continuous latents where distributional mismatch is the failure mode. [[Soft Tokens Hard Truths]] makes the sibling argument for continuous latents via RL. Three-way cluster: theorem says "necessary", empirics from two different latent regimes say "not necessary".

## TL;DR

Hybrid reasoning: compress the first m tokens of a CoT trace into discrete latent tokens from a VQ-VAE codebook, leave the suffix as text. Extend the LLM vocabulary with latent token IDs, fine-tune with randomized m (single-stage, not curriculum). Gains +4.1 / +4.2 / +13.3% on GSM8K / MATH / Fresh-Gaokao-Math-2023 for Llama-3.2-1B/3B/3.1-8B, with 17% trace length reduction.

## Method

Two-stage training.

**Stage 1 — Learn latent abstractions (VQ-VAE):**
- Codebook E of 1024 vectors in R^d.
- Encoder f_enc: chunk X (length L=16) → L/r=1 latent vector.
- Quantization q: nearest-neighbor lookup in codebook.
- Decoder f_dec reconstructs the text chunk conditioned on prompt embedding.
- Loss = reconstruction + VQ loss + β·commitment loss.
- Trained on the full input X=P⊕C⊕S (prompt + CoT + solution), but applied only to C in Stage 2.

**Stage 2 — Hybrid fine-tuning:**
- Replace leftmost m tokens of C with latent abstractions, leaving C[m:] as text.
- Extend LLM vocabulary with unseen latent token IDs, initialize their embeddings.
- Wrap the replaced region with `<boLatent>` / `<eoLatent>` delimiters.
- Randomize m per sample during training (not a fixed curriculum over epochs).

## Recipe

- VQ-VAE: 100k steps, Adam lr=1e-5, batch 32, codebook 1024, compression r=16.
- LLMs: Llama-3.1 / 3.2 family; T5 / GPT-2 trained from scratch on synthetic benchmarks.
- Benchmarks: Keys-Finding Maze (planning), ProntoQA / ProsQA (logic), GSM8K / MATH (math in-domain), Fresh-Gaokao-Math-2023 / DeepMind-Math / College-Math / OlympiaBench-Math / TheoremQA (OOD).
- Baselines: Sol-Only, CoT, iCoT (Deng et al. 2024), Pause Token (Goyal et al. 2023).

## Results

**Math (fine-tuning from Llama):**
- Llama-3.2-1B on MATH: +4.2% vs CoT.
- Llama-3.2-3B on GSM8K: +4.1%.
- Llama-3.1-8B on Fresh-Gaokao-Math-2023: +13.3%.
- Average trace length reduction: 17%.

**Planning/Logic (trained from scratch):**
- Outperforms CoT, iCoT, Pause Token on Keys-Finding Maze, ProntoQA, ProsQA.

**Ablation findings:**
- Partial > whole replacement.
- Left-to-right > subsample.
- Randomized m > curriculum on m.

## Relevance to our project

Relevant for [[spar-latent-reasoning]] as a canonical reference for the *discrete* latent-token branch of compressed reasoning (contrast with COCONUT's continuous hidden-state recycling and LT-Tuning's CPF interpolation). The randomized-m ablation result is a direct challenge to LT-Tuning's staged curriculum claim: if discrete latent tokens don't need a staged curriculum, the case for staged curriculum in the continuous-latent case may rest specifically on the embedding-geometry mismatch (not on the token-drop schedule). Worth citing in Branch D's curriculum-ablation section as a counterexample. The Llama-3.1-8B result provides an 8B-scale data point relevant to Branch A's scaling writeup.

## Citation links to chase

- [[COCONUT]] (Hao et al. 2024) — direct comparison point.
- iCoT (Deng et al. 2024) — curriculum CoT-elimination baseline.
- Pause Token (Goyal et al. 2023) — latent-token baseline.
- Lehnert et al. 2024 (Searchformer) — VQ-VAE planning precedent.
