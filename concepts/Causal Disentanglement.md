---
type: concept
title: "Causal Disentanglement"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/causal
  - type/concept
status: developing
complexity: advanced
domain: interpretability
aliases:
  - "Causal Representation Learning"
  - "Invariance-Based Disentanglement"
  - "ICM Disentanglement"
related:
  - "[[Superposition]]"
  - "[[Sparse Autoencoder]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "[[Toy Models of Superposition]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Provides a theoretical framework for 'what we mean by disentangled latents' and an impossibility result (Locatello 2019) telling us unsupervised disentanglement is impossible without inductive bias — sparsity, auxiliary variables, or multi-environment intervention."
  - slug: "branch-d"
    relevance: primary
    why: "CPF is an inductive bias — the embedding-space anchor is the auxiliary signal that breaks the impossibility. Causal-disentanglement framing justifies why CPF is load-bearing."
  - slug: "branch-c"
    relevance: primary
    why: "Probe methodology must respect identifiability — a probe that recovers a non-identifiable axis is not reading reasoning content, it is reading noise."
  - slug: "branch-a"
    relevance: reference
    why: "Scale context only."
  - slug: "branch-b"
    relevance: reference
    why: "Detach operation is a kind of intervention; causal-mechanism view gives theoretical grounding."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Causal Disentanglement

Branch of representation learning that seeks latent variables corresponding to causal factors of the data-generating process, rather than statistical axes. Provides the theoretical frame under which "disentangled reasoning latents" is a well-defined goal.

## Key result: impossibility theorem

Locatello et al. 2019 ("Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations") proved:

> Without supervision or explicit inductive biases on the model and the data, unsupervised disentanglement of factors of variation is theoretically impossible.

Proof sketch: for any disentangled representation `z ~ p(z)` with independent components, one can construct an entangled `z' = T(z)` with the same marginal distribution by applying any measure-preserving transform `T` (rotations in Gaussian factors, shears, etc.). No unsupervised loss distinguishes them.

Empirically verified across 12,000+ VAE-family models: disentanglement scores are essentially uncorrelated with training dynamics absent an inductive bias.

## Inductive biases that break the impossibility

| Bias | Mechanism | Reference |
|---|---|---|
| **Auxiliary variables** | Observe a variable `u` (time, environment, label); require sources conditionally independent given `u`. | Hyvärinen et al. 2016+ (nonlinear ICA) |
| **Sparse mechanism shift** | Across interventions, only a sparse subset of mechanisms change. | Schölkopf, Locatello, Bauer, Ke et al. 2021 |
| **Multi-environment invariance** | Representation must satisfy a common optimal classifier across domains. | IRM, Arjovsky et al. 2019 |
| **Structural sparsity** | Dependency graph between sources and observations is sparse. | Zheng et al. 2022 |
| **Known graph structure** | Prior knowledge of causal DAG used as regularizer. | Schölkopf et al. 2021 |
| **Independent Causal Mechanisms (ICM)** | Mechanisms `p(x_i | pa(x_i))` change independently across environments. | Peters, Janzing, Schölkopf 2017 |

## Independent Causal Mechanisms principle

Data-generating process factorizes as:
```
p(x_1, ..., x_d) = Π_i p(x_i | pa(x_i))
```
with each conditional governed by an independent causal mechanism. If these mechanisms remain invariant under intervention on a subset of variables, learning them is (in the limit) identifiable.

## Why this matters for latent reasoning

F5 cross-example swap and F4 ablation together probe whether CODI latents encode **causal** per-example content. They don't.

A causal-disentanglement reading of this failure:
- The data-generating process of "reasoning about problem X" has a factor "intermediate calculation of X".
- A disentangled representation should recover this factor as one latent dimension.
- CODI latents fail this test → the network is not encoding intermediate-calculation factors; the gradient just doesn't force it to.

**To enforce the disentangled factor, we need an inductive bias the impossibility theorem leaves room for.** Candidates:

1. **Auxiliary variable (per-problem label).** Supervise latent positions to predict intermediate-step tokens. Matches the recipe of [[SIM-CoT]]'s auxiliary decoder.

2. **Multi-environment invariance.** Train on problems from multiple environments (e.g., arithmetic vs word problems) and require a common optimal decoder across environments — IRM-style.

3. **Sparse mechanism shift.** Across problem instances, only the instance-specific variables change; the reasoning mechanism is invariant. Could be enforced by latent-disentanglement losses that penalize cross-problem variation in mechanism parameters.

4. **Sparse generation.** Sparsity as a weak inductive bias (SAE-like) — not a full solution but a starting point that the theorem permits.

5. **Intervention-based training.** Counterfactual augmentations (swap one operand, one operator) give environments without extra labels.

## F3 / F5 framing

The F3 failure is an instance of "no auxiliary signal breaks the impossibility": training CODI with plain distillation loss leaves the latents unconstrained within a large equivalence class. Adding CPF (embedding-space anchor) is exactly the inductive bias the impossibility theorem says we need.

## Cross-references

- [[Superposition]] — complementary failure-mode framing.
- [[Sparse Autoencoder]] — sparsity as inductive bias for disentanglement.
- [[Feature Collapse]], [[Routing vs Reasoning]] — project-specific failure modes.
