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

2026-04-25 — autoresearch-hybrid validation run on "MobileCLIP2 R@10 on Hexagon" succeeded. Filed [[questions/Research - MobileCLIP2 R@10 on Hexagon NPU]] + 3 sources + 1 concept.

## 🚨 P0 RESOLVED: deployed checkpoint is MobileCLIP2-S2, NOT S4

[[sources/AXERA MobileCLIP2 w8a16 Deployment]] published per-encoder latency table for both variants on AX650 NPU at w8a16:
- **MobileCLIP2-S2:** image enc 19.1 ms, text enc 5.7 ms, combined ~25 ms ✓
- **MobileCLIP2-S4:** image enc 65.3 ms, text enc 12.7 ms, combined ~78 ms ✗

Team-measured 13.7 ms image encoder INT8 on Qualcomm XR2 Gen 2 = consistent with MCi2 / S2, NOT MCi4 / S4. Update `lpcvc_models.py` defaults and `AGENTS.md` if needed. Resolves [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]].

## Top Findings (autoresearch rounds 1-3 + hybrid validation run)

### 🔥 w8a16 is the cross-vendor production default for MobileCLIP2
AXERA defaults to w8a16 (not pure W8A8). Cross-validates `--lite_mp percentage=N;override_qtype=int16` as the right Hub flag when pure W8A8 hurts.

### 🔥 Activation-aware quantization decision tree (try in this order)
1. **Family A (cheap):** `--lite_mp` flag in Hub `submit_quantize_job`. Most likely sufficient.
2. **Family B (vision-specific):** RegCache prefix-token outlier absorption ([[sources/RegCache - Activation Quantization Vision Encoders]]). Training-free.
3. **Family C (heavy):** AIMET native + AdaRound + per-op INT16 on softmax/LayerNorm.

See [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]].

### 🔥 MobileCLIP2 reports R@1, not R@10
Apple's published metric is R@1 on COCO/Flickr. Use as a *lower bound* for our R@10. Relative ranking across variants should hold.

### 🔥 DFNDR-2B-trained MobileCLIP2 is biased toward zero-shot classification
Apple acknowledges in MobileCLIP2 paper: "DFN-pretrained students do not always achieve SOTA retrieval." Implication: MobileCLIP2 may not be optimal for retrieval even ignoring quantization. Fine-tune (CLIC-style) is more important. See [[sources/CLIC - Compositional Awareness in CLIP]].

### 🔥 LPCVC 2025 evaluation paper (arXiv 2604.19054)
Peer-reviewed paper by LPCVC organizers (first author Yung-Hsiang Lu). Single most-direct prior-art reference. Read before submission. See [[sources/LPCV 2025 Evaluation Paper]].

### EfficientFormer NPU data contradicts swish→ReLU intuition
ReLU saves only 0.5 ms over GeLU on iPhone NPU but loses 3.1% accuracy. HardSwish is 10× SLOWER than GeLU. Profile XR2 Gen 2 first; bottleneck is more likely a CPU-fallback op than activation. See [[sources/EfficientFormer Activation Function Ablation]].

### CLIC text-encoder-only fine-tune (highest yield for the deadline)
0.01% pretraining cost. Improves SugarCrepe Replace 86.5% / Swap 84.8%. Maintains MS-COCO retrieval. Vision encoder graph unchanged. See [[sources/CLIC - Compositional Awareness in CLIP]].

### LPCVC 2025 Track 2 (SEUDecoder) is the closest VL analog
Winner pattern: frozen well-quantising VL backbone + small fine-tuned head/decoder. See [[sources/LPCVC 2025 Cross-Track Lessons]].

## Active threads

- ✅ Verify checkpoint identity — done by AXERA evidence (MobileCLIP2-S2)
- Profile XR2 Gen 2 — identify CPU-fallback ops
- Score current INT8 on sample set (the existing TODO)
- Validate Family A (`--lite_mp`) before reaching for Family B/C

## Recommended action ordering (5-day window, updated 2026-04-25)

| Pri | Action | Time | Reasoning |
|-----|--------|------|-----------|
| **P0** | Update `AGENTS.md` and `lpcvc_models.py` to reflect MobileCLIP2-S2 (not S4) as deployed model | 10 min | Avoids further misattribution |
| **P0** | Score current MobileCLIP2-S2 INT8 on sample set; identify Recall@10 baseline | <1 day | Flying blind without this |
| **P0** | Profile XR2 Gen 2; identify CPU-fallback ops | 1 day | Submission requires this anyway |
| **P1** | If Recall@10 hurts: try `--lite_mp percentage=15;override_qtype=int16` (Family A) | <1 day | Cross-vendor validated by AXERA's w8a16 default |
| **P1** | CLIC-style text-encoder fine-tune | 1-2 days | Largest accuracy lever, image graph untouched |
| **P2** | If Family A insufficient: prototype RegCache prefix-token outlier absorption (Family B) | 1 day | Vision-specific; training-free |
| **P2** | Try 192px input variant per LPCVC 2025 T3 lesson | <1 day | Cheap latency win for ViT-based encoders |
| **P3** | Distill from larger CLIP teacher into S2 | 2 days | Most-repeated tactic in LPCV history |

## Pages by area

- **Architecture:** [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]]
- **Quantization:** [[sources/AIMET to QAI Hub Workflow]] · [[sources/Qualcomm AI Hub Quantization Documentation]] · [[sources/AXERA MobileCLIP2 w8a16 Deployment]] · [[sources/AWQ - Activation-aware Weight Quantization]] · [[sources/RegCache - Activation Quantization Vision Encoders]] · [[concepts/INT8 Calibration for Vision-Language Models]] · [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]]
- **Activation tradeoffs:** [[sources/EfficientFormer Activation Function Ablation]] · [[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]
- **Compositionality / fine-tuning:** [[sources/CLIC - Compositional Awareness in CLIP]] · [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]] · [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]] · [[concepts/Hard-Negative Loss for Vision-Language Models]]
- **Distillation / training:** [[concepts/Matryoshka Embeddings for CLIP Retrieval]]
- **LPCV history:** [[sources/LPCVC 2025 Cross-Track Lessons]] · [[sources/LPCV 2025 Evaluation Paper]]
- **Synthesis:** [[questions/Research - LPCVC 2026 Track 1 Winning Recipes]] · [[questions/Research - MobileCLIP2 R@10 on Hexagon NPU]]
- **Open questions:** [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]] (resolved by AXERA evidence)

## Open questions still unresolved

- Team's actual measured Recall@10 on LPCVC sample (P0 TODO).
- Does Hexagon W8A8 on MobileCLIP2-S2 hit the AXERA w8a16 latency or beat it?
- Does RegCache work on MobileCLIP2 image graph as exported? (No public test.)
- AXERA's exact calibration recipe in `AXERA-TECH/axera.ml-mobileclip` GitHub.
- TernaryCLIP measured Recall@K on COCO/Flickr (abstract didn't surface).
- TinyCLIP comparison with MobileCLIP-family — not in TinyCLIP paper directly.
