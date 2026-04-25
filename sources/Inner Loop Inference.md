---
type: source
title: "Inner Loop Inference — Unlocking Latent Capabilities Without Training"
source_type: paper
arxiv_id: "2602.14759"
venue: "arXiv"
date_published: 2026-02-16
authors:
  - "Jonathan Lys"
  - "Vincent Gripon"
  - "Bastien Pasdeloup"
  - "Axel Marmoret"
  - "Lukas Mauch"
  - "Fabien Cardinaux"
  - "Ghouthi Boukli Hacene"
url: "https://arxiv.org/abs/2602.14759"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "RESULT: A pretrained (non-recurrent) Transformer can be made to reason in latent space at inference time with NO additional training by looping individual Transformer blocks (or groups of blocks) on their own output before passing to the next block."
  - "MECHANISTIC FRAMING: Residual connections decompose each block's output into input-copy + block-delta; iterating a block is equivalent to iterated refinement in the shared residual space — aligns with logit-lens-style interpretability claims."
  - "RESULT: Inner-loop inference unlocks latent capabilities that standard forward passes miss — gains on reasoning tasks without any fine-tuning or architecture change."
  - "RELATIONSHIP: Unlike Huginn (trained from scratch as recurrent) and Retrofitted Recurrence (mid-training conversion), Inner Loop Inference is TRAIN-FREE — closest to [[Skip a Layer or Loop it]] (CoLa)."
  - "IMPLICATION: Depth recurrence may be partially latent in any standard Transformer — suggests recurrent training doesn't create capability so much as expose latent capability."
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Train-free recurrence test: apply Inner Loop Inference to Qwen3-4B as a free diagnostic — does Qwen3 already have latent recurrent capability before we train it? Zero-cost preliminary."
  - slug: "branch-b"
    relevance: secondary
    why: "Residual-space iterative-refinement framing motivates a cleaner detach story — detach can be understood as truncating the iterative refinement trace."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Essential counterpoint to the 'recurrent depth requires from-scratch or curriculum training' narrative — if some capability is train-free, the umbrella taxonomy must distinguish trained vs discovered recurrence."
  - slug: "branch-d"
    relevance: reference
    why: "Train-free inner-loop inference doesn't need vocab-anchoring. Useful framing for the CPF discussion: when is anchoring necessary?"
last_reviewed: 2026-04-23
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/inference-time
  - domain/interpretability
  - family/recurrent-depth
related:
  - "[[Scaling Up TTC]]"
  - "[[Skip a Layer or Loop it]]"
  - "[[Retrofitted Recurrence]]"
sources:
  - "[[.raw/papers/2602.14759-inner-loop-inference]]"
---

# Inner Loop Inference

## TL;DR
Loop individual Transformer blocks (or small groups) on their own output at inference time with a pretrained non-recurrent LM. Zero training. Gains on reasoning tasks. Motivated by the residual-decomposition view: each block's output = input + block-delta, so iterating a block is iterative refinement in the shared residual space.

## Method
- **Residual-based iterated block**: for block B_i with output h = B_i(x) + x, apply B_i k times on its own previous output. No parameters change.
- **Block selection**: either single block or small group; empirical choice.
- **Zero training**: drop-in at inference.

## Relevance
Establishes a null baseline for any "recurrent training improves capability" claim — we should always check Inner Loop Inference on the base model first. Cheap, informative.
