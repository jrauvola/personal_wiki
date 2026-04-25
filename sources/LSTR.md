---
type: source
title: "LSTR — Latent Sparse Transcoder Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/interpretability
  - domain/sparse-coding
  - type/source
  - method/transcoder
status: read
source_type: paper
arxiv_id: "2602.01695"
venue: "arXiv"
date_published: 2026-02-02
authors:
  - "Yadong Wang"
  - "Haodong Chen"
  - "Yu Tian"
  - "Chuanxing Geng"
  - "Dong Liang"
  - "Xiang Chen"
url: "https://arxiv.org/abs/2602.01695"
code_repo: null
has_weights: false
confidence: medium
key_claims:
  - "Latent reasoning with dense hidden-state transitions remains difficult to interpret and control; sparse semantic transitions via a Latent Transition Transcoder (LTT) address both."
  - "LTT's residual-skip architecture decouples linear manifold transport (dense) from sparse semantic updates (interpretable)."
  - "Explicit sparsity constraints enable controllable semantic resolution — higher sparsity, more interpretability; lower sparsity, more expressiveness."
  - "LSTR preserves reasoning accuracy and compression efficiency while substantially improving interpretability over dense latent baselines."
  - "Causal interventions on sparse features alter downstream reasoning, demonstrating features act as both interpretable and causally effective operators."
related:
  - "[[CoLaR]]"
  - "[[COCONUT]]"
  - "[[Are LRMs Easily Interpretable]]"
  - "[[Feature Collapse]]"
  - "[[Sparse Autoencoder]]"
sources:
  - "[[.raw/papers/2602.01695-lstr-sparse-transcoders]]"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Sparse-structure add-on compatible with CPF but orthogonal; not the implementation target, useful as interpretability overlay."
  - slug: "branch-a"
    relevance: reference
    why: "Interpretability-over-throughput; not directly architecture-scaling-relevant."
  - slug: "branch-b"
    relevance: reference
    why: "Tangential to detach/BPTT axis."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Sparse-transcoder-as-operator is an interpretability overlay worth citing but not a synthesis input for the north-star workable model; architecture and training recipe would pull us off the V2 / SIM-CoT / LT-Tuning line."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LSTR — Latent Sparse Transcoder Reasoning

Wang, Chen, Tian, Geng, Liang, Chen — [arXiv:2602.01695](https://arxiv.org/abs/2602.01695) (2026-02-02).

## Core thesis

Latent reasoning models compress CoT into dense continuous hidden states, gaining throughput but losing interpretability. Sparse-autoencoder-style transcoders have been used as *post-hoc probes* for interpretability. LSTR elevates them into **active operators** in the reasoning forward pass: sparse semantic transitions replace (or complement) dense transitions, preserving speed while exposing structure.

## Method

### Latent Transition Transcoder (LTT)

Residual-skip architecture with two parallel paths at each reasoning step:

| Path | Representation | Role |
|---|---|---|
| Dense skip | continuous residual | Linear manifold transport |
| Sparse transcoder | small set of active features | Semantic update |

Final latent = dense residual + sparse-feature update.

### Controllable sparsity

Sparsity is a knob:
- High sparsity → few active features per step → easy to label → high interpretability, some accuracy cost.
- Low sparsity → many active features → closer to dense baseline.

User picks the operating point.

## Recipe

- Plugs into continuous-CoT architectures (COCONUT-class).
- Training: joint SFT with sparsity penalty on transcoder activations.
- Interpretability probe: causal intervention on individual sparse features.

## Results

- Matches dense-baseline accuracy + compression efficiency.
- Substantial interpretability gains (concrete numbers not in excerpt).
- Causal interventions on sparse features alter downstream outputs → features are *operators*, not correlational probes.

## Relevance to our project

- **Primary for spar-latent-reasoning.** The SPAR fellowship's interpretability angle needs a concrete bridge between the sparse-autoencoder literature and latent reasoning. LSTR is that bridge — active sparse operators in the reasoning pass, not just probes.
- **Secondary for branch-d.** CPF + LSTR could stack (CPF anchors to vocab manifold, LSTR decomposes trajectory into sparse features), but implementing both is out of scope for the Days 3-7 branch.

## Citation links to chase

- Upstream: [[COCONUT]], [[CoLaR]]
- Related interpretability: [[Are LRMs Easily Interpretable]] (2604.04902)
- Sparse autoencoder literature (worth crawl if not yet in wiki).

## Artifacts

- **Paper:** [arXiv:2602.01695](https://arxiv.org/abs/2602.01695)
- **Code:** none released at crawl time.
- **Raw source:** [[.raw/papers/2602.01695-lstr-sparse-transcoders]]
