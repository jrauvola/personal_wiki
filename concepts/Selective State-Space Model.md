---
type: concept
title: "Selective State-Space Model (Mamba Selection Mechanism)"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/state-space-model
  - method/selective-recurrence
  - method/input-dependent-gating
status: developing
complexity: advanced
domain: state-space-model
aliases:
  - "Mamba selection"
  - "S6"
  - "Input-dependent SSM"
  - "Selective SSM"
related:
  - "[[Mamba]]"
  - "[[RWKV]]"
  - "[[Albert Gu]]"
  - "[[Gumbel-Softmax Latent]]"
  - "[[Latent Scratchpad Architecture]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The mechanism that demonstrates LSTM-style gating works at LLM scale (2.8B+ in Mamba; 14B+ in RWKV-style cousins). Direct underwriting of the LSTM analogy in the Latent Scratchpad page."
  - slug: "branch-d"
    relevance: primary
    why: "Selection IS a learned input-dependent gate over a parallel state-channel. Mamba's Theorem 1 explicitly shows the equivalence with LSTM gating - the architectural family Latent Scratchpad's emission gate belongs to."
  - slug: "branch-a"
    relevance: secondary
    why: "Alternative architecture for Qwen3-scale latent reasoning if attention-stream stability hits ceilings."
  - slug: "branch-b"
    relevance: secondary
    why: "Selective forgetting via Δ is a different framing for detach policy."
  - slug: "branch-c"
    relevance: reference
    why: "Architecture difference may complicate probe transfer."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Selective State-Space Model (Mamba Selection Mechanism)

The mechanism by which Mamba (Gu & Dao 2023) overcame the fundamental weakness of prior linear state-space models: time-invariance. By making the SSM parameters `(A, B, C, Δ)` **functions of the input** `x_t`, Mamba turns a constant-coefficient recurrence into a content-aware one. **Selectivity = the gate that decides what to keep, what to forget, and what to attend to per-token.**

## The selection equations

Standard time-invariant SSM (S4):
```
h_t = A h_{t-1} + B x_t
y_t = C h_t
```
where A, B, C are constant. This **cannot solve selective copy or induction-heads** because constant dynamics treat every token identically.

Selective SSM (S6, what Mamba uses):
```
s_B(x) = Linear_N(x)
s_C(x) = Linear_N(x)
s_Δ(x) = Broadcast_D(Linear_1(x))
τ_Δ = softplus
```
where B(x), C(x), Δ(x) are now input-dependent functions. After discretization:
```
Ā(t), B̄(t) ← discretize(Δ(x_t), A, B(x_t))
h_t = Ā(t) h_{t-1} + B̄(t) x_t
y_t = C(x_t) h_t
```

## Theorem 1 (the gating equivalence)

This is the load-bearing theorem for connecting Mamba to LSTM-style gating. **For the special case N=1, A=-1, B=1, the selective SSM recurrence reduces to:**

```
g_t = σ(Linear(x_t))
h_t = (1 − g_t) h_{t-1} + g_t · x_t
```

The Mamba paper states verbatim:

> "the discretization is the principled foundation of heuristic gating mechanisms"

In other words: **input-dependent Δ + softplus discretization IS the LSTM forget gate, mathematically identified.** Mamba's selection mechanism subsumes (and at scale, supersedes) the gated-recurrence vocabulary that LSTMs introduced in 1997.

## Why selection beats time-invariance

Two diagnostic tasks separate selective from constant SSMs:

- **Selective Copy** — must filter irrelevant tokens between targets at varying gaps. Time-invariant `(Ā, B̄)` cannot conditionally copy or skip; selective Δ(x) can.
- **Induction Heads** — remember token X, predict Y when X reappears. Selective C(x) gates the read; constant C cannot.

Empirical result: Mamba trained at length 256 generalizes to **2^20 = 1M tokens (4000×)**; attention generalizes only 2×; H3/Hyena fail completely.

## Why this concept matters for Latent Scratchpad

The W3.5 Latent Scratchpad emission gate is in **the same architectural family** as Mamba's selection mechanism:

| Property | Mamba selection | Latent Scratchpad emission |
|---|---|---|
| Gate input | `x_t` (current token) | `h_t` (current latent state) |
| Gate parametrization | `s_Δ(x) = Broadcast_D(Linear_1(x))` then softplus | `gate_proj(h)` then sigmoid (or Gumbel-STE Bernoulli) |
| Decision | Continuous: how much to forget vs. accept | Discrete: emit a note vs. pass through |
| Effect on state | Filters / weights state update | Routes signal to parallel scratchpad channel |
| Scale validated | 2.8B (Mamba), 14B (RWKV-cousin) | TBD (W3.5 target: 4B Qwen3) |

**The structural lesson:** input-dependent gates work at LLM scale. The 2.8B Mamba result is the strongest published evidence that W3.5's gate parametrization (a learned input-dependent decision over per-position behavior) is not LSTM-era nostalgia — it's the dominant mechanism in modern non-attention LLM architectures.

## Hardware-aware implementation lessons

Mamba's parallel-scan implementation handles the recurrence efficiently:

- **Kernel fusion:** load (Δ, A, B, C) from HBM to SRAM once; discretize and recur in SRAM; write final output.
- **Parallel scan:** work-efficient parallel scan algorithm gives O(log L) span despite recurrence.
- **Recomputation:** don't store intermediate states for backward pass; recompute.

Result: same memory cost as FlashAttention. **For W3.5:** scratchpad gate evaluation per latent position is sequential (must check budget after each), so similar techniques apply if scratchpad scales beyond K_budget = 3.

## Sources

- [[Mamba]] — Gu & Dao 2023 source paper.
- [[RWKV]] — paired modern validation at 14B.
- [[Albert Gu]] — entity page (also S4 author; also covers Tri Dao co-author + FlashAttention).
- [[Latent Scratchpad Architecture]] — concept page where the analogy is invoked.
