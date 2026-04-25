---
type: source
title: "CODI — Continuous Chain-of-Thought via Self-Distillation"
created: 2026-04-22
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/weak-supervision
  - method/distillation
status: read
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[Feature Collapse]]"
  - "[[Curriculum Distillation]]"
  - "[[Token Efficiency]]"
sources:
  - "[[.raw/papers/2502.21074-codi]]"
source_type: paper
arxiv_id: "2502.21074"
venue: "arXiv"
date_published: 2025-02-28
authors:
  - "Zhenyi Shen"
  - "Hanqi Yan"
  - "Linhai Zhang"
  - "Zhanghao Hu"
  - "Yali Du"
  - "Yulan He"
url: "https://arxiv.org/abs/2502.21074"
code_repo: "https://github.com/zhenyi4/codi"
has_weights: true
status: read
confidence: high
key_claims:
  - "CODI jointly trains a teacher task (Explicit CoT) and a student task (Implicit CoT), distilling reasoning ability from language into continuous space by aligning the hidden states of a designated token."
  - "CODI is the first implicit CoT approach to match the performance of explicit CoT on GSM8k at the GPT-2 scale, achieving a 3.1x compression rate and outperforming the previous state-of-the-art by 28.2% in accuracy."
  - "The final CoT step must be excluded from training data; otherwise the model develops a shortcut where the teacher's pre-answer hidden state copies the final answer token, corrupting the distillation target."
  - "Hidden activations of CoT tokens decompose as h_CoT^l ≈ h_no-CoT^l + f(W_V R(W_K R)^T q), theoretically justifying alignment of student hidden states with teacher to transfer reasoning."
  - "Removing the L1 distillation loss drops GSM8k-Aug accuracy from 43.7% to 24.5%, indicating distillation supervision is load-bearing rather than auxiliary."
  - "On verbose GSM8k-Aug-NL CoTs (65.5 avg tokens), CODI achieves 8.2× compression while surpassing CoT-SFT at GPT-2 scale and yielding 5.9× inference speedup."
projects:
  - slug: "branch-d"
    relevance: primary
    why: "LT-Tuning CPF is being implemented on top of CODI (branch-d goal literal); this is the base method for the primary experiment."
  - slug: "branch-a"
    relevance: primary
    why: "Foundational baseline currently executable in the harness; required as the Qwen3 scaling control."
  - slug: "branch-b"
    relevance: primary
    why: "Minimum-sufficient detach ablation runs over CODI variants (V2/V3/V4); this is the target architecture."
  - slug: "branch-c"
    relevance: secondary
    why: "Probe methodology debugging is framed around CODI-family models; provides context but not the debug target itself."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "CODI is one of the three synthesis inputs for the north-star workable latent reasoning model (V2 / SIM-CoT / LT-Tuning lineage)."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# CODI — Continuous Chain-of-Thought via Self-Distillation

Addresses the inherent complexities and forgetting phenomena associated with multi-stage curriculum training. Curriculum-based latent models require careful, phased transitions from text to continuous vectors, which is computationally expensive and prone to destabilization if intermediate stages lose their mapping to the final answer. CODI bypasses this entirely with a joint, multitask self-distillation framework that enables implicit learning in a single unified training step.

## Core thesis

A model can simultaneously act as its own teacher and student:

- **Teacher pathway** — standard autoregressive language modeling; explicitly verbalizes the intermediate reasoning steps.
- **Student pathway** — bypasses vocabulary space entirely; connects terminal hidden representations directly into subsequent inputs to cultivate continuous thoughts.

To transfer deductive capability from explicit teacher to implicit student, CODI isolates a single alignment target: the hidden state of the token immediately preceding the final answer. A strict distance penalty at this singular boundary injects the structural logic of the explicit rationale into the condensed latent trajectory without requiring full token-by-token continuous mapping.

## Training pipeline

Elegant single-stage execution.

1. **Data prep** — triplets of (query, explicit reasoning steps, final answer). **Critical:** truncate the final reasoning step from the teacher target sequence. If left intact, the model develops a degenerative shortcut where the teacher's hidden state copies the final answer token, circumventing genuine algorithmic processing.
2. **Joint forward pass** —
   - Teacher: cross-entropy over explicitly generated reasoning tokens.
   - Student: cross-entropy over final answer tokens following continuous rollout.
3. **Distillation loss** — $L_1$ distance between normalized hidden activations of the teacher's pre-answer token and the student's corresponding latent state. Normalization via standard deviation across the batch mitigates extreme variance in activation norms across layers.

## Public artifacts

Excellent.

- Codebase: [zhenyi4/codi](https://github.com/zhenyi4/codi)
- Checkpoints (HF):
  - `zen-E/CODI-gpt2`
  - `zen-E/CODI-llama3.2-1b-Instruct`
- Paper: [arXiv:2502.21074](https://arxiv.org/abs/2502.21074) — Shen, Yan, Zhang, Hu, Du, He (v1 Feb 2025; v3 Sep 2025).

## Empirical results

- Matches explicit text reasoning on GSM8K at GPT-2 scale.
- 3.1x compression rate.

## Integration notes

Highest immediate project fit for the current evaluation harness — the sole methodology currently fully implemented and executable (`methodology.md:153`). Strong benchmarkable baseline. Tempered by weak-supervision reliance: because the continuous trajectory is only anchored at the terminal distillation point, intermediate latent states are effectively unconstrained. Local testing docs (`PROJECT_STATE.md:82`) confirm released checkpoints are severely fragile and exhibit degenerative shortcut behavior outside standard mathematical templates. Optimal as a stable, high-performance baseline for structural validation — **not** the terminal target for generalized open-domain latent reasoning.

## SPAR empirical follow-up (2026-04-23)

Our Qwen3-4B-Instruct-2507 reimplementation of CODI V2 (bf16, `num_latent=8`) produces a ~70pp capability collapse vs the base model's zero-shot CoT on GSM8k (0.16 vs 0.86). The F1-F6 battery (see `research_findings/inert_latent_hypothesis_tests.md`) characterizes the learned latents as a *geometric routing key*, not a reasoning trace:

- **F1:** only 2.8% (28/~1000) V2-correct predictions are unique vs zero-shot — self-distillation adds essentially no new capability.
- **F3:** 7/8 latent positions decode to the fixed template `The → 0 → 0 → ? → . → . → . → .` (entropy <0.4 bits except step 3).
- **F4 + F5 + F6:** dropping the latent KV costs 25-29% accuracy, swapping with another example's KV costs 0%, and σ=0.5 Gaussian noise collapses accuracy to <3% — a narrow geometric basin that routes to the format-prior attractor regardless of per-example content.

The self-distillation objective at 4B preserves latents only as a template-routing signal; this is our candidate explanation for why naive CODI scaling breaks. Phase 2 CPF ([[Latent Thoughts Tuning]]) and SIM-CoT aux-decoder interventions are our test of whether the self-distillation recipe is salvageable. See [[Routing vs Reasoning]] and [[Loop-Mode Emission]].
