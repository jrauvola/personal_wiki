---
type: synthesis
title: "Research: LPCVC 2026 Track 1 Winning Recipes"
created: 2026-04-25
updated: 2026-04-25
status: developing
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Master synthesis from autoresearch round 1-2 covering all five user-specified angles."
related:
  - "[[sources/EfficientFormer Activation Function Ablation]]"
  - "[[sources/CLIC - Compositional Awareness in CLIP]]"
  - "[[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]]"
  - "[[sources/Qualcomm AI Hub Quantization Documentation]]"
  - "[[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]"
  - "[[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]"
  - "[[concepts/INT8 Calibration for Vision-Language Models]]"
  - "[[concepts/Hard-Negative Loss for Vision-Language Models]]"
sources:
  - "[[sources/EfficientFormer Activation Function Ablation]]"
  - "[[sources/CLIC - Compositional Awareness in CLIP]]"
  - "[[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]]"
  - "[[sources/Qualcomm AI Hub Quantization Documentation]]"
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Research: LPCVC 2026 Track 1 Winning Recipes

## Overview

LPCVC 2026 Track 1 is the **first year** image-to-text retrieval is a track — there is no direct prior winning solution to copy. Searches for "LPCV 2025 Track 1" return the **classification** track (won by LabLVM, Ajou University, with 0.974 accuracy at 1.6 ms). The retrieval problem is novel for this competition.

This synthesis collects the highest-leverage tactics across the five user-specified angles, ranked by yield-per-effort given the 5-day deadline (closes 2026-04-30).

## Key Findings

### 🔥 1. The team's swish→ReLU activation hypothesis is probably wrong (or at least overstated)

EfficientFormer measured on iPhone 12 NPU: ReLU saves 0.5 ms over GeLU but loses 3.1% top-1 accuracy. HardSwish is 10× SLOWER than GeLU on the same NPU. (Source: [[sources/EfficientFormer Activation Function Ablation]])

The team's `context/PROBLEM_OVERVIEW.md` lists swish replacement as a key technical lever. The data says: probably not, unless QNN is showing CPU fallback for swish ops on Qualcomm specifically. **Profile first, swap second.** Architecture-level changes (CONV-BN folding, replacing CPU-fallback ops) gave EfficientFormer 48% latency reductions; activation swap gave <17%.

> [!gap] Need direct measurement on Qualcomm XR2 Gen 2 — iPhone NPU data may not transfer. But the prior should be "GeLU/swish is probably fine on a modern NPU compiler."

### 🔥 2. CLIC (May 2025) is the single best-fit recipe for the contrastive-caption failure mode

The competition's organizer captions are deliberately constructed contrastive variants ("grey monitor" vs "black monitor"). Standard CLIP fine-tunes *worsen* this. CLIC fine-tunes only the text encoder on concatenated image pairs with hard-negative captions, at **0.01% of CLIP pretraining cost**. Improves SugarCrepe Replace to 86.5% / Swap to 84.8%, AND improves MS-COCO retrieval (+1.3% / +2.2%). (Source: [[sources/CLIC - Compositional Awareness in CLIP]])

**Why this fits LPCVC:**
- Vision encoder frozen → MobileCLIP2-S4 image graph (the 13.7 ms INT8 latency-dominant) is unaffected.
- Only text encoder needs re-export and recompile.
- ~1-2 days wall-clock for full train + eval + recompile.
- Maintains MS-COCO retrieval as a safety net.

### 🔥 3. Calibration-set quality is the load-bearing INT8 quantization variable

Qualcomm AI Hub recommends 500–1000 representative calibration samples for production. Random data is benchmark-only. The team's own notes match (`PROBLEM_OVERVIEW.md`: "500+ representative images; 50–100 causes large accuracy drop"). (Source: [[sources/Qualcomm AI Hub Quantization Documentation]])

The team's TODO of "Inspect `quant_model/*.h5` and run through sample harness to verify quantization" is the single highest-priority diagnostic before submission. Without it, you don't know whether INT8 has cost 1% or 10% of Recall@10.

If pure W8A8 hurts Recall@10 too much: **INT16 activations + INT8 weights is the next step on QNN** before reaching for AIMET. Mixed-precision (different ops at different precision) is unsupported by QAI Hub.

### 4. LoRA-on-CLIP is parameter-efficient but not directly retrieval-validated

CLIP-LoRA (CVPRW 2024) applies LoRA to Q/K/V/O projections at rank 4. Validated for few-shot classification, NOT retrieval. Team's existing `self_training/lora_setup.py` should be checked: are all four projections enabled, or only Q/V (LLM-style shortcut)? Block-LoRA (Jan 2026) is a more recent, more parameter-efficient variant. (Source: [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]])

For LPCVC, LoRA on text encoder + CLIC-style hard-negative loss is a defensible cheap fine-tune. Avoid LoRA on image encoder if it would force full image-encoder re-export.

### 5. Self-training pipeline already in codebase — validate it produces measurable Recall@10 gains before touching backbone

The team's `self_training/` directory contains a complete pipeline (LoRA, FAISS, confidence/negative filters). The autoresearch did not surface specific public recipes that beat this for the small-data CLIP retrieval setting. The team's own pipeline is the right scaffold; the question is whether the loss function and training data match the LPCVC failure mode.

## Key Entities

- **[[entities/Snap Research]]** — EfficientFormer authors; the canonical mobile vision transformer latency reference.
- **[[entities/University of Tübingen ML Group]]** — Matthias Hein lab; CLIC compositional fine-tuning.
- **[[entities/Maxime Zanella]]** — CLIP-LoRA author.
- **Qualcomm AI Hub team** — operational reference for quantization workflow.

## Key Concepts

- **[[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]** — measure-before-swap discipline.
- **[[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]** — CLIC, NegCLIP, CoN-CLIP family.
- **[[concepts/INT8 Calibration for Vision-Language Models]]** — 500+ representative samples, optimized-ONNX-first workflow.
- **[[concepts/Hard-Negative Loss for Vision-Language Models]]** — generation strategies + loss formulations.

## Contradictions

- **Team intuition: swish is the bottleneck.** **Measured data: GeLU is nearly as fast as ReLU on iPhone NPU; HardSwish is 10× slower.** Resolution: profile on Qualcomm XR2 Gen 2 specifically before committing. The intuition may be salvaged if QNN is showing CPU fallback for swish, but the prior should be "probably no big win."
- **General consensus: standard fine-tuning improves CLIP retrieval.** **SugarCrepe / WinoGround literature: most fine-tunes worsen compositionality.** Resolution: the team needs a *compositionality-aware* fine-tune (CLIC / NegCLIP), not vanilla MSCOCO-style training.

## Open Questions

1. **What's the exact swish/GeLU latency on Qualcomm XR2 Gen 2 with QNN?** (Not surfaced in 2 search rounds — needs team measurement.)
2. **Does CLIC's recaptioned-web-data training transfer to LPCVC's narrow object-attribute caption style?** (Worth a 1-epoch ablation.)
3. **What did the LPCV 2025 Track 2/3 winners do for retrieval-style tasks?** (LPCV 2025 Track 1 was classification; retrieval may be in another track.)
4. **MobileCLIP2-S4 INT8 actual Recall@10 on LPCVC sample?** (TBD per team's table — should be measured before submission.)
5. **Per-channel vs per-tensor weight quantization for FastViT-MCi2 depthwise convs?** (Likely meaningful given depthwise is sensitive to outliers.)
6. **Does Block-LoRA (Jan 2026) outperform CLIP-LoRA on retrieval, not just classification?** (No retrieval-specific result surfaced.)
7. **AIMET vs QAI Hub built-in INT8 — measured Recall@10 difference on CLIP-family models?** (Nothing public found.)

## Recommended action ordering for the team (5-day window)

| Priority | Action | Wall-clock | Risk if skipped |
|----------|--------|-----------|-----------------|
| **P0** | Profile XR2 Gen 2 to verify <35 ms combined; identify CPU-fallback ops | 1 day | Submission disqualification |
| **P0** | Score current MobileCLIP2-S4 INT8 on sample set; verify quantization didn't break Recall@10 | <1 day | Flying blind on accuracy |
| **P1** | CLIC-style text-encoder-only fine-tune on concatenated image pairs + hard negatives | 1-2 days | Largest accuracy lever available |
| **P1** | If P0 reveals CPU-fallback ops in profile: address those before activation swap | 1 day | Bigger latency win than swish→ReLU |
| **P2** | Build a 500+ image calibration set from MSCOCO val + LAION + LPCVC sample; re-quantize | 1 day | Avoids known accuracy drop from undersized calibration |
| **P3** | Activation swap experiments (only if P0 profile shows swish/GeLU as actual bottleneck) | <1 day | Likely small win, real accuracy cost |
| **P4** | INT16 activations on QNN as Recall@10 fallback if pure INT8 hurts | <1 day | Compromise on latency for accuracy |

## Sources

- [[sources/EfficientFormer Activation Function Ablation]] — Snap Research, NeurIPS 2022, arXiv:2206.01191
- [[sources/CLIC - Compositional Awareness in CLIP]] — Peleg, Singh, Hein (Tübingen), arXiv:2505.24424, May 2025
- [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]] — Zanella & Ben Ayed, CVPRW 2024
- [[sources/Qualcomm AI Hub Quantization Documentation]] — Qualcomm Technologies, retrieved 2026-04-25
