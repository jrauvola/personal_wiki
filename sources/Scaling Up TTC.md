---
type: source
title: "Scaling Up TTC — Recurrent-Depth Latent Reasoning"
source_type: paper
arxiv_id: "2502.05171"
venue: "arXiv"
date_published: 2025-02-07
authors:
  - "Jonas Geiping"
  - "Sean McLeish"
  - "Neel Jain"
  - "John Kirchenbauer"
  - "Siddharth Singh"
  - "Brian R. Bartoldson"
  - "Bhavya Kailkhura"
  - "Abhinav Bhatele"
  - "Tom Goldstein"
url: "https://arxiv.org/abs/2502.05171"
code_repo: "https://github.com/seal-rg/recurrent-pretraining"
has_weights: true
status: read
confidence: high
key_claims:
  - "RESULT: 3.5B-param recurrent-depth model (Huginn-0125) trained on 800B tokens matches ~50B-equivalent compute on GSM8k/ARC at test-time iteration r=32-64."
  - "RECIPE: Prelude / Recurrent Core / Coda architecture with shared recurrent block; inject prelude output e into every iteration; truncated BPTT through only last k=8 iterations for memory-independent training."
  - "RECIPE: Sample iteration count r during training from heavy-tailed log-normal Poisson distribution Lambda so the model learns to converge across a wide range of depths; initial state s_0 drawn from N(0, sigma^2) injects stochasticity toward fixed-point / path-independent behavior."
  - "RESULT: Path-independence emerges at scale — fixed-point convergence in latent space is independent of initial random state; reasoning benchmarks converge slower (GSM8k) than non-reasoning (OpenBookQA), confirming that recurrent depth is load-bearing for reasoning."
  - "RESULT: Recurrent-depth models naturally support per-token adaptive compute, self-speculative decoding, and KV-cache sharing without additional training — features that require substantial engineering in non-recurrent models."
  - "OBSERVATION: Latent trajectories exhibit emergent geometry — the model learns to rotate shapes in latent space for numerical computation; context-dependent patterns (orbits, drift) emerge with scale."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Recurrent-depth pretraining is a canonical scaling recipe for latent reasoning; our Qwen3 scaling work needs to contrast architectural scaling (Huginn) vs post-hoc latent scaffolding (CODI/LT-Tuning)."
  - slug: "branch-b"
    relevance: primary
    why: "Truncated BPTT with k=8 iterations is exactly the train-memory story for Branch B's detach/fp32 sufficiency ablation; path-independence gives a fixed-point framing for stability diagnostics."
  - slug: "branch-c"
    relevance: reference
    why: "Architecture-level scaling evidence to contrast with Qwen3 probe methodology if convergence contradictions surface."
  - slug: "branch-d"
    relevance: secondary
    why: "No CPF-style anchoring — Huginn does not project to vocab-space — but the depth-recurrent training recipe gives a different anti-collapse angle (stochastic s_0 + path independence as collapse-prevention) that complements CPF."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational paper for the recurrent-depth family (Ouro, Parcae, Retrofitted Recurrence, HRM all cite). Taxonomic anchor for the `scaling via depth recurrence` branch of the umbrella taxonomy."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - domain/scaling
  - family/recurrent-depth
related:
  - "[[Ouro]]"
  - "[[Parcae]]"
  - "[[Hierarchical Reasoning Model]]"
  - "[[From Growing to Looping]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[Step-Decomposed Influence]]"
  - "[[Formal CoT vs Latent]]"
  - "[[Adaptive Loops and Memory]]"
  - "[[RLTT]]"
sources:
  - "[[.raw/papers/2502.05171-scaling-up-ttc]]"
---

# Scaling Up TTC — Recurrent-Depth Latent Reasoning (Huginn-0125)

> [!note] Iteration-sampling design space: Huginn (Poisson-Lognormal r) vs [[Ouro]] (uniform + adaptive exit) vs [[LoopFormer]] (shortcut modulation)
> Three independent designs for making a recurrent block produce meaningful outputs across iteration counts: Huginn samples r from a heavy-tailed Poisson-Lognormal during training; Ouro uses a uniform prior over T ∈ {1..T_max=4} with an entropy-regularized Q-exit gate; LoopFormer adds iteration-index conditioning to the residual shortcut so one network can behave differently per iteration. Not contradictory but distinct points in the design space. Relevant for Branch A: if we retrofit Qwen3 to depth recurrence, which iteration-count regime do we adopt? Paired with the different BPTT choices ([[Retrofitted Recurrence]] uses k=8 truncated; Ouro uses full BPTT across T=4), this defines a 3×2 matrix of concrete options we haven't yet tested.

## TL;DR

A 3.5B-parameter transformer with a **depth-recurrent core block** iterated a variable number of times per forward pass. Pretrained on 800B tokens on Frontier (AMD cluster). At test time, iterating the core 32–64 times gives a compute load equivalent to ~50B parameters, with dramatic gains on reasoning-heavy benchmarks (GSM8k, ARC) and near-flat returns on non-reasoning (OpenBookQA). No CoT data required; works with small context; naturally supports adaptive compute, self-speculative decoding, KV-cache sharing.

## Architecture (Prelude / Recurrent Core / Coda)

Three structural sections:
- **Prelude** — standard transformer blocks that embed inputs x and produce `e = P(x)`.
- **Recurrent Core** — shared transformer block `R`; applied r times. Initial state `s_0 ~ N(0, sigma^2)`. Each iteration: `s_{i+1} = R(s_i, e)` — prelude output `e` is re-injected every step.
- **Coda** — small tail block that reads `s_r` and produces the next-token distribution.

The re-injection of `e` and stochastic `s_0` are the twin primitives driving the design: they force the core to learn **stable iterative operators** (gradient-descent-like maps) rather than memorizing a fixed sequence of transformations. The stochastic `s_0` + path independence (Anil et al., 2022) are cited as the collapse-prevention mechanism.

## Training Recipe

**Iteration sampling.** During training, `r ~ Lambda` where Lambda is a **heavy-tailed log-normal Poisson**. This teaches the model to produce meaningful outputs across the iteration spectrum from r=1 upward.

**Truncated BPTT through the recurrence.** Only backpropagate through the **last k=8 iterations** of the core. Activation memory and backward compute become **independent of r**. The prelude block still receives gradients every step because `e` is re-injected.

**Optimization and data.** 800B tokens on Frontier (AMD MI250X cluster). Data is heavily skewed toward **code and math** (following Allen-Zhu & Li, 2024 — mix instruction data into pretraining). ~4096 context. All data public.

## Test-Time Behavior

- **Scaling curve**: val PPL monotonically improves with r over r ∈ {1, 4, 8, 16, 32, 64} throughout training.
- **Task-dependent saturation**: non-reasoning tasks (OpenBookQA, HellaSwag) saturate around r=8; reasoning tasks (GSM8k, ARC-Challenge) continue improving to r=32+. Validates that recurrent depth is load-bearing for reasoning, not a generic perplexity trick.
- **Emergent latent geometry**: latent trajectories form orbits on numerical tasks (model literally rotates representations for arithmetic); drift/circulation patterns are context-dependent and emerge with scale.

## Natural TTC Features

Because the core is iterative, several features come for free:
- **Per-token adaptive compute** — stop iterating when successive states converge (KL/cosine threshold).
- **Self-speculative decoding** — early iterations act as drafts; later iterations verify. No separate draft model.
- **KV-cache sharing** — across iterations of the same token, KV is identical, so cache reuse is trivial.

## Relevance

- **Branch A (Qwen3 scaling)**: architectural baseline — "recurrent-depth from scratch" (Huginn) is the alternative to "post-hoc latent scaffolding on a pretrained model" (CODI, LT-Tuning). Our scaling story must cite Huginn as the Pareto point that trades one axis (more training compute, from-scratch) for another (no distillation, no CoT data).
- **Branch B (detach/fp32)**: the k=8 truncated BPTT is **exactly** the load-bearing detach we're ablating. Huginn's success at 3.5B with k=8 is evidence that minimum-sufficient truncated-detach scales; path-independence gives a fixed-point framing for why fp32 only matters at the final k steps.
- **Branch D (CPF on CODI)**: Huginn is a counterexample to LT-Tuning's "CPF is necessary for anti-collapse" — it prevents collapse via stochastic `s_0` + iteration-count randomization instead of vocab-anchoring. Useful contrast paragraph in any CPF writeup.
- **SPAR umbrella**: canonical seed of the recurrent-depth family; direct parent of [[Ouro]], [[Parcae]], [[From Growing to Looping]], [[Mechanistic Analysis of Looped Reasoning LMs]], [[RLTT]], [[Formal CoT vs Latent]], [[Adaptive Loops and Memory]], [[Hierarchical Reasoning Model]] (conceptually), and the upcoming retrofit/interpretability wave.

## Citation Links

Citing work in the vault (discovered / ingested via the downstream crawl 2026-04-23):
- [[Ouro]] — 2510.25741 — ByteDance/UCSC 1.4B/2.6B scaled recurrent-depth successor.
- [[Parcae]] — 2604.12946 — scaling laws for stable looped LMs.
- [[Mechanistic Analysis of Looped Reasoning LMs]] — 2604.11791 — analyzes Huginn-0125 directly.
- [[From Growing to Looping]] — 2602.16490 — retrofit via middle-block looping.
- [[RLTT]] — 2602.10520 — trajectory RL fixes Ouro's GRPO failure.
- [[Formal CoT vs Latent]] — 2509.25239 — TC^k complexity characterization.
- [[Adaptive Loops and Memory]] — 2603.08391 — per-layer halting router.
- [[Step-Decomposed Influence]] — 2602.10097 — per-loop TracIn for Ouro.
- [[Are Latent Reasoning Models Easily Interpretable]] — 2604.04902 — interpretability critique.
- [[Hierarchical Reasoning Model]] — 2506.21734 — 27M ARC-AGI conceptual cousin.
