---
type: source
title: "Mamba: Linear-Time Sequence Modeling with Selective State Spaces (Gu & Dao 2023)"
source_type: paper
arxiv_id: "2312.00752"
venue: "arXiv (later COLM 2024)"
date_published: 2023-12-01
authors:
  - "Albert Gu"
  - "Tri Dao"
url: "https://arxiv.org/abs/2312.00752"
code_repo: "https://github.com/state-spaces/mamba"
has_weights: true
status: read
confidence: high
key_claims:
  - "Selective State-Space Model (S6) makes A, B, C, Δ functions of the input x_t (s_B(x) = Linear_N(x), s_C(x) = Linear_N(x), s_Δ(x) = Broadcast_D(Linear_1(x)) with τ_Δ = softplus). This input-dependence is the key mechanism: time-invariant SSMs cannot solve selective copy or induction-heads tasks."
  - "Theorem 1: when N=1, A=-1, B=1, the recurrence reduces to a gated RNN: g_t = σ(Linear(x_t)); h_t = (1 - g_t) h_{t-1} + g_t x_t. Discretization is the principled foundation of heuristic gating mechanisms - so selective SSMs ARE generalized gated recurrent networks."
  - "Hardware-aware parallel scan: kernel fusion (load Δ,A,B,C from HBM to SRAM, discretize and recur in SRAM), parallel scan, recomputation. Achieves same memory cost as FlashAttention transformer."
  - "Trained 130M / 370M / 790M / 1.4B / 2.8B param Mamba on 300B Pile tokens. Mamba-1.4B: 6.80 Pile val ppl (Pythia-1.4B: 7.51, RWKV-1.5B: 7.70). Mamba-2.8B: 6.22 ppl, 63.3% avg zero-shot - matches Pythia 2x its size."
  - "Inference: 5x higher throughput than transformers (recurrent mode, no KV cache). Selective copy extrapolation: trained at length 256, generalizes to 2^20 = 1M tokens (4000x), while attention generalizes only 2x and H3/Hyena fail completely."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The flagship validation that input-dependent gating mechanisms work at LLM scale. Mamba demonstrates LSTM-like gating ideas survive to the multi-billion-parameter regime, directly underwriting the LSTM analogy in the Latent Scratchpad page."
  - slug: "branch-d"
    relevance: primary
    why: "Mamba's selection mechanism IS a learned input-dependent gate over a parallel state-channel. This is the closest published analog to Latent Scratchpad's emission gate, validated at 2.8B."
  - slug: "branch-a"
    relevance: secondary
    why: "Alternative architectural family for Qwen3-scale latent reasoning if attention-based latents have stability ceilings."
  - slug: "branch-b"
    relevance: reference
    why: "Selective forgetting via Δ is a different way to slot 'detach' policy."
  - slug: "branch-c"
    relevance: reference
    why: "Same-family architecture; probe-protocol applies in principle."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/state-space-model
  - family/selective-ssm
  - family/gated-memory
  - type/source
  - status/foundational
related:
  - "[[Selective State-Space Model]]"
  - "[[Albert Gu]]"
  - "[[RWKV]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# Mamba: Linear-Time Sequence Modeling with Selective State Spaces

## TL;DR

State-space models (SSMs) failed prior to Mamba because their A, B, C matrices were time-invariant — they couldn't selectively attend to or forget specific tokens. Mamba makes the SSM parameters input-dependent (the selection mechanism) and validates that this is the key missing ingredient. Result: linear-time-and-memory recurrence that beats transformers up to 2.8B params on language modeling.

## Why this matters for the Latent Scratchpad

Mamba is **the strongest scale validation** for the LSTM analogy in [[Latent Scratchpad]]. The user's intuition — "this is like LSTMs-vs-RNNs — gates that let us store information somewhere else besides the KV cache" — is **exactly** what Mamba demonstrates at 2.8B params. Theorem 1 in the paper makes the equivalence explicit: Mamba's Δ-discretization, when reduced to N=1, A=-1, B=1, **becomes** the LSTM-style gate `h_t = (1 − g_t) h_{t-1} + g_t x_t`.

This is the load-bearing reference for: "input-dependent gates are not LSTM-era artifacts; they survive and dominate at 2.8B scale."

## Method (verbatim equations from §3)

**Selection mechanism:** parameters become functions of the input.
```
s_B(x) = Linear_N(x)
s_C(x) = Linear_N(x)
s_Δ(x) = Broadcast_D(Linear_1(x))
τ_Δ = softplus
```

**Discretized recurrence with selection** (S6):
```
Ā(t), B̄(t) ← discretize(Δ(x_t), A, B(x_t))
h_t = Ā(t) h_{t-1} + B̄(t) x_t
y_t = C(x_t) h_t
```

**Theorem 1 (gating equivalence):** for N=1, A=-1, B=1, the recurrence becomes
```
g_t = σ(Linear(x_t))
h_t = (1 − g_t) h_{t-1} + g_t x_t
```
which is the canonical LSTM/GRU gate. The paper states this explicitly:
> "the discretization is the principled foundation of heuristic gating mechanisms"

## Why selection is the key mechanism

Two diagnostic tasks separate selective from time-invariant SSMs:

- **Selective Copy:** must filter irrelevant tokens between targets. Time-invariant SSMs fail because their constant `(Ā, B̄)` transitions cannot let them select the correct information.
- **Induction Heads:** must remember token X, then predict Y when X reappears. Time-invariant SSMs cannot selectively suppress intervening noise.

Selection extrapolates dramatically: trained at length 256, Mamba generalizes to **2^20 = 1M tokens (4000×)**, while attention extrapolates only 2× and H3/Hyena fail completely (Figure 5).

## Hardware-aware implementation

- **Kernel fusion**: load (Δ, A, B, C) from HBM to SRAM once, discretize and recur in SRAM, write final output. No per-step intermediate state writes.
- **Parallel scan**: a work-efficient parallel scan algorithm gives O(log L) span despite the recurrence dependency.
- **Recomputation**: don't store intermediate states for backward; recompute. Memory cost matches FlashAttention.

## Scale and results

| Model | Params | Tokens | Pile val ppl |
|---|---|---|---|
| Mamba-130M | 130M | 300B | — |
| Mamba-370M | 370M | 300B | — |
| Mamba-790M | 790M | 300B | — |
| Mamba-1.4B | 1.4B | 300B | **6.80** (Pythia: 7.51, RWKV: 7.70) |
| Mamba-2.8B | 2.8B | 300B | **6.22** (Pythia: 6.73) |

- Zero-shot avg: Mamba-1.4B 59.7%, Mamba-2.8B 63.3% — matches Pythia-2× its size.
- Inference: **5× higher throughput than transformers** (recurrent mode, no KV cache).
- DNA: 3-4× fewer parameters for equivalent perplexity vs. HyenaDNA.
- SC09 audio FID: Mamba-6.1M = 0.94 (SaShiMi-baseline 1.99); Mamba-24.3M = 0.67.

## Failure modes / limitations

- **Continuous-discrete tradeoff:** SSMs were originally for continuous-time data; selection improves discrete (text, DNA) but "may conversely impede performance on data that LTI SSMs excel on."
- **Scaling uncertainty:** experiments capped at 2.8B. Authors note: "remains to assess whether Mamba still compares favorably at these larger sizes" (7B+).
- **No selection mechanism for cross-sequence retrieval** — Mamba is a same-stream selective filter, not a separate-channel write.
- **Affordance gap:** no published recipes for LoRA, instruction-tuning, RLHF on Mamba-base.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the input-dependent gate parametrization.** Mamba's `s_Δ(x) = Broadcast_D(Linear_1(x))` projects to a single scalar then broadcasts — exactly the right shape for a per-position emission gate. **BORROW: softplus-on-Δ** as a stable parametrization for a positive scale-like gate quantity. **BORROW: the kernel-fusion idea** if scratchpad sequence handling becomes a bottleneck (probably not at K_budget=3). **ADAPT: the equivalence Theorem 1 framing** — the W3.5 gate is structurally identical to a Mamba single-channel selective gate with N=1, A=-1, B=1, applied to the emission decision rather than the state-update.

## Citation links to chase

- [[Selective State-Space Model]] — concept page formalizing the selection mechanism.
- [[Albert Gu]] — entity page.
- [[RWKV]] — closely-related linear-attention + gating.
- [[Latent Scratchpad]] — idea page (LSTM analogy validated by Mamba).
