---
type: source
title: "From Growing to Looping: A Unified View of Iterative Computation in LLMs"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/architecture
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
sources:
  - "[[.raw/papers/2602.16490-growing-to-looping]]"

source_type: paper
arxiv_id: "2602.16490"
venue: "arXiv"
date_published: 2026-02-18
authors:
  - "Ferdinand Kapl"
  - "Emmanouil Angelis"
  - "Kaitlin Maile"
  - "Johannes von Oswald"
  - "Stefan Bauer"
url: "https://arxiv.org/abs/2602.16490"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Looped (weight-tied) and depth-grown (middle-layer duplication) models exhibit CONVERGENT depth-wise signatures — both lean on late layers and show recurring patterns aligned with the looped/grown block — suggesting both gain from a common form of iterative computation."
  - "At 360M and 1.7B scale (SmolLM-v1, 200B / 400B tokens), applying inference-time looping to the middle block of a depth-grown model (MIDAS/LIDAS) improves accuracy on Copy-Real-Words reasoning primitive up to 2× (LIDAS 48.02% vs baseline 34.62%), despite the model never being trained to loop."
  - "One or two repetitions of a 4-layer middle block is optimal; more repetitions degrade performance."
  - "After cooldown training with looped blocks, LIDAS becomes stable at inference-time additional repetitions, while the baseline degrades noticeably with 3+ extra repetitions."
  - "Depth-grown models gain most with math-heavy cooldown mixtures; additional looping of middle blocks further compounds these gains."

projects:
  - slug: "branch-a"
    relevance: reference
    why: "Architecture-dependent yes, but on SmolLM-v1 not Qwen3; mechanism (depth-grown vs looped equivalence) is framework-level."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach/fp32 ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not about probe validity."
  - slug: "branch-d"
    relevance: reference
    why: "Not directly LT-Tuning adjacent but relevant framing: iterative computation unifies architectural compute axes we might want to mix with latent reasoning."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Key unification claim: depth-grown and looped models are mechanistically two expressions of iterative computation. Useful taxonomy contribution for the writeup and informs whether we should expect Ouro-style gains in depth-grown models (cheaper to implement than from-scratch looped pretraining)."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# From Growing to Looping: A Unified View of Iterative Computation in LLMs

## TL;DR

**Looping (reuse layers) ≡ depth growing (duplicate middle layers)** mechanistically — both produce the same depth-wise signatures (late-layer reliance, patterns aligned with the looped/grown block). Applying **inference-time middle-block looping to a depth-grown model** gives up to 2× accuracy on reasoning primitives, even without training to loop. They're complementary: adapting a middle block to loop during cooldown stabilizes further inference-time looping.

## Setup

- **Base models:** SmolLM-v1-style transformers at 360M and 1.7B params.
- **Training:** ~200B tokens (360M) / 400B tokens (1.7B).
- **Growing schemes:** MIDAS, LIDAS (different middle-layer duplication protocols).
- **Looping schemes:** repeat a block of 4 middle layers during inference, 1-2 repetitions optimal.
- **22 benchmark categories:** open-book Q&A, math word problems, reasoning primitives (Copy-Real-Words etc.), closed-book Q&A, language modeling.

## Method

1. Compare depth-wise layer-ablation and attention signatures between looped and depth-grown models.
2. Show depth-grown models can be inference-time-looped on middle blocks without additional training.
3. Probe how cooldown-time training with looped blocks changes inference-time robustness.
4. Study composability with cooldown data mixtures (math-heavy vs generic).

## Key results

### Mechanistic unification

- Both models show late-layer reliance (ablation at late layers hurts most).
- Recurring patterns aligned with the looped/grown block visible in layer-wise signatures.

### Inference-time looping improves depth-grown models

- LIDAS + inference-time block repetition: Copy-Real-Words up to **2×** accuracy (48.02% vs 34.62% baseline).
- One or two repetitions optimal; more → degradation.

### Training-time loop-aware cooldown stabilizes extrapolation

- Base model degrades at 3+ extra repetitions.
- LIDAS with loop-aware cooldown remains stable at 3+ repetitions.

### Data mixture matters

- Math-heavy cooldown mixtures give biggest reasoning gains for depth-grown models.
- Adapting middle block to loop during that cooldown compounds gains.

## Relevance

- **Alternative to from-scratch looped pretraining.** Ouro-style gains may be partially achievable via depth-growing + inference-time looping (much cheaper than 7.7T tokens).
- **Provides a pragmatic recipe** for testing looped-like latent reasoning without full pretraining: depth-grow a pretrained model, apply math-heavy cooldown, then loop middle blocks at inference. Roughly matches our constraint (no 7.7T-token budget).
- **Unifies taxonomy** for the SPAR writeup: "iterative computation" is the upstream concept, looping/depth-growing are two downstream realizations. Keeps the taxonomy from proliferating methods.

## Cross-links

- [[Ouro]] — from-scratch looped pretraining; this paper provides an alternative construction path.
- [[LoopLM]] — architectural family.
- [[Fixed-Width Depth Recurrence]] — related concept.
