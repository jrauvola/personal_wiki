---
type: source
title: "Loop, Think, Generalize — Implicit Reasoning in Recurrent-Depth Transformers"
source_type: paper
arxiv_id: "2604.07822"
venue: "arXiv"
date_published: 2026-04-09
authors:
  - "Harsh Kohli"
  - "Srinivasan Parthasarathy"
  - "Huan Sun"
  - "Yuekun Yao"
url: "https://arxiv.org/abs/2604.07822"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "FINDING: Standard transformer LLMs fail compositional implicit reasoning — they store facts/rules but cannot combine them in a single forward pass. Recurrent-depth transformers (Huginn, Ouro) address this limitation via iterative computation over shared layers."
  - "STUDY-TASK 1 — Systematic generalization: combining knowledge units that were NEVER used together during training. Evaluates whether the recurrent model truly composes or merely memorizes seen compositions."
  - "STUDY-TASK 2 — Depth extrapolation: test-time recurrence beyond training k. Studies whether learned iteration operators extrapolate to deeper depths."
  - "RESULT: Recurrent-depth transformers show meaningful compositional gains vs non-recurrent baselines on implicit-reasoning probes — supports the claim that iteration IS the mechanism."
  - "CONTEXT: Positions Huginn/Ouro alongside COCONUT (continuous hidden-state CoT) as the two main latent-reasoning families — recurrent-depth vs continuous-token — and argues both alleviate compositional-failure mode."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Direct test of whether recurrent depth helps compositional generalization — exactly the scientific claim our Qwen3 scaling branch is trying to support. Gives us a probe set."
  - slug: "branch-d"
    relevance: secondary
    why: "Compositional generalization probes are a test set we could use to measure CPF's added value, but the paper studies recurrent-depth models (Huginn/Ouro), not the CODI sequence-growing family Branch D targets. Downgraded primary → secondary this sweep: probe-bed rather than recipe input."
  - slug: "branch-c"
    relevance: secondary
    why: "Depth-extrapolation probes are exactly the methodology we need for Qwen3 convergence diagnostics."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Capability-focused follow-up to [[Scaling Up TTC]] — provides concrete task batteries for the recurrent-depth family. Complements theoretical [[Stability and Generalization in Looped Transformers]]."
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/generalization
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Ouro]]"
  - "[[COCONUT]]"
  - "[[Formal CoT vs Latent]]"
  - "[[Stability and Generalization in Looped Transformers]]"
sources:
  - "[[.raw/papers/2604.07822-loop-think-generalize]]"
---

# Loop, Think, Generalize

## TL;DR
An empirical study of implicit reasoning in recurrent-depth transformers (Huginn, Ouro). Evaluates two compositional-generalization modes: **systematic generalization** (combining knowledge never seen together in training) and **depth extrapolation** (test-time recurrence beyond training k). Finds recurrent-depth transformers meaningfully outperform non-recurrent baselines on both.

## Relevance
Gives Branch A concrete probes for "does depth recurrence improve compositional reasoning?" — a cleaner scientific question than benchmark accuracy. Branch D: important check on whether CPF adds value beyond plain recurrent depth on compositional tasks.
