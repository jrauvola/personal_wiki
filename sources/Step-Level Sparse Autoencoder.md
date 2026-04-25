---
type: source
source_type: paper
title: "Step-Level Sparse Autoencoder for Reasoning Process Interpretation"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/latent-reasoning
  - type/source
  - tool/sparse-autoencoder
status: triaged
arxiv_id: "2603.03031"
venue: "arXiv"
date_published: 2026-03-04
authors:
  - "Anonymous"
url: "https://arxiv.org/html/2603.03031v1"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Step-level SAE (SSAE) disentangles reasoning steps by conditioning encoder+decoder on prior-step context, so sparse code encodes only incremental information."
  - "SSAE probes predict step-correctness at 78-86%, step-length at RMSE 1.46, logicality at 71-76% — token-level SAEs fail these tasks at baseline."
  - "Probe-guided weighted voting improves self-consistency: Qwen2.5-0.5B MultiArith 59.44% → 61.67%, DeepSeek-R1-32B AIME2024 86.67% → 90.00%."
  - "Features cluster into five functional categories: Reasoning, Calculation, Final-Resolution, Syntax, Narrative — proportions differ across model families."
  - "Exchanging unique dimensions of SSAE code across steps crosses over reasoning strategy; exchanging shared dimensions only produces surface linguistic variation."
  - "Information-bottleneck structure (λ-scheduled L1) forces SSAE to discard redundant context-predictable tokens and keep only incremental reasoning signal."
related:
  - "[[How does Chain of Thought Think]]"
  - "[[Sparse Feature Circuits]]"
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Autoencoder]]"
  - "[[CODI]]"
  - "[[COCONUT]]"
sources:
  - "[[.raw/external/step-level-sae-2026]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Direct recipe for training an SAE on CODI latent *steps* rather than tokens — step-level conditioning resolves the ambiguity of whether F3's 7/8 positions are genuinely empty or hide incremental content beneath the template."
  - slug: "branch-c"
    relevance: primary
    why: "Step-level SAE probes for step-correctness and logicality give Branch C a principled probe family that is neither LTO nor DDR — it conditions on prior steps like DDR but is monosemantic like LTO would prefer."
  - slug: "branch-d"
    relevance: primary
    why: "SSAE on CPF vs non-CPF CODI directly tests whether CPF injects per-step incremental information or just stabilizes the routing signal."
  - slug: "branch-a"
    relevance: secondary
    why: "Probe-guided weighted voting as an inference-time add-on applicable at any scale."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Step-Level Sparse Autoencoder (SSAE)

Extends SAE interpretability from tokens to reasoning steps. Conditions the encoder and decoder on prior-step context `C_k`, so the sparse code `I^k` represents only the incremental information added by step `s_k`.

## Architecture

For reasoning trajectory `(s_1, ..., s_K)`:

```
x_k        = [C_k; |SEP|; s_k]                 # context + current step
e_k        = Encoder(x_k)                     # contextualized embedding
I^k        = Sparsify(Projector(e_k))          # sparse incremental code
s_k_hat    = Decoder(e_k, I^k_{1:c})           # context + sparse features → step text
```

The decoder sees both the context embedding and the sparse features. This factorization is the load-bearing trick: anything the decoder could infer from `C_k` alone is not forced into the sparse code.

## Loss

```
L_recon     = − (1/L) Σ_{i=1}^L log P(t_i | C_k, I^k_{1:c}, t_{<i})
L_sparsity  = ||I^k||_1
L           = L_recon + λ · L_sparsity
```

With **dynamic λ control** via running-average feedback:
```
λ ← λ · (1 + α) if obs_sparsity > τ_spar
λ ← λ · (1 − α) if obs_sparsity < τ_spar
λ ∈ [λ_min, λ_max]
```

Hyperparams: sparse factor `c=1`, target sparsity `τ_spar=10`, Gaussian noise `σ=0.01`, adjustment rate `α=0.01`.

## Empirical findings

### Probing step properties

| Property | SSAE | Token-SAE baseline |
|---|---|---|
| Step length RMSE | 1.46-2.10 | 28.04-33.30 |
| Step correctness acc | 78-86% | ~50% |
| Logicality acc | 71-76% | ~50% |
| First-token PPL | 1.62-4.09 | 49-103 |

### Functional clustering

N2G mining of SSAE features in Llama-3.2-1B and Qwen2.5-0.5B reveals five functional groups: Reasoning (40% Llama, 20% Qwen), Calculation (26% Qwen), Final-Resolution (36% Qwen), Syntax (18% Qwen), Narrative.

### Dimension-swap experiment

- **Swap unique dimensions across two trajectories** → reasoning strategy crossover (answer changes).
- **Swap shared dimensions** → only linguistic surface changes.

Direct analogue of activation patching at SAE-feature granularity.

### Probe-guided weighted voting

At inference, multiple samples are reweighted by an SSAE-based probe on step-correctness before majority-voting the final answer. Small-model probe lifts frontier-model accuracy (0.5B probe → 32B model gains +3.33 on AIME 2024).

## Direct implications for CODI/COCONUT

- CODI latents occupy positions, not text-steps — but the SSAE conditioning recipe translates: conditioning encoder+decoder on the discrete-token context of each CODI latent position would isolate incremental content.
- F3 would be testable: if the SSAE sparse code at 7 of 8 positions has `||I^k||_1 → 0` (everything is inferable from context alone), the positions are genuinely empty; if not, they carry incremental content masked by the logit-lens readout.
- Shared vs unique-dimension swap is a direct generalization of F5's cross-example swap — F5 swaps everything at once; SSAE lets us swap only the unique incremental part.

## Cross-references

- [[How does Chain of Thought Think]], [[Sparse Feature Circuits]], [[Towards Monosemanticity]]
- [[CODI]], [[COCONUT]], [[Feature Collapse]], [[Routing vs Reasoning]]
