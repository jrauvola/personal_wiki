---
type: idea
title: "Manifold-Constrained Residual Stream (mHC)"
created: 2026-04-24
updated: 2026-04-24
tags:
  - idea
  - architecture/residual-stream
  - pretraining
  - domain/latent-reasoning
status: parked
maturity: sketched
parked_trigger: "post-W4 / workable-larger-model phase (W5+); requires from-scratch pretraining"
grounding_sources:
  - "[[mHC - Manifold Constrained Hyper-Connections]]"
related_concepts:
  - "[[Hyper-Connections (Zhu 2024)]]"
  - "[[Spectral Regularization]]"
related:
  - "[[Research - Latent Scratchpad Precedence]]"
  - "[[Research - Stability Theory for Latent Recurrence]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: reference
    why: "Future-work-only; requires from-scratch pretraining outside current SPAR scope. File for potential W5+ workable-larger-model effort."
last_reviewed: 2026-04-24
reviewed_by: josh
---

# Manifold-Constrained Residual Stream (mHC)

## The idea in two paragraphs

The user flagged this while researching latent scratchpad precedents: DeepSeek's mHC paper widens the residual stream via Hyper-Connections (Zhu 2024) but constrains residual-mixing matrices to the **Birkhoff polytope** (doubly stochastic matrices) via a differentiable **Sinkhorn-Knopp projection** in the forward pass. This restores the identity-mapping property that plain Hyper-Connections sacrificed, curing training instability at scale with only ~6.7% training overhead.

The intuition for our project: a wider residual stream could provide a **parallel channel for a latent scratchpad to live in** — rather than emitting scratchpad tokens into the sequence, maintain them in a parallel lane of the residual stream. This is conceptually appealing but **mHC requires from-scratch pretraining** (outside current SPAR budget). **Parking this** for a post-W4 "workable larger model" phase where from-scratch architectural investment becomes feasible.

## Why it matters

If W3.5 Latent Scratchpad succeeds but has architectural pain points (scratchpad sequence-position emissions contend with answer-generation positions; past_kv reuse is clunky), mHC-style parallel residual lanes offer a cleaner structural home for the scratchpad channel. The per-position write head could project into a dedicated residual lane rather than inserting a token into the sequence. All subsequent latent positions read the scratchpad lane via the standard residual-stream attention pattern. Human readability preserved via a decode-time projection of the scratchpad lane back to vocab.

## Grounding papers

1. **[[mHC - Manifold Constrained Hyper-Connections]]** (Xie et al., DeepSeek, arxiv:2512.24880, Dec 2025) — the canonical paper. Widens residual stream + Sinkhorn-Knopp projection to Birkhoff polytope. **Pretraining-only. No official code. Only community nanoGPT reimplementation by tokenbender exists.** 6.7% training overhead at pretraining scale.
2. **[[Hyper-Connections (Zhu 2024)]]** — the precursor mHC constrains. Widens residual stream for more expressive inter-layer connectivity.
3. Adjacent from our stability autoresearch: **[[Parseval Networks]]** and **[[Orthogonal Recurrent Networks]]** — spectral constraints on weight matrices. mHC applies the same philosophy (constrained doubly-stochastic) to the residual-mixing matrices specifically.

## Mechanism sketch (if we were to implement)

```
Standard transformer residual stream at layer l: h_l = h_{l-1} + f_l(h_{l-1})

Hyper-Connections (Zhu 2024): widens to N parallel lanes
   H_l ∈ R^{N × d}; h_l = Σ_j A_{l,j} · H_{l-1,j} + f_l(H_{l-1})
   where A_l is an N×N mixing matrix per layer

mHC (DeepSeek): constrain A_l to the Birkhoff polytope via Sinkhorn-Knopp
   A_l ← SinkhornKnopp(softplus(W_l))    # differentiable projection
   A_l is doubly stochastic: rows sum to 1, columns sum to 1

Scratchpad-in-lane extension (our proposal):
   Reserve lane 0 for "scratchpad lane"
   Gate decides whether to write: w_t → H_{l, 0} at selected positions
   Rest of the N-1 lanes = normal residual stream
   Decoder reads lane 0 at decode-time via projection → vocab
```

The "write-to-scratchpad-lane" operation is gated (like W3.5) but the target is a specific residual lane rather than a sequence-position token. Subsequent layers see the scratchpad via normal residual-stream attention without any architectural change.

## Why parked, not active

1. **Pretraining only.** mHC requires training the base model from scratch with the wider + constrained residual stream. We cannot LoRA-retrofit mHC into Qwen3-4B.
2. **No official code.** Community nanoGPT reimpl is unvalidated at scale; DeepSeek hasn't released weights or training code.
3. **6.7% pretraining overhead** is small, but pretraining itself is a 100× larger investment than fine-tuning.
4. **Current SPAR scope** is intervention on pretrained bases, not from-scratch pretraining.

## When to unpark

Three triggers that would re-activate this idea:

1. **W3.5 Latent Scratchpad ships and succeeds** (clears F7/F8 gates at 4B). Then the question becomes: is the scratchpad architecturally cramped in sequence-position form? If yes → mHC parallel lanes.
2. **SPAR scope expands** to include from-scratch training at GPT-2 or Llama-1B scale (workable-larger-model effort, W5+).
3. **Community mHC code matures** (tokenbender nanoGPT validated empirically, or DeepSeek releases code). Lowers implementation cost from ★★★★★ to ★★★★.

## Feasibility sketch (for future-you)

Rough cost estimate if we did this at Llama-1B scale (not GPT-2, because Llama-1B is closer to "workable larger"):
- From-scratch Llama-1B pretraining: ~300 billion tokens (Llama 3.2 scale-down) ≈ ~5000 GH200-hours.
- mHC overhead: +6.7% → ~5335 GH200-hours.
- Plus scratchpad gate + decodability loss: +5-10% additional overhead.
- Total: **~6000 GH200-hours or ~250 GH200-days on single GPU**.
- Realistically: distributed 8-GPU = 30 days + 3-4 weeks setup + debugging = **~2 months with a team of 1 ML engineer full-time**.
- Out of SPAR scope; would need a follow-up grant or post-fellowship infrastructure.

## Cheaper first-step test (if we want to touch this before committing)

Before pretraining, a **"retrofit mHC-as-adapters" feasibility study** (noted in the autoresearch gap list) could be a half-day investigation:
- Freeze Qwen3-4B backbone.
- Add low-rank adapter layers that implement a narrow (N=2 or 3) mHC widening on the residual stream, applied only at the latent-rollout step positions.
- Train the adapters on CODI objective.
- Measure whether the adapted residual stream shows richer latent content per F-battery.

If adapters work, it's a proof-of-concept for mHC-style widening without full pretraining. Cost: ~2 coding-agent days + 1 GH200-day for adapter training. Could fit inside current SPAR scope as an exploratory Wave 2.5 branch.

## Open questions

1. Can mHC be retrofit-adapted (narrow + low-rank) into a pretrained model without full pretraining?
2. If scratchpad lives in a residual lane rather than a sequence position, does the gate parametrization change? (Probably yes — gate now writes into a continuous lane rather than emitting a discrete token. Tradeoff: interpretability lower, architectural cleanliness higher.)
3. Does mHC's doubly-stochastic constraint interact well with LoRA adapters, or do the SVDs of BA break the Birkhoff property?
4. Is there a known fine-tune recipe for Hyper-Connections alone (ignoring the mHC constraint)? If yes, we can test the widening half cheaply and add Sinkhorn later.

## Next step if we return to this idea

1. Half-day feasibility investigation on "retrofit mHC-as-adapters" (see above).
2. If adapters show promise AND W3.5 scratchpad is production-ready, design a composition: scratchpad emits to the wide residual lane rather than sequence position.
3. If we're extending scope toward pretraining: file as W5+ and begin budgeting.

## Pulling in relevant information

When re-opening this idea in a future session, read in this order:
1. This page (quick overview + cost estimate)
2. [[mHC - Manifold Constrained Hyper-Connections]] (full paper source)
3. Hyper-Connections original (Zhu 2024) — verify from wiki or crawl
4. Check if tokenbender nanoGPT mHC reimpl has been validated empirically
5. Check for any 2026 fine-tune / adapter papers on Hyper-Connections family
