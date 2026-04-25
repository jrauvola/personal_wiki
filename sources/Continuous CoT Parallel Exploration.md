---
type: source
title: "Continuous Chain of Thought Enables Parallel Exploration and Reasoning (CoT2)"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/theory
  - type/source
  - method/csft
  - method/grpo
status: read
related:
  - "[[COCONUT]]"
  - "[[Reasoning by Superposition]]"
  - "[[GRPO]]"
  - "[[Soft Tokens Hard Truths]]"
sources:
  - "[[.raw/papers/2505.23648-continuous-cot-parallel-exploration]]"
source_type: paper
arxiv_id: "2505.23648"
venue: "ICLR 2026"
date_published: 2025-05-29
authors:
  - "Halil Alperen Gozeten"
  - "M. Emrullah Ildiz"
  - "Xuechen Zhang"
  - "Hrayr Harutyunyan"
  - "Ankit Singh Rawat"
  - "Samet Oymak"
url: "https://arxiv.org/abs/2505.23648"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Continuous Supervised Fine-Tuning (CSFT) trains the model to match a target probability distribution α_t* (convex combination of vocabulary embeddings) via KL divergence instead of one-hot targets — equivalent to token-level knowledge distillation where the teacher distribution comes from a logic/search algorithm."
  - "GRPO-based RL with continuous output tokens uses Dirichlet sampling to generate diverse rollouts in continuous space, bridging discrete-SFT initialization with continuous RL fine-tuning."
  - "CoT2 tokens can emit up to O(d) bits per step (embedding dimension) vs log2(v) bits for discrete tokens (vocabulary size) — quantifying the information-capacity gap that motivates continuous reasoning."
  - "A single-layer transformer with attention + mixture-of-experts MLP can solve the Minimum Non-Negative Sum (MNNS) task using the proposed CoT2 construction."
  - "Continuous CoT requires larger embedding dimensions to represent multiple parallel reasoning traces on more complex tasks — noted as a limitation."
  - "CSFT outperforms both base CoT2 and discrete CoT on MNNS, ProntoQA, and ProsQA; CoT2-MTS (multi-task supervised) further improves performance."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Dirichlet-sampling GRPO + continuous rollouts is a candidate for adding RL to the 8B Qwen3 pipeline — but requires custom infrastructure."
  - slug: "branch-b"
    relevance: reference
    why: "Not a detach/gradient-stability study."
  - slug: "branch-c"
    relevance: reference
    why: "Unrelated."
  - slug: "branch-d"
    relevance: secondary
    why: "CSFT's distributional target (convex combo of vocabulary embeddings) is structurally identical to LT-Tuning's CPF interpolation target — direct theoretical support."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Theory+RL companion to [[Reasoning by Superposition]]; CSFT formulation is structurally equivalent to CPF, useful citation but not an active synthesis input — theoretical framing is anchored by [[Reasoning by Superposition]] and [[Capabilities and Limits of Latent CoT]]."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Continuous Chain of Thought (CoT2) — Parallel Exploration and Reasoning

## TL;DR

Proposes CSFT (Continuous Supervised Fine-Tuning) — train on soft targets α_t* (distributions over vocabulary) via KL loss, equivalent to token-level KD from a logic/search teacher. Extends to GRPO with Dirichlet-sampled rollouts in continuous space. Theoretical construction: single-layer transformer + MoE MLP solves MNNS. Positions "CoT2" as the continuous-targets SFT paradigm and provides information-capacity bound O(d) bits/step vs log2(v).

## Method

**CSFT:**
- At reasoning step t, target α_t* = Σ_i α_{t,i}* e_i is a convex combination of vocabulary embeddings.
- Loss: D(α_t || α_t*) — cross-entropy / KL — aligning model's predicted distribution α_t with teacher.
- Interpretation: token-level knowledge distillation; teacher may be a logic/search algorithm.
- At final step t=m, target is one-hot (discrete answer).

**GRPO with continuous outputs:**
- Dirichlet sampling for generating diverse rollouts from continuous-output models.
- Connects to Latent Dirichlet Allocation and AlphaGo's Dirichlet exploration noise.
- Two sampling methods demonstrated: direct continuous sampling and discrete-to-continuous adaptation.

**Theoretical construction:**
- Single-layer transformer with attention + mixture-of-experts MLP solves MNNS.
- Comparison: base CoT2, CoT2-MTS (multi-task supervised), discrete CoT.

## Recipe

- Tasks: MNNS (synthetic arithmetic), ProntoQA, ProsQA.
- Trained on L40S GPUs (48GB), single GPU per experiment.
- 4-digit MNNS: ~3h/run; 5-digit: ~10x larger.
- Sparse reward RL setup: 1 for correct final answer, 0 otherwise.

## Results

- CSFT > discrete SFT on MNNS, ProntoQA, ProsQA.
- CoT2-MTS (multi-target supervised) > base CoT2.
- Dirichlet-sampled GRPO enables continuous RL training from discrete-SFT initialization.
- Limitation: more complex tasks require larger embedding dimensions to represent parallel traces.

## Relevance to our project

**Primary for spar-latent-reasoning writeup.** Paired with [[Reasoning by Superposition]], this paper completes the theoretical+empirical foundation for continuous-CoT expressivity. The CSFT target formulation (convex combination of vocabulary embeddings supervised via KL) is structurally equivalent to [[Latent Thoughts Tuning]]'s Context-Prediction-Fusion anchor: both push the model's intermediate distributions toward mixtures of vocabulary embeddings rather than hidden-state ambiguous vectors. Secondary for **Branch D** as direct theoretical support for CPF-style anchoring. Secondary for **Branch A** because the Dirichlet-GRPO recipe is a viable test-time enhancement worth considering for 8B scaling (though infrastructure cost is nontrivial).

## Citation links to chase

- [[Reasoning by Superposition]] (2505.12514) — theoretical companion.
- Wang et al. 2022 (Self-consistency) — single-inference aggregation analog.
- AlphaGo (Silver et al. 2017) — Dirichlet noise precedent.
- LDA (Blei et al. 2003) — Dirichlet-prior motivation.
- [[COCONUT]] / [[CODI]] — baselines.
