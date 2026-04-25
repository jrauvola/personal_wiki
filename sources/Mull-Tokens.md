---
type: source
title: "Mull-Tokens — Modality-Agnostic Latent Thinking"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/multimodal
  - type/source
  - method/latent-tokens
  - method/curriculum
  - method/rl
status: read
related:
  - "[[HRPO]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Latent Tokens]]"
  - "[[Token Assorted]]"
  - "[[Curriculum Distillation]]"
sources:
  - "[[.raw/papers/2512.10941-mull-tokens]]"
source_type: paper
arxiv_id: "2512.10941"
venue: "arXiv"
date_published: 2025-12-11
authors:
  - "Arijit Ray"
  - "Ahmed Abdelkader"
  - "Chengzhi Mao"
  - "Bryan A. Plummer"
  - "Kate Saenko"
  - "Ranjay Krishna"
  - "Leonidas Guibas"
  - "Wen-Sheng Chu"
url: "https://arxiv.org/abs/2512.10941"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Modality-agnostic latent tokens pre-trained to hold intermediate information in either image or text modalities can improve visual reasoning without task-specific reasoning data."
  - "A three-stage curriculum — supervised warm-up on interleaved text-image traces, relaxed final-answer-only SFT, GRPO RL refinement — is the recipe for training modality-agnostic Mull-Tokens."
  - "Mull-Tokens achieve +3% average accuracy gain over strongest baseline (direct-answer SFT) across four spatial benchmarks; up to +16% on a visual-puzzle reasoning-heavy split."
  - "Mull-Tokens improve +4% over the latest prior approach of interleaving visual thoughts with text (explicit modality switching)."
  - "Only 10-40 Mull-Tokens suffice; multimodal warm-up data is NECESSARY — latent tokens with text-only data or extra compute without multimodal anchoring does not suffice."
  - "Naively supervising a model to interleave textual thoughts and visual latents can HURT performance compared to text-only reasoning on visual puzzle solving."
projects:
  - slug: "branch-d"
    relevance: secondary
    why: "Three-stage curriculum (supervised warmup → relaxed SFT → RL refinement) is structurally close to LT-Tuning's three-stage recipe, and Stage-1 supervision via frozen encoder vectors (image) or LM-head prediction (text) is a modality-aware analog of CPF's vocabulary-anchoring. Validates the curriculum family in a new domain (multimodal); not a direct CPF implementation."
  - slug: "branch-a"
    relevance: reference
    why: "Qwen2.5-VL 7B experiments; no architecture-scaling signal at 8B+ for text-only latent reasoning."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach/fp32/BPTT stability discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe-methodology."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Evidence that the latent-reasoning recipe (learned latent tokens + curriculum + RL refinement) transfers beyond text — supports writeup's claim that synthesis target is a general mechanism, not text-specific. Uses GRPO, same tooling lineage as HRPO and Adaptive Latent RL."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Mull-Tokens

Ray, Abdelkader, Mao, Plummer, Saenko, Krishna, Guibas, Chu (Google / UW / Stanford / Boston Univ), [arXiv:2512.10941](https://arxiv.org/abs/2512.10941), Dec 2025. Project page: [arijitray.com/multimodal_thinking](https://arijitray.com/multimodal_thinking/).

## TL;DR

Augments a VLM (Qwen2.5-VL 7B) vocabulary with K=10-40 modality-agnostic learned latent tokens `<Mull>_k`, trained with a three-stage curriculum: (1) warm-up with interleaved text-image supervision where each `<Mull>` token is supervised toward either an LM-head text target (cross-entropy) or a frozen image-encoder vector (cosine loss); (2) relaxed SFT with only final-answer loss; (3) GRPO RL refinement. +3% avg over direct-answer SFT on four spatial benchmarks; +16% on puzzle split; +4% over prior interleaved-text-image methods.

## Method

### Architecture

- Base: Qwen2.5-VL 7B (text decoder + frozen image encoder `g_φ`).
- Vocab expansion: K learned tokens `z_{1:K} = (<Mull>_1, ..., <Mull>_K)`.
- Training sequence at inference: `(question, z_{1:K}, answer)` — latent tokens are internal compute.

### Stage 1 — Warm-up (supervised)

Given CoT trace `c_{1:T}` where each `c_t ∈ V_txt ∪ V_img`:

- Build interleaved sequence `s = (q, z_1, c̃_1, ..., z_T, c̃_T, y)` where `c̃_t` is text step or image placeholder.
- For each `<Mull>`-position hidden state `h^Mull_t`:
  - If next step is text: `L_text = -log p_θ(c_t | s_<t)` through LM head.
  - If next step is image `I_t`: `L_img = 1 - cos(ĥ^Mull_t, ĝ_φ(I_t))`.
- Total: `L_1 = L_AR + λ_text · ΣL_text + λ_img · ΣL_img`.

### Stage 2 — Relaxed training (final-answer only)

- Sequence: `(q, z_{1:K}, y)` — drop intermediate CoT.
- Loss: standard autoregressive cross-entropy on `y` only.
- Latent tokens un-supervised; model freely optimizes latent chain.

### Stage 3 — RL refinement

- GRPO with reward on final answer correctness.
- Rewards causal usefulness of latent chain.

## Recipe

1. Pick any VLM with text decoder + frozen image encoder.
2. Add K=10-40 `<Mull>` tokens to vocab.
3. Stage 1: SFT on multimodal CoT dataset with dual (text / image-encoder) supervision.
4. Stage 2: SFT on `(q, <Mull>×K, answer)` only.
5. Stage 3: GRPO with answer-correctness reward.

## Results

| Benchmark | Gain over strongest baseline |
|---|---|
| BLINK (visual puzzles / IQ) | +16% on puzzle-heavy split |
| VSI-Bench (video spatial) | gains reported |
| SAT (action/motion spatial) | gains reported |
| ERQA (robotics trajectories) | gains reported |
| **Average** | **+3% absolute over direct-answer SFT** |
| vs interleaved text-image prior | +4% |

Ablation highlights:

- **Multimodal warm-up data is necessary.** Text-only warm-up or "extra compute without multimodal anchoring" fails.
- Surprisingly, direct-answer SFT is the STRONGEST baseline — intermediate text reasoning HURTS on visual puzzles. Mull-Tokens beat even this strong baseline.
- Naively interleaving textual thoughts with visual latents (prior art) can HURT relative to text-only reasoning.

## Relation to CPF / HRPO / LT-Tuning

- Three-stage curriculum (warmup → relaxed SFT → RL) mirrors LT-Tuning's three-stage structure and HRPO's progressive gate curriculum.
- Stage-1 dual supervision (LM-head for text, frozen encoder for image) is a *modality-aware anchoring* — structurally analogous to CPF's `e_pred` (probability-weighted vocab embedding anchor). Here the anchor is a concrete target vector (text token or image encoder output), not a soft mixture.
- Stage 3 uses GRPO, same tooling lineage as HRPO and [[Adaptive Latent RL]].
- First validation of the "learned latent tokens + curriculum + RL refinement" recipe in the multimodal domain.

## Relevance

**Secondary for branch-d.** The curriculum structure validates a family that includes CPF, not CPF itself. If branch-d works on CODI, a Mull-Tokens-style VLM follow-up is a natural scaling axis. **Secondary for spar-latent-reasoning** — evidence that the latent-reasoning recipe transfers beyond text strengthens the writeup's claim that the synthesis target is a general mechanism.

## Citation links to chase

- [[HRPO]] — same RL refinement philosophy (GRPO).
- [[Latent Tokens]] (Sun et al.) — token-level latent optimization precursor.
- [[COCONUT]] — single latent-token lineage.
- Latent reasoning refs 22/49/68/69 in paper — explicit inspiration; verify what's beyond HRPO/COCONUT/LT-Tuning lineage we already have.
