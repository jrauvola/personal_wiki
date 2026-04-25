---
type: source
title: "Hierarchical Reasoning Model"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/architecture
  - type/source
  - method/recurrent
  - method/deep-equilibrium
status: read
related:
  - "[[COCONUT]]"
  - "[[LoopLM]]"
  - "[[Ouro]]"
  - "[[Fixed-Width Depth Recurrence]]"
  - "[[Adaptive Exit Gate]]"
sources:
  - "[[.raw/papers/2506.21734-hierarchical-reasoning-model]]"
source_type: paper
arxiv_id: "2506.21734"
venue: "arXiv"
date_published: 2025-06-26
authors:
  - "Guan Wang"
  - "Jin Li"
  - "Yuhao Sun"
  - "Xing Chen"
  - "Changling Liu"
  - "Yue Wu"
  - "Meng Lu"
  - "Sen Song"
  - "Yasin Abbasi Yadkori"
url: "https://arxiv.org/abs/2506.21734"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "HRM, with 27M parameters and 1000 training samples (no pre-training, no CoT supervision), achieves 40.3% on ARC-AGI, surpassing o3-mini-high (34.5%) and Claude 3.7 8K-context (21.2%)."
  - "Two coupled recurrent modules (high-level slow + low-level fast) execute N high-level cycles of T low-level timesteps; L-module re-converges at each cycle, producing NT effective depth via 'hierarchical convergence.'"
  - "One-step gradient approximation (Deep Equilibrium Model / Implicit Function Theorem-inspired) replaces BPTT, giving O(1) memory vs O(T), enabling scalable recurrent training."
  - "Adaptive Computation Time via Q-learning head lets the model dynamically halt after M_min ≤ m ≤ M_max segments, trained with sequence loss + Q-loss jointly."
  - "Participation ratio (PR) of H-module state (89.95) is substantially larger than L-module state (30.22) after Sudoku-Extreme training, mirroring cortical dimensionality hierarchy."
  - "HRM solves Sudoku-Extreme Full and 30x30 maze pathfinding with near-perfect accuracy where CoT-based frontier LLMs score 0%."
projects:
  - slug: "branch-a"
    relevance: secondary
    why: "Recurrent-architecture alternative to Qwen/Gemma scaling — relevant only if architecture-dependence finding pushes toward recurrent designs."
  - slug: "branch-b"
    relevance: secondary
    why: "One-step gradient approximation + deep-supervision detach is a BPTT-free alternative worth citing in detach/fp32 ablation writeup."
  - slug: "branch-c"
    relevance: reference
    why: "Probe-methodology context only; HRM uses different benchmark suite."
  - slug: "branch-d"
    relevance: reference
    why: "Not a fusion/anchor recipe; orthogonal to LT-Tuning CPF."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Key taxonomic contrast as the 'no-CoT, from-scratch recurrent' branch — cited in the writeup as a counterpoint to distillation-based methods, but not a synthesis input for the V2/SIM-CoT/LT-Tuning north-star."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Hierarchical Reasoning Model (HRM)

## TL;DR

HRM is a 27M-parameter recurrent architecture that performs latent reasoning with two interdependent modules (slow H-module + fast L-module), trained without pretraining or CoT supervision. It uses a one-step DEQ-style gradient approximation (O(1) memory, no BPTT) and an ACT Q-learning halting head. Achieves near-perfect Sudoku-Extreme and 30x30 maze accuracy, and 40.3% on ARC-AGI, beating much larger frontier LLMs. The participation-ratio hierarchy (H=89.95 > L=30.22) mirrors cortical dimensionality gradients.

## Method

- **Architecture:** input net f_I, low-level recurrent module f_L, high-level recurrent module f_H, output head f_O. Both modules are encoder-only Transformer blocks (Llama-style: RoPE, GLU, RMSNorm, Post-Norm, Adam-atan2).
- **Hierarchical convergence:** N high-level cycles of T low-level timesteps. L-module iterates T times toward a local equilibrium conditioned on current H-state; H-module updates once per cycle and resets L-module's convergence phase. Effective depth = NT without vanishing-gradient pathology.
- **One-step gradient:** treats final L and H states as equilibria; backprops through only the last forward step of each module. Theoretically grounded in DEQ / Implicit Function Theorem (Neumann series truncated after first term). O(1) memory.
- **Deep supervision:** hidden state between supervision segments is detached; segments behave like 1-step gradient approximations of recursive deep supervision. Provides regularization and stability without replay buffers/target networks.
- **Adaptive Computation Time:** Q-head predicts (Q_halt, Q_continue) from final H-state; episodic MDP with binary reward (correctness on halt, 0 on continue). Randomized M_min (uniform over [2, M_max] with prob ε, else 1). Stable Q-learning follows from Post-Norm + AdamW weight decay bounding parameters.

## Recipe

- Sudoku-Extreme Full, 30x30 mazes, ARC-AGI: ~1000 training samples.
- No pre-training, no CoT data.
- Adam-atan2 optimizer, constant LR with linear warmup.
- stablemax replacing softmax for small-sample generalization.
- Truncated LeCun-Normal init for parameters; truncated-Normal init for z0 states (std 1, trunc 2), fixed across training.

## Results

- Sudoku-Extreme Full: near-perfect; frontier CoT LLMs: 0%.
- 30x30 mazes (optimal path): near-perfect; CoT baselines: 0%.
- ARC-AGI Challenge: 40.3% (vs o3-mini-high 34.5%, Claude 3.7 8K 21.2%) with only 900-token context.
- Inference-time scaling: increasing M_max at test time improves Sudoku monotonically; ARC-AGI saturates quickly.
- Brain correspondence: H-module PR = 89.95, L-module PR = 30.22 after Sudoku-Extreme training; scaling unique trajectories 10→100 grows H-module PR monotonically.

## Relevance to our project

Primary interest for [[spar-latent-reasoning]] because HRM is the dominant example of *non-curriculum* latent reasoning — it learns reasoning structure from scratch rather than distilling from an explicit CoT teacher. This makes it a useful contrast point when we frame LT-Tuning/CODI/COCONUT curricula as a distinct branch of the field. The one-step DEQ gradient is a useful citation for [[branch-b]]'s BPTT/detach ablations: HRM shows that O(1) memory training can be stable given appropriate normalization (Post-Norm) and optimizer choices (AdamW weight decay). Not directly portable to our CODI/LT-Tuning stack because HRM is trained from scratch on synthetic tasks, not fine-tuned from a pretrained LLM.

## Citation links to chase

- Gallici et al. (theoretical stability of Q-learning under Post-Norm + weight decay).
- DEQ / Implicit Function Theorem grounding (Bai et al. 2019).
- Stream-of-Search / Searchformer (CoT-supervised transformer baselines on maze).
