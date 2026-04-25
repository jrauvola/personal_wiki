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

2026-04-25 — autoresearch round 3 with 4 parallel subagents. Total filed: 14 pages across 3 rounds. Major new finding: possible MobileCLIP-S2/MCi2 vs MobileCLIP2-S4/MCi4 checkpoint mismatch — flagged as P0.

## Top Findings (autoresearch rounds 1-3)

### 🚨 P0: VERIFY — which MobileCLIP checkpoint is actually deployed?
- Team brief says MobileCLIP2-S4 (uses MCi4, ~321M image params).
- Measured 13.7 ms INT8 image encoder is consistent with **MCi2** (~36M image params), not MCi4.
- 5-min check: `grep "mobileclip2_s4\|mci4"` in codebase + count params on loaded model.
- See [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]].

### 🔥 LPCVC 2025 Track 2 (SEUDecoder) is the closest VL analog
- Same QAI Hub workflow as 2026. Same Snapdragon class. Vision+text dual-encoder pattern.
- Winning recipe: **frozen well-quantising VL backbone + small fine-tuned head/decoder**. 3rd place explicitly fine-tuned XDecoder rather than replacing backbone.
- Direct read-across: freeze MobileCLIP image encoder; fine-tune only text side (CLIC) or thin projection.
- See [[sources/LPCVC 2025 Cross-Track Lessons]].

### 🔥 Cheapest single latency win: drop input resolution
- LPCVC 2025 Track 3 winner (UMN): "Reducing image resolution significantly improves running time while having only a minor impact on accuracy, especially for ViT-based architectures."
- Team currently runs 224 input on a 256-native MCi backbone (resize baked in graph). Try **192 or 160** before exotic optimizations.

### 🔥 Per-channel weight quantization is mandatory for MCi-family
- MCi2 is depthwise-heavy (RepMixer + ConvFFN-DW + RepCPE + stem DW + patch-embed depthwise). Per-tensor weights catastrophically fail on depthwise (~50× channel variance).
- Verify QAI Hub default has per-channel ON. Without it, expect >1pp R@10 loss vs FP.
- See [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]].

### 🔥 W8A16 is the standard production setting for transformer attention on Hexagon
- Pure W8A8 typically fails on attention activation outliers (heavy tails).
- QAI Hub supports A16W8 globally; mixed precision (A16 only on softmax) requires AIMET.
- See [[sources/AIMET to QAI Hub Workflow]].

### 🔥 Matryoshka loss = single training run gives entire accuracy/latency Pareto
- One training pass with `matryoshka_dims=[64,128,256,384,512,768]` produces a model where you can pick the dim at submission. <0.019 nDCG gap between 256-d and 512-d on CLIP retrieval.
- See [[concepts/Matryoshka Embeddings for CLIP Retrieval]].

### CLIC text-encoder-only fine-tune (highest yield for the deadline)
- 0.01% pretraining cost. Improves SugarCrepe Replace 86.5% / Swap 84.8%. Maintains MS-COCO retrieval.
- Vision encoder graph unchanged → no image-encoder recompile needed.
- See [[sources/CLIC - Compositional Awareness in CLIP]].

### Activation function (swish→ReLU): probably NOT the win the team thinks
- EfficientFormer iPhone NPU: ReLU saves 0.5 ms over GeLU but loses 3.1% accuracy. HardSwish 10× slower than GeLU.
- Hexagon-MLIR docs use GELU as their motivating polynomial-approximation example — operational on HTP, slower than ReLU but not catastrophic.
- Profile XR2 Gen 2 first; CPU-fallback ops (Resize, custom ops) likely dominate over activation.

### Knowledge distillation is the most-repeated tactic in LPCV history
- 2/3 of 2023 podium teams used it. SigLIP2 image encoder → MobileCLIP image encoder (with frozen CLIP-tokenizer text head, per DCLIP pattern) is the most LPCVC-compliant variant.
- See [[concepts/Knowledge Distillation for Mobile CLIP Retrieval]].

### LPCVC 2024 didn't run
- Series went on hiatus. LPCVC 2025 (under QAI Hub) is the only relevant prior. No 2024 winning recipes exist.

## Active threads

- Verify checkpoint identity (MCi2 vs MCi4) — 5-min check.
- Profile XR2 Gen 2 — identify CPU-fallback ops.
- Score current INT8 on sample set (the existing TODO).
- Self_training pipeline development continues.

## Recommended action ordering (5-day window)

| Pri | Action | Time | Reasoning |
|-----|--------|------|-----------|
| **P0** | Verify which checkpoint is deployed (5 min) | 5 min | Reframes everything else |
| **P0** | Profile XR2 Gen 2; identify CPU-fallback ops; score current INT8 on sample | 1 day | Submission requires this anyway |
| **P0** | Verify per-channel weight quantization is ON in QAI Hub recipe | 30 min | Catastrophic if off |
| **P1** | CLIC-style text-encoder fine-tune | 1-2 days | Largest accuracy lever; image graph untouched |
| **P1** | Try 192px input variant (re-export + recompile + score) | <1 day | Cheap latency win per LPCVC 2025 T3 |
| **P2** | Try W8A16 globally if R@10 dropped from FP | 1 day | Fallback for attention outliers |
| **P2** | Matryoshka loss in self_training; gives accuracy/dim trade-space | 1-2 days | Free Pareto from one run |
| **P3** | Activation swap experiments (only if P0 profile shows swish as actual bottleneck) | 1 day | Likely small win, real accuracy cost |
| **P3** | Distill SigLIP2-B image encoder → MobileCLIP image encoder, frozen CLIP text head | 2 days | Highest ceiling, highest risk |

## Pages created (all 3 rounds)

**Synthesis + open questions:**
- [[questions/Research - LPCVC 2026 Track 1 Winning Recipes]]
- [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]]

**Sources:**
- [[sources/EfficientFormer Activation Function Ablation]]
- [[sources/CLIC - Compositional Awareness in CLIP]]
- [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]]
- [[sources/Qualcomm AI Hub Quantization Documentation]]
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]]
- [[sources/AIMET to QAI Hub Workflow]]
- [[sources/LPCVC 2025 Cross-Track Lessons]]

**Concepts:**
- [[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]
- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]
- [[concepts/INT8 Calibration for Vision-Language Models]]
- [[concepts/Hard-Negative Loss for Vision-Language Models]]
- [[concepts/Matryoshka Embeddings for CLIP Retrieval]]

**Entities:**
- [[entities/Snap Research]]

## Open questions still unresolved

- AIMET-vs-QAI-Hub-built-in measured Recall@10 delta on MobileCLIP-family — no public side-by-side. Worth team experiment.
- Exact `options` flag strings for `submit_quantize_job` (per_channel, adaround, calibration_method) — not in public docs.
- LPCVC 2025 Track 2 SICer/SEUDecoder team writeup — architecture details not published. Worth direct outreach.
- TripletCLIP retrieval-specific R@K (vs the published compositionality numbers).
- Sigmoid vs softmax contrastive loss under LoRA fine-tuning — no measured comparison.
