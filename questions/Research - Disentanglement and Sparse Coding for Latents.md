---
type: synthesis
title: "Research: Disentanglement and Sparse Coding for Latents"
created: 2026-04-23
updated: 2026-04-23
tags:
  - research
  - domain/interpretability
  - domain/latent-reasoning
  - domain/mechanistic
status: developing
question: "Can sparse coding, superposition disentanglement, and invariance-breaking techniques break CODI's routing-lock / template-attractor failure modes?"
answer_quality: draft
related:
  - "[[Toy Models of Superposition]]"
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Step-Level Sparse Autoencoder]]"
  - "[[Superposition]]"
  - "[[Sparse Autoencoder]]"
  - "[[Feature Absorption and Splitting]]"
  - "[[Matryoshka Sparse Autoencoder]]"
  - "[[Causal Disentanglement]]"
  - "[[Nelson Elhage]]"
  - "[[Samuel Marks]]"
  - "[[Bernhard Schölkopf]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
sources:
  - "[[Toy Models of Superposition]]"
  - "[[Towards Monosemanticity]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Step-Level Sparse Autoencoder]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Top-level synthesis of the anti-superposition toolkit applicable to CODI's F3/F5 battery; writeup backbone for the interpretability section."
  - slug: "branch-c"
    relevance: primary
    why: "Directly answers the probe-typology contest (LTO vs DDR) — sparse coding gives a principled basis both probes approximate and attribution patching gives a causal benchmark."
  - slug: "branch-d"
    relevance: secondary
    why: "Anti-superposition / feature-diversity losses motivated by this research extend the CPF vocabulary of anti-collapse mechanisms."
  - slug: "branch-a"
    relevance: reference
    why: "Scale threshold for interpretable CoT structure (70M → 2.8B) informs the architecture-dependence framing."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Research: Disentanglement and Sparse Coding for Latents

## Overview

Three convergent literatures — superposition theory (Anthropic 2022–2024), sparse-autoencoder dictionary learning (Cunningham, Bricken, Templeton, Gao, Marks 2023–2025), and causal representation learning (Locatello, Schölkopf 2019–2021) — give us a principled framework for diagnosing and breaking the F3 template-attractor / F5 decoder-invariance failures in CODI V2. The core move: treat F3/F5 as a **superposition artifact at position-granularity**, use sparse autoencoders to extract the hidden per-example content, and use causal-representation inductive biases (sparsity, auxiliary variables, multi-environment invariance) to train the next generation of latent-reasoning models so the content becomes decoder-visible.

This synthesis is structured for direct methodological reuse — the loss terms, probe formulations, and experimental protocols here plug into the existing F-battery / CODI harness.

## Key Findings — anti-superposition toolkit ↔ our failure modes

### F1. F3 template-lock is the canonical superposition-at-position signature

7 of 8 CODI latent positions decode (logit-lens) to the identical template `The → 0 → 0 → ? → . → . → . → .` with <0.4 bits entropy, while step 3 alone carries per-example content. [[Toy Models of Superposition]] predicts exactly this regime when:
- features (= "position holds per-example content for problem X") are sparse (only 1-of-8 positions does so at a time in the trained model),
- importance is concentrated (the decoder only needs one position to route, so gradient pressure allocates one direction and shares the rest),
- nonlinearity (the LM softmax) filters interference downstream.

The 7-into-1 direction packing is geometrically the same phenomenon Elhage et al. describe as polysemantic neurons — but at *position*-granularity instead of neuron-granularity. (Source: [[Toy Models of Superposition]])

### F2. F5 decoder-invariance confirms the basis mismatch

Swapping B's latent KV with A's leaves B's accuracy unchanged. This would be impossible if the latent were encoding per-example reasoning content in a *decoder-decodable* basis: the decoder would then produce B's answer using A's features, degrading accuracy. Instead, the 0.78 median cosine / 63-PC variance of F5 proxy shows per-example content **exists** in the latent KV but the decoder ignores it — it's orthogonal to the direction the decoder reads. This is the exact pathology sparse autoencoders are designed to reveal: hidden features that are real, geometric, but not in the readout basis. (Source: [[Towards Monosemanticity]], [[How does Chain of Thought Think]])

### F3. Sparse autoencoders give a probe-typology winner

Branch C's LTO vs Decoding-Depth-Recurrent probe contest is currently under-determined — different linear probes recover different things because the underlying basis is superposed. An SAE trained on CODI's latent activations provides the **canonical basis both probes approximate**. Concretely:

- Linear probe X fires on feature-set F_X ⊂ SAE features.
- Linear probe Y fires on F_Y.
- The SAE-feature-level attribution (via [[Sparse Feature Circuits]]' attribution patching) is the ground-truth causal baseline.
- Branch C verdict: whichever probe's feature-set aligns more with causally-implicated features wins. Neither or both alignment → the probe typology is not load-bearing; other factors (training data, init) dominate.

(Source: [[Sparse Feature Circuits]], [[How does Chain of Thought Think]])

### F4. Step-level SAE conditioning isolates per-position incremental content

[[Step-Level Sparse Autoencoder]] (SSAE) conditions the encoder/decoder on prior-step context `C_k`, so the sparse code encodes **only the incremental information** added at step `k`. Applied to CODI latent positions:
- If 7 of 8 positions have `||I^k||_1 → 0`, they genuinely carry only context-predictable signal (routing / format-prior).
- If `||I^k||_1 > 0` at "empty" positions, there's hidden incremental content the default decoder ignores — a *different* failure mode than pure F3 template-lock.

This directly distinguishes routing-mode-with-no-content from routing-mode-with-invisible-content. SSAE probes for step-correctness hit 78-86% accuracy where token-level SAEs hit baseline — evidence that step conditioning is a load-bearing inductive bias, not just a convenience. (Source: [[Step-Level Sparse Autoencoder]])

### F5. Causal disentanglement theorem legitimizes CPF as an inductive bias

[[Causal Disentanglement]] (Locatello 2019 + Schölkopf 2021) proves unsupervised disentanglement is **impossible** without inductive biases on model or data. The Branch D hypothesis that CPF `e_fusion = α·h_ctx + (1-α)·e_pred` is load-bearing is, from this frame, the embedding-space anchor acting as the auxiliary signal the impossibility theorem requires. Variants of CPF are equivalent to:
- **Auxiliary variable.** `e_pred` is a token-prediction target (supervision-lite).
- **Sparse mechanism shift.** `α` gates which mechanism fires per position.
- **Multi-environment invariance.** Across problem instances, the decoder's reliance on the fused latent must satisfy a common optimal mapping (implicit IRM).

This reframes CPF as *the specific inductive bias that breaks the impossibility* — not just a hack to stabilize training. (Source: [[Causal Disentanglement]], [[Latent Thoughts Tuning]])

## Proposed probe formulations and loss terms

Equation-level candidates for immediate implementation:

### P1. SAE on CODI latents (baseline probe)

Train a JumpReLU SAE on CODI latent positions:
```
h  = JumpReLU_θ(W_enc(x − b_dec) + b_enc)        # sparse code
x̂  = W_dec h + b_dec                              # reconstruction
L  = ||x − x̂||²_2 + λ · ||h||_0                  # L0 via STE
```
- `x` = CODI latent at position p, batch of examples.
- Dictionary width `k = 16 · d_model` as a starting point.
- Target sparsity ~20 active features per example.

Per-position readout: for each feature `i`, measure firing rate at each of the 8 positions. F3 prediction: a small set of features fires at all 7 "empty" positions (template features), and a disjoint set fires at position 3 (per-example features).

### P2. Step-conditioned SAE (SSAE) for incremental content

Adapted from [[Step-Level Sparse Autoencoder]]:
```
e_k        = Encoder([C_k; |SEP|; latent_k])
I^k        = SparseCode(e_k)
latent_k_hat = Decoder(e_k, I^k)
L_recon    = ||latent_k − latent_k_hat||²
L_sparsity = ||I^k||_1
L          = L_recon + λ · L_sparsity    # λ dynamic-scheduled
```
Context `C_k` = discrete-token context + prior CODI latents. Isolates incremental content per latent position.

### P3. Attribution patching for causal feature identification

Per [[Sparse Feature Circuits]]:
```
IG_i ≈ (f_i(x_correct) − f_i(x_corrupt)) · ∂m/∂f_i |_{interpolated}
```
Measure which SAE features `i` are causally responsible for the correct answer's log-prob `m`. F4 prediction (ablation sensitivity): features at position 3 have high attribution; features at other positions have near-zero attribution (consistent with the 25-29% accuracy drop from ablating 7 positions).

### P4. Anti-superposition loss (training-time, Branch D-compatible)

Add to the CODI training loss a **feature-diversity penalty** on the latent positions:

**Orthogonality penalty on latent-position Gram:**
```
L_diversity = Σ_{p ≠ q} |⟨latent_p, latent_q⟩|² / (|latent_p| · |latent_q|)
```
Small per-example weight; penalizes trivial "all positions collapse to one direction" solution while tolerating the "position 3 is special" fingerprint seen empirically.

**Variant: population-level orthogonality (avoids over-constraining individual examples).**
Batch-averaged positional Gram:
```
L_diversity = ||E_x[latent_p latent_q^T]||²_F     for p ≠ q
```

### P5. Multi-environment invariance (IRM-flavored)

Partition training data into environments `e_1, ..., e_E` (e.g., by problem type: arithmetic / word problem / geometric). Apply IRM penalty:
```
L_IRM = Σ_e R^e(φ) + λ · ||∇_w R^e(w · φ)|_{w=1}||²
```
where `φ` is the CODI decoder applied to fused latents and `R^e` is the per-environment risk. Forces the decoder to use the fused latent in a way that a common classifier-head solves all environments — breaking the disentanglement impossibility via multi-environment signal.

### P6. Matryoshka-SAE probe hierarchy (for Branch C)

Per [[Matryoshka Sparse Autoencoder]]:
```
x̂_i = W_dec[:, :k_i] h_{1:k_i} + b_dec              for i = 1, ..., N
L   = Σ_i ||x − x̂_i||² + λ_i · ||h_{1:k_i}||_1
```
Widths `k_1=16, k_2=64, k_3=256, k_4=1024`. 

At each width `k_i`, train a linear probe for the target (step-correctness, answer, operator). The *first* width at which probe accuracy saturates tells us how many monosemantic features are actually load-bearing for the target. This is the principled resolution of Branch C's probe-granularity question.

## Key concepts applicable to our work

- [[Superposition]] — core framework for F3 template-lock.
- [[Sparse Autoencoder]] — primary tool, variant choices (JumpReLU recommended for production).
- [[Feature Absorption and Splitting]] — failure mode to watch for in naive SAE applications.
- [[Matryoshka Sparse Autoencoder]] — absorption-resistant variant; primary candidate for F3 probe construction.
- [[Causal Disentanglement]] — theoretical framing for why CPF and related losses are necessary (impossibility theorem) not optional.
- [[Feature Collapse]], [[Routing vs Reasoning]] — project-side concepts that ground these techniques in F-battery observations.

## Key entities

- [[Nelson Elhage]] — lead of Toy Models of Superposition; frames the representational theory.
- [[Samuel Marks]] — sparse feature circuits recipe (attribution patching + SAE).
- [[Bernhard Schölkopf]] — senior author of causal representation learning literature; grounds our inductive-bias choices.

## Sources

- [[Toy Models of Superposition]] — Elhage et al. 2022 (Anthropic / Harvard). Foundational superposition paper. *high confidence, canonical.*
- [[Towards Monosemanticity]] — Bricken, Templeton et al. 2023 (Anthropic). First empirical SAE extraction of monosemantic features from transformer residual stream. *high confidence, canonical.*
- [[Sparse Feature Circuits]] — Marks, Rager et al. 2024 (ICLR 2025). Attribution patching for feature-level circuit discovery. *high confidence, peer-reviewed.*
- [[How does Chain of Thought Think]] — 2025 (arxiv 2507.22928). First feature-level causal study of CoT. *medium-high confidence; preprint but clean methodology.*
- [[Step-Level Sparse Autoencoder]] — 2026 (arxiv 2603.03031). Context-conditioned SAE for reasoning-step disentanglement. *medium confidence; preprint, clean empirics.*

Additional grounding references consulted (not filed as sources this round, but cross-referenced):
- Gao et al. 2024 (OpenAI) — Scaling and Evaluating Sparse Autoencoders. Top-K SAE. https://cdn.openai.com/papers/sparse-autoencoders.pdf
- Rajamanoharan et al. 2024 (DeepMind) — Jumping Ahead: JumpReLU SAE. https://arxiv.org/abs/2407.14435
- Nabeshima & Bussmann 2025 — Learning Multi-Level Features with Matryoshka Sparse Autoencoders. https://arxiv.org/abs/2503.17547
- Chanin et al. 2024 — A is for Absorption. https://arxiv.org/abs/2409.14507
- Cunningham et al. 2023 — Sparse Autoencoders Find Highly Interpretable Features in Language Models. https://arxiv.org/abs/2309.08600
- Locatello et al. 2019 — Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations. https://arxiv.org/abs/1811.12359
- Schölkopf, Locatello et al. 2021 — Towards Causal Representation Learning. https://arxiv.org/abs/2102.11107
- Arjovsky et al. 2019 — Invariant Risk Minimization. https://arxiv.org/abs/1907.02893
- Templeton et al. 2024 (Anthropic) — Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet. https://transformer-circuits.pub/2024/scaling-monosemanticity/
- Hyvärinen et al. 2016+ — nonlinear ICA with auxiliary variables (identifiability framework).

## Contradictions

1. **L1 vs L0 sparsity.** Classical Bricken SAEs use L1; Gao 2024's Top-K and Rajamanoharan 2024's JumpReLU argue L1 causes shrinkage and feature absorption. Resolution: for CODI application, prefer JumpReLU or Matryoshka; L1 is only acceptable as a baseline or when absorption is empirically low for the target activations. (See [[Feature Absorption and Splitting]].)

2. **Scale threshold for interpretable CoT.** [[How does Chain of Thought Think]] finds CoT produces no feature-level modular structure below 2.8B and a sharp threshold at 2.8B. This contradicts implicit assumptions in smaller-model interpretability work (e.g., Pythia-70M studies that claim to find CoT circuits). Our Qwen3-4B scale is above the threshold; Branch A's 9B scaling should push further above. But this directly predicts that below-1B continuous-CoT experiments (COCONUT scale) will show qualitatively different / weaker feature structures than what we see at 4B+.

3. **Impossibility theorem vs "feature-sparsity is enough."** Locatello 2019 proves unsupervised disentanglement needs inductive bias; Cunningham 2023 + Bricken 2023 show sparsity alone gives interpretable features. Partial resolution: sparsity *is* one of the inductive biases the impossibility leaves room for; "impossibility" refers to distributional-independence-only models. But this means we can't assume sparsity is sufficient for *causal* disentanglement — we still need auxiliary signals (CPF) or intervention-based training for causally-meaningful latent axes.

## Open Questions

1. **Does SAE on CODI actually recover per-example features at the "empty" positions?** The F5 result says per-example content exists in the KV; the F3 result says it's not in the logit-lens readout. SAE should either (a) find the hidden features — validating the superposition reading, or (b) find none — validating the genuine-emptiness reading. Untested.

2. **Does feature-diversity / orthogonality loss during training break routing-lock?** P4 above is a minimal-cost addition. Ablate: CODI baseline vs CODI + L_diversity vs CODI + CPF + L_diversity. Untested.

3. **What's the Matryoshka-SAE width at which F3 features saturate?** Probing hierarchy of k=16/64/256/1024 answers Branch C's probe-granularity question directly. Untested.

4. **Is the 70M→2.8B CoT scale threshold a real threshold or a gradient?** Replicating at 1B, 1.5B, 2B would characterize the phase-change curve. Relevant to Branch A's scaling story.

5. **Can IRM-style multi-environment training be applied at CODI's data scale?** GSM8K has natural environment partitions (word vs pure-arithmetic). Feasibility unknown; no prior art in the continuous-latent-reasoning family.

6. **Does Step-Level SAE conditioning recipe transfer to continuous latents?** SSAE was built for discrete-step trajectories. The conditioning signal (`C_k` = context + prior steps) is well-defined for CODI-style per-position latents, but the reconstruction target becomes a vector rather than a token sequence. Adaptation non-trivial.

7. **Feature absorption test on CPF-trained vs vanilla CODI.** If CPF really injects per-example content, Matryoshka SAE should show more distinct features at position 3 in CPF-trained models. A clean empirical test.

8. **How does anti-superposition loss interact with detach (Branch B)?** Orthogonality penalty on latent positions is compatible with detach, but their combined effect on gradient flow is untested.

## Skipped (page-limit)

- Gated SAE (Rajamanoharan 2024) detail.
- Invariant Risk Minimization detailed review (covered cursorily in F5).
- SynthSAEBench evaluation framework.
- Orthogonal SAE (augmented with chunked orthogonality penalty) — mentioned but not filed as source.
- 2024 Anthropic "Scaling Monosemanticity" Claude 3 Sonnet paper — significant but overlaps heavily with [[Towards Monosemanticity]] for our purposes.

These can be crawled in a follow-up pass if Branch C or D takes up SAE-based probing as a core method.

## Status-at-a-glance

- Pages created this session: 14 (5 sources, 5 concepts, 3 entities, 1 synthesis).
- Round count: 2 of 3 (third round not needed; gaps were methodological detail, not framing gaps).
- Recommended next action: prototype P1 (vanilla SAE on CODI latents) on the existing bf16 checkpoint; if features are found at position 3 only, file as first cross-method validation of the routing-vs-reasoning framing.
