---
type: source
title: "KL-Regularized Reinforcement Learning is Designed to Mode Collapse"
created: 2026-04-23
updated: 2026-04-23
tags:
  - type/source
  - domain/rl
  - domain/posterior-collapse
  - domain/mode-collapse
status: triaged
source_type: paper
arxiv_id: "2510.20817"
venue: "arXiv"
date_published: 2025-10-23
authors: []
url: "https://arxiv.org/abs/2510.20817"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Under reverse-KL regularized RL, optimal policy is G_β(y) = (1/ζ)·π_ref(y)·exp(R(y)/β); this is inherently multimodal only when R differences are balanced against reference probabilities."
  - "Common intuition 'reverse KL → mode-seeking; forward KL → mass-covering' is wrong; both can collapse depending on β, reward structure, and reference policy."
  - "Key diagnostic: log ratio G_β(y₁)/G_β(y₂) = log(π_ref(y₁)/π_ref(y₂)) + (R(y₁)−R(y₂))/β; when rewards match, RL never up-weights low-support answers."
  - "Proposed fix MARA (Mode Anchored Reward Augmentation): r̄_i = R(z) + β·[log π_ref(z) − log π_ref(y_i)] for high-quality samples; two lines of code."
related:
  - "[[Deep Variational Information Bottleneck]]"
  - "[[CALM]]"
  - "[[Adaptive Latent RL]]"
  - "[[GRPO]]"
sources:
  - "https://arxiv.org/html/2510.20817v1"
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "If any later fine-tuning of CPF uses KL-to-reference (PPO, GRPO, DPO), this paper's finding predicts mode collapse. Directly relevant if CPF is paired with an RL stage."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Foundational negative result on KL-regularized RL + reasoning; must be cited when discussing GRPO-based latent methods (Adaptive Latent RL, CoLaR)."
  - slug: "branch-a"
    relevance: reference
    why: "Not directly Qwen3-scaling, but predicts behaviour of any RL-stage on top of scaled models."
  - slug: "branch-b"
    relevance: reference
    why: "Peripheral to detach ablation."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe work."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# KL-Regularized RL is Designed to Mode Collapse

October 2025 position paper + analysis arguing that mode collapse under KL-regularized RL is an **inherent property of the global optimum**, not merely an optimisation artefact — and that the common intuition about reverse-KL vs forward-KL is wrong.

## Core analysis

**Optimal reverse-KL-regularized policy (standard result):**
$$
G_\beta(y) = \frac{1}{\zeta}\, \pi_\text{ref}(y)\, \exp(R(y) / \beta)
$$

**Log-ratio diagnostic (Prop 4.1):**
$$
\log \frac{G_\beta(y_1)}{G_\beta(y_2)} = \log \frac{\pi_\text{ref}(y_1)}{\pi_\text{ref}(y_2)} + \frac{1}{\beta}[R(y_1) - R(y_2)]
$$

**Two failure modes:**

1. **Equal rewards** ($R(y_1) = R(y_2)$): $G_\beta$ ratio = reference ratio. RL is *incapable* of up-weighting low-support correct answers — whatever shape the reference policy has, the optimum keeps.

2. **Unequal rewards**: exponential blow-up — tiny ΔR amplified by $e^{\Delta R / \beta}$ causes one mode to dominate.

Both cases conspire to produce mode collapse.

## The fix: Mode-Anchored Reward Augmentation (MARA)

For high-quality samples above a threshold $\tau$, replace $R$ with:
$$
\bar{r}_i = R(z) + \beta \cdot [\log \pi_\text{ref}(z) - \log \pi_\text{ref}(y_i)]
$$

where $z$ is the mode anchor (highest-support correct answer). This equalises the effective reward across correct modes relative to their reference probabilities, so the optimum is no longer uniquely peaked on one mode.

Requires two lines of code; works with both reverse and forward KL.

## Relevance to latent-reasoning RL

Adaptive Latent RL ([[Adaptive Latent RL]]), [[GRPO]]-based methods, and any DPO-on-latents method uses KL-to-reference. This paper predicts:
- Latent RL *will* reduce to a single-trajectory attractor at the optimum.
- Increasing β fights collapse but blunts learning.
- The correct fix is reward-shaping, not β-tuning.

For branch-d specifically: if CPF is fine-tuned with RL after its supervised stage, the RL stage can collapse what the supervised stage taught. MARA-style reward shaping would need to be added.

## Connection to the Mode-Elicitation finding

Parallels [[LaDi-RL]]'s "mode elicitation collapse" on latent-diffusion RL. Both papers claim latent RL destroys diversity that supervised training established. Different mechanisms (KL-structure vs denoising collapse), convergent conclusion: RL on latents needs special regularization to stay multimodal.

## Canonical citation form

(authors TBD). (2025). KL-Regularized Reinforcement Learning is Designed to Mode Collapse. arXiv:2510.20817.
