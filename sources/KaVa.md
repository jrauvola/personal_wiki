---
type: source
title: "KaVa — Latent Reasoning via Compressed KV-Cache Distillation"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/distillation
  - domain/architecture
  - source/paper
status: read
source_type: paper
arxiv_id: "2510.02312"
venue: "arXiv (preprint); ICLR 2026"
date_published: 2025-10-02
authors:
  - "Anna Kuzina"
  - "Maciej Pioro"
  - "Paul N. Whatmough"
  - "Babak Ehteshami Bejnordi"
url: "https://arxiv.org/abs/2510.02312"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "KaVa is the first framework that bridges [the latent-reasoning supervision gap] by distilling knowledge directly from a compressed KV-cache of the teacher into a latent-reasoning student via self-distillation, leveraging the representational flexibility of continuous latent tokens to align stepwise KV trajectories."
  - "The abstract, unstructured knowledge within compressed KV-cache, which lacks direct token correspondence, can serve as a rich supervisory signal for a latent reasoning student."
  - "R-KV eviction using a combined importance+redundancy score S_{i,h,l} = λ·I_{i,h,l} + (1−λ)·R_{i,h,l} with λ=0.1 outperforms attention-only, cosine-only, and right-crop baselines for compressing an N_C-length teacher cache down to M entries."
  - "KaVa exhibits markedly smaller degradation from equation-only to natural-language traces: 56.5 → 55.7 on Llama-3.2-1B GSM8k-AUG vs GSM8k-AUG-NL (GSM8k-Hard), where CODI drops substantially more under the same shift."
  - "Parallel decoding via T=3 Jacobi iterations over M=24 latent tokens (PCCoT) reduces the backward-pass chain from O(M) to O(T), yielding ~6.9 forward passes per question on Llama-3.2-1b vs ~65 for full CoT (≈89% reduction)."
  - "KaVa scales to Llama-3.2-3B (65.7 on GSM8k-AUG, beating CODI by ~4.7 points); Gemma-3 family and 4B+ scales are untested."
related:
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[SIM-CoT]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[KV-Cache Distillation]]"
  - "[[Self-Distillation]]"
  - "[[PCCoT]]"
  - "[[R-KV Eviction]]"
sources:
  - "[[.raw/papers/2510.02312-kava]]"
  - "[[.raw/papers/kava_notes]]"
projects:
  - slug: "branch-a"
    relevance: reference
    why: "KaVa doesn't touch Qwen3 scaling; no bearing on the architecture-dependent Gemma-finding writeup."
  - slug: "branch-b"
    relevance: secondary
    why: "Parallel Jacobi decoding (T=3) shortens the backward chain to ~102 ops vs 136 for sequential CODI on 34-layer models — directly relevant to detach/bf16 stability diagnostics; KaVa's no-detach, full-BPTT-through-T=3 setup is a natural control."
  - slug: "branch-c"
    relevance: not-applicable
    why: "No probe methodology or Qwen3 debugging content."
  - slug: "branch-d"
    relevance: primary
    why: "KaVa is a direct alternative fusion/anti-collapse recipe: per-step KV targets close the same supervision gap LT-Tuning's CPF attacks; porting KaVa to Gemma-3/CODI at 4B would be a novel contribution explicitly outside KaVa's tested range."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Core taxonomic member of the latent-CoT distillation literature; interpretability protocol (lm_head decoding of latents, KV cosine-similarity diagonals) is directly reusable for SPAR writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# KaVa — Latent Reasoning via Compressed KV-Cache Distillation

**arXiv:** [2510.02312v1](https://arxiv.org/abs/2510.02312) (Oct 2, 2025) · **Venue:** arXiv preprint; ICLR 2026
**Authors:** Anna Kuzina, Maciej Pioro, Paul Whatmough, Babak Ehteshami Bejnordi (Qualcomm AI Research; IDEAS NCBR / IPPT PAN)
**Code/weights:** no public GitHub repo or HF weights as of late March 2026.

## Core Contribution

KaVa is the first method to **distill knowledge directly from a compressed teacher KV-cache into a latent-reasoning student via self-distillation**. It closes the supervision gap that plagues [[CODI]] and [[COCONUT]]: in those methods, latent tokens receive no per-step target and are supervised only via the final answer token. KaVa constructs a rich, per-step internal target by compressing the teacher's full CoT KV-cache down to `M` entries — matching the student's latent budget — and matching the student's latent K/V trajectories to it.

Framing from the survey: traditional explicit CoT suffers from massive KV-cache accumulation that blocks deployment to memory-constrained / edge settings, while early intrinsic latent methods trained on rigid math templates degrade severely on verbose natural-language traces. KaVa's headline finding is that even after aggressive layer-wise and head-wise eviction destroys discrete token correspondence, the surviving dense KV representations retain a structured "cognitive fingerprint" that a continuous student can internalize.

## Architecture (3 components)

1. **Backbone.** A single shared model alternates between:
   - **Teacher mode:** consumes the full `<Q, CoT>` and builds a per-layer, per-head KV cache $K_t, V_t \in \mathbb{R}^{N_C \times H \times L \times d}$.
   - **Student mode:** generates `M` continuous latent tokens via `<bot> z₁ ... z_M <eot>`.
2. **Compression module (R-KV eviction).** Prunes the length-`N_C` teacher cache down to `M` entries using a combined **importance + redundancy** score per (token, head, layer):
   - *Importance* `I`: attention scores from answer tokens back to CoT keys — reuses the teacher's forward-pass attention (free).
   - *Redundancy* `R`: negative pairwise cosine similarity among keys — diverse keys preferred.
   - Score: $S_{i,h,l} = \lambda \cdot I_{i,h,l} + (1-\lambda) \cdot R_{i,h,l}$ with **λ=0.1**.
3. **KV-matching loss.** Aligns student K/V to compressed teacher K/V per layer / step:

   $L_{KV} = \frac{1}{2M} \bigl(\lVert \mathrm{sg}[\tilde{K}_t] - K_s \rVert_p + \lVert \mathrm{sg}[\tilde{V}_t] - V_s \rVert_p\bigr)$

   `p=1` (L1 / Smooth L1) works best for most settings; `p=2` (MSE) is sometimes better at larger scale. `sg[·]` is stop-gradient on the teacher.

## Training Objective

$L_{KaVa} = \mathrm{CE}_{\text{student}}(A \mid Z, Q) + \mathrm{CE}_{\text{teacher}}(A, C \mid Q) + \alpha_1 \cdot L_{\text{CODI}} + \alpha_2 \cdot L_{KV}$

- **Student CE:** predict answer from question + latent.
- **Teacher CE:** predict answer + CoT from question (keeps teacher LM head sharp).
- **L_CODI** (Shen et al.): aligns the hidden state of the last pre-answer token between teacher and student (1 token only).
- **L_KV:** the new term — aligns the full K/V trajectory.

Llama-1B reference config: `α₁=10`, `α₂=1`, `λ=0.1`, L1 loss, layer-wise std normalization.

## Key Structural Choice — Parallel Decoding via Jacobi Iteration (PCCoT)

**This is what lets KaVa avoid the bf16 / long-backward-chain pathology.**

Rather than generating latent tokens one-at-a-time (CODI-style), KaVa uses [[PCCoT]] (Wu et al. 2025): all `M` latent tokens are updated in parallel over `T` Jacobi iterations. Best config: **M=24, T=3**.

- Sequential CODI unroll: `M` passes through the network (e.g., 24).
- PCCoT/KaVa: `T` passes (e.g., 3).

Backward chain length comparison on a 34-layer backbone (e.g., Gemma-3-4B):
- CODI with M=4: 4 × 34 = 136 ops → overflows bf16.
- KaVa/PCCoT with T=3: ~3 × 34 = 102 ops (plus teacher pass) — shorter than even `M=6` sequential CODI.

The paper reports no bf16 stability issues because the parallel decoding inherently shortens the backward chain.

## Gradient Flow

- **Stop-gradient on teacher** throughout (both hidden states in `L_CODI` and K/V in `L_KV`).
- **No explicit detach between Jacobi iterations.** Quote: "we first generate the whole student sequence with Jacobi iterations and then perform the distillation."
- Full BPTT through the `T=3` iterations.

## Key Results (Llama-3.2-1B-Instruct)

| Method | GSM8k-AUG (eq only) | GSM8k-AUG-NL (natural lang) |
|--------|---------------------:|-----------------------------:|
| Full CoT (upper bound) | 61.6 | 53.2 |
| No-CoT (lower bound)   | 30.9 | 33.1 |
| iCoT                   | 19.0 | 15.2 |
| COCONUT                | 45.3 | 27.2 |
| CODI                   | 55.6 | 49.7 |
| PCCoT                  | 53.4 | 50.7 |
| **KaVa**               | **56.5** | **55.7** |

**Headline finding.** KaVa barely degrades from equation-only (56.5) to natural language (55.7); CODI drops 20+ points on Qwen-0.5B moving to natural language. KV distillation absorbs abstract, non-token-aligned structure.

Scales to Llama-3.2-3B: **65.7 on GSM8k-AUG**, beating CODI by ~5 points. **3B is the largest backbone tested** — no Gemma-3 or 4B+ experiments.

## Efficiency

KaVa uses only 3 Jacobi iterations → **~6.9 forward passes per question on Llama-1B vs ~65 for Full CoT (≈90% reduction)**. The survey summarizes the broader compute envelope as a **62% – 92% forward-pass reduction** vs full textual CoT.

## Ablations

| Ablation | Result |
|----------|--------|
| Drop last step of teacher trace | Critical (CODI already knew this) |
| KV loss type | L1 > MSE on small models; MSE sometimes better at larger scale |
| R-KV λ | 0.1 optimal (both importance AND redundancy needed) |
| Eviction method | R-KV > cosine-only > attention-only > right-crop |
| # latent tokens `M` | 24 best on Llama-1B |
| # Jacobi iterations `T` | 3 > {0, 1} (non-trivial iterations matter); too many hurts at M=24 |
| Projection layer | Helps (drops to 52.2 without) |
| L_CODI loss | Helps (drops to 52.8 without) |

## Interpretability (Section 5 — directly reusable protocol)

They decode latent tokens via `lm_head` directly:

- On [[GSM8k-AUG]] (equation-only): decoded latents often match the teacher trace token-by-token, e.g. `<<650*2=1300>>`.
- On [[GSM8k-AUG-NL]] (natural language): decoded latents lose token-level correspondence (compressed cache mixes tokens), but answers remain correct.
- KV cosine similarity between student and compressed teacher shows a clean diagonal pattern (Figure 7).

This is a **ready-made interpretability protocol** (lm_head decoding + KV cosine diagonals) applicable to our models.

## Hyperparameters (Llama-1B reference)

- LoRA: r=128, α=32, dropout=0.1
- Optimizer: AdamW, LR = 8e-4, cosine schedule
- Batch size 128, 10 epochs
- Gradient clip = 2
- M=24 latent tokens, T=3 Jacobi iterations
- α₁=10 (CODI), α₂=1 (KV)

## Relevance to Our Work

**What KaVa teaches us**

1. **Parallel decoding sidesteps the long-chain problem.** If we use T=3 Jacobi iterations instead of M=24 sequential unrolls, explicit detach may be unnecessary — a natural control for [[branch-b]]'s detach ablation.
2. **The real supervision gap is solvable with KV distillation.** The concern that "CODI behaves like a classifier" may stem from latent tokens having no per-step target. KaVa provides one.
3. **R-KV compression is the load-bearing engineering piece** — needs clean implementation.
4. **Works up to 3B; Gemma-3-4B is uncharted.** Porting KaVa to Gemma-3 at 4B would be a real contribution.

**What KaVa does NOT address**

1. Never tests on Gemma-3 (our setup).
2. Never tests >3B.
3. No precision / stability discussion (presumably bf16, but no failure modes reported at the tested scales).
4. Does not interpret latent reasoning dynamics mechanistically — only shows token-level decoding and KV similarity.

## Survey-level Assessment

From the [[papers/research|research survey]]: KaVa is a "profound leap forward in the science of representation learning and knowledge distillation" but **not an optimal near-term integration target** for the local evaluation harness. It is engineering-heavy (bespoke head-wise eviction modules and parallel Jacobi decoders), no public code or weights exist as of late March 2026, and should be monitored for future open-source releases but deferred in favor of more readily available paradigms.
