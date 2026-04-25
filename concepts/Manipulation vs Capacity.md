---
type: concept
title: "Manipulation vs Capacity"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/interpretability
status: seed
related:
  - "[[LoopLM]]"
  - "[[Ouro]]"
sources:
  - "[[Ouro]]"

complexity: intermediate
domain: latent-reasoning
aliases:
  - "Capacity vs Manipulation"
  - "Capo vs Mano"
  - "Knowledge Capacity vs Knowledge Manipulation"

projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Reusable diagnostic framework — can directly ask 'does CODI / KaVa / LT-Tuning buy capacity or manipulation?' using Capo + Mano + Multi-hop QA protocols."
  - slug: "branch-a"
    relevance: reference
    why: "Framework for interpreting Qwen3 scaling results along the capacity vs manipulation axis."
  - slug: "branch-b"
    relevance: reference
    why: "If detach-ablation shifts behavior on reasoning-heavy vs retrieval-heavy MMLU subcats, that's the same cut."
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "branch-d"
    relevance: secondary
    why: "Would sharpen the CODI / LT-Tuning story: do fusion-anchored latents add manipulation or capacity? Direct experimental handle."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Manipulation vs Capacity

A diagnostic framing, formalized by [[Ouro]] via the **Physics-of-LMs** experimental program, for decomposing language-model performance gains into two distinct axes:

- **Knowledge capacity** — how many bits of factual information the model can store per parameter.
- **Knowledge manipulation** — how deeply the model can compose, reason over, or transform the knowledge it already holds.

## Why it matters

Most "my method makes the model smarter" claims conflate these. The claim "looping helps" is much sharper once you ask: does looping let the model **know more** or **do more with what it knows**?

## Operationalization (Ouro §6)

### Capo — knowledge capacity
- **Setting:** GPT-2 style 1M–40M params, `bioS(N)` synthetic biographies, N ∈ {20K–500K}, 1000 exposures.
- **Metric:** memorized bits / parameter.
- **Ouro result:** Loop-1 and Loop-4 **both ≈ 2 bits/parameter.** Looping does NOT raise capacity.

### Mano — knowledge manipulation
- **Setting:** modular arithmetic on binary trees, depth L ∈ {10, 16, 24}. Example: `+ * a b c` → `(a*b) + c mod 23`.
- **Metric:** accuracy at each depth.
- **Ouro result:** Loop (2⊗6) beats iso-FLOP Base (12⊗1) even at L=24 (78.0 vs 34.8). Looped models beat both iso-parameter and iso-FLOP baselines on deep composition.

### Multi-hop QA
- **Setting:** synthetic 3-hop QA.
- **Metric:** sample efficiency + convergence speed.
- **Ouro result:** Loop-2/Loop-4 learn with significantly fewer training samples than iso-parameter Loop-1. Gain is in **sample efficiency**, not asymptotic accuracy.

### MMLU category slice (Ouro App. B.4)

T=1 → T=4 gains on Ouro-1.4B:

| Cluster | Example subcats | Gain |
|---------|-----------------|------|
| **Reasoning-heavy** | Elementary math, Formal logic, Logical fallacies, High-school stats | **+125–155%** |
| **Retrieval-heavy** | Moral scenarios, Global facts, Virology, Anatomy | **+8–21%** |

The asymmetry in this cut is the cleanest single-table evidence for the manipulation-not-capacity thesis.

## How to port this to other methods

To ask "does method X buy capacity or manipulation?":

1. Run Capo (bits/param on bioS) on an X-augmented model vs iso-parameter base.
2. Run Mano (binary-tree modular arithmetic, deepening L) on both.
3. Run Multi-hop QA with varied hop count.
4. Slice a benchmark like MMLU by reasoning-heavy vs retrieval-heavy subcats.

Consistent pattern: if X helps manipulation, expect asymmetric benchmark gains concentrated on reasoning-heavy slices and Mano-style deep-composition tasks; if X helps capacity, expect uniform gains with no depth asymmetry.

## Caveats

- Capo at large model scales not tested in Ouro — the ≈2 bits/param claim is at 1M–40M scale. Unknown whether a looped 2.6B actually matches a 5.6B dense on memorization-heavy evals at deployment scale.
- The framing assumes capacity and manipulation are cleanly separable; real benchmarks mix both.
