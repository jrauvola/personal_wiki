---
type: concept
title: "KV Compression"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/concept
  - memory-efficiency
status: developing
complexity: advanced
domain: architecture
aliases:
  - "KV-Cache Compression"
  - "KV-Cache Distillation"
  - "Cache Eviction"
related:
  - "[[Token Efficiency]]"
  - "[[Adaptive Latent RL]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/research.md]]"
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Orthogonal to CPF fusion but shares the anti-collapse lineage via KaVa's KV-matching loss."
  - slug: "branch-a"
    relevance: secondary
    why: "KV efficiency at 8B+ is relevant to stable Qwen3 scaling."
  - slug: "branch-b"
    relevance: secondary
    why: "KaVa-style truncation is listed as secondary interest for the minimum-sufficient detach ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology debugging."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Memory-side taxonomic axis for the writeup."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# KV Compression

A family of techniques that compress, evict, or distill the transformer KV-cache — either to lower the memory footprint of explicit CoT, or to bridge the supervision gap between verbose teacher natural-language reasoning and a student's condensed continuous trajectory.

## Problem framing from the survey

Even when transitioning to latent reasoning eliminates autoregressive output-decoding latency, traditional explicit CoT architectures continue to suffer from massive KV-cache accumulation, rendering them unsuitable for memory-constrained or edge deployment. Early intrinsic latent models trained on structured mathematical templates exhibit severe degradation on open-ended natural language traces — a "supervision gap" inherent in weak distillation.

## Techniques referenced

- **Importance × Redundancy eviction** — KaVa's approach (covered in a separate wiki note): score every token across all heads and layers balancing attention-based importance and pairwise cosine similarity redundancy, prune cache to a compressed state matching the student's continuous trajectory length.
- **KV-Matching Loss** — stop-gradient on the teacher cache; $L_p$-norm distance between teacher and student KV matrices; Jacobi iteration to decode latent sequences in parallel during alignment.

## Cross-references

Sources touching KV compression directly or adjacently: [[Adaptive Latent RL]] (sequence-level halting reduces KV growth), and the separately-migrated KaVa note (outside this migration pass per task scope).
