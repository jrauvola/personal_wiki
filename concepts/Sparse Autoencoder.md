---
type: concept
title: "Sparse Autoencoder"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/concept
status: developing
complexity: advanced
domain: interpretability
aliases:
  - "SAE"
  - "Dictionary Learning"
related:
  - "[[Superposition]]"
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Step-Level Sparse Autoencoder]]"
  - "[[Feature Absorption and Splitting]]"
sources:
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Step-Level Sparse Autoencoder]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Primary tool candidate for testing whether CODI latent positions carry monosemantic reasoning features — addresses the core F3/F5 interpretation question."
  - slug: "branch-c"
    relevance: primary
    why: "Gives a principled basis for the LTO vs DDR probe-typology contest — both probes should agree on SAE-feature-positive examples."
  - slug: "branch-d"
    relevance: primary
    why: "SAE on CPF-trained vs vanilla CODI directly measures whether CPF injects distinguishable features (as opposed to just stabilizing the routing signal)."
  - slug: "branch-a"
    relevance: secondary
    why: "Scale-threshold finding (70M shows no features; 2.8B does) speaks to the architecture-dependent story."
  - slug: "branch-b"
    relevance: reference
    why: "Could in principle measure feature diversity across detach variants, but not core to Branch B."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Sparse Autoencoder (SAE)

Dictionary-learning method for decomposing neural-network activations into sparse combinations of overcomplete features, one feature per direction. The canonical tool for pulling superposed features apart in trained transformers.

## Canonical formulation

For activation `x ∈ R^d`, overcomplete latent `h ∈ R^k` with `k ≫ d`:

```
h  = σ(W_enc (x − b_dec) + b_enc)        # encoder
x̂  = W_dec h + b_dec                      # decoder (reconstruction)
L  = ||x − x̂||²_2 + λ · R(h)              # loss
```

## Activation / sparsity variants

| Variant | Activation σ | Sparsity term R(h) | Notes |
|---|---|---|---|
| **Vanilla ReLU-SAE** (Bricken 2023) | ReLU | `λ · ||h||_1` | L1 biases features toward zero — "shrinkage". |
| **Top-K SAE** (Gao 2024, OpenAI) | Hard top-k mask | implicit (exactly k nonzero) | No shrinkage, but hard-gate discontinuity. |
| **Gated SAE** (Rajamanoharan 2024) | ReLU + gating | L1 on gate pre-activations | Decouples magnitude from activation. |
| **JumpReLU SAE** (Rajamanoharan 2024, DeepMind) | Step-threshold piecewise | L0 via straight-through estimator | State-of-the-art on Gemma-2 9B at given sparsity. |
| **Matryoshka SAE** (Nabeshima & Bussmann 2025) | ReLU | nested L1 over widths | Reduces feature-absorption from 0.49 → 0.05. |
| **Step-Level SAE** (2026) | ReLU | L1 + context conditioning | Isolates incremental info, not absolute activation. |

## Evaluation metrics

- **Explained variance** — `1 − E[||x − x̂||²] / E[||x − E[x]||²]`.
- **Dead features** — fraction of `h` dimensions never firing on any example.
- **Mean activation sparsity** — `E[||h||_0]` per example.
- **Downstream loss proxy** — `x̂` plugged into next layer; measure task-metric degradation.
- **Feature interpretability** — human or automated (top-activating examples → language description).
- **Circuit recovery AUC** — attribution patching test (see [[Sparse Feature Circuits]]).

## Strengths

- Finds features no single neuron encodes.
- Features are causally meaningful — clamping drives the model to produce the concept.
- Pipeline scales to Claude 3 Sonnet (2024 Anthropic scaling work) and Gemma 2 9B.

## Known failure modes

- **Feature absorption** — parent features fail to fire, children absorb their activations. See [[Feature Absorption and Splitting]].
- **Feature splitting** — widening dictionary fractures features; scale-dependent.
- **Dead features** — sparsity penalty kills features entirely.
- **Composition** — some concepts need compositions of features, not single features.

## Canonical recipe applied to CODI

```python
# 1. Collect latent activations (batch × 8 positions × d_model)
latents = run_codi(problems)

# 2. Flatten over examples × positions → training set
X = latents.reshape(N*8, d_model)

# 3. Train SAE (k = 16 * d_model, λ tuned so mean ||h||_0 ≈ 20)
sae = SAE(d_in=d_model, d_hidden=16*d_model, activation="jumprelu")
sae.fit(X, epochs=..., lr=...)

# 4. Per-position analysis
for pos in range(8):
    H_pos = sae.encode(latents[:, pos, :])  # (N, k)
    active_features = (H_pos > 0).float().mean(dim=0)  # (k,)
    # → distribution of feature firings per position
```

F3 prediction: positions 0,1,2,4,5,6,7 all fire the same 1–2 features (format-prior); position 3 fires per-example features.

## Cross-references

- [[Superposition]], [[Feature Absorption and Splitting]]
- [[Towards Monosemanticity]], [[How does Chain of Thought Think]]
- [[Sparse Feature Circuits]], [[Step-Level Sparse Autoencoder]]
