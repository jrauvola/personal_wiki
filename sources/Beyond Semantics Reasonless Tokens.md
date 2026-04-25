---
type: source
title: "Beyond Semantics — The Unreasonable Effectiveness of Reasonless Intermediate Tokens"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/interpretability
  - type/source
  - method/trace-validity
status: read
related:
  - "[[COCONUT]]"
  - "[[Quora Faithfulness Probe]]"
  - "[[Token Assorted]]"
sources:
  - "[[.raw/papers/2505.13775-beyond-semantics-reasonless-tokens]]"
source_type: paper
arxiv_id: "2505.13775"
venue: "arXiv"
date_published: 2025-05-19
authors:
  - "Karthik Valmeekam"
  - "Kaya Stechly"
  - "Vardhan Palod"
  - "Atharva Gundawar"
  - "Subbarao Kambhampati"
url: "https://arxiv.org/abs/2505.13775"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "On a controlled 30×30 maze pathfinding domain with formal A* trace validity, trace correctness and solution correctness are only loosely coupled — models with correct plans frequently emit traces that fail A* validation."
  - "Training on a 'Swap' dataset — where reasoning traces are randomly permuted between problems, breaking the trace–solution correspondence — produces solution accuracy competitive with training on matched traces."
  - "This challenges the prevailing interpretation of CoT trace content as semantically meaningful and causally predictive of final plans in R1-style long-CoT models."
  - "The authors construct an A* trace validator for the gridworld path-finding domain to measure trace validity independently of solution correctness."
  - "Diverse maze generation (varied algorithms, structural patterns) enables systematic OOD evaluation."
  - "Observation: CoT trace content may function more as filler / latent-compute scaffolding than as interpretable derivation."
projects:
  - slug: "branch-a"
    relevance: reference
    why: "Interpretability-flavored; not a scaling recipe."
  - slug: "branch-b"
    relevance: reference
    why: "Not a gradient/detach axis."
  - slug: "branch-c"
    relevance: secondary
    why: "Relevant methodology for probe validity: even explicit CoT traces don't always causally predict plans, so hidden-state probes need similar independent verification."
  - slug: "branch-d"
    relevance: reference
    why: "Tangentially related to faithfulness but not CPF."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Important framing for interpretability section — if discrete CoT traces are already 'reasonless,' the interpretability loss from switching to continuous latents is smaller than commonly argued."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Beyond Semantics — Reasonless Intermediate Tokens

## TL;DR

Empirically decouples CoT trace correctness from final-plan correctness on a controlled maze domain with formal A* trace validation. Training on a Swap dataset (randomly permuting traces between problems) yields competitive solution accuracy — challenging the narrative that CoT traces contain semantically meaningful, causally-load-bearing derivations. In R1-style long-CoT models, most "reasoning tokens" may be filler / scaffolding.

## Method

- **Domain:** 30×30 gridworld path finding with walls, unique start/goal cells, 4-action move space.
- **Trace format:** following Lehnert et al. 2024 (Searchformer) and Su et al. 2024 (Dualformer) — A* search traces as tokenized sequences.
- **Validator:** custom A* trace validator that checks each generated trace follows the exact A* semantics (step correctness, consistency with the algorithm).
- **Training datasets:**
  - Matched: each problem paired with its own valid A* trace (baseline).
  - **Swap:** reasoning traces randomly permuted across problems — trace no longer corresponds to its problem.
- **Evaluation:** trace validity + plan correctness measured independently.

## Recipe

- Train decoder-only transformers from scratch on matched and Swap datasets.
- Problem + trace + plan format; supervised next-token prediction.
- OOD evaluation across maze types not seen during training (different generation algorithms).

## Results

- Matched and Swap training produce similar plan accuracy.
- Plan correctness and trace validity only loosely correlated even in matched training.
- For frontier models (DeepSeek R1), trace outputs are too ambiguous in natural language to validate.

## Relevance to our project

**Secondary for spar-latent-reasoning framing:** if explicit discrete CoT tokens are already largely "reasonless" scaffolding for planning, then the interpretability cost of moving to continuous latent reasoning is smaller than skeptics argue. This strengthens the motivation for continuous-CoT research. **Secondary for Branch C (conditional):** when we probe Qwen3 hidden states for reasoning content, this paper is a useful reminder that even explicit textual CoT is not reliably faithful — so failing to find clean structure in continuous probes does not falsify the method; conversely, finding structure is more surprising and more informative. Relates to [[Quora Faithfulness Probe]] critique of CoT faithfulness claims.

## Citation links to chase

- Lehnert et al. 2024 (Searchformer) — A*-trace predecessor.
- Su et al. 2024 (Dualformer) — dual fast/slow trace model.
- Gandhi et al. 2024 (Stream-of-Search) — BFS/DFS trace training.
- Yang et al. 2022 — MCTS-as-CoT trajectories.
- Saha et al. 2024 (System 1.x) — dual-model fast/slow.
