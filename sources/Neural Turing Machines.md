---
type: source
title: "Neural Turing Machines (Graves, Wayne, Danihelka 2014)"
source_type: paper
arxiv_id: "1410.5401"
venue: "arXiv"
date_published: 2014-10-20
authors:
  - "Alex Graves"
  - "Greg Wayne"
  - "Ivo Danihelka"
url: "https://arxiv.org/abs/1410.5401"
code_repo: null
has_weights: false
status: read
confidence: high
key_claims:
  - "NTM extends a neural network (the 'controller') with an external memory matrix accessed via differentiable read/write heads with content-based and location-based addressing."
  - "The memory interaction is end-to-end differentiable, so the architecture can be trained by standard gradient descent — no REINFORCE needed."
  - "NTM can learn simple algorithms from input-output examples: copying, sorting, associative recall, N-gram language modeling."
  - "A controller LSTM iteratively reads, writes, and updates memory across T steps before producing output. The iteration loop IS the algorithmic computation — the network is not just a function-fitter but a learner of explicit computational procedures."
  - "Successor: Differentiable Neural Computer (Graves 2016, Nature 538) adds dynamic memory allocation and temporal attention; demonstrates graph reasoning (London Underground shortest-path) and family-tree inference."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Historical root of 'differentiable iterative reasoning'. Not a direct COCONUT ancestor, but the conceptual precedent for 'loop a shared controller over external state' — reused in every memory-augmented latent reasoner since."
  - slug: "branch-a"
    relevance: reference
    why: "Not architecturally relevant to Qwen3 scaling; cited as historical precedent only."
  - slug: "branch-b"
    relevance: reference
    why: "Controller-memory loop is the grandparent pattern of CODI's M-step rollout through the LLM's own KV-cache."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: not-applicable
    why: "Unrelated to fusion axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/memory-augmented-networks
  - family/external-memory
  - type/source
  - status/historical
related:
  - "[[Adaptive Computation Time]]"
  - "[[Universal Transformers]]"
  - "[[Alex Graves]]"
sources: []
---

# Neural Turing Machines (Graves, Wayne, Danihelka 2014)

## TL;DR

First neural network coupled to a differentiable external memory with content/location-based addressing. Controller (LSTM or FFN) iteratively reads, writes, and updates memory; end-to-end gradient descent trainable. Learns copy, sort, associative recall from examples.

## Why this matters

NTM is the *conceptual grandparent* of every latent-reasoning method that uses iterative compute over internal state. It established three patterns reused across the field:

1. **Controller iterating over external state.** NTM's controller reads/writes a memory matrix; modern latent reasoners iterate over their own KV-cache. Same pattern, just the memory is implicit.
2. **End-to-end differentiability.** All components (addressing, read, write) are differentiable — no REINFORCE. Quiet-STaR, CODI, LT-Tuning all preserve this property; COCONUT's special tokens do too.
3. **Learning from examples, not programs.** No symbolic programs or rules; algorithms emerge from gradient descent. This is the founding premise of the entire latent-reasoning field.

## Method

**Architecture.**
- Controller network $C$ (typically LSTM).
- Memory $M \in \mathbb{R}^{N \times W}$ — $N$ slots of width $W$.
- Read head: produces weights $w_t^r \in \Delta^N$, reads $r_t = w_t^{r \top} M$.
- Write head: produces weights $w_t^w$, erase vector $e_t$, add vector $a_t$; updates $M \leftarrow M \odot (1 - w_t^w e_t^\top) + w_t^w a_t^\top$.

**Addressing.**
- Content-based: $w^c_i \propto \exp(\beta \cdot \cos(k, M_i))$ where $k$ is the query.
- Location-based: convolutional shift + sharpening.
- Combination: $w = g \cdot w^c + (1-g) \cdot w^{prev}$ (interpolation) followed by shift.

**Training.** Sequence-to-sequence loss on next-token prediction; gradient descent via BPTT.

## Results

Simple algorithmic tasks (copy, repeat-copy, associative recall, N-gram, priority sort): NTM learns from examples and generalizes to longer sequences than training data.

## Successor: Differentiable Neural Computer

Graves et al. 2016 (Nature 538, 471-476) extends NTM with:
- **Dynamic memory allocation** (via "usage vectors" tracking which slots are in use).
- **Temporal link matrix** recording the order of writes.
- Demonstrates graph reasoning (finding shortest paths on London Underground map) and family-tree question answering.

## Relevance to CODI / COCONUT contrast

NTM is not in the direct COCONUT lineage, but it establishes the precedent that *reasoning* can be something a network *does over time via iteration*, not just a function it computes feedforward. The key philosophical step from NTM to COCONUT:

- **NTM:** controller + explicit memory matrix.
- **COCONUT:** LLM + implicit memory (KV cache + hidden states).

CODI's M-step latent rollout is essentially "NTM-style iteration, but the controller is a 4B LLM and the memory is the KV cache."

## Citation links to chase

- [[Adaptive Computation Time]] (Graves 2016) — same author, step-count learning.
- Differentiable Neural Computer (Graves 2016, Nature) — the scalable successor.
- [[Alex Graves]] — entity page.
