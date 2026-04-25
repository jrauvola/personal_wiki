---
type: concept
title: "Loop-Mode Emission"
created: 2026-04-23
updated: 2026-04-24
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/failure-mode
  - domain/interpretability
status: evergreen
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Format-Prior Loop"
  - "Template Loop Emission"
related:
  - "[[Shortcut Behavior]]"
  - "[[Routing vs Reasoning]]"
  - "[[Feature Collapse]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[SIM-CoT]]"
  - "[[SwiReasoning]]"
  - "[[ThinkRouter]]"
  - "[[CODI]]"
sources:
  - "[[.raw/experiments/inert_latent_F1_F6]]"
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Loop-mode emission is the Track A / Phase 1 headline failure mode for V2 bf16 at Qwen3-4B; direct characterization for Branch A."
  - slug: "branch-d"
    relevance: primary
    why: "CPF and related fusion anchors are candidate mitigations for loop-mode emission."
  - slug: "branch-b"
    relevance: reference
    why: "Detach variants modulate loop rate; not the primary axis for this failure mode."
  - slug: "branch-c"
    relevance: secondary
    why: "Loop-detection regex is a cheap inference-time diagnostic that probe methodology should include."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Concrete, named failure mode for the writeup; paired with [[Routing vs Reasoning]]."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Loop-Mode Emission

## Definition

A latent-reasoning model is in *loop-mode emission* when its output is a repeating format-prior substring (≥15 chars repeated ≥3×) that does not consult the question's content.

## Diagnostic criteria (from SPAR, 2026-04-23)

- **Loop detection:** regex pattern of a ≥15 character substring repeated ≥3× in the decoded prediction.
- **Question-content check:** fraction of loop substrings containing any digit present in the question. Below ~20% → loop is context-free; above ~70% → loop consults the question.
- **Target-alignment check:** fraction of loop substrings containing any digit from the target. Elevated fractions for small-target benchmarks (e.g. SVAMP) reflect random-match probability, not question-reading.

## V2 bf16 empirics (num_latent=8)

From `research_findings/inert_latent_hypothesis_tests.md` F2:

| benchmark | loop rate | loop has question-digit |
|---|---|---|
| GSM8k | 99.9% | 12% |
| GSM-hard | 100.0% | 13% |
| SVAMP | 100.0% | 12% |

Nearly all V2 bf16 predictions are looped, and only ~12% of loops show any question-digit overlap — the loop is context-free.

## Relationship to routing

Loop-mode emission is the **output-side manifestation** of [[Routing vs Reasoning#Routing|routing-mode latents]]: latents route the decoder into the format-prior loop attractor, and once inside the attractor the decoder emits the template regardless of input. The Track A first-sentence-trim finding (flat num_latent curve after trimming predictions at first period) is direct evidence that V2's rising num_latent accuracy curve is a lucky-match artifact of extended loop content, not iterative reasoning.

## Interventions targeted at loop-mode emission

- Auxiliary step decoder ([[SIM-CoT]]) — break the template by forcing per-step decoder-visibility.
- [[Context-Prediction-Fusion]] — anchor latents against the vocab so that loops cost fidelity.
- Hybrid discrete-latent switches ([[SwiReasoning]], [[ThinkRouter]]) — let the model escape from the loop attractor with a discrete token.

## Open questions

- Does loop-mode emission scale with model size, or is it a 4B-specific failure?
- Is loop-mode driven primarily by training distribution (CODI's aug-NL) or by the distillation objective itself?
- Can a looping-detector auxiliary loss during training eliminate loop-mode without hurting accuracy?

## Stacked diagnostic (2026-04-24)

F4 latent-KV ablation × Track A first-sentence-trim regrading, *stacked*, is a concrete criterion for distinguishing "real capability" from "loop-lucky-match + KV-dependent format prior." On GSM8k n=1319: F4-lost examples (88) are 94.3% target-in-loop (tight loops) yet 76/88 remain Track-A-trim-correct — i.e. Track A "rescues" loop-lucky predictions that F4 breaks, and vice versa. Intersecting the two surviving sets gives the 8.5% stacked floor (112/1319), below either test alone. The gap between F4 or Track A (~11-12%) and their intersection (~8.5%) is the size of the loop-lucky / format-prior routing component. See [[Routing vs Reasoning]] and `research_findings/f4_per_example_diagnosis.md`.
