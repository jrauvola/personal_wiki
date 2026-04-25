---
type: source
title: "COCONUT — Chain of Continuous Thought"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - type/source
  - method/weak-supervision
  - method/curriculum
status: read
related:
  - "[[CODI]]"
  - "[[SIM-CoT]]"
  - "[[Feature Collapse]]"
  - "[[Curriculum Distillation]]"
sources:
  - "[[.raw/papers/2412.06769-coconut]]"
  - "[[.raw/papers/research.md]]"
source_type: paper
arxiv_id: "2412.06769"
venue: "arXiv (COLM 2025)"
date_published: 2024-12-09
authors:
  - "Shibo Hao"
  - "Sainbayar Sukhbaatar"
  - "DiJia Su"
  - "Xian Li"
  - "Zhiting Hu"
  - "Jason Weston"
  - "Yuandong Tian"
url: "https://arxiv.org/abs/2412.06769"
code_repo: "https://github.com/facebookresearch/coconut"
has_weights: false
status: read
confidence: high
key_claims:
  - "Coconut utilizes the last hidden state of the LLM as a representation of the reasoning state, termed 'continuous thought.' Instead of decoding this state into words, we feed it back to the model as the next input embedding directly in the continuous space."
  - "Special tokens <bot> and <eot> are employed to mark the beginning and end of the latent thought mode, respectively."
  - "Continuous thoughts in Coconut can encode multiple potential next steps simultaneously, allowing for a reasoning process akin to breadth-first search (BFS)."
  - "In the initial stage, the model is trained on regular CoT instances. In the subsequent stages, at the k-th stage, the first k reasoning steps in the CoT are replaced with k×c continuous thoughts, where c is a hyperparameter controlling the number of latent thoughts replacing a single language reasoning step."
  - "The objective does not encourage the continuous thought to compress the removed language thought, but rather to facilitate the prediction of future reasoning."
  - "Coconut outperforms CoT on verbose logical reasoning tasks that require substantial search during planning and achieves a better trade-off between accuracy and efficiency."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Curriculum-based baseline against which LT-Tuning CPF anti-collapse gains are measured; not the primary implementation target."
  - slug: "branch-a"
    relevance: primary
    why: "Bespoke 8B snapshot (Laura's) is explicitly wired into the harness; required for Qwen3 scaling comparisons."
  - slug: "branch-b"
    relevance: secondary
    why: "COCONUT's recurrent hidden-state injection is a reference for detach/BPTT ablations, but CODI is the specific ablation target."
  - slug: "branch-c"
    relevance: reference
    why: "General canonical method context only."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Canonical taxonomic reference for curriculum-based latent reasoning; essential framing for the writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# COCONUT — Chain of Continuous Thought

The canonical foundation for modern curriculum-based latent reasoning. Fundamental hypothesis: the discrete language space is a highly inefficient medium for complex planning, as grammar and syntactic coherence consume bandwidth that could be allocated to pure symbolic logic.

## Core thesis

COCONUT establishes a dedicated latent mode. Instead of projecting the final hidden layer into the vocabulary space, the continuous output vector is routed directly back into the transformer stack as the subsequent input embedding. Transitions between language generation and implicit computation are regulated by specialized control embeddings: `<bot>` (begin-of-thought) and `<eot>` (end-of-thought).

Because a continuous vector does not collapse into a single discrete word, it can concurrently maintain multiple competing logical trajectories in superposition. As recurrent hidden states evolve, the model dynamically evaluates and prunes parallel branches, mimicking a robust search algorithm before collapsing probability mass into a textual answer. This yields emergent breadth-first search capabilities.

## Training pipeline

Multi-stage curriculum progressively transitioning the model away from explicit supervision.

- **Stage 0 (warmup)** — standard SFT on complete, explicit reasoning chains.
- **Subsequent stages** — in each stage, a larger portion of explicit textual reasoning steps is truncated from training targets. Continuous thoughts (recycled hidden states) are inserted into the input sequence to compensate.
- **Expansion hyperparameter** — dictates the number of continuous vectors inserted per explicit step removed.
- **Optimization** — end-to-end differentiable; cross-entropy loss applied only to surviving language tokens and the ultimate answer string.
- **Anti-forgetting** — uniform probability sampling interleaves earlier-stage training data into later optimization phases to preserve the mapping back to the human vocabulary.

## Public artifacts

- Meta has published the official codebase.
- Official HF weights from the researchers are **not publicly accessible** as of March 2026.
- Community backfill:
  - `bmarti44/coconut-curriculum-checkpoints` (GPT-2 124M)
  - `Onlydrinkwater/llama32-1b-gsm-coconut-checkpoint` (Llama 3.2 1B)

## Integration notes

Project fit is exceptionally high. The harness already supports the community GPT-2 checkpoints and is explicitly wired to accommodate the bespoke 8B snapshot (Laura's) at `README.md:73`, `README.md:129`, `methodology.md:173`. Methodologically unparalleled on tasks requiring logical backtracking, planning, and search-space navigation; significantly outperforms linear CoT baselines. But weak-supervision reliance makes it vulnerable to noise accumulation and semantic drift at large scale or on OOD mathematical complexity. Retain for compatibility with ongoing internal research and canonical status; optimizations should look toward stronger supervision frameworks.
