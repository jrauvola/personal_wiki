---
type: concept
title: "LoopLM"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/architecture
  - domain/latent-reasoning
status: seed
related:
  - "[[Ouro]]"
  - "[[Fixed-Width Depth Recurrence]]"
  - "[[Adaptive Exit Gate]]"
  - "[[Parcae]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[From Growing to Looping]]"
  - "[[RLTT]]"
  - "[[Think-at-Hard]]"
  - "[[Formal CoT vs Latent]]"
  - "[[Adaptive Loops and Memory]]"
  - "[[Step-Decomposed Influence]]"
sources:
  - "[[Ouro]]"
  - "[[Parcae]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"

complexity: intermediate
domain: architecture
aliases:
  - "Looped Language Model"
  - "Loop-LM"

projects:
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Framework-level anchor for comparing depth-recurrent latent reasoning to sequence-growing latent CoT (CODI/COCONUT)."
  - slug: "branch-a"
    relevance: not-applicable
    why: ""
  - slug: "branch-b"
    relevance: reference
    why: "Conceptual parallel: reducing loop depth is the stability analog of detaching the backward chain."
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "branch-d"
    relevance: reference
    why: "Contrast point: fixed-width depth recurrence vs CODI sequence-growing latents."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# LoopLM

Framework for language models that apply the full transformer stack `t` times to the **same token positions**. Instantiated by [[Ouro]] (the specific 1.4B / 2.6B model family).

## Definition

$$F^{(t)}(x) = \text{lmhead} \circ \underbrace{M_L \circ M_L \circ \cdots \circ M_L}_{t \text{ times}} \circ \text{emb}(x)$$

Where `M_L` is a stack of L transformer layers. Weight-tied across loop iterations — "depth recurrence," no new parameters per loop.

## Contrast with neighbors

| Family | Extra compute lives in | Sequence length grows? | Params added? |
|--------|------------------------|------------------------|---------------|
| **LoopLM** | Re-applying stack to same positions | **No** | No (weight-tied) |
| CODI / COCONUT / KaVa | Latent tokens `<bot>...<eot>` appended | **Yes** | No (reuses base) |
| MoR (Mixture of Recursions) | Similar depth-loop family | No | No |
| Universal Transformer | Depth-shared layers + ACT halting | No | No |
| Dense transformer | Deeper stack (distinct params) | No | **Yes** |

## Core claims (from Ouro)

- At 1.4B/2.6B, matches 2-3× larger dense transformers on reasoning benchmarks.
- Gains concentrate on **knowledge manipulation**, not memorization (Capo ≈ 2 bits/param regardless of loops; Mano gains dominant — see [[Manipulation vs Capacity]]).
- Full BPTT through all recurrent iterations is feasible but requires shortened depth for stability (8 → 4).
- Performance **peaks at trained depth**, degrades beyond (no free extrapolation).

## Why it's a useful cross-reference anchor

Any future paper on:
- depth-recurrent / weight-tied inference
- halting / adaptive compute
- continuous vs discrete CoT
- fixed-width latent reasoning

should be compared to LoopLM as the current scale-referent in this niche.

## Downstream literature (from Ouro crawl)

- [[Parcae]] — stable looped LMs at 1.3B with negative-diagonal parameterization; derives L(T) = L_∞ + Z·exp(−zT) test-time scaling law + μ_rec ∝ FLOP^0.40 train-FLOP allocation.
- [[Mechanistic Analysis of Looped Reasoning LMs]] — analyzes Ouro, Huginn, retrofitted Llama/OLMo: cyclic fixed points, attention stabilizes in 1-2 iters, stages of inference re-enact per iteration; Ouro drifts past T_train.
- [[From Growing to Looping]] — looping and depth-growing share mechanistic signatures; inference-time middle-block looping on grown models yields 2× on reasoning primitives.
- [[RLTT]] — trajectory-level credit assignment fixes Ouro's reported GRPO/DAPO post-SFT RL failure (+14-34 pts on math).
- [[Think-at-Hard]] — selective per-token latent iteration on Qwen3 addresses latent-overthinking; only 6% of tokens re-iterate.
- [[Formal CoT vs Latent]] — complexity separations: looped TF captures TC^k at log^k n iterations, beats CoT (⊆ TC^{k-1}).
- [[Adaptive Loops and Memory]] — decouples think-harder (loops) from know-more (memory banks); reinforces Manipulation vs Capacity.
- [[Step-Decomposed Influence]] — per-iteration data-attribution tool for looped transformers; step-resolved TracIn.
