---
type: source
title: "Latent Thoughts Tuning"
created: 2026-04-22
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/anti-collapse
  - domain/curriculum
  - type/source
  - method/fusion
status: read
source_type: paper
arxiv_id: "2602.10229"
venue: "arXiv"
date_published: 2026-02-10
authors:
  - "Weihao Liu"
  - "Dehai Min"
  - "Lu Cheng"
url: "https://arxiv.org/abs/2602.10229"
code_repo: "https://github.com/NeosKnight233/Latent-Thoughts-Tuning"
has_weights: false
confidence: high
key_claims:
  - "Untied input/output embedding weights cause geometric distribution mismatch when recurrently injecting hidden states back into the input layer, inducing feature collapse after few iterations."
  - "Context-Prediction-Fusion (e_fusion = α · h_ctx + (1 − α) · e_pred) anchors the latent trajectory to the discrete token manifold by interpolating contextual hidden states with vocabulary-prior embeddings."
  - "A three-stage curriculum (Explicit CoT warmup → dynamic latent generation → CPF activation) is load-bearing; removing Stage 3 fusion causes 23.5% accuracy degradation at 8B."
  - "LT-Tuning sustains 68.8% average accuracy on math-reasoning benchmarks at 8B while COCONUT drops to ~41.5% at the same scale."
  - "Confidence-threshold dynamic switching allocates more latent tokens to harder problems, yielding adaptive compute without external halting networks."
  - "Open GitHub codebase available (NeosKnight233/Latent-Thoughts-Tuning); no pre-trained serialization weights released to Hugging Face Hub as of late March 2026."
related:
  - "[[Feature Collapse]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[Dynamic Switching Protocol]]"
  - "[[Curriculum Distillation]]"
  - "[[COCONUT]]"
  - "[[SIM-CoT]]"
  - "[[CODI]]"
  - "[[KaVa]]"
  - "[[Weihao Liu]]"
  - "[[NeosKnight233 Latent-Thoughts-Tuning]]"
sources:
  - "[[.raw/papers/2602.10229-latent-thoughts-tuning]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CPF equation + 3-stage curriculum is the exact recipe Branch D is designed to implement on CODI."
  - slug: "branch-a"
    relevance: secondary
    why: "Stage-1 CoT warmup recipe is directly reusable for Qwen3 scaling baselines; method is architecture-dependent though (untied embedding assumption)."
  - slug: "branch-b"
    relevance: reference
    why: "Fusion mechanism is orthogonal to detach/BPTT axis; useful context for interpreting grad-stability results but not a direct ablation target."
  - slug: "branch-c"
    relevance: reference
    why: "General anti-collapse context; no direct bearing on Qwen3 probe methodology or configuration debugging."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "North-star explicitly targets synthesizing LT-Tuning lessons; CPF + curriculum is the load-bearing contribution for the writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Latent Thoughts Tuning (LT-Tuning)

Liu, Min, Cheng — [arXiv:2602.10229](https://arxiv.org/abs/2602.10229) — *Latent Thoughts Tuning: Bridging Context and Reasoning with Fused Information in Latent Tokens* (submitted 2026-02-10). Code: [NeosKnight233/Latent-Thoughts-Tuning](https://github.com/NeosKnight233/Latent-Thoughts-Tuning). No released checkpoints.

## Core thesis

Large latent-reasoning architectures with untied input/output embeddings suffer geometric distribution mismatch when raw hidden states are recurrently injected back into the input layer. After a few iterations, continuous vectors degenerate into identical, semantically void representations — [[Feature Collapse]] — destroying algorithmic planning capacity. LT-Tuning solves this by interpolating the recurrent hidden state with a vocabulary-prior embedding, anchoring the latent trajectory to the discrete token manifold.

## Method

### Context-Prediction-Fusion (CPF)

Two components blended per step:

**Predictive (vocabulary prior):**

`e_pred = ∑_{w ∈ V} P̂(w) · E(w)`

Probability-weighted sum of vocabulary embeddings. This is where the anchor to discrete token space comes from — even if the hidden state drifts, `e_pred` stays inside the vocabulary manifold.

**Fused latent embedding:**

`e_fusion = α · h_{t−1, I} + (1 − α) · e_pred`

Tunable α balances contextual history against predictive anchor. When α → 1, behaves like COCONUT (raw hidden-state injection, prone to collapse). When α → 0, the latent is just vocabulary-distribution — effectively explicit CoT. LT-Tuning uses intermediate α.

### Dynamic switching protocol

At each step, model evaluates prediction confidence. Below threshold τ → insert `<thinking>` token, enter latent phase. Above → emit discrete token. Yields adaptive compute: harder problems get more latent steps automatically.

### Three-stage curriculum

| Stage | Name | What it does |
|---|---|---|
| 1 | Explicit CoT warmup | Standard SFT on CoT data; establishes baseline step-decomposition |
| 2 | Dynamic latent generation | Introduces `<thinking>` tokens with raw hidden states (no fusion yet); acclimates attention to recurrent inputs |
| 3 | CPF activation | Swaps raw hidden states for `e_fusion`; permanently immunizes against collapse |

Ablation: removing Stage 3 causes **23.5% accuracy degradation at 8B**. Stage 3 is load-bearing; the curriculum is not decorative.

## Recipe

- **Architecture:** Llama 1B / 3B / 8B
- **Datasets:** GSM8K-NL, ASDiv-Aug, MultiArith, SVAMP (math reasoning)
- **Objective:** per-stage (Stage 1: `ℒ_CoT = −∑_t log p_θ(y_t | x, y_<t)`; later stages extend with latent-token loss — see paper for specifics)
- **Curriculum gating:** confidence threshold τ learned or tuned per stage
- **Fusion coefficient α:** tuned (paper details)

## Results

| Model | LT-Tuning avg | COCONUT avg |
|---|---|---|
| Llama 1B | 36.4% | — |
| Llama 3B | 52.4% | — |
| Llama 8B | **68.8%** | **41.5%** (down from 50.3% at smaller scale) |

Feature-collapse visualization shows LT-Tuning maintains semantic diversity across reasoning steps; COCONUT does not.

## Relevance to our project

- **Branch D primary target.** The entire scientific thrust of Branch D is "implement CPF on top of our CODI base." LT-Tuning gives us: the equation, the curriculum, the ablation confirming Stage 3 matters, and Llama-scale validation.
- **Risk flagged.** No released checkpoints. Running from scratch requires the full three-stage curriculum — substantially more effort than a post-hoc fine-tune would be.
- **Architecture dependency.** The "untied embedding" framing is Llama-style; we need to verify applicability to Qwen3 (which has `tie_word_embeddings = false`) and Gemma-3 (ties).
- **Open concept.** Does CPF help below 8B? Paper shows gains at 1B/3B too, but the *collapse-mitigation* framing is scale-dependent; see [[meta/projects/branch-d]] for experiment design notes.

## Citation links to chase

- Downstream of: [[COCONUT]], [[SIM-CoT]], [[CODI]]
- Related anti-collapse work: [[KaVa]] (KV-distillation angle), [[SIM-CoT]] (auxiliary decoder)
- Sibling fusion work: none yet identified in our corpus — worth a crawl once S2 key is live.

## Artifacts

- **Paper:** [arXiv:2602.10229](https://arxiv.org/abs/2602.10229)
- **Code:** [[NeosKnight233 Latent-Thoughts-Tuning]] — verified 9 stars, Python 99.2%, no released checkpoints (2026-04-22)
- **Raw source:** [[.raw/papers/2602.10229-latent-thoughts-tuning]]

## SPAR empirical follow-up (2026-04-23)

F3 (7/8 latent positions decode to the fixed template `The → 0 → 0 → ? → . → . → . → .`, entropy <0.4 bits) is *exactly* the failure mode CPF is designed to prevent — a recurrent hidden state that has drifted out of the vocab manifold and routes the decoder to a degenerate format-prior attractor (see [[Feature Collapse]] and [[Loop-Mode Emission]]). The F5 null result strengthens the motivation further: swapping latent KV across examples leaves accuracy unchanged (0.10 → 0.10 at N=30, 13% text change rate, 0.78 median pair cosine), i.e. the per-example KV content is downstream-invisible. If we force each latent to be a weighted blend `e_fusion = α·h + (1−α)·e_pred` over vocab embeddings, the KV content becomes visible to the decoder *by construction*.

LT-Tuning is the load-bearing Phase 2b experiment on CODI V2 + Qwen3-4B and the clean test of whether [[Context-Prediction-Fusion]] breaks the F3/F5/F6 routing-mode signature. The five-way convergence of our F-battery strengthens Branch D priority over any lighter-touch CODI patch.
