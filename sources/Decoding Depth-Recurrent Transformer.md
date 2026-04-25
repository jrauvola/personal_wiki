---
type: source
title: "Decoding the Depth-Recurrent Transformer — Is Huginn Doing Latent CoT?"
source_type: paper
arxiv_id: "2507.02199"
venue: "arXiv"
date_published: 2025-07-02
authors:
  - "Wenquan Lu"
  - "Yuechuan Yang"
  - "Kyle Lee"
  - "Yanshu Li"
  - "Enqi Liu"
url: "https://arxiv.org/abs/2507.02199"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "RESULT: Probing Huginn-3.5B with Logit Lens and Coda Lens reveals limited evidence of interpretable latent CoT — rank trajectories of intermediate-result tokens do not show the step-by-step pattern seen in explicit CoT models."
  - "RESULT: Probing inconsistency: hidden state semantics depend heavily on which block (e.g., R1 vs R4) and which decoding method is used — sharp discontinuities across recurrent blocks unlike feedforward transformers."
  - "RESULT: Increasing recurrence depth yields only marginal gains and 'falls well short of matching' explicit CoT on arithmetic tasks when probed carefully."
  - "METHOD: Introduces Coda Lens — applies the coda block to intermediate hidden states to decode them through the model's own output head, giving a more faithful probing signal than Logit Lens in this architecture."
  - "IMPLICATION: Test-time compute scaling in Huginn is real (final accuracy improves with r) but the mechanism is NOT latent CoT as naively imagined — suggests the model uses a different computational strategy."
projects:
  - slug: "branch-c"
    relevance: primary
    why: "Direct probe-methodology critique of recurrent-depth models — exactly what Branch C needs if Qwen3 convergence anomalies require probe-validity checks. Coda Lens is a concrete diagnostic tool we should port."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "First interpretability study of Huginn specifically — essential companion to [[Scaling Up TTC]]. Challenges the 'latent CoT' framing and motivates [[Are Latent Reasoning Models Easily Interpretable]] and [[Mechanistic Analysis of Looped Reasoning LMs]]."
  - slug: "branch-a"
    relevance: secondary
    why: "Architecture-dependent probe results — if Qwen3 recurrent retrofits also show block-wise discontinuities, it's evidence the phenomenon is general, not Huginn-specific."
  - slug: "branch-d"
    relevance: reference
    why: "Indirect: motivates vocab-anchoring (CPF) as a way to get interpretable latent trajectories — the non-anchored Huginn is exactly what CPF aims to avoid."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/interpretability
  - domain/latent-reasoning
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Are Latent Reasoning Models Easily Interpretable]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[Two-Scale Latent Dynamics]]"
  - "[[Latent Thinking Optimization]]"
sources:
  - "[[.raw/papers/2507.02199-decoding-depth-recurrent]]"
---

# Decoding the Depth-Recurrent Transformer

## TL;DR
A probing study of Huginn-3.5B on arithmetic tasks. Uses Logit Lens and a new **Coda Lens** to track intermediate-result token ranks across recurrent block iterations. Finds (1) limited evidence of interpretable latent CoT, (2) sharp cross-block discontinuities in hidden-state semantics (unlike feedforward transformers), (3) marginal gains from deeper recurrence on arithmetic — well short of explicit CoT.

## Method
- **Logit Lens**: apply the final unembedding matrix to intermediate hidden states.
- **Coda Lens** (novel): apply the model's own coda block (2-layer post-recurrent head) to intermediate states — gives a more faithful readout in an architecture where the coda does non-trivial computation.
- **Rank trajectory**: track the rank of final-answer tokens and intermediate-result tokens across iterations.

## Key Findings
1. **Sharp block discontinuities** — R1 vs R4 probe very differently; no smooth decoding trajectory.
2. **Probing inconsistency** — Logit Lens and Coda Lens disagree; layer index and decoding method both matter.
3. **Marginal arithmetic gains** — more recurrence doesn't clearly lead to step-wise computation on arithmetic, contradicting the 'latent CoT' narrative.

## Relevance
- Branch C: exactly the probe methodology Qwen3 probes would face. Coda Lens is an artifact we should replicate.
- SPAR umbrella: first shot across the bow of the "Huginn does latent reasoning" claim — pairs with [[Are Latent Reasoning Models Easily Interpretable]] (more negative evidence) and [[Mechanistic Analysis of Looped Reasoning LMs]] (cyclic-fixed-point alternative story).
