---
type: concept
title: "Self-Distillation (Teacher-Student)"
created: 2026-04-22
updated: 2026-04-22
tags:
  - concept/distillation
  - domain/latent-reasoning
status: seed
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Self-Distillation"
  - "Teacher-Student Self-Distillation"
  - "Shared-Backbone Distillation"
related:
  - "[[KV-Cache Distillation]]"
  - "[[KaVa]]"
  - "[[CODI]]"
  - "[[SIM-CoT]]"
sources:
  - "[[KaVa]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Nearly every CODI-family latent-reasoning recipe relies on shared-backbone self-distillation; load-bearing for CPF-on-CODI."
  - slug: "branch-b"
    relevance: secondary
    why: "Self-distillation's gradient-flow topology (teacher forward is stop-gradded, student BPTTs through latent generation) is directly relevant to detach ablations."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Structural concept shared across the latent-CoT distillation literature; cross-linking hub for the writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Self-Distillation (Teacher-Student)

**Definition.** A distillation setup in which a single model backbone serves as both teacher and student — switching between modes rather than using two independent networks. The teacher path consumes a richer input (e.g. full CoT) and provides supervisory signals; the student path consumes a reduced input (e.g. question only + continuous latents) and is trained to match the teacher's internals.

## Canonical latent-CoT instantiation

Used across [[CODI]], [[SIM-CoT]], [[KaVa]], and related methods:

- **Teacher mode:** same backbone, consumes `<Q, CoT>`; produces ground-truth hidden states, K/V cache, and/or logits. Stop-gradient is typically applied on these targets.
- **Student mode:** same backbone, consumes `<Q, <bot> z₁ ... z_M <eot>>` where `z_i` are continuous latents; is trained to (a) predict the answer and (b) match teacher internals.
- **Shared weights:** only one set of parameters is updated — the student's objective flows back into the shared backbone, and the teacher signal is implicit in how those same weights process the fuller input.

## What varies across methods

| Method | Teacher signal | Student unroll |
|--------|----------------|----------------|
| CODI | Hidden state of last pre-answer token (1 position) | Sequential, `M` passes |
| SIM-CoT | Auxiliary decoder aligned to teacher tokens | Sequential |
| [[KaVa]] | Compressed K/V across all layers/heads ([[KV-Cache Distillation]]) | Parallel via [[PCCoT]] Jacobi iterations |
| [[Latent Thoughts Tuning]] | Vocabulary-space predictions (CPF interpolation) | Curriculum-staged |

## Why self-distillation (rather than independent teacher + student)

- **Parameter efficiency.** One model, one set of weights — half the memory, half the checkpointing cost.
- **Alignment guarantee.** The student's representational geometry is by construction the same as the teacher's, which is necessary for internal distillation signals (K/V, hidden states) to be directly comparable in the same space.
- **Curriculum naturalness.** Since the teacher and student share parameters, improving the student improves the teacher — the targets co-evolve, avoiding the stale-teacher problem of fixed distillation.

## Caveats

- Requires careful stop-gradient discipline to avoid the teacher signal collapsing to the student's current guess.
- Gradient flow through latent generation can create long backward chains (bf16 instability, long-chain overflow). [[PCCoT]]-style parallel decoding shortens this chain.

## Related

- [[KV-Cache Distillation]] — specific signal used by KaVa
- [[KaVa]] — canonical modern example
- [[CODI]] — original self-distillation-for-latent-CoT formulation
