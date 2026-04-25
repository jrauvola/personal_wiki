---
type: question
title: "Research — Latent Scratchpad Precedence"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/architecture
  - domain/interpretability
  - type/question
status: developing
question: "Has anyone published an architecture combining latent-primary reasoning + sparse discrete interpretable vocab tokens emitted at gate-chosen positions, in text-only LLMs? If not, what are the closest prior works?"
answer_quality: solid
projects:
  - slug: spar-latent-reasoning
    relevance: primary
    why: "Determines whether W3.5 Latent Scratchpad is novel contribution or me-too."
  - slug: branch-d
    relevance: primary
    why: "If W3.5 advances, scratchpad composes with CPF on the same backbone."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Latent Scratchpad Architecture]]"
  - "[[Latent Sketchpad]]"
  - "[[Tiny Recursive Model]]"
  - "[[mHC - Manifold Constrained Hyper-Connections]]"
  - "[[Token Assorted]]"
  - "[[HRPO]]"
  - "[[Quiet-STaR]]"
  - "[[Pause Tokens]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
sources:
  - "[[Latent Sketchpad]]"
  - "[[Tiny Recursive Model]]"
  - "[[mHC - Manifold Constrained Hyper-Connections]]"
  - "[[Token Assorted]]"
  - "[[HRPO]]"
  - "[[Quiet-STaR]]"
---

# Research — Latent Scratchpad Precedence

> Question: Is the proposed W3.5 architecture (latent primary + sparse discrete vocab side-channel + learned gate, in a text-only LLM) genuinely novel, or has someone already published it?

## Overview

The user proposed a hybrid architecture, "Latent Scratchpad":
- **Primary:** continuous latent reasoning tokens (CODI/COCONUT-style — `M` latent steps).
- **Side-channel:** sparse, **discrete**, vocab-decoded "notes" emitted at gate-chosen transitions.
- **Property:** notes are human-readable; subsequent latent steps attend back to them.
- **Training:** gate is learned with a sparsity penalty.

This page audits the literature for the four most likely places precedence could exist:
1. Visual analogue of the same pattern (Latent Sketchpad).
2. Discrete-side-channel recipes (Token Assorted, HRPO, Quiet-STaR).
3. Recursive-latent recipes user thought might be similar (TRM).
4. Wider-residual-stream pretraining work the user wanted to compose with (mHC).

## Key findings

### 1. Latent Sketchpad is the closest prior art ([[Latent Sketchpad]], arXiv:2510.24514, Oct 2025)
- **Same architectural pattern** — primary reasoning stream (text) interleaved with an interpretability side-channel that is "written" at model-chosen positions and rendered through a small decoder.
- **Two key differences from the user's proposal:** (a) primary is **textual**, not latent; (b) side-channel is **continuous visual latents** rendered through a "Sketch Decoder" to images, not discrete vocab tokens.
- This is the paper to cite as direct inspiration. Repo released: [hwanyu112/Latent-Sketchpad](https://github.com/hwanyu112/Latent-Sketchpad).

### 2. TRM is NOT a scratchpad precedent ([[Tiny Recursive Model]], arXiv:2510.04871, Oct 2025)
- The user's lead on "Alexia tiny reasoning model" is real — the paper exists and is impressive (7M params, 45% ARC-AGI-1).
- But TRM has **no scratchpad mechanism**: latent z is purely internal, never decoded at intermediate steps, no gate, no discrete side-channel.
- TRM is adjacent to CODI/COCONUT in formulation (recursive latent refiner), not adjacent to the user's proposal.

### 3. Discrete-token side-channel recipes already exist, but none match the full pattern
- **Token Assorted** ([[Token Assorted]], arXiv:2502.03275, Su et al., Meta+UCB): mixes discrete VQ-VAE codes into reasoning traces. Side-channel is **opaque VQ codes**, not vocab-readable. **No gate** — random replacement during training. Compresses initial reasoning steps.
- **HRPO** ([[HRPO]], arXiv:2505.18454, Yue et al., NeurIPS 2025): learned **gating** mechanism that **blends** prior hidden states with sampled tokens in the same stream. **Not a separate side-channel** — it's a single mixed stream where the gate controls the blend ratio. Closest to the gate-mechanism component of W3.5.
- **Quiet-STaR** ([[Quiet-STaR]], arXiv:2403.09629, Zelikman 2024): learned `<startofthought>`/`<endofthought>` tokens emit rationales before each output. Primary stream is **text**, not latent. Rationales are full text segments, not sparse note-tokens.
- **Pause Tokens** ([[Pause Tokens]], Goyal 2023): adds dummy compute tokens; no emission, no gate, no interpretability claim.

### 4. mHC is real but pretraining-only ([[mHC - Manifold Constrained Hyper-Connections]], arXiv:2512.24880, Dec 2025)
- DeepSeek paper widening residual stream via doubly-stochastic-constrained Hyper-Connections + Sinkhorn-Knopp projection.
- 6.7% training overhead vs HC. No fine-tune / LoRA retrofit recipe.
- **Useful framing** — wider residual stream as "parallel channel" — but **not actionable for W3.5** because it requires from-scratch pretraining.
- Only community implementation exists ([tokenbender's nanoGPT port](https://github.com/tokenbender/mHC-manifold-constrained-hyper-connections)); no official DeepSeek code or checkpoints.

### 5. Scratchpad Thinking (Goyal 2025) is interpretability analysis, not architecture
- arXiv via OpenReview EV30qkZXrR. Mechanistically analyzes CODI and finds it **already alternates** storage steps and computation steps internally.
- Implication: a discrete scratchpad side-channel may **surface** a structure that exists already in CODI's latent steps. Strong motivation for W3.5.

## Novelty verdict

**The W3.5 Latent Scratchpad architecture appears genuinely novel** as a specific combination, but it sits within a well-trodden research area. The novelty is the *combination* of four already-individually-published components, in the text-only setting:
- (a) latent-primary backbone (COCONUT/CODI),
- (b) discrete-**vocab** (not VQ) side-channel emitted out-of-stream,
- (c) **learned sparsity-penalized gate** controlling emission,
- (d) the resulting discrete trace is **directly human-readable without a decoder**.

No surveyed paper (including the comprehensive [[Latent CoT Survey]] arXiv:2507.06203) documents this exact pattern. The closest precedent is Latent Sketchpad in vision; the W3.5 contribution is to port the pattern to text-only LLMs and replace the visual continuous-latent + decoder pipeline with a discrete-vocab + tied-output-embedding mechanism.

## Key entities

- [[Alexia Jolicoeur-Martineau]] — Samsung SAIL Montreal; TRM
- [[Zhenda Xie]] — DeepSeek; mHC
- [[Huanyu Zhang]] — `hwanyu112`; Latent Sketchpad
- [[DiJia Su]] — Meta+UCB; Token Assorted (existing entity)
- [[Eric Zelikman]] — Quiet-STaR (existing entity)
- [[Zhenrui Yue]] — UIUC; HRPO (existing entity)

## Key concepts

- [[Latent Scratchpad Architecture]] (the proposed pattern)
- [[Implicit CoT Precursors]] (existing — broader context)
- [[Loop-Mode Emission]] (existing — adjacent emission-from-latent concept)

## Contradictions / open questions

- **Open:** does the gate degenerate? In HRPO the gate moves smoothly from token-dominant → hidden-dominant during training; in W3.5 the gate must learn **discrete on/off** behavior, which is harder to train (needs Gumbel-softmax or REINFORCE).
- **Open:** how do we get supervision for the note content during training without manual reference notes? Possible answers: (a) self-distill from a CoT teacher into compressed notes; (b) train without note supervision and let notes emerge; (c) curriculum like COCONUT's K-stage but for emission rate.
- **Open:** does the discrete trace actually reflect the latent computation, or does the gate learn to emit decoy notes that don't represent the underlying reasoning? (Faithfulness concern à la [[Filler Tokens]] / Pfau.)

## Sources

- [[Latent Sketchpad]] — arXiv:2510.24514, closest prior art (visual side-channel).
- [[Tiny Recursive Model]] — arXiv:2510.04871, Alexia's paper; not a scratchpad.
- [[mHC - Manifold Constrained Hyper-Connections]] — arXiv:2512.24880, residual-stream widening, pretraining-only.
- [[Token Assorted]] — existing source page; opaque VQ side-channel.
- [[HRPO]] — existing source page; learned gate but in-stream blend.
- [[Quiet-STaR]] — existing source page; emit-rationales but text primary.
- [[Latent CoT Survey]] — existing source page; comprehensive survey, no documented match for the W3.5 pattern.

## Notes

- Hard cap on pages this autoresearch session: 9 created (well under 15).
- WebFetch count: 7. WebSearch count: 7. Both within Round 1+2 budget.
- Round 3 not used — Round 1+2 conclusively answered the precedence question.
