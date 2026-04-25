---
type: source
title: "Think-at-Hard: Selective Latent Iterations"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/architecture
  - method/lora
  - method/adaptive-compute
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
  - "[[Adaptive Exit Gate]]"
sources:
  - "[[.raw/papers/2511.08577-think-at-hard]]"

source_type: paper
arxiv_id: "2511.08577"
venue: "arXiv"
date_published: 2025-11-11
authors:
  - "Tianyu Fu"
  - "Yichen You"
  - "Zekai Chen"
  - "Guohao Dai"
  - "Huazhong Yang"
  - "Yu Wang"
url: "https://arxiv.org/abs/2511.08577"
code_repo: "https://github.com/thu-nics/TaH"
has_weights: false
status: read
confidence: high
key_claims:
  - "Fixed-depth recurrent transformers suffer 'latent overthinking': easy tokens correct after pass 1 are revised into errors at additional iterations — uniform iteration causes more errors than corrections."
  - "Think-at-Hard (TaH) gates extra iterations per-token via a lightweight MLP decider; only ~6% of tokens receive a second iteration."
  - "LoRA adapters applied only at iterations d>1 shift the objective from general next-token prediction to focused hard-token refinement without touching pass-1 accuracy."
  - "Duo-causal attention extends causality to BOTH token sequence AND iteration-depth dimensions, preserving full sequence parallelism while allowing cross-iteration flow."
  - "On Qwen3-0.6B base: TaH gives 35.2 vs 31.2 baseline avg across GSM8K/MATH500/AMC23/AIME25/OlympiadBench; on Qwen3-1.7B: 52.8 vs 47.8. 4.0-5.0% avg gain at same param count vs Qwen3-SFT-same-data baselines."
  - "With <3% extra params (LoRA + decider), gains reach 5.3-5.4% over strong Qwen3 baselines and 8.5-12.6% over uniform-2-iter baselines."

projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Uses Qwen3-0.6B/1.7B base — EXACT Qwen-family backbone Branch A studies. Results show looping + adaptive-compute training works on Qwen3; complements the architecture-dependent scaling question."
  - slug: "branch-b"
    relevance: reference
    why: "LoRA-only second-iter modifier is another form of parameter-sharing / compute-adding; orthogonal to detach/fp32 concerns."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool."
  - slug: "branch-d"
    relevance: secondary
    why: "Token-level adaptive-depth + LoRA adapter shift during latent iterations is a CHEAP alternative path to LT-Tuning-style curriculum — worth comparing as a 'minimum-intervention' version of fusion-anchored latents."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Public code + Qwen3 base is attractive, but looping-style adaptive-depth is not on the V2 / SIM-CoT / LT-Tuning synthesis line; strong taxonomic reference for the 'selective per-token iteration' branch and a plausible downstream experiment."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Think-at-Hard: Selective Latent Iterations

## TL;DR

Recurrent/looped transformers that iterate every token fall into **latent overthinking**: easy tokens get correct after pass 1, then revised to errors. **TaH** gates latent iterations with a lightweight neural decider (only ~6% of tokens re-iterate), shifts the iteration objective via **LoRA adapters** (d>1 only), and uses **duo-causal attention** (causal across both sequence and depth dimensions). On Qwen3-0.6B/1.7B: 4-5% avg gain at same-param over Qwen3 SFT, 8-12% over uniform-2-iter baselines.

## Phenomenon: Latent Overthinking

- Figure 1 in paper shows: when all tokens iterate, the set of *corrections* (wrong→right) is smaller than the set of *revisions* (right→wrong) on easy tokens.
- Implication: extra compute should be allocated, not uniform.

## Architecture

### Neural decider

- Lightweight MLP.
- Input: concatenated hidden states.
- Output: continuation probability c^i(d) ∈ [0,1] per token i at depth d.
- Gates whether this token gets another iteration.

### LoRA for iteration-specific objective

- LoRA adapters applied **only at iterations d>1**.
- Shift base LLM objective from general next-token to focused hard-token refinement.
- Pass 1 is untouched — preserves baseline accuracy.
- <3% extra parameters.

### Duo-causal attention

- Standard causal: attend to earlier positions (j ≤ i).
- Duo-causal: attend to earlier positions AND shallower iteration depths: X≤i(≤d) = {xj(k) | j ≤ i, k ≤ d}.
- Preserves sequential parallelism.
- Enables cross-iteration info flow without breaking attention mask parallelism.

## Training

- **Base:** Qwen3-0.6B-Base, Qwen3-1.7B-Base.
- **Data:** Math subset of Open-R1 (~300M tokens after filtering responses > 8192 tokens).
- **LR:** 4e-5; 5 epochs, cosine scheduler.
- **Two-stage:**
  1. Backbone supervision under oracle policy π (which tokens should iterate).
  2. Decider imitation learning, backbone frozen.

## Results

Accuracy across 5 benchmarks (GSM8K, MATH500, AMC23, AIME25, OlympiadBench):

| Model | GSM8K | MATH500 | AMC23 | AIME25 | Olymp | Avg |
|---|---|---|---|---|---|---|
| Qwen3-0.6B | 62.5 | 47.2 | 23.4 | 4.2 | 18.8 | 31.2 |
| **TaH (0.6B)** | 64.4 | 51.2 | 32.5 | 4.2 | 23.9 | **35.2** |
| **TaH+ (0.6B)** | 68.8 | 54.2 | 30.6 | 5.0 | 24.0 | **36.5** |
| Qwen3-1.7B | 82.1 | 68.4 | 42.2 | 13.3 | 33.0 | 47.8 |
| **TaH (1.7B)** | 84.5 | 74.4 | 48.4 | 17.9 | 38.8 | **52.8** |
| **TaH+ (1.7B)** | 85.8 | 73.0 | 51.2 | 14.6 | 41.2 | **53.2** |

- 4.0-5.0% avg gain over Qwen3-SFT same-data baseline at 0 extra params (base TaH).
- 5.3-5.4% gain with <3% extra params (TaH+).
- 8.5-12.6% vs uniform-2-iter baseline.
- Only **~6% of output tokens** trigger second iteration.

## Relevance

- **Qwen3 connection:** Direct evidence that token-level adaptive-depth looping works on Qwen3-0.6B/1.7B, which strengthens (not resolves) the Branch A question of architecture-dependent latent reasoning. TaH is a looping intervention that DOES work on Qwen3, vs our observation that Gemma-3-style Q/K RMSNorm changes matter for CODI.
- **Cheap vs Ouro / Parcae:** 300M tokens on 2× Qwen3 scale is within our budget, unlike Ouro's 7.7T-token pretraining or Parcae's 1.3B from-scratch.
- **Complementary to LT-Tuning:** TaH uses LoRA to shift iteration-level objective; LT-Tuning uses CPF + curriculum to anchor latents. Could plausibly be composed: apply LT-Tuning curriculum, then TaH selective-iteration on top.
- **Latent overthinking** is a new named failure mode to track — may apply to CODI when we push latent-token count high.

## Cross-links

- [[Ouro]] — TaH's selective-iter is a finer-grained version of Ouro's adaptive exit gate.
- [[Adaptive Exit Gate]] — similar mechanism at coarser (full-depth) granularity.
- [[LoopLM]] — same architectural family.
