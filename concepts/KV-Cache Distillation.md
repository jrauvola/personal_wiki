---
type: concept
title: "KV-Cache Distillation"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept/distillation
  - domain/latent-reasoning
  - domain/architecture
status: seed
complexity: advanced
domain: latent-reasoning
aliases:
  - "KV Distillation"
  - "Compressed KV-Cache Distillation"
related:
  - "[[KaVa]]"
  - "[[Self-Distillation]]"
  - "[[CODI]]"
  - "[[COCONUT]]"
sources:
  - "[[KaVa]]"
projects:
  - slug: "branch-b"
    relevance: secondary
    why: "KV matching across parallel decoding steps interacts with detach/fp32 gradient stability — a natural diagnostic axis."
  - slug: "branch-d"
    relevance: primary
    why: "Per-step KV supervision is a direct alternative/companion to CPF's vocab-space anchoring for closing the CODI supervision gap."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Core technique in the latent-CoT distillation taxonomy for the fellowship writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# KV-Cache Distillation

**Definition.** A distillation technique in which the supervisory signal is the teacher's per-layer / per-head key-value cache (after optional compression), matched against a continuous student's K/V trajectory via a vector-space loss. Contrasts with token-level distillation (matching output distributions) and hidden-state distillation (matching a single post-final-layer hidden vector).

## Motivation — the supervision gap

In latent-CoT methods like [[CODI]] and [[COCONUT]], the student generates `M` continuous latent tokens but receives supervision only from the final answer token (and, in CODI, from a single hidden-state match on the last pre-answer token). Intermediate latent positions have no direct target. KV-cache distillation supplies a per-step, per-layer target.

## Mechanism (as introduced in [[KaVa]])

1. Teacher mode produces a full CoT KV cache: $K_t, V_t \in \mathbb{R}^{N_C \times H \times L \times d}$.
2. A compression / eviction step reduces the teacher cache from length `N_C` to `M`, matching the student's latent budget. KaVa uses [[R-KV Eviction]]: $S_{i,h,l} = \lambda \cdot I_{i,h,l} + (1-\lambda) \cdot R_{i,h,l}$ with λ=0.1 — balancing importance (attention from answer to CoT keys) against redundancy (negative pairwise cosine similarity among keys).
3. A KV-matching loss aligns the student's K/V trajectory to the compressed teacher cache with stop-gradient:

   $L_{KV} = \frac{1}{2M} \bigl(\lVert \mathrm{sg}[\tilde{K}_t] - K_s \rVert_p + \lVert \mathrm{sg}[\tilde{V}_t] - V_s \rVert_p\bigr)$

   L1 / Smooth-L1 tends to outperform MSE on small models; MSE can win at larger scale.

## Why it's surprising

Aggressive eviction destroys discrete token-level correspondence between teacher and student positions. KaVa's empirical claim is that the *distributional / structural* content survives compression — a "cognitive fingerprint" that a continuous student can internalize without needing one-to-one token alignment. This is what enables the ~1-point degradation from [[GSM8k-AUG]] to [[GSM8k-AUG-NL]], vs 6–20 points for CODI/COCONUT.

## Contrast with sibling techniques

| Technique | Target | Granularity |
|-----------|--------|-------------|
| Output-distribution distillation | Logits / token probabilities | per generated token |
| CODI hidden-state match | One hidden state (last pre-answer token) | single position |
| **KV-cache distillation** | **All K/V across layers × heads** | **per latent step × per layer × per head** |
| Feature-map distillation (CNN lit) | Intermediate activations | per layer |

## Open questions

- Does KV matching scale past the 3B backbones KaVa tested? Gemma-3 / 4B+ unverified.
- How does KV matching interact with explicit detach / fp32 strategies across parallel-vs-sequential decoding?
- Can KV-cache distillation combine additively with vocab-space anchoring (e.g. [[Latent Thoughts Tuning]]'s CPF)?

## Related

- [[KaVa]] — canonical source
- [[Self-Distillation]] — KaVa's specific teacher-student setup
- [[R-KV Eviction]] — the compression module
- [[PCCoT]] — the parallel decoding scheme that KaVa pairs with KV distillation
