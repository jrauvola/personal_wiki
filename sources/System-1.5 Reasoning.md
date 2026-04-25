---
type: source
title: "System-1.5 Reasoning — Dynamic Shortcuts in Language and Latent Spaces"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/self-distillation
  - method/early-exit
  - method/adaptive-compute
status: read
related:
  - "[[CODI]]"
  - "[[Adaptive Latent RL]]"
  - "[[Self-Distillation]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2505.18962-system-1-5-reasoning]]"
source_type: paper
arxiv_id: "2505.18962"
venue: "arXiv"
date_published: 2025-05-25
authors:
  - "Xiaoqiang Wang"
  - "Suyuchen Wang"
  - "Yun Zhu"
  - "Bang Liu"
url: "https://arxiv.org/abs/2505.18962"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Recent latent-space reasoning methods improve efficiency by operating on hidden states without decoding into language, yet they treat all steps uniformly, failing to distinguish critical deductions from auxiliary steps and resulting in suboptimal use of computational resources."
  - "The model depth shortcut (DS) adaptively reasons along the vertical depth by early exiting non-critical tokens through lightweight adapter branches, while allowing critical tokens to continue through deeper Transformer layers."
  - "The step shortcut (SS) reuses hidden states across the decoding steps to skip trivial steps and reason horizontally in latent space."
  - "Training System-1.5 Reasoning involves a two-stage self-distillation process: first distilling natural language CoT into latent-space continuous thought, and then distilling full-path System-2 latent reasoning into adaptive shortcut paths (System-1.5 Reasoning)."
  - "On GSM8K, System-1.5 Reasoning achieves reasoning performance comparable to traditional CoT fine-tuning methods while accelerating inference by over 20x and reducing token generation by 92.31% on average."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Two-stage self-distillation is directly comparable to LT-Tuning's 3-stage curriculum; shortcut-path distillation as stage 2 is an additional ingredient worth considering in the CPF/CODI curriculum."
  - slug: "branch-a"
    relevance: secondary
    why: "Claims 20× inference speedup on GSM8K — Qwen3-scale throughput matters; worth checking whether shortcuts transfer."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Two-stage self-distillation is an instance of the V2/SIM-CoT/LT-Tuning synthesis — concrete data point."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# System-1.5 Reasoning — Dynamic Shortcuts in Language and Latent Spaces

Wang, Wang, Zhu, Liu, [arXiv:2505.18962](https://arxiv.org/abs/2505.18962).

## TL;DR

Latent methods today apply the full transformer depth to every reasoning step — wasted compute when some steps are trivial. System-1.5 introduces two dynamic shortcuts:
- **Depth shortcut (DS):** non-critical tokens early-exit via lightweight adapter branches; critical tokens continue through deeper layers.
- **Step shortcut (SS):** hidden states reused across steps to skip trivial steps.

Training is **two-stage self-distillation**: stage 1 distills NL CoT → latent continuous thought (a CODI-style recipe); stage 2 distills full-path System-2 latent reasoning → adaptive shortcut paths. On GSM8K, comparable accuracy with 20× inference speedup and 92.31% token reduction.

## Method

- Stage 1 distillation — standard teacher-student across explicit → continuous.
- Stage 2 distillation — full-path "System-2" latent rollout → shortcut paths.
- DS adapter branches implement per-token early exit.
- SS hidden-state reuse implements per-step skipping.

## Recipe

1. Pretrain or take existing latent-CoT model (e.g., CODI-style).
2. Stage 1: NL CoT → continuous thought distillation.
3. Stage 2: full-path reasoning → shortcut-path distillation; add DS adapter branches + SS skip heuristic.
4. Inference: dynamically route per token/step.

## Results

- GSM8K: ≈ CoT-SFT accuracy, 20× inference speedup, 92.31% token reduction.

## Relevance

Two-stage distillation is structurally similar to LT-Tuning's 3-stage curriculum — both commit to **multi-phase distillation** rather than single-shot supervision. For branch-d, the concrete question is whether stage-2 shortcut distillation can be added on top of CPF fusion to yield further efficiency wins while preserving the anti-collapse gains. The 20× speedup claim is quantitatively aggressive; worth checking under stable supervision regimes.

## Citation links to chase

- CODI (stage-1 distillation baseline).
- Adaptive Latent RL (dynamic compute allocation as a comparison class).
