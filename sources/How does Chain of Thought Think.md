---
type: source
source_type: paper
title: "How does Chain of Thought Think? Mechanistic Interpretability of Chain-of-Thought Reasoning with Sparse Autoencoding"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/latent-reasoning
  - type/source
  - tool/sparse-autoencoder
status: triaged
arxiv_id: "2507.22928"
venue: "arXiv"
date_published: 2025-07-30
authors:
  - "Anonymous"
url: "https://arxiv.org/abs/2507.22928"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "SAE features swapped from CoT to noCoT runs raise answer log-prob by Δ=3.1 nats in Pythia-2.8B but have no reliable effect in Pythia-70M — a sharp scale threshold."
  - "CoT conditions produce significantly higher activation sparsity and feature-interpretability scores in the 2.8B model: 0.056 vs -0.013 for non-CoT (t=2.96, p=0.004)."
  - "Useful reasoning information is distributed across many moderately-activated features, not concentrated in top-K — random-K feature patching often outperforms top-K."
  - "CoT features activate fewer neurons per SAE feature than non-CoT features — more modular internal computation emerges with scale."
  - "Layer-2 residual-stream SAEs at final-token position recover the patchable reasoning directions."
  - "Feature swapping does not help the 70M model at any K — interpretability scale threshold exists independent of task accuracy."
related:
  - "[[Sparse Feature Circuits]]"
  - "[[Step-Level Sparse Autoencoder]]"
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Autoencoder]]"
  - "[[CODI]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/external/cot-sae-2025]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Direct methodology for testing whether CODI latents carry reasoning features — SAE + feature-patching recipe plugs straight into our F-battery."
  - slug: "branch-c"
    relevance: primary
    why: "Resolves probe-typology debate empirically: SAE features are the canonical basis; patching is the causal-test. Our LTO/DDR probes should agree with SAE attribution on reasoning-positive examples."
  - slug: "branch-a"
    relevance: primary
    why: "Establishes a scale threshold (70M → 2.8B) below which CoT induces NO interpretable modular structure. Directly relevant to the architecture-dependent story: Qwen3-4B may or may not be above the threshold; 8B likely is."
  - slug: "branch-d"
    relevance: secondary
    why: "Feature patching from CPF-trained → non-CPF CODI would quantify what CPF actually adds as a feature-count / attribution-mass delta."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# How does Chain of Thought Think?

First feature-level causal study of CoT faithfulness. Combines sparse autoencoders with activation patching to extract monosemantic features from Pythia-70M and Pythia-2.8B on GSM8K.

## Setup

- **Models.** Pythia-70M, Pythia-2.8B.
- **Data.** GSM8K train split, up to 1000 problems.
- **Input.** 256-token cap; two formats — CoT (3-shot) and noCoT (bare problem).
- **Site.** Residual stream of layer 2 at the final-token position.
- **SAE.** ReLU encoder, L1 sparsity. Dictionary ratios 4 and 8 tested.

## Loss

```
L_total = ||x − x̂||² + λ · ||h||_1
h       = ReLU(W_enc x + b_enc)
x̂       = W_dec h + b_dec
```
Separate SAEs trained on CoT and noCoT activations → dictionaries `D_CoT` and `D_noCoT`.

## Feature-patching recipe

Replace activations at a chosen feature subset `S`:
```
h_patch[S]  = h_CoT[S]
h_patch[S̄] = h_noCoT[S̄]
x̂_patch    = W_dec h_patch + b_dec
```
Then run the rest of the model. Effect:
```
Δ log P = log P_patched(ans) − log P_baseline(ans)
```

Two selection schemes: **Top-K** (largest |h_CoT − h_noCoT|), **Random-K** (uniform).

## Results

| Model | CoT feature-interpretability | noCoT | t, p |
|---|---|---|---|
| Pythia-70M | 0.018 (ns) | — | p=0.935 |
| Pythia-2.8B | 0.056 | −0.013 | t=2.96, p=0.004 |

- 2.8B confidence improves from 1.2 → 4.3 log-prob under CoT feature injection.
- 70M shows monotonic **decline** with CoT features — injection is harmful below threshold.
- Random-K often matches or exceeds Top-K in 2.8B → reasoning info is spread across features.

## Key conceptual move

CoT isn't just a text-decoration; it changes the internal computation structure when scale exceeds a threshold. Small models verbalize a rationale without internalizing it.

## Direct implications for our project

1. **F3 / F5 at 4B scale.** Qwen3-4B-Instruct-2507 is closer to the 2.8B than the 70M regime — so the CoT-SAE recipe should work. If SAE features at CODI's latent positions are near-zero for 7 of 8 positions and nonzero for position 3, that matches F3 template-attractor geometry directly.
2. **Scale threshold.** If Branch A scales 4B→9B and sees routing-lock disappear at 9B, that's a replicate of this paper's 70M→2.8B CoT threshold.
3. **Random-K > Top-K finding** implies the right intervention is **many small perturbations** rather than few big ones — motivates broad feature-diversity losses over localized clamps.

## Cross-references

- [[Sparse Feature Circuits]], [[Step-Level Sparse Autoencoder]], [[Towards Monosemanticity]]
- [[CODI]], [[Feature Collapse]], [[Routing vs Reasoning]]
