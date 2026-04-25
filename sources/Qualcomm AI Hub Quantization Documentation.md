---
type: source
source_type: documentation
title: "Qualcomm AI Hub — Quantization Documentation"
venue: "Qualcomm AI Hub Workbench"
date_published: 2026-04-25
authors: ["Qualcomm Technologies"]
url: "https://workbench.aihub.qualcomm.com/docs/hub/quantize_examples.html"
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Authoritative spec for INT8/INT16 quantization on Hexagon NPU — calibration sample requirements, supported precisions, recommended workflow."
key_claims:
  - "QNN runtime supports INT8 weights with INT8 OR INT16 activations. ONNX runtime: same. TFLite: INT8 weights + INT8 activations only."
  - "Recommended calibration sample size: tutorial uses 100; production deployment requires 500–1000 samples."
  - "Calibration data should be representative (preprocessed, real samples) not random — random data is only valid for 'quick benchmark' scenarios."
  - "Mixed precision (different ops at different precisions) is NOT currently supported across runtimes."
  - "Recommended workflow: source model → optimized ONNX → quantize with calibration → compile to QNN context binary with --quantize_io."
  - "Compiling to ONNX before quantizing 'allows the compiler to run optimization passes' — improves accuracy preservation."
  - "Hexagon HMX unit supports INT4, INT8, INT16, FP16."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Qualcomm AI Hub Quantization Documentation

## Summary

Authoritative reference for quantizing models for Qualcomm Hexagon NPU via QAI Hub. Confirms the team's existing assumptions about calibration set size (500+ images per `context/PROBLEM_OVERVIEW.md`) and adds operational detail on the recommended workflow.

## Supported precision combinations

| Runtime | Weights | Activations |
|---------|---------|-------------|
| TFLite | INT8 | INT8 only |
| QNN | INT8 | INT8 or INT16 |
| ONNX Runtime | INT8 | INT8 or INT16 |

**Mixed precision** (different ops at different precisions) is NOT currently supported. This is a constraint when ops like LayerNorm or softmax need higher precision than the bulk of matmuls.

## Calibration set requirements

- **Tutorial example:** 100 samples (insufficient for production)
- **Production recommendation:** 500–1000 representative samples
- **Random data:** valid only for benchmark, NOT for accuracy-sensitive deployment
- **Format:** preprocessed in the same format the deployed model expects

## Recommended workflow

1. Source model (PyTorch or ONNX)
2. Compile to **optimized ONNX** first — lets the compiler run graph-level optimization passes that improve quantization accuracy
3. Quantize the optimized ONNX with calibration data
4. Compile quantized ONNX to QNN context binary using `--quantize_io` flag
5. Profile on target device (XR2 Gen 2) for latency and Recall@10 verification

The optimization-pass step is load-bearing — quantizing a raw export typically loses more accuracy than quantizing a graph the compiler has cleaned up.

## Hardware notes

- Hexagon HMX (matrix unit) supports INT4, INT8, INT16, FP16.
- INT8 matmul throughput is roughly 4× FP16 on Qualcomm NPU (general industry figure, not directly stated in this doc but consistent with the team's measured 39.3 ms → 13.7 ms speedup for MobileCLIP2-S4 image encoder).

## What this confirms / changes for the team

- ✅ The team's "500+ images for calibration" rule (per `context/PROBLEM_OVERVIEW.md`) matches Qualcomm's official guidance.
- ⚠️ Verify the team is compiling to ONNX *before* quantizing, not quantizing the raw PyTorch export. If `export_onnx.py` runs raw export and `quantize_utils.py` quantizes that directly, there's a missing optimization pass.
- ⚠️ INT16 activations are an option if pure INT8 hurts Recall@10 too much. Worth a single comparison run at submission time.

## Cross-references

- [[concepts/INT8 Calibration for Vision-Language Models]]
- [[concepts/QNN Compile Pipeline for Mobile CLIP]]
