---
type: concept
title: "Activation Function Latency-Accuracy Tradeoff on Mobile NPU"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Direct lever the team is considering (swish→ReLU swap). Concept page consolidates the per-hardware measured data so the team can decide without re-collecting evidence."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Activation Function Latency-Accuracy Tradeoff on Mobile NPU

## What this concept is

The folk wisdom "ReLU is fastest, GeLU is slow" comes from CPU/GPU benchmarks. On mobile NPUs (iPhone ANE, Qualcomm Hexagon), the actual latency depends on the compiler's kernel coverage for each op. Smooth activations (GeLU, swish) often have hand-tuned NPU kernels; piecewise variants (HardSwish, ReLU6) sometimes don't, leading to surprising slowdowns.

## Measured data points

| Hardware | Compiler | Activation | Latency | Source |
|----------|---------|------------|---------|--------|
| iPhone 12 NPU | CoreMLTools | GeLU | 3.0 ms | [[sources/EfficientFormer Activation Function Ablation]] |
| iPhone 12 NPU | CoreMLTools | ReLU | 2.5 ms | same |
| iPhone 12 NPU | CoreMLTools | HardSwish | 32.4 ms | same |

Top-1 accuracy on ImageNet (EfficientFormer-L1):
- GeLU: 82.4%
- ReLU: 79.3% (−3.1%)
- HardSwish: 80.3% (−2.1%)

> [!gap] No directly comparable measured data for Qualcomm XR2 Gen 2 / Hexagon HMX with QNN was found in autoresearch round 1-2. The team should produce this table for their own target before deciding.

## How to apply

When evaluating an activation swap for latency:

1. **Profile first, swap second.** Run the QNN profile job and check whether activation kernels are CPU-fallback. If yes, swap is justified. If no, ReLU's accuracy cost is probably not worth a small NPU-side win.
2. **Beware HardSwish-class traps.** Piecewise activations that "should" be cheap can be 10× slower if the compiler doesn't fuse them.
3. **3% top-1 accuracy ≈ several Recall@10 points.** For a competition where the gap between current best (0.7527) and baseline (0.7260) is 0.0247, a 3% backbone-accuracy hit is likely to dominate any latency savings.
4. **Architecture changes give bigger wins.** EfficientFormer's patch-embed redesign saved 48% latency; activation swap saved <17%. If latency is the blocker, look at backbone architecture or quantization first.

## Open questions

- What does the swish/GeLU/ReLU ablation look like *specifically* on Qualcomm Hexagon HMX with QNN context binary compile? (Needs measurement on the team's target.)
- Does QNN's `--target_runtime qnn_context_binary` automatically rewrite GeLU to a fused fast path, or run it as multiple ops?
- Is there published data on the team's exact backbone (FastViT-MCi2 in MobileCLIP2-S4) on XR2 Gen 2? (Search rounds did not surface this.)

## Cross-references

- [[sources/EfficientFormer Activation Function Ablation]]
- [[concepts/QNN Compile Pipeline for Mobile CLIP]]
