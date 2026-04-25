---
type: concept
title: "Latent Scratchpad Architecture"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/architecture
  - domain/latent-reasoning
  - domain/interpretability
status: developing
complexity: advanced
domain: latent-reasoning
aliases:
  - "Latent Scratchpad"
  - "W3.5"
projects:
  - slug: spar-latent-reasoning
    relevance: primary
    why: "Candidate north-star architecture pattern — latent reasoning + interpretable discrete side-channel."
  - slug: branch-d
    relevance: primary
    why: "Composes cleanly with CPF: CPF anchors latent to discrete manifold; scratchpad emits from that anchored latent."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Latent Sketchpad]]"
  - "[[Token Assorted]]"
  - "[[HRPO]]"
  - "[[Quiet-STaR]]"
  - "[[Pause Tokens]]"
  - "[[Research - Latent Scratchpad Precedence]]"
sources:
  - "[[Latent Sketchpad]]"
  - "[[Token Assorted]]"
  - "[[HRPO]]"
---

# Latent Scratchpad Architecture

## Definition

An architecture pattern where:

1. **Primary channel:** `M` continuous latent reasoning tokens do the heavy computation (CODI/COCONUT-style — last hidden state fed back as next embedding, no decoding to vocab).
2. **Side channel:** at select positions chosen by a learned gate, the model emits `0..N` short **discrete** tokens (from the LM's existing vocabulary) that act as interpretable "notes."
3. **Attend-back property:** emitted discrete tokens are visible to subsequent latent steps via standard self-attention — the model can read its own notes.
4. **Interpretability:** the discrete channel is natively human-readable (no separate decoder required, unlike Latent Sketchpad's visual latents).
5. **Sparsity:** the gate has an information/rate penalty encouraging the model to write only when a note is load-bearing, giving a sparse audit trail.

## Contrast with related patterns

| Pattern | Primary | Side-channel | Interpretable? | Gate? |
|---|---|---|---|---|
| **Latent Scratchpad (proposed W3.5)** | Continuous latent (CODI/COCONUT) | Discrete vocab tokens | Directly | Yes — learned rate-penalized gate |
| Latent Sketchpad (Zhang 2025) | Text | Continuous visual latents → Sketch Decoder → images | Via decoder | Autoregressive in-stream |
| Token Assorted (Su 2025) | Text | VQ-VAE discrete codes | Not really (opaque codes) | No gate — random mix |
| HRPO (Yue 2025) | Blend of hidden states and token embeds | Same stream | Tokens yes | Learned gate — but gate **blends** not **emits separately** |
| Quiet-STaR (Zelikman 2024) | Text | Rationale tokens before each output token | Yes | Learnable `<startofthought>`/`<endofthought>` |
| Compressed CoT (Cheng 2024) | Text | Continuous contemplation tokens | Optional post-hoc decode | No |
| COCONUT / CODI | Continuous latent | None | No | N/A |

## Novelty claim

The specific combination — **latent-primary + discrete-vocab side-channel + learned gate + sparsity constraint, in text-only LLMs** — appears unoccupied as of 2026-04. Each individual component has a precedent, but no published work combines them:
- Latent Sketchpad proves the pattern works in **vision**.
- Token Assorted proves discrete side-channels aid reasoning, but codes are **opaque VQ** not vocab-readable.
- HRPO proves learned gates work, but blends in-stream rather than emits to a separate channel.
- Quiet-STaR proves learned `<thought>` emission works, but the primary channel is **text**, not latent.

See [[Research - Latent Scratchpad Precedence]] for full justification.

## Implementation sketch (W3.5)

- Start from a latent-reasoning backbone (CODI or COCONUT-trained model).
- Add a small auxiliary **gate head** (scalar sigmoid per latent step) and a **note head** (tied to output embedding, produces logits over vocab).
- At each latent step: gate decides "emit K tokens or skip." If emit, sample/greedy K tokens from note head; these tokens are inserted into the sequence before the next latent step.
- Training loss:
  - Standard CE on final answer (as in CODI).
  - Gate rate penalty `λ·E[g]` or hard KL-to-Bernoulli(p) for sparsity.
  - Optional auxiliary loss: note tokens must match a short "reference note" if provided by a curriculum.
- Inference: discrete notes are human-readable trace of what the model thinks it is doing.

## Open questions

- Does the gate degenerate (always emit → regular CoT; never emit → pure CODI)?
- How to collect/curate the optional reference notes for the auxiliary loss (if used)?
- Does the sparsity constraint actually improve interpretability, or does it push notes into ambiguity?
- Can we compose with CPF ([[Context-Prediction-Fusion]]) — CPF anchors the latent, scratchpad emits from anchored state?
