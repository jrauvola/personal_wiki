---
type: source
title: "Differentiable Neural Computer (Graves et al. 2016, Nature)"
source_type: paper
arxiv_id: null
venue: "Nature 538, 471-476"
date_published: 2016-10-12
authors:
  - "Alex Graves"
  - "Greg Wayne"
  - "Malcolm Reynolds"
  - "Tim Harley"
  - "Ivo Danihelka"
  - "Agnieszka Grabska-Barwińska"
  - "Sergio Gómez Colmenarejo"
  - "Edward Grefenstette"
  - "Tiago Ramalho"
  - "John Agapiou"
  - "Adrià Puigdomènech Badia"
  - "Karl Moritz Hermann"
  - "Yori Zwols"
  - "Georg Ostrovski"
  - "Adam Cain"
  - "Helen King"
  - "Christopher Summerfield"
  - "Phil Blunsom"
  - "Koray Kavukcuoglu"
  - "Demis Hassabis"
url: "https://www.nature.com/articles/nature20101"
code_repo: "https://github.com/Mostafa-Samir/DNC-tensorflow"
has_weights: false
status: read
confidence: high
key_claims:
  - "DNC adds dynamic memory allocation (usage vector u_t) and a temporal link matrix L_t to NTM, enabling memory reuse and order-preserving sequential reads."
  - "Memory write weighting is a learned gated mix of allocation-based weighting a_t (write to a fresh slot) and content-based weighting c_t^w: w_t^w = g_t^w [g_t^a a_t + (1 - g_t^a) c_t^w]."
  - "Temporal link L_t[i,j] = (1 - w_t^w[i] - w_t^w[j]) L_{t-1}[i,j] + w_t^w[i] p_{t-1}[j] tracks the order of writes; forward read f_t = L_t w_{t-1}^r and backward read b_t = L_t^T w_{t-1}^r reconstitute write order."
  - "Each read head mixes three modes (content / forward / backward) via a learned softmax pi_t over modes."
  - "DNC solves graph-reasoning tasks (shortest path on London Underground), family-tree inference, mini-SHRDLU block puzzles, and bAbI - all from gradient descent end-to-end, no REINFORCE."
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Direct ancestor of every modern external-memory + gated-access pattern. The DNC's three-mode read (content + forward-time + backward-time) is the conceptual prior for Latent Scratchpad's gated emission + attention-back via past_kv."
  - slug: "branch-d"
    relevance: secondary
    why: "Closest historical match for the 'gated parallel-channel write' pattern that W3.5 Latent Scratchpad will instantiate at LLM scale - the gate over allocation a_t vs content c_t^w is what W3.5's emission gate generalizes."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-LLM era; not in scaling family."
  - slug: "branch-b"
    relevance: reference
    why: "Differentiable iterative memory-update is conceptually parallel to CODI's M-step rollout."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/memory-augmented-networks
  - family/external-memory
  - type/source
  - status/historical
related:
  - "[[Neural Turing Machines]]"
  - "[[Alex Graves]]"
  - "[[Neural Turing Machine Memory Access]]"
  - "[[Latent Scratchpad Architecture]]"
sources: []
---

# Differentiable Neural Computer (Graves et al. 2016)

## TL;DR

NTM successor that addresses NTM's two main weaknesses: (1) no memory reuse — NTM cannot release a slot once written; (2) no temporal order — NTM cannot reconstruct sequential write history. DNC adds a usage vector for dynamic memory allocation and a link matrix for temporal addressing. Demonstrates graph reasoning (shortest path) and bAbI from end-to-end gradient descent.

## Why this matters for the Latent Scratchpad

DNC is the historical ancestor of Latent Scratchpad's "gated parallel-channel write" pattern. The DNC's write head **chooses, per timestep, between writing to a fresh allocated slot or a content-addressed existing slot**, controlled by a learned gate `g_t^a`. This is structurally identical to W3.5's "gate decides whether this latent step emits a discrete note to the scratchpad."

The link matrix is the conceptual prior for the past_kv attention-back mechanism: scratchpad notes attend back into subsequent latent positions exactly the way DNC's forward-read head reconstitutes the temporal write order.

## Method (verbatim equations from Wikipedia / Nature article)

**Usage vector update:**
```
u_t = (u_{t-1} + w_{t-1}^w − u_{t-1} ∘ w_{t-1}^w) ∘ ψ_t
```
where ψ_t is a retention vector (locations the read heads "freed" decay back to zero usage).

**Allocation weighting** (over least-used slots φ_t):
```
a_t[φ_t[j]] = (1 − u_t[φ_t[j]]) · ∏_{i=1}^{j−1} u_t[φ_t[i]]
```

**Write weighting** (gated mix of allocation a_t and content c_t^w):
```
w_t^w = g_t^w [g_t^a a_t + (1 − g_t^a) c_t^w]
```

**Precedence weighting** (tracks "what was written most recently"):
```
p_t = (1 − Σ_i w_t^w[i]) p_{t-1} + w_t^w
```

**Temporal link matrix** (L_t[i,j] is the strength of the "j → i" temporal link):
```
L_t[i,j] = (1 − w_t^w[i] − w_t^w[j]) L_{t-1}[i,j] + w_t^w[i] p_{t-1}[j]
```

**Forward / backward read weights** (reconstitute time-ordered traversal):
```
f_t^i = L_t · w_{t-1}^{r,i}
b_t^i = L_t^T · w_{t-1}^{r,i}
```

**Read mode mixing** (three-way softmax over content / forward / backward):
```
π_t^i = softmax(π̂_t^i)
```

## Tasks demonstrated

- **bAbI** — synthetic QA. DNC solves all 20 tasks jointly (a benchmark NTM struggled on).
- **London Underground graph reasoning** — DNC navigates a 30-station graph and finds shortest paths to unseen station pairs. Demonstrates compositional generalization over a learned memory representation.
- **Family-tree inference** — answers 4-hop questions about kinship from tree edges presented sequentially.
- **Mini-SHRDLU block puzzles** — plans block-stacking sequences via curriculum learning.

## Failure modes / limitations

- Memory size N is fixed at training time. DNC does not generalize to larger memory at inference (a limitation also shared by NTM).
- Wall-clock training is slow because every step does N-way softmax over allocations. Sparse-DNC (Rae et al. 2016) addresses this via locality-sensitive hashing.
- The link matrix is O(N²) per timestep — quadratic memory in slot count, which is why DNC was never scaled to LLM-sized memories until [[Memorizing Transformers]] revisited the kNN-memory pattern.

## Direct mapping to W3.5 Latent Scratchpad

**BORROW: the allocation-vs-content gate `g_t^a`.** Writing to a "fresh" slot vs. updating an existing one is exactly the choice W3.5's gate makes between "emit new note" vs. "pass through silently." The DNC parametrization (sigmoid gate, end-to-end gradient) is directly transferable. **ADAPT: the temporal link matrix L_t** — W3.5 doesn't need an explicit L_t because past_kv already records sequence order; the link matrix is what the standard transformer attention mask gives for free. **IGNORE: dynamic allocation over a fixed-N memory matrix** — W3.5's scratchpad is variable-length / append-only (latents themselves are the memory), so allocation is trivially "append the next note."

## Citation links to chase

- [[Neural Turing Machines]] (Graves 2014) — the predecessor.
- [[Alex Graves]] — entity page.
- [[Memorizing Transformers]] — modern kNN-external-memory descendant at LLM scale.
- [[Compressive Transformer]] — different memory-compression pattern (Rae 2020).
