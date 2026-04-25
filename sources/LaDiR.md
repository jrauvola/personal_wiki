---
type: source
title: "LaDiR: Latent Diffusion Enhances LLMs for Text Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/diffusion
  - type/source
  - method/latent-diffusion
status: read
related:
  - "[[Ouro]]"
  - "[[COCONUT]]"
  - "[[Haoqiang Kang]]"
sources:
  - "[[.raw/papers/2510.04573-ladir]]"

source_type: paper
arxiv_id: "2510.04573"
venue: "arXiv"
date_published: 2025-10-06
authors:
  - "Haoqiang Kang"
  - "Yizhe Zhang"
  - "Nikki Lijing Kuang"
  - "Nicklas Majamaki"
  - "Navdeep Jaitly"
  - "Yi-An Ma"
  - "Lianhui Qin"
url: "https://arxiv.org/abs/2510.04573"
code_repo: null
has_weights: false
status: read
confidence: medium
key_claims:
  - "A VAE-structured latent-thought space plus a blockwise bidirectional latent-diffusion denoiser enables iterative refinement of reasoning; block-level diffusion preserves autoregressive cross-block causality."
  - "On 7 math benchmarks with LLaMA-3.1-8B backbone, LaDiR beats Coconut and matches/exceeds AR CoT SFT where Coconut fails to surpass AR CoT."
  - "On Countdown planning (CD-4), LaDiR improves Pass@1 by >25 pts over LLaMA-8B SFT and Pass@100 with highest diversity; CD-5 yields ~30 pt Pass@1 gain."
  - "Test-time compute scaling: going from 5→10 denoising steps yields +11.7 avg on 7 math benchmarks; 5→50 steps yields +9.8 total."
  - "Stage-2 rollout training (with flow-matching loss retained, no curriculum) mitigates error accumulation and the latent-collapse failure mode of Coconut."
  - "Interpretability: denoising refines semantic reasoning (green anchors, pink refined expressions) over raw lexical content; VAE-structured latents are interpretable through decoder."

projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "No bearing on Qwen3 architecture-dependent finding."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Diffusion is orthogonal to detach/fp32 backward-chain concerns."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to Qwen3 convergence debugging."
  - slug: "branch-d"
    relevance: reference
    why: "Different paradigm (latent diffusion over VAE blocks) from CODI/LT-Tuning sequence-growing latents; Stage-2 rollout 'no-curriculum but keep flow-matching' is a tangential design choice to LT-Tuning's 3-stage curriculum — not directly portable."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "An alternate post-training latent-reasoning paradigm (diffusion-based) worth tracking for the SPAR writeup's taxonomy; 8B LLaMA backbone means implementable at our scale if we later needed a diffusion-style baseline, but it's not in our current experimental scope."

last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# LaDiR: Latent Diffusion Enhances LLMs for Text Reasoning

**Affiliations (from Apple-sponsored acknowledgment):** authors from academic labs; project sponsored by Apple, NSF (TILOS), DARPA AIE.

## TL;DR

Encode each reasoning-step sentence into a fixed-size block of latent thought tokens via a β-VAE; run a **latent-diffusion flow-matching** model over these blocks with **blockwise bidirectional attention** (causal across blocks, bidirectional within); generate the final answer autoregressively conditioned on denoised latents. Two-stage training (teacher-forcing → rollout). Outperforms Coconut and AR CoT SFT on math + Countdown planning.

## Method

### Architecture (3 components)

1. **Blockization** — split CoT on "The answer is" then per-sentence; each sentence → block of L_b latent tokens.
2. **β-VAE (β=1e-5):** encoder = fine-tuned LLM + L_b learnable embeddings + two linear heads for (μ, σ); decoder = frozen pretrained LLM. Sample Z^(b) ~ N(μ, σ).
3. **Reasoning model (LLM backbone):** insert `<BOT> Z^(b) <EOT>` blocks + timestep embedding for the block being predicted; special binary head predicts next block is `<BOT>` (continue) or `<SOA>` (stop + answer). Hybrid mask: within-block **bidirectional**, across-block **causal**.

### Training loss

Flow-matching loss on latent blocks + CE on answer tokens + CE on `<SOA>`/`<BOT>` special tokens:

$\mathcal{L} = \lambda_{FM} \cdot \mathcal{L}_{FM} + \lambda_{Ans} \cdot \mathcal{L}_{Ans} + \lambda_{Spec} \cdot \mathcal{L}_{Spec}$ (λ = 5, 1, 2)

**VAE augmentations:** Gaussian noise σ·k (k=3) on latents; token substitution (p=0.3) at encoder input.

### Training stages

- **Stage 1 (teacher forcing):** condition on oracle latents Z^(1:B) from VAE encoder.
- **Stage 2 (rollout):** same B as GT, generate own latents from noise with fewer steps (50→10, FlowGRPO-style). Keep gradients through denoising trajectory so answer supervision flows into latent predictions. Retain flow-matching loss (not curriculum-dropped like Coconut).

### Inference

- Block-by-block: init Gaussian noise → flow-match integrate backward (t=1→0) → produces Z^(b).
- Stopping: model predicts `<SOA>` signal.
- Answer: autoregressive decoding conditioned on all Z^(≤B̂).
- **Diversity boosters:** increased initial noise variance; repulsion gradient (KSD-style) pushes batch latents apart, decayed as γ_t = γ_max · (t/T).

## Training recipe — math

- **Backbone:** LLaMA-3.1-8B.
- **Data:** DART-MATH (train only).
- 6 latent tokens per block.
- β=1e-5; decoder frozen; encoder fine-tuned.
- Inference: init noise σ̃=2, γ_max=0.8.

## Results

### Math (pass@1 avg across 7 benchmarks: MATH, GSM8K, College-Math, DM-Math, OlympiadBench-Math, TheoremQA, Fresh-Gaokao-Math-2023)

- LaDiR > all prior latent reasoning methods (including Coconut by 2% avg pass@1).
- LaDiR ≥ AR CoT SFT, especially on DM-Math and College-level where AR struggles with long-horizon consistency.
- Stage-2 training adds consistent improvements across all 7.

### Countdown planning

| Setting | LLaMA-8B SFT Pass@1 | LaDiR Pass@1 | Δ |
|---|---|---|---|
| CD-4 | baseline | +25 pts | |
| CD-5 | baseline | +30 pts | |

- Highest diversity among all baselines (>2 pts over MGDM).
- Pass@k curve rises steeply — surpasses MGDM at large k.

### Test-time compute scaling

- 5 → 10 denoising steps: +11.7 avg on 7 math benchmarks.
- 10 → 30: additional +4.8.
- 10 → 50: total +9.8.
- Motivates adaptive denoising policies.

### Ablations

- Flow-matching (u) beats ε / x_0 / v / MSE.
- Block size ~6 tokens optimal; <1 harms reconstruction, >6 introduces redundancy.
- Diversity: γ_max ∈ [0.3, 0.5] optimal; γ_max ≥ 1.0 kills accuracy.

## Relevance

- **Different paradigm from CODI/COCONUT/LT-Tuning:** generates latents via **diffusion** over VAE-compressed sentence blocks, not via autoregressive latent emission.
- **Block-level latent structure** is a plausible middle ground between per-token latents (CODI) and full sequence-growing CoT.
- **Stage-2 'rollout with flow-matching preserved'** is LaDiR's anti-collapse trick — conceptually parallels SIM-CoT's auxiliary decoder and LT-Tuning's CPF as anti-collapse mechanisms; the underlying commonality is *keep a supervision signal tied to the latent distribution during end-to-end rollout*.
- Countdown planning gains are particularly striking — looped/diffusion methods seem to do genuinely better than AR on combinatorial planning.

## Cross-links

- [[Ouro]] — contrast: LaDiR is post-training latent reasoning on existing 8B, Ouro is from-scratch 7.7T-token looped pretraining.
- [[COCONUT]] — LaDiR directly benchmarks against and beats it.
- [[CODI]] / [[Latent Thoughts Tuning]] — alternative post-training latent-reasoning paradigms.
