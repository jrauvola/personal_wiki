---
type: source
title: "Reasoning by Superposition — A Theoretical Perspective on Chain of Continuous Thought"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/theory
  - type/source
  - method/superposition
status: read
related:
  - "[[COCONUT]]"
  - "[[Continuous CoT Parallel Exploration]]"
  - "[[Soft Thinking]]"
  - "[[Latent Reasoning as Chain of Superposition]]"
sources:
  - "[[.raw/papers/2505.12514-reasoning-by-superposition]]"
source_type: paper
arxiv_id: "2505.12514"
venue: "NeurIPS 2025"
date_published: 2025-05-18
authors:
  - "Hanlin Zhu"
  - "Shibo Hao"
  - "Zhiting Hu"
  - "Jiantao Jiao"
  - "Stuart Russell"
  - "Yuandong Tian"
url: "https://arxiv.org/abs/2505.12514"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "A two-layer transformer with D continuous-CoT steps can solve directed graph reachability for graphs of n vertices where D is the diameter and D < n; the best known constant-depth transformer with discrete CoT requires O(n^2) steps."
  - "The constructive proof holds for widely-used positional encodings including sinusoidal and RoPE — not a problem-specific or length-specific construction."
  - "Continuous thought vectors behave as superposition states encoding multiple search frontiers simultaneously, enabling implicit parallel BFS per autoregressive step; discrete tokens correspond to 'collapsed' single-branch states forcing sequential search."
  - "Gradient-based training on graph-reachability produces the predicted superposition structure automatically — no explicit supervision to align latent vectors with alternative search paths is required."
  - "Empirically, a two-layer transformer with continuous CoT outperforms a 12-layer transformer with discrete CoT on graph reachability."
  - "Attention-pattern inspection confirms that continuous thoughts encode multiple plausible search frontiers in parallel, matching the theoretical construction."
projects:
  - slug: "branch-a"
    relevance: reference
    why: "Theoretical framing only; not a scaling recipe."
  - slug: "branch-b"
    relevance: reference
    why: "Not a gradient-stability study."
  - slug: "branch-c"
    relevance: reference
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Anti-collapse theory orthogonal to LT-Tuning's empirical CPF fix."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical theoretical foundation for continuous-CoT expressivity; essential framing paper for the writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Reasoning by Superposition

## TL;DR

Theoretical proof that continuous-CoT is strictly more expressive than discrete CoT for graph reachability: a 2-layer transformer with D continuous thoughts solves D-diameter graph reachability, vs O(n^2) discrete steps for constant-depth transformers. The proof constructs continuous thoughts as superposition states encoding multiple BFS frontiers in parallel. Empirically, gradient descent recovers this superposition structure without explicit guidance.

## Method

**Theoretical setup:**
- 2-layer autoregressive transformer with sinusoidal or RoPE positional encoding.
- Embedding partitioned into content / buffer1 / buffer2 / position; token embeddings orthonormal in content subspace.
- Continuous thought = transformer output, directly appended as next input (COCONUT paradigm).

**Main theorem:**
- For any directed graph G with n vertices and diameter D, the 2-layer transformer with D continuous-CoT steps outputs correct reachability.
- Construction: each latent thought vector is a superposition of currently-reachable node embeddings; one step of attention performs a BFS frontier expansion.
- Comparison: Merrill & Sabharwal (2023a) showed constant-depth transformers with discrete CoT need O(n^2) steps for reachability.

**Empirical verification:**
- Train a 2-layer transformer with continuous CoT on graph-reachability.
- Inspect attention patterns and intermediate representations: multiple search frontiers present in superposition.
- Compare: 12-layer transformer with discrete CoT underperforms.

## Recipe

- Task: directed graph reachability (given start node, candidate destination).
- Supervision: only the optimal path (no alignment supervision for latent vectors).
- Standard training — gradient descent recovers the superposition representation.

## Results

- Theoretical upper bound: D steps (diameter) vs O(n^2) for discrete.
- Empirical: 2-layer continuous CoT > 12-layer discrete CoT on graph-reachability accuracy.
- Superposition automatically emerges in training; no special loss needed.

## Relevance to our project

Primary for [[spar-latent-reasoning]] as the theoretical anchor for why continuous CoT is worth pursuing at all. Provides a clean expressivity separation that grounds COCONUT-style and related empirical results. Shared author (Shibo Hao) with [[COCONUT]]. Less directly useful for Branch A/B/D because it's a theoretical/synthetic-task paper, not a scaling or stability recipe — but essential context for the writeup's framing section. The result that superposition emerges *without* explicit supervision is evidence that anti-collapse mechanisms (CPF, auxiliary decoders) are addressing training-dynamics pathologies at scale, not fundamental expressivity limits.

## Citation links to chase

- Merrill & Sabharwal (2023a, 2025) — discrete CoT expressivity lower bounds.
- Cohen et al. 2025 — graph shortest path via line-graph spectral decomposition.
- [[COCONUT]] — direct empirical predecessor.
- [[Continuous CoT Parallel Exploration]] (2505.23648) — complementary empirical/theoretical work on same topic.
