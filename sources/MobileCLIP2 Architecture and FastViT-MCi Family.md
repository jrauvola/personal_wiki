---
type: source
source_type: paper
title: "MobileCLIP2 Architecture and FastViT-MCi Family"
arxiv_id: "2508.20691"
venue: "TMLR"
date_published: 2025-08-28
authors: ["Apple ML Research"]
url: "https://arxiv.org/abs/2508.20691"
code_repo: "https://github.com/apple/ml-mobileclip"
has_weights: true
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Architecture truth source. Resolves backbone identity (MCi2 vs MCi4), names the exact ops the team is quantizing, identifies depthwise per-channel quantization as mandatory."
key_claims:
  - "MobileCLIP2-S4 uses the MCi4 backbone (5-stage), not MCi2. MCi family: S0→MCi0, S1→MCi1, S2/B→MCi2, S3→MCi3, S4→MCi4."
  - "MCi2: depths [4,12,24,4], embed dims [80,160,320,640], MLP ratio 3.0, ~36M image params, native input 256×256."
  - "Token mixers in MCi2: stages 1-3 use RepMixer (pure depthwise convs); only stage 4 uses MHSA. ~44 RepMixer blocks + 4 attention blocks per forward."
  - "ConvFFN block: 7×7 depthwise + BatchNorm2d → 1×1 → GELU → 1×1. ~48 GELU calls per forward in MCi2."
  - "MCi-family uses BatchNorm2d (not LayerNorm) including the pre-attention norm in stage 4. BN folds into preceding conv at inference — major INT8-friendliness win over plain ViTs."
  - "MobileCLIP2 distillation: 2-teacher ensemble (DFN2B-CLIP-ViT-L-14 variants), KL on row-wise softmax similarities both directions, λ=1.0 pure distillation (no CLIP contrastive term). MobileCLIP1 used λ=0.5 mix."
  - "DFN-pretrained students 'do not always achieve SOTA retrieval' — DFN tilts toward zero-shot classification, may underperform on retrieval tasks."
  - "MobileCLIP2-S4 zero-shot Flickr30K R@1: T→I 78.0, I→T 92.4."
  - "MobileCLIP1 zero-shot COCO R@1: S0=40.4/58.7, S2=45.4/63.4, B=50.6/68.8."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# MobileCLIP2 Architecture and FastViT-MCi Family

## Summary

The authoritative architecture spec for the MobileCLIP / MobileCLIP2 family. Verified against `apple/ml-mobileclip` source (`mobileclip/models/mci.py`, `mobileclip/configs/*.json`) and the TMLR 2025-08 paper. Resolves the team's checkpoint-identity question (see [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]]).

## MCi family map (verified)

| MobileCLIP variant | Backbone | Stages | ~Image params | Native input |
|--------------------|----------|--------|---------------|--------------|
| MobileCLIP-S0 / MobileCLIP2-S0 | MCi0 | 4 | small | 256 |
| MobileCLIP-S1 / MobileCLIP2-S1 | MCi1 | 4 | small | 256 |
| MobileCLIP-S2 / **MobileCLIP2-B** | MCi2 | 4 | ~36M | 256 |
| MobileCLIP2-S3 | MCi3 | **5** | larger | 256 |
| **MobileCLIP2-S4** | **MCi4** | **5** | **~321M** | 256 |

The team's `lpcvc_models.py` model registry lists `mobileclip2_s4` separately from `mobileclip2_b` and `mobileclip_s2`. **A 13.7 ms INT8 image-encoder latency on XR2 Gen 2 is consistent with a ~36M-param backbone, not a 321M-param backbone** — flag the deployed-checkpoint question before further optimization.

## MCi2 architecture (relevant if team is on S2/B)

- **Stem:** 3 stacked `MobileOneBlock` (3×3 stride-2 dense + 3×3 stride-2 depthwise + 1×1 pointwise).
- **Patch-embed between stages:** `ReparamLargeKernelConv` (depthwise 7×7 large-kernel + 3×3 small-kernel branch, reparameterized at inference) + `MobileOneBlock` 1×1 pointwise.
- **Stages 1-3 (RepMixer):** depthwise 3×3 conv + BN, no attention.
- **Stage 4 (Attention):** `BatchNorm2d` over 4D feature map → MHSA (Q/K/V Linear + softmax + Linear proj, head_dim=32).
- **ConvFFN every block:** 7×7 depthwise + BN → 1×1 → GELU → 1×1.
- **Position encoding:** RepCPE (7×7 depthwise conv) inserted only before stage 4.
- **After reparameterization:** RepMixer collapses to single 3×3 depthwise + bias; MobileOne blocks collapse to single Conv2d.

**Inference graph dominated by:** depthwise convs + 1×1 pointwise + BN + GELU. Stage-4 softmax is the only attention-side op. Critical: BN is foldable into preceding conv — no per-token statistics, no FP32 fallback needed.

## MCi4 architecture (relevant if team is actually on S4)

5-stage variant, ~321M image params, similar block design to MCi2 but more depth and width. ~19.6 ms FP latency on iPhone Apple Neural Engine per the paper. Hitting 13.7 ms INT8 on XR2 Gen 2 would be a remarkable result requiring verification.

## Quantization implications (cross-ref [[concepts/INT8 Calibration for Vision-Language Models]])

**Quantization-friendly:**
- BN-everywhere: folds into preceding conv weights, no per-token statistics, no FP32 fallback.
- Depthwise + 1×1 dominates: well-understood quantization patterns.

**Quantization-hostile (for MCi2 backbone):**
- **GELU** in every ConvFFN (~48 calls/forward in MCi2). Operational on Hexagon HTP via polynomial approximation (per Hexagon-MLIR), but non-trivial latency slice. Possible target for ReLU swap with a brief fine-tune.
- **Softmax** in stage-4 attention (4 calls/forward in MCi2). Often forced to INT16 fallback.
- **Depthwise convs** (RepMixer + ConvFFN-DW + RepCPE): per-channel weight quantization is **mandatory**. Per-tensor weights catastrophically fail on depthwise (~50× channel variance in dynamic range) — measured +70.6 pp top-1 going per-tensor → per-channel on MobileNetV2.

## Distillation recipe (MobileCLIP2)

- **Teachers:** ensemble of `DFN2B-CLIP-ViT-L-14-s39b` + `DFN2B-CLIP-ViT-L-14`, independent logit scales (70, 60).
- **Loss:** KL divergence on row-wise softmax similarities, both I→T and T→I directions.
- **Mixing:** λ=1.0 (pure distillation; no CLIP contrastive term). MobileCLIP1 used λ=0.5.
- **Caveat:** DFN-pretrained teachers tilt toward zero-shot classification; "do not always achieve SOTA retrieval." This is relevant for LPCVC because the competition IS retrieval. Worth checking whether the team's MobileCLIP2 weights actually beat MobileCLIP1 weights on the LPCVC sample retrieval task.

## Cross-references

- [[questions/Open Question - Which MobileCLIP Checkpoint Is Actually Deployed]]
- [[concepts/INT8 Calibration for Vision-Language Models]]
- [[concepts/Knowledge Distillation for Mobile CLIP Retrieval]]
- [[entities/Apple ML Research]]

## Sources used

- arXiv 2508.20691 (MobileCLIP2 paper)
- `apple/ml-mobileclip/mobileclip/models/mci.py` (ground-truth MCi spec)
- `apple/ml-mobileclip/mobileclip/configs/mobileclip_s2.json`
- arXiv 2311.17049 (MobileCLIP1 paper, CVPR 2024)
