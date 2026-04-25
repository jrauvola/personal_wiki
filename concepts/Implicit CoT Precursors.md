---
type: concept
title: "Implicit CoT Precursors"
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Pre-COCONUT implicit reasoning"
  - "iCoT lineage"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - family/implicit-cot
  - type/concept
  - status/historical
status: mature
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "The 2022-2024 pre-COCONUT implicit-CoT literature is the genealogical root of every 2024-2026 training block we evaluate. Concept hub required for the writeup's 'how we got here' chapter."
  - slug: "branch-b"
    relevance: reference
    why: "Context for the curriculum/distillation design space from which CODI's single-stage self-distillation emerged."
  - slug: "branch-d"
    relevance: primary
    why: "CPF / LT-Tuning descends directly from Deng 2023's hidden-state distillation. Essential frame for what CPF specifically adds."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling history: precursors are all ≤7B; COCONUT GPT-2-only; CODI GPT-2/Llama-1B. Framing for the Qwen3 scaling push."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Probe methodology adjacent only."
last_reviewed: 2026-04-22
reviewed_by: autoreview
related:
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[Pause Tokens]]"
  - "[[Filler Tokens]]"
  - "[[Quiet-STaR]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
sources:
  - "[[Implicit CoT via Knowledge Distillation]]"
  - "[[Stepwise Internalization]]"
  - "[[Pause Tokens]]"
  - "[[Filler Tokens]]"
  - "[[Quiet-STaR]]"
---

# Implicit CoT Precursors

The 2022-2024 pre-COCONUT literature on reasoning **without emitting text tokens**. This concept page indexes the precursor methods that collectively set up the COCONUT/CODI paradigm and identifies which design decision of the modern field each one bequeathed.

## The four design axes that precursors populate

Any latent-reasoning method is the cross-product of four choices. Each precursor locked in one or two axes before COCONUT.

| Axis | Options (pre-COCONUT) | Locked in by |
|------|----------------------|-------------|
| **Where does the reasoning live?** | (a) hidden states across layers; (b) extra token positions; (c) both | Deng 2023 — hidden-states; Goyal 2023 — extra tokens; Zelikman 2024 — both |
| **How is the reasoner trained?** | (α) distillation from explicit CoT teacher; (β) pretraining with rationales; (γ) curriculum-based removal | Deng 2023 — α; Zelikman 2024 — β; Deng 2024 — γ |
| **Are continuous thoughts fed back as inputs?** | (i) no — pre-COCONUT answer is uniformly NO; (ii) yes — COCONUT's innovation | — (all precursors answer "no") |
| **Is the computation gated?** | (A) fixed T/M steps; (B) ACT/PonderNet halting | All precursors fixed T |

COCONUT's single innovation (Dec 2024) was turning axis 3 from "no" to "yes" — the hidden-state is fed back as the next input embedding. Everything else was already in the precursor literature.

## The five precursor papers

### 1. Pause Tokens (Goyal et al. 2023)

- **Paper:** [[Pause Tokens]] — arXiv:2310.02226, ICLR 2024.
- **Mechanism:** Append $M=10$ learnable `<pause>` tokens before extracting output; mask loss on pause positions.
- **Training:** Pause-**pretraining** + pause-finetuning; pretraining is load-bearing, FT alone doesn't work.
- **Scale:** Decoder-only 1B on C4. +18% SQuAD EM, +8% CommonsenseQA, +1% GSM8K.
- **Locks in:** special-token delimiters at LLM scale. Direct ancestor of COCONUT's `<bot>`/`<eot>`.

### 2. Implicit CoT via Knowledge Distillation (Deng, Prasad, Fernandez, Smolensky, Chaudhary, Shieber 2023)

- **Paper:** [[Implicit CoT via Knowledge Distillation]] — arXiv:2311.01460.
- **Mechanism:** Teacher (explicit CoT) → Emulator (predicts teacher hidden states at CoT positions from prompt alone) → Student (uses emulator's hidden states as phantom scratch-pad, emits answer directly).
- **Training:** MSE/distillation on hidden states at CoT positions; no token emission.
- **Scale:** GPT-2 Small on 4×4 multiplication. ~90% accuracy at no-CoT inference speed.
- **Locks in:** "vertical reasoning" — compress CoT into hidden states across layers, not into tokens across a sequence. Direct ancestor of CODI, LT-Tuning, KaVa, SIM-CoT.

### 3. Quiet-STaR (Zelikman et al. 2024)

- **Paper:** [[Quiet-STaR]] — arXiv:2403.09629, COLM 2024.
- **Mechanism:** Generate discrete rationale between learnable `<start-thought>` / `<end-thought>` tokens at **every** token position during pretraining; mix rationale-informed next-token prediction with base prediction via learnable mixing head.
- **Training:** REINFORCE — rationale is rewarded when its presence raises ground-truth next-token likelihood.
- **Scale:** Mistral-7B. Zero-shot GSM8K 5.9% → 10.9%.
- **Locks in:** thought-delimiter special tokens; per-token (not per-question) latent thinking; implicit thought during pretraining.

### 4. Filler Tokens / Let's Think Dot by Dot (Pfau, Merrill, Bowman 2024)

- **Paper:** [[Filler Tokens]] — arXiv:2404.15758, COLM 2024.
- **Mechanism:** Replace CoT tokens with fixed meaningless fillers (e.g., `'.......'`).
- **Training:** Requires dense per-step supervision; sparse task-reward fails.
- **Scale:** Small transformers on 3SUM variant + quantifier-nested boolean tasks.
- **Locks in:** theoretical justification — extra token positions = extra TC^0 parallel slots → strictly larger complexity class. Warning: sparse supervision doesn't teach filler-token usage (predicts later "weak supervision fails" literature).

### 5. Stepwise Internalization (Deng, Choi, Shieber 2024)

- **Paper:** [[Stepwise Internalization]] — arXiv:2405.14838.
- **Mechanism:** Single model, no teacher/emulator. Train on explicit CoT; remove tokens linearly (Δ=8/epoch for multiplication, Δ=1/epoch for GSM8K). Removal smoothing + optimizer reset for stability.
- **Training:** Pure curriculum; no continuous-thought feedback; no special tokens.
- **Scale:** GPT-2 Small solves 9×9 multiplication at 99%; Mistral-7B >50% GSM8K with no intermediate token emission.
- **Locks in:** single-model curriculum as a complete solution; proves teacher-student scaffolding is optional. Direct parent of COCONUT's stage-k truncation schedule.

## What COCONUT added on top of the precursors

COCONUT (Dec 2024) is best understood as **Stepwise Internalization + Pause Tokens + continuous-thought feedback**. The first two ingredients were in the field 6-12 months earlier; the third is genuinely novel:

1. From Stepwise Internalization: multi-stage curriculum, token removal, single model (no emulator).
2. From Pause Tokens: `<bot>`/`<eot>` delimiters.
3. Novel: **the removed tokens are replaced by the model's own previous hidden states**, fed back as input embeddings (axis 3 above).

The anti-forgetting uniform-probability interleaving at rate $p=0.3$ appears to be a COCONUT original (not a direct inheritance) — it addresses the catastrophic forgetting that pure Stepwise Internalization handled with optimizer reset + removal smoothing.

## What CODI changed vs COCONUT

CODI (Feb 2025) is the other direction off Deng 2023:

- Keeps hidden-state feedback (axis 3 "yes").
- Replaces curriculum (γ) with **single-stage self-distillation** (α): the same model acts as teacher (in CoT mode) and student (in latent mode); an L1 loss aligns the hidden state of the token immediately preceding the answer.
- Drops Deng 2023's separate emulator; adds Deng 2024's single-model pattern.

CODI is essentially "Deng 2023 hidden-state distillation + Deng 2024 single-model + COCONUT continuous-thought feedback" — minus the curriculum.

## Why this concept page matters

Wave-4 proposals for "fundamentally different training blocks" should be re-grounded in which precursor they draw from, so we don't re-invent wheels. The genealogy tree:

```
ACT (Graves 2016)
 └─ Universal Transformers (Dehghani 2018) — depth-recurrent
    ├─ PonderNet (Banino 2021) — probabilistic halting
    └─ (inherited by Ouro, HRM, MoR, AdaPonderLM)

Neural ODEs (Chen 2018) ─── DEQ (Bai 2019) — fixed-point

Pause Tokens (Goyal 2023) ──┐
Filler Tokens (Pfau 2024) ──┤
Implicit CoT KD (Deng 2023)─┼─ Stepwise Internalization (Deng 2024) ──┐
Quiet-STaR (Zelikman 2024) ─┘                                          │
                                                                        ▼
                                                        COCONUT (Hao 2024) — curriculum + feedback
                                                        CODI (Shen 2025) — self-distillation
                                                        LT-Tuning — CPF-fused
                                                        SIM-CoT — aux decoder
```

## See also

- [[COCONUT]], [[CODI]] — direct descendants.
- [[Adaptive Computation Time]], [[Universal Transformers]], [[PonderNet]] — the parallel halting-head lineage.
- [[Neural ODEs]], [[Deep Equilibrium Models]] — continuous-depth / fixed-point lineage.
