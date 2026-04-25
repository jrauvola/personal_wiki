---
type: source
title: "A Mechanistic Analysis of Looped Reasoning Language Models"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/interpretability
  - domain/architecture
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
sources:
  - "[[.raw/papers/2604.11791-mech-analysis-looped]]"

source_type: paper
arxiv_id: "2604.11791"
venue: "arXiv"
date_published: 2026-04-13
authors:
  - "Hugh Blayney"
  - "Álvaro Arroyo"
  - "Johan Obando-Ceron"
  - "Pablo Samuel Castro"
  - "Aaron Courville"
  - "Michael M. Bronstein"
  - "Xiaowen Dong"
url: "https://arxiv.org/abs/2604.11791"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "In looped reasoning LMs (Ouro 1.4B, Huginn-0125, retrofitted Llama/OLMo), each layer in the recurrent block converges to a DISTINCT fixed point: the block follows a consistent cyclic trajectory in latent space across iterations."
  - "Attention matrices across recurrences become near-identical within 1-2 iterations (Frobenius-norm analysis shows diagonal similarity bands)."
  - "Mixing 'stages of inference' observed in feedforward models are RE-ENACTED within each loop iteration — the recurrent block repeats the feedforward stages depth-by-depth."
  - "Input injection (adding random noise vectors each recurrence) is necessary for distinct per-layer fixed points; without it, all layers collapse to the same fixed point (degenerate)."
  - "Retrofitted Llama (with added recurrence) reaches TRUE fixed points and keeps stable stages up to 128 test-time recurrences; Ouro shows continuous drift past training recurrences, correlating with Ouro's documented performance degradation at T>4."
  - "Block size (4/8/12 layers), input injection, and normalization (pre-norm vs sandwich) all influence emergence and stability of cyclic fixed points."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Not a Qwen3 architecture-dependent scaling finding."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach-stability or fp32 tool."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool."
  - slug: "branch-d"
    relevance: reference
    why: "Mechanistic recurrence analysis is tangential to LT-Tuning CPF but provides framing for why latents can stop evolving (fixed-point convergence) — same failure mode we see in feature collapse."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Mechanism-level explanation for Ouro's T>4 degradation — valuable citation for the writeup's LoopLM section, but we are not executing mech-interp on Ouro as a primary pipeline; fixed-point/input-injection findings are an anchor only if we turn toward Ouro-specific probing."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# A Mechanistic Analysis of Looped Reasoning Language Models

## TL;DR

Mechanistic-interp analysis of three looped models (**Ouro 1.4B, Huginn-0125, retrofitted Llama & OLMo**) shows:
1. Recurrent blocks converge to **cyclic trajectories** where each internal layer reaches a distinct fixed point.
2. Attention stabilizes within 1-2 iterations.
3. Within each iteration, the recurrent block **re-enacts feedforward-style inference stages**.
4. **Input injection** is necessary for distinct fixed points; without it all layers collapse to one fixed point.
5. Retrofitted Llama extrapolates to 128 recurrences with stable stages; **Ouro drifts past training depth** → correlates with Ouro's T>4 performance degradation.

## Method

- Analyze cyclic recurrence of hidden states across τ iterations.
- Measure: Frobenius distance between attention matrices across iterations, fixed-point distance between latent states across loops, ColSum-Concentration metric for attention-mass concentration (for detecting stages of inference).
- Sweep: block depth (4, 8, 12), input injection (noise vec merged at each recurrence) on/off, pre-norm vs sandwich normalization.

## Key findings

### 1. Distinct cyclic fixed points

Each of the L layers in a recurrent block converges to its own fixed point as iterations increase. Block follows a stable cyclic trajectory rather than converging to one identity-like fixed point.

### 2. Attention stabilizes fast

Frobenius-norm analysis of attention matrices: diagonal bands of high similarity within 1-2 iterations per layer. Attention-head behavior becomes constant across recurrences.

### 3. Stages repeat, not progress

Recurrent block learns the same stages of inference seen in feedforward transformers (per Lad et al., 2024 framework). Each iteration cycles through those stages rather than carrying them forward monotonically.

### 4. Input injection is necessary

Without input injection: all layers converge to the SAME fixed point (degenerate, information-destroying). With noise-vector input injection: distinct per-layer fixed points emerge → healthy cyclic trajectory.

### 5. Generalization — the Ouro-specific finding

- **Retrofitted Llama** reaches true fixed points, maintains stable stages to 128 test-time recurrences.
- **Ouro** shows continuous drift beyond training recurrences (trained T=4) — a concrete mechanistic cause for the performance degradation Ouro documents at T=5-8.

## Relevance

- **Explains Ouro's T-drop mechanistically.** Our [[Ouro]] page notes performance degrades past T=4 (trained depth) and interprets it as "peaks at trained depth, no free extrapolation." This paper provides the mechanism: Ouro doesn't actually reach stable fixed points — latent states drift without bound, so extra loops drag representations off the manifold they were trained on.
- **Predicts what would fix Ouro:** stronger input injection, different normalization, or smaller block depth to ensure fixed-point convergence.
- **Directly useful for our interpretability pipeline.** Fixed-point convergence diagnostics are a load-bearing analysis for any Ouro/looped-LM we probe. Tuned lens could plausibly pick up the stage-repetition structure as a signature.
- **Connects to [[Feature Collapse]] literature:** fixed-point collapse without input injection is structurally analogous to representational collapse in latent CoT without fusion/auxiliary signals.

## Cross-links

- [[Ouro]] — primary case study.
- [[LoopLM]], [[Fixed-Width Depth Recurrence]] — framework this paper dissects.
- [[Feature Collapse]] — fixed-point collapse without input injection is a variant.
