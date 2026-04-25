---
type: synthesis
title: "Research: Info and Distribution Constraints for Latents"
created: 2026-04-23
updated: 2026-04-23
tags:
  - research
  - domain/information-theory
  - domain/regularization
  - domain/latent-reasoning
  - domain/anti-collapse
status: developing
question: "Which information-theoretic and distribution-regularization techniques could break routing-lock / template-attractor failures in our CODI V2 Qwen3-4B latent reasoning model?"
answer_quality: draft
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[HSIC Bottleneck]]"
  - "[[VICReg]]"
  - "[[Barlow Twins]]"
  - "[[Contrastive Predictive Coding]]"
  - "[[InfoVAE]]"
  - "[[Continuous Autoregressive Language Models]]"
  - "[[KL-Regularized RL is Designed to Mode Collapse]]"
  - "[[Emergence of Invariance and Disentanglement]]"
  - "[[Variational Information Bottleneck]]"
  - "[[Conditional Entropy Bottleneck]]"
  - "[[Whitening-Based Anti-Collapse]]"
  - "[[Distribution Regularizer Catalog]]"
  - "[[Alex Alemi]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
  - "[[Context-Prediction-Fusion]]"
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
  - "[[Emergence of Invariance and Disentanglement]]"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Direct menu of IB / distribution losses for CPF extensions; every regularizer family is mapped to an F1-F6 failure mode."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational synthesis for the regularization chapter of the writeup. All equations equation-level, all claims sourced."
  - slug: "branch-b"
    relevance: secondary
    why: "HSIC-IB, VICReg, Barlow Twins, whitening methods are batch-local and compatible with detach regimes."
  - slug: "branch-a"
    relevance: secondary
    why: "Regularizers are scaling-neutral but CALM's per-dim KL-clip result (71/128 collapse) reappears at scale; anticipated."
  - slug: "branch-c"
    relevance: secondary
    why: "Per-dim KL, cross-position correlation, and InfoNCE-variant diagnostics extend the F-battery probe methodology."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Research: Info and Distribution Constraints for Latents

## Overview

This synthesis answers: **What information-theoretic and distribution-regularization techniques could plug into our CODI V2 Qwen3-4B latent-reasoning harness to break the routing-lock / template-attractor failures measured in the F1-F6 battery ([[Routing vs Reasoning]])?**

Three failures targeted:
- **F3 template lock:** 7/8 latent positions decode to a fixed string with <0.4 bits entropy — classic posterior-collapse signature.
- **F5 swap-null:** swapping example A's latent KV with example B's on the same question produces 0% accuracy change — latents don't carry per-example information used by the decoder. MI reading: $I(Z;Y|\text{question}) \approx 0$.
- **F6 narrow basin:** σ=0.5 Gaussian noise on the KV drops accuracy from ~16% to <3% — needle-sharp attractor.

Five regularizer families surveyed: VIB (variational IB), CEB (conditional entropy), HSIC-IB (kernel-based), whitening methods (Barlow Twins, VICReg), and contrastive (InfoNCE). A sixth (OT / Sinkhorn) is flagged as a literature gap worth pursuing.

## Key Findings

### 1. F3 template lock is canonical posterior collapse; CALM's per-dim KL-clip is the prescription

[[Continuous Autoregressive Language Models]] (CALM, Oct 2025) observed the direct analogue of F3 — 71 of 128 latent *dimensions* collapse to the prior without remediation — and fixed it with per-dimension KL clipping:
$$
\mathcal{L}_\text{KL}^\text{clip} = \sum_i \max(\lambda_\text{KL}, \mathcal{L}_{\text{KL}, i})
$$
with $\lambda_\text{KL} = 0.5$. Adapted to CODI's per-position collapse:
$$
\mathcal{L}_\text{CODI-KL-clip} = \mathcal{L}_\text{CE}(y) + \sum_{t=1}^T \max\!\left(\lambda_\text{KL},\, \mathrm{KL}(q(KV_t|x) \| r(KV_t))\right)
$$
(Source: [[Continuous Autoregressive Language Models]])

### 2. F5 swap-null is literally the InfoNCE training signal

The F5 eval protocol (shuffle latents within minibatch, measure accuracy delta) is the *test-time* version of the InfoNCE *training-time* loss. Teaching CODI during training that example $i$'s latent is the best match for example $i$'s question:
$$
\mathcal{L}_\text{swap-NCE} = -\sum_i \log \frac{\exp(z_i^T W q_i)}{\sum_j \exp(z_j^T W q_i)}
$$
forces $I(Z;Y|\text{question}) > 0$ by construction. [[Contrastive Predictive Coding]] gives the MI bound $I \ge \log(N) - \mathcal{L}$, so batch size $N \gtrsim 32$ is needed to deliver non-trivial signal.
(Source: [[Contrastive Predictive Coding]])

### 3. CPF is already an implicit VIB — CEB formalises it with a learnable γ

[[Context-Prediction-Fusion]]'s equation $e_\text{fusion} = \alpha \cdot h_\text{ctx} + (1-\alpha) \cdot e_\text{pred}$ is a convex mix of:
- $h_\text{ctx}$: full context info (the VIB/CEB forward-encoder side)
- $e_\text{pred}$: Y-conditional vocab-simplex projection (the CEB backward-encoder side)

[[Conditional Entropy Bottleneck]]'s $\text{VCEB} = \langle \log e(z|x) \rangle - \langle \log b(z|y) \rangle - \gamma \langle \log c(y|z) \rangle$ with $b(z|y) \leftrightarrow e_\text{pred}$ reformulates CPF as a principled IB with a learnable γ replacing CPF's hand-tuned α. Target: Minimum Necessary Information (MNI) at γ=1.
(Source: [[Conditional Entropy Bottleneck]])

### 4. Whitening regularizers (VICReg variance hinge, cross-position Barlow) fix F3 and F6 without a prior

VICReg's variance hinge (Source: [[VICReg]]):
$$
v(Z) = \frac{1}{d}\sum_j \max(0, \gamma - \sqrt{\mathrm{Var}(z^j) + \epsilon})
$$

directly widens per-dimension spread — F6 basin-widening *by construction*. Cross-position Barlow Twins (Source: [[Barlow Twins]]):
$$
\mathcal{L}_\text{pos-BT} = \sum_i (1 - C^{t,t}_{ii})^2 + \lambda \sum_{i\ne j} (C^{t,t'}_{ij})^2
$$

forces positions to carry decorrelated info — direct F3 attack. Both are batch-local, detach-compatible, no prior-choice headache.

### 5. KL-regularized RL on top of CPF would destroy these gains

[[KL-Regularized RL is Designed to Mode Collapse]] (Oct 2025) proves that standard KL-regularized RL collapses to a single mode at the *global optimum* — not just an optimisation artefact. Diagnostic:
$$
\log \frac{G_\beta(y_1)}{G_\beta(y_2)} = \log \frac{\pi_\text{ref}(y_1)}{\pi_\text{ref}(y_2)} + \frac{R(y_1) - R(y_2)}{\beta}
$$

When $R$ differences are small vs $\beta$, small reward gaps exponentially dominate the ratio. Fix (MARA): reward-shape high-quality samples to equalise modes.

**Implication for branch-d:** if CPF is ever RL-fine-tuned (GRPO, PPO, DPO), the RL stage will undo supervised anti-collapse gains unless MARA-style reward shaping is added.
(Source: [[KL-Regularized RL is Designed to Mode Collapse]])

## Proposed Loss Formulations (equation-level)

Drop-in losses for the CODI harness, ordered by expected impact:

### L1 — CODI-KL-clip (F3)
$$
\mathcal{L}_\text{KL-clip} = \sum_{t=1}^T \max\!\left(\lambda_\text{KL},\, \mathrm{KL}(q(KV_t|x) \| r(KV_t))\right)
$$
Requires making the encoder stochastic (Gaussian with learned mean+std). $\lambda_\text{KL} = 0.1$ start.

### L2 — Swap-InfoNCE (F5)
$$
\mathcal{L}_\text{swap-NCE} = -\sum_i \log \frac{\exp(z_i^T W q_i)}{\sum_j \exp(z_j^T W q_i)}
$$
Batch $N \geq 32$; bilinear $W$ is only new parameter; $\lambda=0.1$ weight.

### L3 — VICReg variance hinge (F6)
$$
\mathcal{L}_\text{VIC-var} = \frac{1}{d}\sum_j \max(0,\ \gamma - \mathrm{std}(KV_{\cdot, j}))
$$
γ set to 0.3 × empirical mean-layer-norm std. No stochastic encoder required.

### L4 — Cross-position Barlow Twins (F3, alternative to L1)
$$
\mathcal{L}_\text{pos-BT} = \sum_i (1 - C^{t,t}_{ii})^2 + \lambda_\text{BT} \sum_{t \ne t'} \sum_{i \ne j} (C^{t,t'}_{ij})^2
$$
$\lambda_\text{BT} = 5 \cdot 10^{-3}$. No stochastic encoder; pure post-hoc statistics.

### L5 — CEB-CPF (replaces hand-tuned α)
$$
\mathcal{L}_\text{CEB} = \mathcal{L}_\text{CE}(y) + \|h_\text{ctx} - \mathrm{sg}(e_\text{pred})\|_2^2 + \gamma \cdot \mathrm{KL}[p(z|x)\|\mathrm{sg}(e_\text{pred})]
$$
γ scheduled to approach 1; requires stochastic encoder on the latent.

### Recommended stack for BranchD V3
$$
\mathcal{L}_\text{total} = \mathcal{L}_\text{CE}(y) + \lambda_1 \mathcal{L}_\text{KL-clip} + \lambda_2 \mathcal{L}_\text{swap-NCE} + \lambda_3 \mathcal{L}_\text{VIC-var}
$$
Starts $\lambda_1=1, \lambda_2=0.1, \lambda_3=1$. Needs ablation.

## Key Entities

- [[Alex Alemi]]: VIB lead author (ICLR 2017).
- Ian Fischer: CEB author; co-author on VIB.
- Yann LeCun: co-author on VICReg and Barlow Twins; broader EBM advocacy.
- Shengjia Zhao, Jiaming Song, Stefano Ermon: InfoVAE authors.
- Aaron van den Oord: InfoNCE / CPC author.
- Naftali Tishby (memoriam): IB founder.

## Key Concepts

- [[Variational Information Bottleneck]]: family of IB regularizers; canonical formulation and posterior-collapse failure mode.
- [[Conditional Entropy Bottleneck]]: tighter-bound IB with absolute MNI target; natural CPF formalisation.
- [[Whitening-Based Anti-Collapse]]: Barlow Twins / VICReg family; prior-free, detach-compatible regularizers.
- [[Distribution Regularizer Catalog]]: equation-level menu mapping each regularizer to an F-failure.

## Contradictions

- **InfoVAE vs VIB on how to avoid posterior collapse.** InfoVAE claims VIB's per-example KL $q(z|x) \| p(z)$ *causes* collapse, and proposes replacing with aggregated-posterior MMD. VIB does not acknowledge this (pre-InfoVAE). Resolution: InfoVAE is more credible for the "decoder is too flexible" regime we're in; use MMD or the CALM KL-clip variant, not pure KL.
- **HSIC-IB claim of "no backprop needed" vs modern practice.** HSIC paper claims per-layer optimization beats backprop. Recent work (2023+) has not reproduced this for large transformers; HSIC is more commonly used as an auxiliary end-to-end loss rather than a backprop replacement. Treat the "no backprop" claim with skepticism.
- **InfoNCE tightness.** The original CPC paper claims InfoNCE is a valid MI lower bound. Recent work (f-MICL, 2024) shows it is actually a lower bound on a different divergence, and is rather *loose* on MI. Doesn't change the practical utility for contrastive training, but affects how to interpret the learned "I".

## Open Questions

1. **Is there a Wasserstein / Sinkhorn regularizer specifically for latent CoT?** Searched extensively; no 2024-2025 paper applies optimal transport to latent-CoT rollouts. Gap: a paper proposing Wasserstein-matching of per-step latent distributions to a mixture-prior reference. Could be branch-d V4.
2. **EBM regularization for latent CoT?** Found: one tangential reference (Energy Matching, April 2025) noting EBMs "experience visible mode collapses that slow down sampling." No direct application of EBM regularization to chain-of-thought latents. LeCun's H-JEPA is conceptually adjacent but not explicit CoT. Gap.
3. **CEB empirical γ schedule for LLM reasoning?** CEB paper only benchmarks on image classification. Need to be the first to empirically tune γ for LLM reasoning with backward-encoder = $e_\text{pred}$.
4. **Do whitening regularizers (VICReg, Barlow Twins) transfer to 3584-dim KVs?** Image SSL literature uses 8192-dim projector embeddings; transformer KV is 3584-dim but has very different statistics (layer-normed, long-tailed). Calibration open.
5. **Is MNI reachable on stochastic reasoning datasets?** CEB paper says γ=1 → MNI only on deterministic datasets. GSM8K has stochastic rollout paths; can we still use MNI as a target or do we need a stochastic-MNI variant?
6. **Cross-batch InfoNCE for small batches.** Our training batches may be <32; InfoNCE bound at log(32) = 5 bits may be too weak. Need MoCo-style cross-batch queue.

## Sources

See related frontmatter. Ordered by relevance:

1. [[Deep Variational Information Bottleneck]] — Alemi et al., ICLR 2017 (foundational; potentially stale but framework still canonical)
2. [[Conditional Entropy Bottleneck]] — Fischer, 2020 (medium-stale; theory still current)
3. [[HSIC Bottleneck]] — Ma et al., AAAI 2020 (medium-stale; kernel formulation unchanged)
4. [[VICReg]] — Bardes, Ponce, LeCun, ICLR 2022 (current)
5. [[Barlow Twins]] — Zbontar et al., ICML 2021 (current)
6. [[Contrastive Predictive Coding]] — van den Oord, 2018 (foundational; equations still canonical)
7. [[InfoVAE]] — Zhao, Song, Ermon, AAAI 2019 (current)
8. [[Continuous Autoregressive Language Models]] — Oct 2025 (fresh; most directly applicable)
9. [[KL-Regularized RL is Designed to Mode Collapse]] — Oct 2025 (fresh; negative result we must cite)
10. [[Emergence of Invariance and Disentanglement]] — Achille & Soatto, JMLR 2018 (foundational theory)

## Scope limitations

**Not covered (noted in Open Questions):**
- Wasserstein / Sinkhorn losses for latent CoT — literature gap, flagged for own research.
- EBM regularization for latent CoT — literature gap.
- Cross-reference to our existing [[SeLaR]] (round-2 contrastive-push-away) — SeLaR is training-free inference-time; this synthesis is training-time regularization. The two are complementary and both ship.

**Known stale:** VIB (2017) and CEB (2020) and InfoNCE (2018) are foundational; while the specific 2017-2020 equations still stand, more recent tighter MI bounds exist (f-MICL, CLUB, MINE). Flagged for follow-up autoresearch.
