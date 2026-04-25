---
type: concept
title: "NTM Memory Access (Content + Location-Based Addressing)"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/external-memory
  - method/addressing
  - method/differentiable-memory
status: developing
complexity: intermediate
domain: external-memory
aliases:
  - "Content-based addressing"
  - "Location-based addressing"
  - "NTM addressing"
related:
  - "[[Neural Turing Machines]]"
  - "[[Differentiable Neural Computer]]"
  - "[[End-to-End Memory Networks]]"
  - "[[Latent Scratchpad Architecture]]"
  - "[[Selective State-Space Model]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Foundational mechanism vocabulary for the entire external-memory family. Latent Scratchpad's gate + emission decision is a generalization of NTM's interpolation gate g_t + content/location address."
  - slug: "branch-d"
    relevance: secondary
    why: "The g_t interpolation between content-based and location-based weighting is the structural prior for any 'gate decides where to write' mechanism, including W3.5 Latent Scratchpad's emit/pass-through decision."
  - slug: "branch-a"
    relevance: reference
    why: "Pre-LLM era; not in scaling family."
  - slug: "branch-b"
    relevance: reference
    why: "Iterative-update mechanism is a conceptual ancestor."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# NTM Memory Access (Content + Location-Based Addressing)

The mechanism by which Neural Turing Machines (Graves 2014) and DNC (Graves 2016) generate read/write weighting vectors `w_t ∈ Δ^N` over an N-slot external memory matrix. The mechanism is fully differentiable and learned end-to-end without REINFORCE.

## The four-step addressing pipeline

NTM addressing produces `w_t` from a key `k_t`, key-strength `β_t`, interpolation gate `g_t`, shift weighting `s_t`, and sharpening `γ_t` via this pipeline:

### Step 1 — Content-based weighting (Eq. 5)

```
w_t^c(i) = exp(β_t · K[k_t, M_t(i)]) / Σ_j exp(β_t · K[k_t, M_t(j)])
```

Cosine-similarity attention with temperature `β_t`. Standard softmax-attention-over-memory. Higher `β_t` sharpens; `β_t = 0` is uniform.

### Step 2 — Interpolation with previous weighting (Eq. 7)

```
w_t^g = g_t · w_t^c + (1 − g_t) · w_{t−1}
```

The interpolation gate `g_t ∈ [0,1]` decides how much to use **content addressing** (g=1) vs **persist the previous step's address** (g=0). This is the **canonical "stay vs move" decision** that all later gated-memory architectures inherit.

### Step 3 — Shift weighting (Eq. 8)

```
w̃_t(i) = Σ_j w_t^g(j) · s_t(i − j)
```

Circular convolution with a learned shift kernel `s_t ∈ Δ^{shift_range}`. Allows the head to move ±k positions per step. **This is the "location-based" component** — independent of memory contents, purely positional.

### Step 4 — Sharpening (Eq. 9)

```
w_t(i) = w̃_t(i)^{γ_t} / Σ_j w̃_t(j)^{γ_t}
```

Power-law sharpening with `γ_t ≥ 1`. Counteracts blur from convolution; pushes the attention distribution toward one-hot when needed.

## The two address types

| Type | Mechanism | What it solves |
|---|---|---|
| **Content-based** | `w^c` via key-similarity softmax | Associative recall — "find the slot that matches this key" |
| **Location-based** | shift `s_t` + interpolation `g_t` | Sequential traversal — "move to the next slot regardless of content" |

The genius of NTM is that these are mixed via the single learned gate `g_t`. The model learns **per-step** whether the task demands content-recall or sequential traversal.

## Why this matters for Latent Scratchpad

W3.5's emission gate is a **structural generalization** of NTM's interpolation gate:

- NTM: `g_t = 1` → re-address by content; `g_t = 0` → keep previous address.
- W3.5: `gate = 1` → emit a discrete note this step; `gate = 0` → pass through (latent only).

Both are learned binary decisions that route attention/state. The key difference: NTM's gate operates **inside a single read-head's address selection**; W3.5's gate operates **at the rollout level**, deciding whether the latent step's output also enters a parallel discrete channel.

## Erase-add memory update (NTM-only)

After computing the write weighting, NTM updates memory:

```
M̃_t(i) = M_{t−1}(i) · [1 − w_t^w(i) · e_t]      (erase)
M_t(i) = M̃_t(i) + w_t^w(i) · a_t                (add)
```

`e_t ∈ [0,1]^W` is the erase vector, `a_t ∈ R^W` is the add vector. **Erase-then-add allows partial overwrites** — a write can selectively zero out some dimensions and add others.

## Successor refinements

- **DNC (Graves 2016):** Adds usage-vector-based dynamic allocation `a_t` and temporal link matrix `L_t`. Replaces NTM's location-based shift with allocation + forward/backward link traversal — strictly more expressive.
- **MemN2N (Sukhbaatar 2015):** Drops location-based addressing entirely; uses pure content-addressing softmax with multi-hop. Simpler, scales better but cannot do sequential traversal.
- **Transformer self-attention** (modern): pure content-based addressing (no location-based) but with per-head specialization. Position info enters via positional encoding, not the addressing pipeline.

## Why pure backprop sufficed (no REINFORCE)

The NTM paper states verbatim:

> "every component of the architecture is differentiable, making it straightforward to train with gradient descent"

The interpolation gate `g_t`, the shift `s_t`, and the sharpening `γ_t` are all continuous outputs of sigmoid / softmax / softplus heads — no discrete sampling. This is the **founding precedent** that differentiable soft-attention over memory is gradient-trainable, which all later architectures (including W3.5) inherit.

## Sources

- [[Neural Turing Machines]] — original paper (Graves 2014).
- [[Differentiable Neural Computer]] — successor (Graves 2016 Nature).
- [[End-to-End Memory Networks]] — pure-content-addressing alternative (Sukhbaatar 2015).
- [[Latent Scratchpad Architecture]] — modern descendant.
