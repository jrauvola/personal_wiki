---
type: source
source_type: paper
title: "EfficientFormer Activation Function Ablation"
arxiv_id: "2206.01191"
venue: "NeurIPS 2022"
date_published: 2022-06-02
authors: ["Yanyu Li", "Geng Yuan", "Yang Wen", "Eric Hu", "Georgios Evangelidis", "Sergey Tulyakov", "Yanzhi Wang", "Jian Ren"]
url: "https://arxiv.org/abs/2206.01191"
code_repo: "https://github.com/snap-research/EfficientFormer"
has_weights: true
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Direct activation-function latency table for mobile NPU — challenges the team's swish→ReLU intuition with measured numbers."
key_claims:
  - "On iPhone 12 NPU with CoreMLTools, ReLU is only 0.5 ms faster than GeLU (2.5 vs 3.0 ms) but loses 3.1% top-1 accuracy (79.3% vs 82.4%)."
  - "HardSwish is 10× SLOWER than GeLU on iPhone NPU (32.4 ms vs 3.0 ms) despite being 'efficient' on other hardware — compiler dependency dominates."
  - "Activation choice for mobile NPU must be measured per-target — generic 'ReLU is fastest' rules of thumb are wrong for transformers on iPhone NPU."
  - "EfficientFormer NPU latency is 7× faster than CPU on iPhone (1.6 vs 11.5 ms) — NPU placement matters more than activation choice for total budget."
  - "Architectural speed drivers (patch embedding, dimension-consistent 4D/3D blocks, CONV-BN folding) gave bigger latency wins than activation tuning."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# EfficientFormer Activation Function Ablation

## Summary

EfficientFormer (Snap Research, NeurIPS 2022) is the canonical reference for mobile vision transformer latency on Apple Neural Engine. Its activation-function ablation (Appendix B Table 3) is the most-cited measured data on the GeLU/ReLU/HardSwish tradeoff on mobile NPU.

## The ablation that matters

On iPhone 12 NPU with CoreMLTools:

| Activation | Latency (ms) | Top-1 Accuracy |
|------------|-------------|----------------|
| GeLU (default) | 3.0 | 82.4% |
| ReLU | 2.5 | 79.3% |
| HardSwish | **32.4** | 80.3% |

**Implications for LPCVC 2026 Track 1:**

1. **Swish/GeLU is not necessarily the bottleneck the team assumes.** On iPhone NPU, GeLU runs nearly as fast as ReLU. The same may hold on Qualcomm XR2 Gen 2 — needs measurement before committing to a swap. (Source: Table 3, Appendix B)
2. **HardSwish is a trap on some compilers.** 10× slowdown vs GeLU on iPhone — confirms that "ReLU6-based ≡ fast" is wrong without measuring. (Source: Table 3)
3. **3.1% accuracy loss for 0.5 ms savings is a bad trade** for a Recall@10 competition where 0.0247 R@10 separates current best (0.7527) from baseline (0.7260). (Inference, not direct quote)

> [!gap] iPhone 12 NPU ≠ Qualcomm XR2 Gen 2. Activation kernel implementations differ between Apple's ANE and Qualcomm Hexagon HMX. Measure on target before generalizing.

## Architectural levers that gave bigger wins

The paper's actual speedup gains came from architecture, not activation:

1. **Patch embedding via 3×3 conv stem with fast downsampling** — 48% latency reduction over large-kernel patch embed.
2. **Dimension-consistent 4D/3D block split** — eliminates expensive reshape ops between conv and attention layers.
3. **CONV-BN normalization** — BN can be folded into preceding conv at inference; LayerNorm cannot. Removes a normalization op entirely.
4. **Latency-driven supernet slimming** — Gumbel-Softmax sample importance + per-millisecond accuracy-drop scoring (Appendix A).

EfficientFormer-L1 hits 1.6 ms on iPhone NPU vs 11.5 ms on CPU — 7× speedup. NPU placement and op compatibility matter more than activation tuning for hitting the 35 ms gate.

## What this means for the team

- **Don't blindly swap swish→ReLU.** Profile both on XR2 Gen 2 first. If the gap is 0.5 ms, the accuracy cost almost certainly isn't worth it.
- **Look for ops that fall back to CPU** in the QNN profile output. These dominate latency far more than activation choice. Resize, normalization, custom ops are common offenders.
- **CONV-BN folding** is a free latency win if the model exports preserve BN-conv pairs. Verify in the ONNX graph.

## Cross-references

- [[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]
- [[entities/Snap Research]]
