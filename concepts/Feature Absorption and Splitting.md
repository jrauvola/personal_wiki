---
type: concept
title: "Feature Absorption and Splitting"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/concept
  - failure-mode
status: developing
complexity: advanced
domain: interpretability
aliases:
  - "SAE Absorption"
  - "Hierarchical Absorption"
related:
  - "[[Sparse Autoencoder]]"
  - "[[Superposition]]"
  - "[[Matryoshka Sparse Autoencoder]]"
  - "[[Feature Collapse]]"
sources:
  - "[[Towards Monosemanticity]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Limits which SAE variants can be safely applied to CODI latents — naive SAE on CODI might show absorption where per-step reasoning features are absorbed by a 'reasoning-general' feature."
  - slug: "branch-c"
    relevance: secondary
    why: "Complicates interpretation of monosemantic features as a 'canonical basis' — probes based on absorbed features are misleading."
  - slug: "branch-d"
    relevance: reference
    why: "Context for CPF evaluation: absorption-resistant SAE variants (Matryoshka, Orthogonal) give more robust post-hoc measurements."
  - slug: "branch-a"
    relevance: not-applicable
    why: "Not a scaling concern."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Feature Absorption and Splitting

Two related failure modes of vanilla sparse autoencoders when the underlying feature structure is hierarchical. Introduced in Chanin et al. 2024 ("A is for Absorption").

## Splitting

As the SAE dictionary width grows, a single broad feature from a narrower dictionary **splits** into multiple more-specific children:

```
narrow-SAE: "mathematics" feature
wide-SAE:  "algebra", "geometry", "number-theory" features
```

Not pathological in itself — reflects genuine hierarchy in the data — but means feature interpretation is **dictionary-width-dependent**: the "same" activation has different optimal decompositions at different widths.

## Absorption (pathological)

Parent features fail to activate where expected, with their activations "absorbed" into child features:

```
Input: "algebra textbook"
Expected: "math" + "algebra" both fire
Observed: "math" silent, "algebra" fires alone
```

This is a direct consequence of the L1 sparsity penalty preferring a sparser decomposition whenever child features alone reconstruct acceptably.

## Mathematical failure mode

Given parent feature `p` and child feature `c` with `c ⊂ p` in concept:

Vanilla SAE loss prefers `h = [0, 1]` over `h = [1, 1]` even when the parent should semantically fire, because:
```
L_sparsity([0, 1]) = 1 < L_sparsity([1, 1]) = 2
L_recon            difference is negligible (child alone reconstructs)
```

Sparsity optimization **actively suppresses** correct parent activation.

## Measurement

Chanin et al. introduce an absorption metric: for concept-split pair `(parent, child)`, measure the fraction of child-expected examples where the parent also activates above threshold. Low parent-activation rate on child-positive examples = high absorption.

- Vanilla SAEs: absorption rate 0.49.
- Matryoshka SAE: absorption rate 0.05 (see [[Matryoshka Sparse Autoencoder]]).

## Why this matters for CODI interpretation

If we train a naive SAE on CODI latents and observe that:
- A single "routing-mode" feature fires at all 7 "empty" positions.
- No per-step sub-features activate alongside it.

...this could be either:
1. **Real** — the positions genuinely encode just the routing signal.
2. **Absorption artifact** — per-step child features exist but the L1 penalty is suppressing the parent "routing" feature OR the parent is active but absorbing its children's activations.

Distinguishing requires Matryoshka / Orthogonal SAE variants that control for absorption.

## Mitigations

| Method | Mechanism |
|---|---|
| **Matryoshka SAE** | Nested dictionaries at multiple widths, trained jointly. Small dictionaries must reconstruct independently → forced to hold parent features. |
| **Orthogonal SAE** | Chunked orthogonality penalty on decoder features — directly prevents child features from absorbing by making them decoder-orthogonal to the parent. |
| **Mixture-of-Experts SAE** | Dictionary routed per-input; experts specialize without absorbing other experts. |
| **L0 (JumpReLU / TopK)** | Replace L1 with L0 via straight-through estimator — removes the shrinkage pressure that causes absorption. |

## Cross-references

- [[Sparse Autoencoder]], [[Matryoshka Sparse Autoencoder]]
- [[Superposition]], [[Feature Collapse]]
