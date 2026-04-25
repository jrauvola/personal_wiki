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

2026-04-25 — project bootstrapped in wiki vault. No autoresearch yet.

## Key Recent Facts

- LPCVC 2026 Track 1 deadline: **April 30, 2026** (5 days away).
- Best model in hand: MobileCLIP2-S4, R@10 = 0.7527 on sample, FP16 image enc 39.3 ms, INT8 13.7 ms.
- Latency gate: image+text encoders combined < 35 ms on XR2 Gen 2 (Proxy).
- Active R&D: self-training pipeline with LoRA + FAISS retrieval index + confidence/negative filters.
- Standard benchmarks (MSCOCO, Flickr30K) are saturated for MobileCLIP2-S4 (R@10 = 0.93–0.99); they are non-predictive of competition performance because the competition uses contrastive captions ("grey monitor" vs "black monitor").
- Compositionality benchmarks (SugarCrepe, ColorSwap, Winoground, ARO) are the right validation surface.

## Active threads

- Self-training pipeline (`self_training/` in codebase) under active dev.
- ONNX export with baked preprocessing — verify Resize op is not CPU fallback on QNN.
- Activation function swap (swish → ReLU/ReLU²) for latency.
- Awaiting QAI Hub profile job to verify <35 ms combined budget.

## Open questions to research

- What activation functions yield the best latency-vs-accuracy tradeoff on Qualcomm XR2 Gen 2 NPU specifically?
- What did LPCV 2025 Track 1 winning solution actually do?
- How well do MobileCLIP2-S2 / S3 / B trade off vs S4 on this exact hardware?
- Is there public data on Matryoshka embeddings reducing inference cost on mobile NPUs?
- Self-training tactics that work in the small-labeled-data regime for retrieval?
- Calibration-set construction for INT8 W8A8 quantization on CLIP-family models — what produces the best Recall@10?
