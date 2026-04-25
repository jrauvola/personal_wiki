---
type: concept
title: "Matryoshka Sparse Autoencoder"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/concept
  - tool/sparse-autoencoder
status: developing
complexity: advanced
domain: interpretability
aliases:
  - "Matryoshka SAE"
  - "Nested SAE"
related:
  - "[[Sparse Autoencoder]]"
  - "[[Feature Absorption and Splitting]]"
  - "[[Superposition]]"
sources:
  - "[[Towards Monosemanticity]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Absorption-resistant SAE variant is the right tool to apply to CODI latents — naive SAE would conflate hierarchical features in the reasoning trace."
  - slug: "branch-c"
    relevance: secondary
    why: "Nested-dictionary structure gives a hierarchy of probes: broad probes from small dictionary, specific probes from large — addresses probe-granularity contest directly."
  - slug: "branch-d"
    relevance: secondary
    why: "Matryoshka on CPF-trained CODI cleanly separates 'CPF adds routing stability' from 'CPF adds incremental reasoning features'."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Not a scaling concern."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Matryoshka Sparse Autoencoder

SAE variant (Nabeshima & Bussmann 2025, ICML) that simultaneously trains nested dictionaries at multiple widths, forcing each width to be self-sufficient for reconstruction. Reduces feature absorption from ~0.49 (vanilla SAE) to ~0.05.

## Formulation

Given dictionary widths `k_1 < k_2 < ... < k_N`, define nested latent slices `h_{1:k_i}` and reconstructions:

```
x̂_i = W_dec[:, :k_i] · h_{1:k_i} + b_dec     for i = 1, ..., N
L   = Σ_i (||x − x̂_i||² + λ_i · ||h_{1:k_i}||_1)
```

Constraint: the first `k_1` latents must be **sufficient** to reconstruct `x` well. The next `k_2 − k_1` latents only specialize.

## Why this prevents absorption

In vanilla SAE, child features have lower L1 cost than parent+child (as documented in [[Feature Absorption and Splitting]]), so the parent gets suppressed.

In Matryoshka, the loss at the smaller width `k_1` can only use the first `k_1` features. If the parent is not in that slice, the small-dictionary reconstruction fails, paying a large penalty at the `L_1` term. This forces the first `k_1` slots to hold exactly the high-frequency "parent" features that must be there for the broadest reconstruction.

The hierarchy is enforced by construction — broad features occupy early slots, specific features occupy later slots, absorption is architecturally impossible for the first-slot features.

## Empirical results (Gemma-2-2B, TinyStories)

- Absorption rate: **0.05** (vs 0.49 for vanilla SAE).
- Sparse probing accuracy: higher than vanilla at matched width.
- Targeted concept erasure: cleaner — removing a feature removes exactly the concept.
- Mild reconstruction trade-off vs vanilla at the same total width.

## Implementation

```python
class MatryoshkaSAE(nn.Module):
    def __init__(self, d_in, widths=[32, 128, 512, 2048]):
        self.W_enc = nn.Linear(d_in, max(widths))
        self.W_dec = nn.Linear(max(widths), d_in)
        self.widths = widths

    def forward(self, x):
        h = ReLU(self.W_enc(x - self.b_dec))
        losses = []
        for k in self.widths:
            h_k = h.clone()
            h_k[..., k:] = 0
            x_hat = self.W_dec(h_k) + self.b_dec
            losses.append(F.mse_loss(x_hat, x) + self.lam[k] * h_k.abs().sum())
        return sum(losses)
```

## Application to CODI latents

A Matryoshka SAE on CODI latent positions gives:

- **Small-width slice (k=16 or 32).** Should contain the "routing / template / format-prior" feature. If F3 is real, this feature should fire at all 7 collapsed positions.
- **Middle-width slice (k=512).** Per-step reasoning features — which problem-specific operations does each position carry?
- **Largest-width slice (k=2048+).** Fine-grained per-example features.

Because of the nesting, any features found at the broad width are guaranteed to be real parents, not absorption artifacts. This directly addresses the F3 question: is the template-lock a single feature or a cloud of locally-varying features averaged to one readout?

## Cross-references

- [[Sparse Autoencoder]] — base method.
- [[Feature Absorption and Splitting]] — problem this solves.
- [[Superposition]] — theoretical motivation.
