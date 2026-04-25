---
type: source
title: "SeLaR — Selective Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/stochastic-latent
  - type/source
  - method/inference-time
  - method/entropy-gated
status: read
source_type: paper
arxiv_id: "2604.08299"
venue: "arXiv"
date_published: 2026-04-09
authors:
  - "Renyu Fu"
  - "Guibo Luo"
url: "https://arxiv.org/abs/2604.08299"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Global activation injects perturbations into high-confidence steps, impairing reasoning stability."
  - "Soft embeddings quickly collapse toward the highest-probability token, limiting exploration of alternative trajectories."
  - "SeLaR introduces an entropy-gated mechanism that activates soft embeddings only at low-confidence steps, while preserving discrete decoding at high-confidence steps."
  - "An entropy-aware contrastive regularization pushes soft embeddings away from the dominant (highest-probability) token's direction, encouraging sustained exploration of multiple latent reasoning paths."
  - "Experiments on five reasoning benchmarks demonstrate that SeLaR consistently outperforms standard CoT and state-of-the-art training-free methods."
related:
  - "[[Stochastic Soft Thinking]]"
  - "[[Soft Thinking]]"
  - "[[ThinkRouter]]"
  - "[[SwiReasoning]]"
  - "[[Shortcut Behavior]]"
  - "[[Gumbel-Softmax Latent]]"
sources:
  - "[[.raw/papers/2604.08299-selar]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Entropy-aware contrastive regularization pushes soft embeddings away from dominant token — a training-free anti-collapse mechanism parallel to CPF. Downgraded primary → secondary this sweep: SeLaR is inference-time only, not a training recipe on the Branch D CPF-on-CODI implementation path. Worth citing as convergent evidence, not a direct comparator."
  - slug: "branch-a"
    relevance: reference
    why: "Inference-time only; orthogonal to Qwen3 scaling architecture axis."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a training-stability mechanism."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Explicit two-failure taxonomy (perturbation-at-confidence + collapse-to-top-1) + selective activation + contrastive anti-collapse = clean synthesis of SST Greedy-Pitfall + ThinkRouter routing + Latent-SFT contrastive loss. Canonical writeup citation for the training-free anti-collapse recipe."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# SeLaR — Selective Latent Reasoning

Fu, Luo, [arXiv:2604.08299](https://arxiv.org/abs/2604.08299), Apr 2026.

## TL;DR

Training-free latent reasoning recipe that explicitly addresses the two failure modes diagnosed by SST and related work: (1) soft embeddings inject perturbations into high-confidence steps (wasted noise) and (2) soft embeddings collapse toward top-1 at low-confidence steps (Greedy Pitfall). Fix: **entropy-gated activation** (soft only when needed) + **entropy-aware contrastive regularization** (push away from dominant token). Beats CoT and SOTA training-free latent methods on 5 reasoning benchmarks.

## Method

### Entropy-gated activation

- High-confidence (low-entropy) step → keep discrete decoding. Why: soft perturbation here just injects noise into an already-confident prediction.
- Low-confidence (high-entropy) step → emit soft embedding. Why: this is where latent exploration is needed.

Same structural shape as [[ThinkRouter]] but inverted in one sense: ThinkRouter goes **discrete** at low confidence (to avoid noise aggregation); SeLaR goes **soft** at low confidence (to get exploration), with a contrastive regularizer preventing collapse.

### Entropy-aware contrastive regularization

Pushes soft embedding **away from the top-1 token direction** — direct anti-Greedy-Pitfall mechanism. Enforces that the aggregated embedding does not collapse to the dominant token.

### Training-free

Inference-time only; no retraining.

## Recipe

1. Load any CoT-capable LLM.
2. At each step: compute entropy of next-token distribution.
3. If low entropy → decode discretely.
4. If high entropy → build probability-weighted soft embedding, applying contrastive regularization against the top-1 direction.
5. Feed back and continue.

## Results

- Consistent gains over standard CoT on 5 reasoning benchmarks.
- Outperforms SOTA training-free latent methods.

## Relevance

- **Primary for branch-d.** SeLaR's entropy-aware contrastive regularization is a direct anti-collapse mechanism — structural sibling to CPF's α·h_ctx anchor. Both aim to prevent the soft embedding from collapsing to top-1; CPF uses the hidden-state anchor; SeLaR uses contrastive pushing-away.
- **Primary for spar-latent-reasoning.** Cleanest training-free synthesis: two-failure taxonomy + gated activation + contrastive anti-collapse. Writes the recipe.

## Citation links

- Upstream: [[Stochastic Soft Thinking]] (Greedy Pitfall), [[Soft Thinking]] (soft embeddings baseline).
- Sibling hybrids: [[ThinkRouter]] (inverted routing), [[SwiReasoning]] (switch), [[Dynamic Switching Protocol]].
- Contrastive siblings: [[Latent-SFT]] (contrastive SFT at training time).

## Artifacts

- **Paper:** [arXiv:2604.08299](https://arxiv.org/abs/2604.08299)
- **Code:** none released at crawl time.
- **Raw source:** [[.raw/papers/2604.08299-selar]]
