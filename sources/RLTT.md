---
type: source
title: "RLTT: Rewarding Latent Thought Trajectories for LoopLMs"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/reinforcement-learning
  - method/rl
  - method/looped-lm
  - type/source
status: read
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
  - "[[Adaptive Exit Gate]]"
  - "[[GRPO]]"
sources:
  - "[[.raw/papers/2602.10520-rltt]]"

source_type: paper
arxiv_id: "2602.10520"
venue: "arXiv"
date_published: 2026-02-11
authors:
  - "Jonathan Williams"
  - "Esin Tureci"
url: "https://arxiv.org/abs/2602.10520"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "Standard RL (GRPO) assigns credit only to the final latent state — mismatched with LoopLM multi-step internal computation; this is the direct cause of Ouro's reported GRPO/DAPO post-SFT failure."
  - "RLTT distributes reward across all loop iterations with weighted sum ∑ω_t across t=1..T_max, ∑ω_t=1; three weightings tested (exit-probability from Ouro's gate, progressive exponential, uniform)."
  - "On Ouro-2.6B-Thinking (MATH split, 140 steps, 4xH200), RLTT beats GRPO by +14.4 on MATH-500, +16.6 on AIME24, +10.0 on BeyondAIME, +34.3 on GSM8K (pass@1 deterministic)."
  - "Transfer zero-shot to non-math: +18.7 GPQA, +3.5 MMLU-ST, +3.3 MBPP; train on math → generalize."
  - "RLTT converges to substantially SHORTER responses than GRPO without explicit brevity reward — emergent side-effect of trajectory-level alignment; ~10% training wall-clock speedup."
  - "Theorem A.5: under diminishing-reward-returns assumptions, trajectory-level credit yields weakly smaller optimal decoding length than terminal-only objectives."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "LoopLM-RL, not Qwen3 architecture-dependent."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach/fp32 tool."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not a probe methodology tool."
  - slug: "branch-d"
    relevance: reference
    why: "Trajectory-level credit assignment could in principle be ported to CODI (reward each latent step, not just final token) — interesting future-work pointer but heavy infra lift; the exit-probability weighting requires a learned gate we wouldn't have."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "DIRECTLY resolves Ouro's reported RL failure — was a flagged open problem in our [[Ouro]] ingest. Uses public Ouro-2.6B-Thinking checkpoint, open replication target. Same RL infra requirement (variable-depth rollout) our Ouro page called out as upstream-broken — RLTT shows it IS surmountable if you distribute credit."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# RLTT: Rewarding Latent Thought Trajectories

## TL;DR

LoopLMs like [[Ouro]] reason over multiple latent loops. Standard RL (GRPO) gives reward only to the final latent state → mismatched with the multi-step internal computation and, per Ouro's own §RL-failure section, breaks. **RLTT distributes reward across all loop iterations** via a weighted sum of per-iteration policy gradients. Trained on Ouro-2.6B-Thinking with MATH, RLTT gets +14-34 pts over GRPO on math benchmarks and transfers zero-shot to non-math.

## Core fix

Standard objective — only P_θ^(T_max) at final loop:

$\nabla J_{GRPO} = \mathbb{E}\left[\sum_i \sum_j \nabla \log P_\theta^{(T_{max})}(y_{ij} | x, y_{i<j}) \hat{A}_i\right]$

RLTT — replace terminal distribution with weighted sum across t=1..T_max:

$\nabla J_{RLTT} = \mathbb{E}\left[\sum_i \sum_j \sum_t \omega_t \nabla \log P_\theta^{(t)}(y_{ij} | x, y_{i<j}) \hat{A}_i\right], \quad \sum_t \omega_t = 1$

**Three weighting strategies:**
- **Exit-probability** — uses [[Adaptive Exit Gate|Ouro's learned halting]] signal.
- **Progressive** — later loops exponentially up-weighted.
- **Uniform** — equal credit.

## Training recipe

- **Model:** Ouro-2.6B-Thinking (base LoopLM ckpt).
- **Dataset:** MATH training split (Hendrycks 2021).
- 140 optimization steps, 4× H200 GPUs.
- 32 prompts/batch × 8 rollouts/prompt.
- Max 2048 generation tokens during training.
- LR 1e-6 (warmup), KL coef 1e-3.
- Binary 0/1 reward (answer correctness only — no external verifier).
- ~10% training wall-clock speedup vs GRPO (shorter responses emerge naturally).

## Results — Pass@1 deterministic

**Math (in-domain):**

| Benchmark | GRPO | RLTT | Δ |
|---|---|---|---|
| MATH-500 | 71.6 | 86.0 | **+14.4** |
| AIME24 | 16.7 | 33.3 | **+16.6** |
| BeyondAIME | 6.0 | 16.0 | **+10.0** |
| GSM8K | 59.7 | 94.0 | **+34.3** |

**Non-math (zero-shot transfer):**

| Benchmark | GRPO | RLTT | Δ |
|---|---|---|---|
| ARC-C | 93.7 | 94.4 | +0.7 |
| MMLU-ST | 86.1 | 89.6 | +3.5 |
| GPQA | 19.7 | 38.4 | **+18.7** |
| MBPP | 61.3 | 64.6 | +3.3 |

Paired t-tests (p<0.05) confirm significance across sampling-based eval.

## Secondary findings

1. **Response length:** RLTT converges to shorter responses without brevity incentive.
2. **Loop-count robustness:** RLTT beats GRPO at every loop count; especially large margins at 1-2 loops.
3. **Token efficiency:** consistent advantage across decode budgets 1024-4096.
4. **No entropy collapse:** pass@k maintains steeper scaling than GRPO.
5. **Theorem A.5:** trajectory-level credit → weakly smaller optimal decoding length under diminishing-return assumptions.
6. **GSNR analysis (Table 10):** gradient signal quality improves most on the hardest benchmarks (AIME24, BeyondAIME).

## Relevance

- **Direct resolution of Ouro's open RL failure.** Our [[Ouro]] page flagged vLLM/SGLang rollout infra as broken for variable-depth; RLTT sidesteps by reframing credit assignment so the off-policy mismatch becomes tractable. Net: LoopLMs + RL are viable if you attribute across loops.
- **Replicable target:** Ouro-2.6B-Thinking is public; recipe is 140 steps on 4× H200 — feasible for us if we later want to try RL on a latent-reasoning model.
- **Architecture-specific, not portable off-the-shelf to CODI:** RLTT as written uses Ouro's learned halting gate for exit-prob weighting; CODI has no gate. Uniform or progressive weighting would still work but lose one of the three weightings.

## Cross-links

- [[Ouro]] — model this method patches.
- [[LoopLM]] — architectural family.
- [[GRPO]] — baseline the method replaces.
- [[Adaptive Exit Gate]] — source of exit-probability weighting.
