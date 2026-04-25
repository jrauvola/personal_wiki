---
type: source
title: "Two-Scale Latent Dynamics for Recurrent-Depth Transformers"
source_type: paper
arxiv_id: "2509.23314"
venue: "arXiv"
date_published: 2025-09-27
authors:
  - "Francesco Pappone"
  - "Donato Crisostomi"
  - "Emanuele Rodolà"
url: "https://arxiv.org/abs/2509.23314"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "FINDING: Recurrent-depth transformer iterates have a two-scale geometry: within a looped block, updates are small-scale refinements (shrinking step norms, increasing orthogonality); across consecutive blocks, states undergo larger-scale drift."
  - "FINDING: Across training checkpoints, loop steps get smaller and more orthogonal — the model learns to do local refinement rather than linear pushing in a fixed direction."
  - "METHOD: Proposes a second-order (acceleration-based) early-exit rule — exits when the norm of the difference between consecutive loop updates stabilizes. Triggers precisely when the local spiral converges."
  - "RESULT: The acceleration-based exit outperforms Huginn's KL-divergence exit AND plain step-norm exit on the latency-quality Pareto — more robust to threshold variation; less hyperparameter tuning."
  - "IMPLICATION: The 'spiral' latent geometry is the load-bearing mechanism for recurrent refinement — a concrete replacement for the 'latent CoT' framing."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Acceleration-based early-exit is a direct, cheap inference-efficiency lever for any recurrent-depth model we train. Outperforms Huginn's default — a clear upgrade."
  - slug: "branch-b"
    relevance: primary
    why: "Shrinking + orthogonalizing loop steps is the geometric signature of fixed-point convergence — gives Branch B's stability diagnostics a concrete metric (measure step-norm decay and inter-step angle)."
  - slug: "branch-c"
    relevance: secondary
    why: "Alternative geometric probe to rank-trajectory tracking — independent of decoding method, so it sidesteps the [[Decoding Depth-Recurrent Transformer]] probe inconsistency issue."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Geometric characterization of recurrent-depth dynamics; essential companion to [[Scaling Up TTC]] and [[Mechanistic Analysis of Looped Reasoning LMs]]."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/interpretability
  - domain/inference-time
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Mechanistic Analysis of Looped Reasoning LMs]]"
  - "[[AdaPonderLM]]"
  - "[[Decoding Depth-Recurrent Transformer]]"
sources:
  - "[[.raw/papers/2509.23314-two-scale-latent-dynamics]]"
---

# Two-Scale Latent Dynamics

## TL;DR
Geometrically characterizes recurrent-depth iterates: **within a looped block**, updates are small-scale refinements (shrinking step norms, increasing orthogonality between consecutive updates); **across consecutive blocks**, states drift at a larger scale. Step-size decay is a signature of fixed-point convergence. Motivates a **second-order (acceleration) early-exit rule** that beats Huginn's KL-divergence exit on the latency-quality Pareto.

## Method
- **Diagnostic**: measure ||s_{i+1} - s_i|| (step norm) and cos(s_{i+1}-s_i, s_i-s_{i-1}) (consecutive-step angle) along the loop.
- **Signature**: shrinking norms + increasing orthogonality → model is doing local refinement, not global pushing.
- **Exit rule**: exit when the second-order difference (||s_{i+1} - 2 s_i + s_{i-1}||) falls below threshold τ — local spiral has stabilized.

## Results
- On Huginn-3.5B: acceleration-exit strictly dominates KL-exit on latency-quality curve.
- Much less sensitive to τ than step-norm exit (which loses quality under aggressive thresholds).

## Relevance
Concrete metrics and exit rule — ready to port. Two-scale geometry is now the default mental model for recurrent-depth dynamics.
