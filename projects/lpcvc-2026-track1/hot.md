---
type: meta
title: "Hot Cache"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: project workspace surface
updated: 2026-04-25
---

# Recent Context

## Last Updated

2026-04-25 — autoresearch round 1+2 completed. Filed master synthesis + 4 sources + 4 concepts + 1 entity. Key findings flag a contradiction with team's swish→ReLU intuition.

## Top Findings (autoresearch 2026-04-25)

1. **🔥 Swish→ReLU intuition is probably wrong for LPCVC's deadline.** EfficientFormer measured: ReLU saves 0.5 ms but loses 3.1% accuracy on iPhone NPU; HardSwish is 10× SLOWER. Profile Qualcomm XR2 Gen 2 first; the bottleneck is more likely a CPU-fallback op than the activation itself. ([[sources/EfficientFormer Activation Function Ablation]])

2. **🔥 CLIC (May 2025) is the highest-yield-per-day fine-tune for the contrastive-caption failure.** Frozen vision encoder + text-only fine-tune, 0.01% of pretraining cost. SugarCrepe Replace 86.5% / Swap 84.8%, AND maintains MS-COCO retrieval (+1.3% / +2.2%). Vision encoder graph (the latency-dominant 13.7 ms INT8 path) untouched. ([[sources/CLIC - Compositional Awareness in CLIP]])

3. **🔥 The "verify quantization Recall@10" TODO is the load-bearing diagnostic.** Without it, flying blind on whether INT8 cost 1% or 10%. Inspect `quant_model/*.h5` and run sample harness immediately.

4. **LPCV 2025 had no retrieval track** — Track 1 was classification (LabLVM, 0.974 acc, 1.6 ms). 2026 Track 1 is the first retrieval year. No prior winning recipe to copy.

5. **Calibration set: ≥500 representative images, optimized-ONNX-first.** Qualcomm AI Hub's official guidance matches the team's existing `PROBLEM_OVERVIEW.md` note. Compile to ONNX before quantizing — common missed step.

## Active threads

- Self-training pipeline (`self_training/` in codebase) under active dev — validate it produces measurable Recall@10 gains before backbone changes.
- ONNX export with baked preprocessing — verify Resize op is not CPU fallback in QNN profile.
- Awaiting QAI Hub profile job to verify <35 ms combined budget.

## Recommended next actions (ranked, see synthesis for full table)

- **P0:** Profile XR2 Gen 2; identify CPU-fallback ops; score current INT8 on sample
- **P1:** CLIC-style text-encoder fine-tune; address profile-revealed bottlenecks
- **P2:** Expand calibration set to 500+ representative images; re-quantize
- **P3:** Activation swap *only if* profile shows swish as actual bottleneck

## Pages created today

- Synthesis: [[questions/Research - LPCVC 2026 Track 1 Winning Recipes]]
- Sources: [[sources/EfficientFormer Activation Function Ablation]], [[sources/CLIC - Compositional Awareness in CLIP]], [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]], [[sources/Qualcomm AI Hub Quantization Documentation]]
- Concepts: [[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]], [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]], [[concepts/INT8 Calibration for Vision-Language Models]], [[concepts/Hard-Negative Loss for Vision-Language Models]]
- Entities: [[entities/Snap Research]]

## Open questions to research next

- Does CLIC's recaptioned-web-data training transfer to LPCVC's narrow object-attribute caption style?
- What's the actual swish/GeLU latency on Qualcomm XR2 Gen 2 with QNN context binary?
- AIMET vs QAI Hub built-in INT8 — measured Recall@10 difference on CLIP-family?
- Did any LPCV 2024/2025 Track 2 or 3 deal with retrieval-style problems?
