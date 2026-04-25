---
type: concept
title: "Distribution Regularizer Catalog for Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/regularization
  - domain/information-theory
  - domain/anti-collapse
  - type/concept
status: developing
complexity: advanced
domain: latent-reasoning
aliases:
  - "Anti-Collapse Regularizer Catalog"
  - "Info-Theoretic Regularizer Menu"
related:
  - "[[Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Whitening-Based Anti-Collapse]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[Continuous Autoregressive Language Models]]"
  - "[[Contrastive Predictive Coding]]"
  - "[[InfoVAE]]"
sources:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[HSIC Bottleneck]]"
  - "[[VICReg]]"
  - "[[Barlow Twins]]"
  - "[[Contrastive Predictive Coding]]"
  - "[[InfoVAE]]"
  - "[[Continuous Autoregressive Language Models]]"
  - "[[KL-Regularized RL is Designed to Mode Collapse]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Taxonomy of drop-in anti-collapse losses for CPF extensions; each row maps directly to an F1-F6 failure."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Writeup-ready catalog for the regularization chapter. One place to cite the full space."
  - slug: "branch-b"
    relevance: secondary
    why: "Identifies which regularizers are compatible with detach regimes (batch-local, gradient-flow-agnostic)."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling-neutral; some regularizers may scale differently with model size."
  - slug: "branch-c"
    relevance: secondary
    why: "Probe-form derivatives of these regularizers (per-dim KL, per-position correlation) extend the F-battery."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Distribution Regularizer Catalog for Latent Reasoning

A ranked, equation-level menu of distribution/information-theoretic regularizers that could plug into CODI (or any latent-reasoning setup) to break the routing-lock / template-attractor failures measured in the F1-F6 battery.

## Targeted failure → regularizer map

Based on the SPAR F1-F6 battery on CODI V2 Qwen3-4B ([[Routing vs Reasoning]]):

| Failure | Symptom | Information-theoretic reading | Recommended loss family |
|---|---|---|---|
| **F3** template lock | 7/8 positions, entropy <0.4 bits | Per-position posterior collapse | Per-position KL-clip (CALM); InfoVAE MMD; cross-position Barlow |
| **F5** swap-null | 0% Δ under A↔B swap | $I(Z; Y \mid \text{question}) \approx 0$ | InfoNCE contrastive swap loss |
| **F6** narrow basin | σ=0.5 → <3% | Deterministic encoder, $f_\Sigma(x) \to 0$ | VIB KL term; VICReg variance hinge; CALM latent dropout |

## The five main regularizer families

### 1. Variational Information Bottleneck (VIB)

**Equation:**
$$
\mathcal{L}_\text{VIB} = -\mathbb{E}_{\epsilon}\!\left[\log q(y | z)\right] + \beta \cdot \mathrm{KL}\!\left[p(z|x) \,\|\, r(z)\right]
$$

**Use for:** F3 (if schedule β carefully), F6 (ensures $f_\Sigma > 0$).

**Risk:** posterior collapse itself if β too high. Literature fix: KL-annealing, free-bits, per-dim KL-clipping (CALM).

See: [[Deep Variational Information Bottleneck]], [[Variational Information Bottleneck]].

### 2. Conditional Entropy Bottleneck (CEB)

**Equation:**
$$
\mathcal{L}_\text{CEB} = \langle \log e(z|x) \rangle - \langle \log b(z|y) \rangle - \gamma \cdot \langle \log c(y|z) \rangle
$$

**Use for:** direct CPF replacement (see [[Context-Prediction-Fusion]]). γ=1 targets MNI.

**Risk:** requires a working $b(z|y)$ — our $e_\text{pred}$ is close but has limitations.

See: [[Conditional Entropy Bottleneck]].

### 3. HSIC Bottleneck

**Equation:**
$$
\mathcal{L}_\text{HSIC} = \mathrm{nHSIC}(KV_t, X) - \beta \cdot \mathrm{nHSIC}(KV_t, Y)
$$

with $\mathrm{nHSIC}(X, Y) = \mathrm{tr}(\tilde{K}_X \tilde{K}_Y)$ using Gaussian kernels.

**Use for:** detach-regime training (branch-b) where end-to-end gradients are unavailable.

**Risk:** kernel bandwidth σ tuning, β=500 in paper likely wildly wrong for transformer KVs.

See: [[HSIC Bottleneck]].

### 4. Whitening / variance-covariance regularization

**VICReg equation:**
$$
\mathcal{L}_\text{VIC} = \mu \cdot \underbrace{\tfrac{1}{d}\sum_j \max(0, \gamma - \mathrm{std}(z_j))}_\text{variance hinge} + \nu \cdot \underbrace{\tfrac{1}{d}\sum_{i \neq j} C_{ij}^2}_\text{covariance}
$$

**Barlow Twins equation:**
$$
\mathcal{L}_\text{BT} = \sum_i (1 - C_{ii})^2 + \lambda \sum_{i \neq j} C_{ij}^2
$$

**Use for:** F3 (cross-position Barlow), F6 (VICReg variance term).

**Risk:** statistical diversity doesn't guarantee functional diversity; pair with InfoNCE.

See: [[VICReg]], [[Barlow Twins]], [[Whitening-Based Anti-Collapse]].

### 5. InfoNCE contrastive

**Equation:**
$$
\mathcal{L}_\text{InfoNCE} = -\mathbb{E}\!\left[\log \frac{\exp(f(z^+, c))}{\sum_{j} \exp(f(z_j, c))}\right]
$$

**Use for:** F5 swap-null (direct attack on $I(Z; Y | c) = 0$).

**Risk:** loose MI bound; needs large N (batch size) to deliver non-trivial signal; false negatives in minibatch.

See: [[Contrastive Predictive Coding]].

## The CALM per-dim KL-clip extension

$$
\mathcal{L}_\text{KL-clip} = \sum_t \sum_i \max(\lambda_\text{KL}, \mathcal{L}_{\text{KL}, t, i})
$$

**Use for:** F3 positional/dimensional collapse. Sits on top of any VIB.

See: [[Continuous Autoregressive Language Models]].

## The "swap-InfoNCE" proposal for F5

Given a minibatch of $(q_i, z_i)$ pairs (question + latent KV):
$$
\mathcal{L}_\text{swap-NCE} = -\sum_i \log \frac{\exp(z_i^T W q_i)}{\sum_j \exp(z_j^T W q_i)}
$$

This *literally* teaches the model that example-$i$'s latent is the best match for example-$i$'s question. At eval, swapping $z$ from example $j$ into example $i$'s rollout will now degrade accuracy — F5 no longer reads "0%".

Training cost: one extra $N^2$ softmax per batch; bilinear projection $W$ is the only new parameter.

## Optimal Transport angle (open)

Wasserstein / Sinkhorn regularization of the latent distribution would:
- Match the aggregated posterior $q(z) = \mathbb{E}_x[q(z|x)]$ to a reference via OT cost rather than KL
- Give a *metric* rather than divergence (respects geometry)
- Cost: Sinkhorn iteration per batch, $O(N^2 \cdot L)$ for $L$ iterations (10-50 typical)

No 2025 paper applies this directly to latent CoT — a gap in the literature worth pursuing (see Open Questions in [[Research - Info and Distribution Constraints for Latents]]).

## What NOT to use (negative results)

- **Plain β-VAE on CoT.** Posterior-collapse-prone; long history of failures in NLG (see InfoVAE motivation). Use CALM-style KL-clip or InfoVAE MMD instead.
- **KL-regularized RL on top of CPF.** [[KL-Regularized RL is Designed to Mode Collapse]] shows this undoes supervised anti-collapse gains. If RL fine-tuning is planned, need MARA-style reward shaping.
- **Plain InfoNCE with tiny batches (N<32).** Bound saturates at log(N) bits, too weak to distinguish per-example.
- **HSIC-IB with paper's β=500.** Tuned for CIFAR; transformer KVs need recalibration.

## Recommended combination for CODI-BranchD

A concrete stack that addresses F3 + F5 + F6 simultaneously:
$$
\mathcal{L}_\text{total} = \mathcal{L}_\text{CE}(y) + \underbrace{\lambda_1 \mathcal{L}_\text{KL-clip}}_\text{F3} + \underbrace{\lambda_2 \mathcal{L}_\text{swap-NCE}}_\text{F5} + \underbrace{\lambda_3 \mathcal{L}_\text{VIC}^\text{variance}}_\text{F6}
$$

Start point: $\lambda_1 = 1, \lambda_\text{KL}=0.1, \lambda_2 = 0.1, \lambda_3 = 1$, γ (variance hinge) = 0.3 · mean-layer-norm-std. Needs ablation.
