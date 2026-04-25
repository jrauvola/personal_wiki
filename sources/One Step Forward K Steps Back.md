---
type: source
title: "One Step Forward and K Steps Back — Denoising Recursion Models"
source_type: paper
arxiv_id: "2604.18839"
venue: "arXiv"
date_published: 2026-04-20
authors:
  - "Chris Cameron"
  - "Wangzheng Wang"
  - "Nikita Ivanov"
  - "Ashmita Bhattacharyya"
  - "Didier Chételat"
  - "Yingxue Zhang"
url: "https://arxiv.org/abs/2604.18839"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "PROBLEM: Looped transformers used for iterative refinement have no supervision over intermediate refinement paths — training specifies only the target, not how to get there. This makes long refinement trajectories hard to learn."
  - "METHOD (Denoising Recursion Models, DRM): Similar to diffusion models — corrupt the target with varying magnitudes of noise and train the looped block to reverse corruption step-by-step. Unlike diffusion, training and inference behaviors are aligned (both iterative)."
  - "TRICK: 'One step forward and K steps back' — during training, take one noise step forward and K denoising steps back; teaches the model to be robust to being 'overshot' and to correct trajectories."
  - "CLAIM: Aligns training and inference dynamics — avoids the training/inference-misalignment issue of single-step diffusion reversal."
  - "FRAMING: Bridges diffusion models and looped transformers — latent refinement as explicit denoising trajectory."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Trajectory anchor is a third anti-collapse axis alongside CPF (vocab anchor) and SIM-CoT (auxiliary decoder); citable comparison point in the writeup. Downgraded primary → secondary this sweep: diffusion-style training is a different paradigm from CODI sequence-growing latents and no code is available."
  - slug: "branch-a"
    relevance: secondary
    why: "Iterative refinement with trajectory supervision is a scaling-story alternative — pairs well with diffusion-style latent reasoning (LaDiR)."
  - slug: "branch-b"
    relevance: reference
    why: "Training/inference alignment is the same problem as detach vs no-detach — DRM solves it via trajectory-level loss rather than gradient surgery."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Diffusion-adjacent branch of latent reasoning connecting looped transformers to LaDiR and the diffusion sub-family. Downgraded primary → secondary this sweep: no code/weights, conceptual bridge rather than synthesis input."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/architecture
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[LaDiR]]"
  - "[[Stability and Generalization in Looped Transformers]]"
sources:
  - "[[.raw/papers/2604.18839-one-step-forward-k-back]]"
---

# One Step Forward and K Steps Back

## TL;DR
Denoising Recursion Models (DRM) bridge diffusion and looped transformers: corrupt the target with varying noise magnitudes and train the looped block to reverse corruption iteratively. The "one step forward, K steps back" scheme — take one noise step, then K denoising steps — aligns training and inference dynamics, unlike single-step diffusion reversal.

## Relevance
A third axis of anti-collapse supervision: **trajectory anchor** (supervise the refinement path) — complementing **vocab anchor** (CPF) and **auxiliary-decoder anchor** (SIM-CoT). Essential cross-reference in Branch D's CPF writeup.
