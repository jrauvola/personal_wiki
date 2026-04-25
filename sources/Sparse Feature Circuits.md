---
type: source
source_type: paper
title: "Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/source
  - tool/sparse-autoencoder
status: triaged
arxiv_id: "2403.19647"
venue: "ICLR 2025"
date_published: 2024-03-28
authors:
  - "Samuel Marks"
  - "Can Rager"
  - "Eric J. Michaud"
  - "Yonatan Belinkov"
  - "David Bau"
  - "Aaron Mueller"
url: "https://arxiv.org/abs/2403.19647"
code_repo: "https://github.com/saprmarks/feature-circuits"
has_weights: false
confidence: high
key_claims:
  - "Attribution patching on SAE features discovers causal subcircuits responsible for specific language model behaviors."
  - "Attribution patching uses a single forward + backward pass, beating prior circuit-discovery methods on AUC while being >100x cheaper."
  - "SHIFT: human-judged task-irrelevant features can be ablated to improve generalization of a downstream classifier."
  - "Feature circuits scale to thousands of features across automatically surfaced behaviors, giving an unsupervised interpretability pipeline."
  - "Discovered circuits for subject-verb agreement route through a small set of SAE features corresponding to number and agreement attributes."
  - "Editing SAE features surgically modifies behavior while preserving unrelated capability."
related:
  - "[[Towards Monosemanticity]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Step-Level Sparse Autoencoder]]"
  - "[[Sparse Autoencoder]]"
sources:
  - "[[.raw/external/sparse-feature-circuits-2024]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Attribution patching on SAE features is the right tool to test whether CODI latent positions are functional (attribution > 0) or decorative (attribution ≈ 0) — a direct probe for routing vs reasoning."
  - slug: "branch-c"
    relevance: primary
    why: "Gives Branch C's probe-typology contest a causal baseline: both LTO and DDR probes should agree with SAE-feature attribution on the same examples if either is correctly identifying a reasoning feature."
  - slug: "branch-d"
    relevance: secondary
    why: "SAE-feature circuits on CPF-trained vs vanilla CODI would localize which latent positions CPF 'repairs'."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling context."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Sparse Feature Circuits

Marks et al. (ICLR 2025) combine sparse autoencoders with attribution patching to discover causal circuits at feature (not attention-head) granularity.

## Attribution patching

Let `M` be the model, `f_S` be the set of SAE features at a particular site, and `m(x)` be the metric of interest (e.g. log-prob of the correct answer).

Attribution of feature `i` via integrated gradients:
```
IG_i = (f_i(x_clean) − f_i(x_corrupt)) · ∫₀¹ ∂m/∂f_i (x_corrupt + α·(x_clean − x_corrupt)) dα
```
In practice approximated by one forward + one backward pass with a first-order linearization (attribution patching, Nanda et al. 2023).

Total cost: O(|features|) dot products, not O(|features|) forward passes.

## SHIFT

**S**urgical **H**uman-**I**n-the-loop **F**eature **T**rimming:

1. Train SAE on the model.
2. Build a classifier on frozen features.
3. Attribution-rank features for the task metric.
4. Human judges which top features are task-irrelevant spurious correlates.
5. Ablate those features → classifier generalizes better.

The method shows that attribution identifies spurious-feature reliance and ablation restores generalization.

## Unsupervised interpretability pipeline

For a behavior `B` observed at scale:
1. Collect examples of `B`.
2. Attribute the SAE features responsible at each site (residual, MLP, attention).
3. Cluster attributions → feature circuit for `B`.
4. Cross-reference discovered features against feature dashboards.

## Implications for latent reasoning

Attribution patching is a direct tool for the F3/F4/F5 battery:

- **F3 template attractor** — attribute from "template token at position p" back to SAE features at all upstream positions. If attribution is concentrated on format-prior SAE features, confirms routing-mode hypothesis.
- **F4 ablation dependence** — attribution predicts which positions actually carry signal. Positions with zero attribution are inert, matching F4's 25-29% accuracy drop from ablating 7/8 positions.
- **F5 cross-example swap** — attribution should be example-specific for reasoning positions; the F5 result predicts attribution is example-invariant (routing signature).

## Cross-references

- [[Sparse Autoencoder]], [[Towards Monosemanticity]], [[How does Chain of Thought Think]]
