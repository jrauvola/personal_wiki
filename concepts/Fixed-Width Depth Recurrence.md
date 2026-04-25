---
type: concept
title: "Fixed-Width Depth Recurrence"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/architecture
  - domain/latent-reasoning
status: seed
related:
  - "[[LoopLM]]"
  - "[[Ouro]]"
  - "[[Parcae]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[From Growing to Looping]]"
  - "[[Think-at-Hard]]"
  - "[[Adaptive Loops and Memory]]"
sources:
  - "[[Ouro]]"
  - "[[Parcae]]"

complexity: intermediate
domain: architecture
aliases:
  - "Weight-Tied Depth Loop"
  - "Same-Position Recurrence"

projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Defines the compute axis of looped-LM reasoning that doesn't grow sequence length — useful framing distinction across the literature."
  - slug: "branch-a"
    relevance: not-applicable
    why: ""
  - slug: "branch-b"
    relevance: reference
    why: "Gradient backward-chain length is bounded by depth × loops; 'reduce loops for stability' is architecturally analogous to detach."
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "branch-d"
    relevance: reference
    why: "Clear contrast to CODI/COCONUT sequence-growing latents; could in principle be ported to LT-Tuning (reuse positions instead of appending)."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Fixed-Width Depth Recurrence

A way to add compute to a transformer forward pass without growing sequence length or parameter count: apply the full transformer stack `t` times to the **same** token positions, with weights tied across iterations.

## Signature

Forward pass:

$$h^{(0)} = \text{emb}(x); \quad h^{(i)} = M_L(h^{(i-1)}) \quad \text{for } i = 1 \ldots t; \quad y = \text{lmhead}(h^{(t)})$$

- **Width fixed:** token positions, hidden dim, KV cache layout all unchanged across iterations.
- **Depth effective:** at step `t`, the network has effectively `t × L` sequential transformer-layer applications but only `L` distinct parameter sets.

## Two-dimensional compute budget

Unlike standard transformers (one knob: parameter count) or CODI-style latent CoT (one knob: number of extra `<bot>` tokens), fixed-width depth recurrence gives **two independent compute knobs**:

1. **N** — parameters.
2. **T** — recurrent steps per forward pass.

Scaling laws (Ouro App. D) fit the three-knob joint L(N, D, T) with R² ≈ 0.96.

## Where it lives in the taxonomy

- **Parameter-sharing axis:** shares weights across depth (like Universal Transformer, ALBERT — but ALBERT ties across equal-width layers of a fixed-depth stack; LoopLM re-applies the whole stack).
- **Compute axis:** adds FLOPs without adding tokens (unlike CODI/COCONUT).
- **KV-cache axis:** cache entries represent the same positions, iteratively refined (unlike latent-CoT where each iteration adds a cache slot).

## Practical consequences

- **Prefill cost:** 4× (each step needs own KV cache — can't share at prefill without catastrophic drop; Ouro Table 14: GSM8K 78.92 → 18.73 if first-step cache shared).
- **Decoding cost:** ~1× with last-step KV cache (representations at step T dominate generation).
- **Gradient chain length:** bounded by `T × L`. Reducing T shortens BPTT — Ouro's 8→4 reduction removed loss spikes without any detach.
- **Extrapolation:** brittle — performance peaks at trained T; degrades past. Not truly "adaptive depth at inference" unless paired with [[Adaptive Exit Gate]].

## Openings it creates

- Could be applied on top of an existing pretrained model by running its stack twice (untrained-loop analog of a prompt cache), but Ouro suggests this only works cleanly when baked into pretraining.
- Mixing with CODI: reuse positions of a latent span instead of appending tokens for each latent step — speculative, no paper does it yet.

## Updated landscape (from Ouro crawl)

- **Stability:** [[Parcae]] shows constraining ρ(Ā) < 1 via negative-diagonal parameterization prevents residual explosion WITHOUT reducing recurrent depth — an architectural alternative to Ouro's 8 → 4 step reduction.
- **Cheaper construction path:** [[From Growing to Looping]] shows depth-grown models can be inference-time-looped on middle blocks to recover ~2× on reasoning primitives without from-scratch looped pretraining (much cheaper than Ouro).
- **Fine-grained variant:** [[Think-at-Hard]] does selective per-token iteration on Qwen3 — only 6% of tokens get a second iteration, via a lightweight neural decider + LoRA adapters for d>1.
- **Mechanistic substrate:** [[Mechanistic Analysis of Looped Reasoning LMs]] shows recurrent blocks converge to *distinct per-layer fixed points* forming a cyclic trajectory; Ouro drifts past T_train while retrofitted Llama stays stable to T=128.
- **Train-time backward-chain budget:** Parcae uses μ_bwd = ⌈μ_rec/2⌉ truncated BPTT — the scaling-law-aware analog of our detach-at-k ablation.
