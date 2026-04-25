---
type: source
title: "From Explicit CoT to Implicit CoT: Learning to Internalize CoT Step by Step (Deng, Choi, Shieber 2024)"
source_type: paper
arxiv_id: "2405.14838"
venue: "arXiv"
date_published: 2024-05-23
authors:
  - "Yuntian Deng"
  - "Yejin Choi"
  - "Stuart Shieber"
url: "https://arxiv.org/abs/2405.14838"
code_repo: "https://github.com/da03/Internalize_CoT_Step_by_Step"
has_weights: false
status: read
confidence: high
key_claims:
  - "Single-model curriculum: start with explicit CoT training, then linearly remove tokens over epochs via schedule s(t) = ⌊Δt/T⌋ — Δ=8 tokens/epoch for multiplication, Δ=1 for GSM8K."
  - "No teacher-student architecture (unlike earlier iCoT-KD): the same model is trained end-to-end; reasoning is internalized as CoT tokens are gradually removed."
  - "Training stabilizers load-bearing: 'removal smoothing' (random offsets in the removal schedule) + 'optimizer reset' (zero Adam second-moments when removal step occurs) prevent loss jumps from token deletions."
  - "GPT-2 Small on 9-digit × 9-digit multiplication: 99% accuracy. Standard CoT training fails beyond 4×4."
  - "Mistral-7B on GSM8K: >50% accuracy with NO intermediate token emission at inference."
  - "Does not use continuous-thought feedback (unlike COCONUT); CoT tokens are removed, nothing is substituted. This is the key architectural distinction."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Direct predecessor to COCONUT's staged curriculum. Clean minimal-moving-parts baseline that isolates the 'gradual CoT removal' hypothesis without any continuous-thought complication."
  - slug: "branch-a"
    relevance: secondary
    why: "Mistral-7B GSM8K result is scaling-relevant baseline; 9×9 multiplication demonstrates depth-of-reasoning gains from curriculum alone."
  - slug: "branch-b"
    relevance: reference
    why: "Training-stability techniques (removal smoothing, optimizer reset) are relevant to BPTT/detach stability but not a direct axis intervention."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: secondary
    why: "Pure curriculum ablation (no fusion, no anchor) — useful contrast for isolating CPF's contribution."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - family/implicit-cot
  - method/curriculum
  - method/no-continuous-thought
  - type/source
related:
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[COCONUT]]"
  - "[[Pause Tokens]]"
  - "[[Yuntian Deng]]"
sources: []
---

# Stepwise Internalization (Deng, Choi, Shieber 2024)

## TL;DR

Single-model curriculum: progressively remove CoT tokens over epochs, with removal smoothing + optimizer reset for stability. GPT-2 Small solves 9×9 multiplication at 99%; Mistral-7B solves >50% of GSM8K without emitting any intermediate tokens. No teacher-student, no continuous-thought feedback — pure curriculum ablation.

## Why this matters to our project

Stepwise Internalization is the **cleanest curriculum-only ablation** of the latent-reasoning program:

- **No emulator.** Drops the teacher-student auxiliary model from [[Implicit CoT via Knowledge Distillation]].
- **No continuous-thought feedback.** Unlike [[COCONUT]], the removed CoT positions are *not* replaced with recycled hidden states — they are simply *absent* from the training target.
- **No anchor / fusion.** Unlike LT-Tuning's CPF, there is no explicit mechanism to bind latent trajectory to vocab space.

This makes it the **null model** for curriculum-based latent reasoning: if a task's gains from COCONUT vanish when you drop continuous-thought feedback and just do Stepwise Internalization, the curriculum is doing most of the work. If COCONUT dominates Stepwise Internalization on a task, the continuous-thought machinery is load-bearing. This dichotomy has not been explicitly published — probably the single most valuable ablation missing from the field.

## Method

**Curriculum schedule:** 
$$
s(t) = \lfloor \Delta t / T \rfloor
$$
where $s(t)$ is the number of CoT tokens to remove at training step $t$, $\Delta$ is the tokens-per-epoch rate, $T$ is total training steps.

- Multiplication: $\Delta = 8$ per epoch.
- GSM8K: $\Delta = 1$ per epoch.

**Removal smoothing.** Instead of removing exactly $s(t)$ tokens at each step, sample from $s(t) + \text{Uniform}(-\delta, +\delta)$ to avoid abrupt loss jumps.

**Optimizer reset.** At each removal event, zero Adam's second-moment accumulator to prevent stale step-size estimates from causing instability.

**No special tokens.** The CoT region is simply truncated; no `<bot>`/`<eot>` delimiters, no filler tokens.

## Results

**GPT-2 Small on N×N multiplication:**

| N | Standard training | Stepwise Internalization |
|---|-------------------|--------------------------|
| 4 | ≈100% | ≈100% |
| 5 | <10% | 99%+ |
| 7 | <1% | 99%+ |
| 9 | <1% | 99%+ |

**Mistral-7B on GSM8K:** >50% accuracy with NO emitted intermediate tokens at inference.

## Relevance to CODI / COCONUT contrast

This is the most important precursor to read before proposing curriculum alternatives. The paper's minimalism is exactly what the field is missing: if you run Stepwise Internalization + Pause Tokens, you get nearly everything COCONUT offers without the continuous-thought-recycling complexity. The **missing ablation** in the literature is:

$$
\Delta_{\text{continuous thought}} = \text{COCONUT accuracy} - \text{Stepwise Internalization accuracy}
$$

If this delta is small on most benchmarks, the entire COCONUT complexity is unjustified. If large, it provides a clean story for "what continuous-thought feedback specifically adds." Either way, the comparison tells us what we actually need.

## Citation links to chase

- [[Implicit CoT via Knowledge Distillation]] (Deng 2023) — teacher-student predecessor.
- [[COCONUT]] — adds continuous-thought feedback on top of this curriculum.
- [[Pause Tokens]] — orthogonal "add null tokens" intervention.
