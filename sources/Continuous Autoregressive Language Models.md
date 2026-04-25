---
type: source
title: "Continuous Autoregressive Language Models (CALM)"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/latent-reasoning
  - domain/continuous-autoregressive
  - domain/posterior-collapse
status: triaged
source_type: paper
arxiv_id: "2510.27688"
venue: "arXiv"
date_published: 2025-10-30
authors: []
url: "https://arxiv.org/abs/2510.27688"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Continuous Autoregressive LM (CALM) observed severe posterior collapse: 71 of 128 latent dimensions collapsed to the standard normal prior without remediation."
  - "Fix: KL clipping L_KL^clip = Σ_i max(λ_KL, L_{KL,i}) with λ_KL = 0.5 — per-dimension minimum KL floor forces every dim to participate in reconstruction."
  - "Additional robustness: dropout p=0.15 on latent vectors and input tokens during autoencoder training encourages redundancy."
  - "With clipping + dropout, latent stds σ_i ≈ 0.3 and token-level accuracy > 99.9% even under substantial perturbation."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[InfoVAE]]"
  - "[[Feature Collapse]]"
  - "[[Routing vs Reasoning]]"
  - "[[CODI]]"
sources:
  - "https://arxiv.org/html/2510.27688v1"
projects:
  - slug: "branch-d"
    relevance: primary
    why: "CALM's core finding — 71/128 dimensional collapse, fixed by per-dim KL clipping — is the *direct* analogue of our F3 (7/8 positional collapse). KL-clip is a plug-in add-on to any latent-reasoning VIB loss. Confirms our diagnosis and provides an off-the-shelf fix."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "2025 paper providing concrete per-dimension anti-collapse engineering recipe; essential citation for the writeup."
  - slug: "branch-b"
    relevance: secondary
    why: "Dropout-based redundancy regularisation is compatible with detach; CALM's 99.9% accuracy under perturbation is a target benchmark for F6 robustness."
  - slug: "branch-a"
    relevance: secondary
    why: "Continuous-autoregressive framing relates to how our CODI KV sequence is effectively a continuous LM — architectural class match."
  - slug: "branch-c"
    relevance: reference
    why: "Per-dimension collapse probe is a useful additional F-battery check."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Continuous Autoregressive Language Models (CALM)

October 2025 paper introducing a continuous-autoregressive LM. The methodologically important contribution for us is the **per-dimension posterior-collapse finding and remedy**: 71 of 128 latent dims collapse to the prior unless clipped.

## The finding

Without remediation: **71 of 128 latent dimensions collapse to the standard-normal prior.** Dimensions with zero KL divergence achieve the shortest path in loss space — minimal reconstruction penalty relative to clustering information into a minimal-sufficient set.

Consequence: collapsed dimensions become pure Gaussian noise, destabilising downstream LM training.

## The fix: KL clipping

**Clipped KL loss:**
$$
\mathcal{L}_\text{KL}^\text{clip} = \sum_{i=1}^\ell \max(\lambda_\text{KL}, \mathcal{L}_{\text{KL},i})
$$

with $\lambda_\text{KL} = 0.5$ enforcing a per-dimension KL floor. Forces every dimension to carry at least $\lambda_\text{KL}$ nats of info.

Complemented by:
- Dropout on latent vectors: $p = 0.15$
- Dropout on input tokens: $p = 0.15$

Result: per-dim stds $\sigma_i \approx 0.3$, token-level accuracy > 99.9% even under substantial perturbation.

## Direct structural analogue to CODI F3

**Our F3 (from F1-F6 battery):** 7 of 8 latent *positions* collapse to entropy <0.4 bits — nearly zero information.

**CALM's finding:** 71 of 128 latent *dimensions* collapse to KL ≈ 0.

Different axis (position vs dimension), same pathology: the trivial "match the prior" solution dominates because the decoder doesn't rely on that slot.

**Proposed CODI-KL-clip** (adapted to our positional collapse):
$$
\mathcal{L}_\text{CODI-KLclip} = \mathcal{L}_\text{CE}(y) + \sum_{t=1}^{T} \max\!\left(\lambda_\text{KL},\ \mathrm{KL}(q(KV_t | x) \,\|\, r(KV_t))\right)
$$

applied **per latent position** $t$. This prevents any position from fully collapsing to the prior.

## Open question about CALM that we'd want to know

CALM's fix works on a non-reasoning continuous LM (token-level reconstruction). Does the per-dim KL-clip solution transfer to reasoning setups where the signal is much weaker than token reconstruction? CODI's loss is next-token cross-entropy, not full-sequence reconstruction — the gradient on the latent from the Y-head is far sparser than CALM's reconstruction loss, so the KL-clip floor may need to be tuned lower.

## Canonical citation form

(authors TBD). (2025). Continuous Autoregressive Language Models. arXiv:2510.27688v1.
