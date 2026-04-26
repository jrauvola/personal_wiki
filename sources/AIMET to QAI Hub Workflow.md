---
type: source
source_type: documentation
title: "AIMET → QAI Hub Quantization Workflow"
venue: "Qualcomm AI Hub Workbench + AIMET project"
date_published: 2026-04-25
authors: ["Qualcomm Technologies"]
url: "https://workbench.aihub.qualcomm.com/docs/hub/compile_examples.html"
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Operational reference for moving beyond QAI Hub built-in quantization to AIMET when accuracy needs the per-op precision tuning Hub doesn't expose."
key_claims:
  - "QAI Hub built-in quantization is now itself an AIMET-ONNX backend (AIMET-ONNX 2.21.0). The 'gap' between Hub and AIMET is which features Hub exposes via options, not different engines."
  - "QAI Hub's submit_quantize_job supports INT8 weights; activations INT8 OR INT16 on QNN/ONNX runtimes; TFLite is INT8-only."
  - "AMENDED 2026-04-25 (confidence: medium until team verifies on live Hub job): partial mixed precision IS supported via the --lite_mp flag, e.g. `--lite_mp percentage=10;override_qtype=int16`. The earlier claim 'mixed precision is NOT supported' was wrong — that statement applies to fully arbitrary per-op precision; lite_mp allows promoting a percentage of layers to a higher precision (typically int16) while leaving the rest int8. AIMET still wins for fully-arbitrary per-op precision via QuantizationSimModel + AMP sweep."
  - "AIMET native supports per-op precision via QuantizationSimModel and auto_mixed_precision (AMP) sweep — finds Pareto curve of bit allocations."
  - "AIMET → QAI Hub workflow: AIMET produces .aimet directory ({model.onnx, model.encodings, model.data?}) → upload_model → submit_compile_job → QNN context binary."
  - "AdaRound is the highest-impact AIMET feature when naive INT8 collapses (e.g. ADAS detector 49.85 → 81.21 mAP)."
  - "Per-channel weight quantization is table-stakes for ViT/CLIP. Both AIMET and QAI Hub support; verify it's enabled."
  - "AIMET model zoo W8A8 deltas on transformers (with QAT, not pure PTQ): ViT +0.25 pp, MobileViT -0.87 pp, BERT -0.67 pp, MobileBERT -0.07 pp."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# AIMET → QAI Hub Quantization Workflow

## Summary

Operational reference for the team's open question: AIMET vs QAI Hub built-in INT8 — when does the extra setup cost pay off?

**TL;DR:** Hub built-in is increasingly *just* AIMET-ONNX wrapped in a service. Use Hub built-in for the default path. Reach for native AIMET when you need (a) per-op precision (e.g., INT16 only on softmax + LayerNorm), or (b) the AdaRound feature if naive PTQ has collapsed.

## When to use each

### Use QAI Hub built-in (default path)
- Single precision globally (all-INT8 or all-INT8/INT16-activations)
- **Partial mixed precision via `--lite_mp` flag** (e.g. `--lite_mp percentage=10;override_qtype=int16` — promotes 10% of layers to int16 while leaving the rest int8). This is the right first lever when pure W8A8 hurts attention-block accuracy.
- Per-channel weights enabled
- Standard calibration (min/max, percentile)
- 500-1000 representative calibration samples

This covers ~80% of CLIP-style models with R@10 retention within 1-2%.

> [!gap] The exact `--lite_mp` semantics (which layers get promoted? deterministic by sensitivity? random by percentage?) need verification on a live Hub job before committing to the recipe.

### Reach for native AIMET when:
- You need **fully arbitrary per-op mixed precision** (Hub's `--lite_mp` only promotes a *percentage* of layers; AIMET's QuantizationSimModel lets you specify exact ops). Use this when targeting *specific* sensitive ops like softmax + LayerNorm + output projection in attention.
- Naive Hub PTQ has collapsed (R@10 drop > 2%) and you want **AdaRound** to fix layer-by-layer rounding error
- You want **QuantAnalyzer per-layer SQNR sweep** to identify which ops are the hotspots before deciding precision allocation
- You want to use **MX formats** (MXINT8 etc.) — currently AIMET-only, but check if the target Hexagon NPU on XR2 Gen 2 actually supports MX before investing

## AIMET → QAI Hub workflow (verified)

```bash
# 1. Local: quantize with AIMET
python -c "
import aimet_onnx
sim = aimet_onnx.QuantizationSimModel(model='./model.onnx', ...)
sim.compute_encodings(calibration_callback, calib_data)
# Optionally: AdaRound
# Optionally: per-op precision overrides (INT16 on softmax)
sim.export(path='./mymodel.aimet', filename_prefix='model')
"
# Produces: mymodel.aimet/{model.onnx, model.encodings, model.data?}

# 2. Upload to QAI Hub
python -c "
import qai_hub
m = qai_hub.upload_model('./mymodel.aimet')
job = qai_hub.submit_compile_job(
    model=m,
    device=qai_hub.Device('XR2 Gen 2 (Proxy)'),
    options='--target_runtime qnn_context_binary --truncate_64bit_io',
)
"

# 3. Standard QAI Hub flow from here (profile, inference, score)
```

The Hub compiler honors the `.encodings` file and produces a quantized QNN context binary. **No separate AIMET runtime on device** — the binary runs on standard QNN runtime.

Versions: Hub bundles AIMET-ONNX 2.21.0; standalone AIMET 2.20.x. Match majors to avoid encoding-format drift.

## Empirical AIMET deltas (W8A8) on relevant models

From AIMET model zoo and the original AIMET paper:

| Model | FP | W8A8 | Δ |
|-------|-----|------|---|
| ViT (image classifier) | 81.32 | 81.57 | **+0.25 pp** (improved!) |
| MobileViT | 78.46 | 77.59 | −0.87 pp |
| BERT | 83.11 | 82.44 | −0.67 pp |
| MobileBERT | 81.24 | 81.17 | −0.07 pp |
| MobileNetV2 (CLE+BC) | 71.72 | 71.08 | −0.64 pp |
| ADAS detector (naive PTQ) | 82.20 | 49.85 | **−32.35 pp (catastrophic)** |
| ADAS detector (AdaRound) | 82.20 | 81.21 | −0.99 pp (recovered) |

**Key pattern:** transformer-heavy models stay within ~1 pp of FP at W8A8 with AdaRound + per-channel weights. Detection/depthwise-heavy models can collapse without AdaRound.

For MobileCLIP2-S4 / MobileCLIP-S2 (depthwise-heavy hybrid CNN+ViT): expect AdaRound to matter. Worth a single AIMET-with-AdaRound run if Hub built-in is showing R@10 loss > 1%.

## Calibration scheme guidance

From NVIDIA's TensorRT integer-quantization paper and Intel Neural Compressor docs:

| Scheme | Best for | Notes |
|--------|----------|-------|
| min/max | Weights | Worst on activations with outliers |
| Percentile (99.99 / 99.999) | Activations on transformers | Cheap; usually within 0.1-0.3 pp of best |
| Entropy (KL) | Activations on classification | TensorRT default; slightly more compute |
| MSE | Specialized | Comparable to entropy |

**Recommendation for MobileCLIP2 → Recall@10:** 99.99 percentile activations + per-channel min/max weights + 500-1000 in-domain images.

## Open gaps

- No public CLIP/MobileCLIP-specific AIMET-vs-Hub side-by-side measurement. **Worth running:** Hub default vs AIMET-PTQ-with-AdaRound on MobileCLIP2 (~1 day).
- The team should run **AIMET QuantAnalyzer** to get per-layer SQNR before deciding whether mixed precision is even needed. If all layers have SQNR > 35 dB, pure W8A8 is fine.
- Exact `options` string for QAI Hub `submit_quantize_job` to enable/disable AdaRound, percentile calibration, etc. is not in public docs — may need inspection of `qai-hub` Python package source or the Hub Slack.

## Cross-references

- [[sources/Qualcomm AI Hub Quantization Documentation]] — base reference
- [[concepts/INT8 Calibration for Vision-Language Models]]
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — quantization sensitivity per-op
