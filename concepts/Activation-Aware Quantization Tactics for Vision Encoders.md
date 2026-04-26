---
type: concept
title: "Activation-Aware Quantization Tactics for Vision Encoders"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "The deciding factor for whether MobileCLIP2 INT8 retains Recall@10. Synthesizes three methods (AWQ, RegCache, AIMET) with the right one to try first for the team's failure mode."
last_reviewed: 2026-04-25
reviewed_by: autoresearch-hybrid
---

# Activation-Aware Quantization Tactics for Vision Encoders

## The problem

Naive INT8 PTQ on transformer-style vision encoders (ViT, CLIP, MobileCLIP) loses 1-3% accuracy minimum, sometimes >5%, because attention activations have heavy-tailed distributions. A few outlier activations dominate the quantization range; the bulk of non-outlier activations get crushed to too few bits.

For LPCVC 2026 Track 1 specifically: this is the difference between MobileCLIP2-S2 INT8 retaining Recall@10 ≈ 0.75 vs collapsing to 0.65.

## Three families of fix, ordered by effort

### Family A — Cheap, works on Hub (try first)

**Tactic:** `--lite_mp percentage=N;override_qtype=int16` flag in `submit_quantize_job`.

Promotes a percentage of layers to INT16 activations while leaving the rest INT8. Cross-validated by AXERA's choice to default w8a16 for MobileCLIP2-S2 deployment ([[sources/AXERA MobileCLIP2 w8a16 Deployment]]).

**Cost:** zero training, zero new infrastructure. Just a Hub flag.
**Expected gain:** recover most of the 1-3% R@10 loss. Sufficient for many cases.
**Source:** [[sources/AIMET to QAI Hub Workflow]] (amended 2026-04-25).

### Family B — Medium effort, vision-specific (try second)

**Tactic:** RegCache prefix-token outlier absorption.

Insert outlier-absorbing prefix tokens, let outliers concentrate there, delete prefixes before downstream use. Training-free. Vision-specific (purpose-built for ViT/CLIP outlier patterns, not LLM-derived).

**Cost:** modify the ONNX export pipeline to add prefix tokens; modify post-encoder to delete them. ~half-day engineering.
**Expected gain:** more targeted than `--lite_mp` because it addresses the *cause* (outliers) rather than *masking* it (more bits).
**Source:** [[sources/RegCache - Activation Quantization Vision Encoders]].

### Family C — High effort, fully arbitrary (only if A and B fail)

**Tactic:** AIMET native + AdaRound + per-op precision.

Run `QuantAnalyzer` per-layer SQNR sweep → identify hotspot ops (typically softmax + LayerNorm in attention) → mark those for INT16, rest INT8 → AdaRound for layer-wise rounding refinement → export `.aimet` → recompile via QAI Hub.

**Cost:** requires AIMET environment, calibration set re-prep, per-op precision sweep. Full day plus.
**Expected gain:** smallest residual error of the three, but the marginal R@10 over Family A+B is often <0.5%.
**Source:** [[sources/AIMET to QAI Hub Workflow]].

## What does NOT directly transfer from LLM literature

- **AWQ** ([[sources/AWQ - Activation-aware Weight Quantization]]) — focuses on INT4 *weight-only* for LLMs. The activation-aware *principle* generalizes (use activation statistics to identify salient channels), but the recipe doesn't fit our INT8-weights + INT8/INT16-activations regime directly.
- **SmoothQuant** — LLM-derived; per RegCache's abstract, "outliers behave differently in vision models versus language models." Smaller gains on ViT than on LLM.
- **TernaryCLIP** ([[sources/TernaryCLIP - 1.58-bit CLIP Compression]] — to-be-filed) — interesting compression but extreme (1.58-bit). Not the right tool for an INT8 retention problem.

## Recommended decision tree for the team

```
1. Run current MobileCLIP2-S2 W8A8 on LPCVC sample. Score Recall@10.
   ├── If R@10 >= 0.74 (within 1% of FP baseline): SHIP IT. Don't optimize further.
   └── Else (R@10 < 0.74):
       2. Try Hub --lite_mp percentage=15;override_qtype=int16.
          ├── If R@10 recovers to ≥ 0.74: SHIP IT.
          └── Else still gap:
              3. Try RegCache (prefix-token outlier absorption).
                 ├── If R@10 recovers: SHIP IT.
                 └── Else still gap:
                     4. Reach for AIMET + AdaRound + per-op INT16.
```

This minimizes effort. Most likely path: Step 2 is enough.

## Cross-references

- [[sources/AXERA MobileCLIP2 w8a16 Deployment]] — cross-vendor w8a16 default for MobileCLIP2
- [[sources/AIMET to QAI Hub Workflow]] — Hub vs AIMET tradeoffs
- [[sources/AWQ - Activation-aware Weight Quantization]] — LLM activation-aware principle
- [[sources/RegCache - Activation Quantization Vision Encoders]] — vision-specific tactic
- [[concepts/INT8 Calibration for Vision-Language Models]] — calibration recipe
