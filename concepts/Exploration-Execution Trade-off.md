---
type: concept
title: "Exploration-Execution Trade-off"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/theory
  - domain/curriculum
status: developing
complexity: advanced
domain: latent-reasoning
aliases:
  - "Symbolic Index trade-off"
  - "Decisional certainty trade-off"
related:
  - "[[Capabilities and Limits of Latent CoT]]"
  - "[[Weak vs Strong Supervision Study]]"
  - "[[Curriculum Distillation]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Feature Collapse]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Theoretical justification for LT-Tuning's 3-stage curriculum — curriculum is proven necessary to traverse the trade-off."
  - slug: "branch-a"
    relevance: primary
    why: "Predicts which benchmarks expose architecture-dependent divergence: computation-heavy benchmarks live in high-Symbolic-Index regime, where latent reasoning is most fragile."
  - slug: "branch-b"
    relevance: reference
    why: "Orthogonal to detach/BPTT, but informs which tasks to evaluate on."
  - slug: "branch-c"
    relevance: reference
    why: "General theory; not probe-specific."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Theoretical keystone for the writeup's method-taxonomy organization."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Exploration-Execution Trade-off

Theoretical framing from [[Capabilities and Limits of Latent CoT]] (2602.01148) — explains why latent CoT models show the characteristic split of *high exploration* / *low computation* accuracy.

## The trade-off

Let **Symbolic Index** (SI) ≈ inverse entropy of the step-level output distribution.

| Regime | SI | Behavior |
|---|---|---|
| Low SI | high entropy | Broad search, exploration wins, error accumulation on computation |
| High SI | low entropy | Committed decisions, execution wins, exploration degenerates |

**Fundamental claim**: you cannot set a constant SI that achieves both high exploration and high execution. The trade-off is not an empirical limitation — it's theoretical.

## Empirical evidence

From Zou, Xiong, Liu (2026):

| Task type | Benchmark | Accuracy |
|---|---|---|
| Exploration | ProsQA | 97.0% |
| Computation | GSM8K | 34.1% |

The 63-point spread is the trade-off in action.

## Why curriculum learning is necessary

Three theorems from the paper:

1. **Fundamental trade-off**: no constant-SI policy achieves both capabilities.
2. **Direct training fails provably**: distributional mismatch between training and inference under fixed SI causes error that cannot be reduced.
3. **Curriculum learning works**: progressive SI adjustment across training phases traverses the trade-off.

This converts [[Latent Thoughts Tuning]]'s empirical finding (Stage 3 CPF activation gives +23.5% at 8B) from a hyperparameter-tuning observation into a **theorem**: curriculum is required, not optional.

## Practical implications

- **Choose benchmarks by regime.** Computation-heavy (GSM8K, MATH) probes the fragile high-SI regime; exploration-heavy (ProsQA, multi-hop QA) probes the safe low-SI regime. Reporting both separately is essential to claim general latent-reasoning capability.
- **Curriculum is load-bearing.** Three-stage curricula (LT-Tuning, CODI) aren't decorative — they're mechanistically required.
- **Architecture may set prior SI.** Different architectures (Qwen3 vs Gemma-3 vs Llama) may have different default Symbolic Indices due to embedding-tying, RMSNorm placement, etc., which may be *the* architecture-dependence mechanism [[branch-a]] has been chasing.

## Connection to Shortcut Behavior

Low SI + complex task → error accumulation → model falls back on [[Shortcut Behavior]]. High SI + novel task → commitment to wrong answer → different failure mode. Both failure modes live on the SI axis.

## Sources

- [[Capabilities and Limits of Latent CoT]] — primary source.
- [[Weak vs Strong Supervision Study]] — empirical companion (strong supervision ≈ pinning SI high).
- [[Latent Thoughts Tuning]] — curriculum implementation informally solving the trade-off.
