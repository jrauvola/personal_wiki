---
type: concept
title: "INT8 Calibration for Vision-Language Models on Mobile NPU"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Calibration set quality directly determines Recall@10 retention after INT8 quantization. The team's pipeline is the load-bearing path to the 13.7 ms latency."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# INT8 Calibration for Vision-Language Models on Mobile NPU

## Concept

Post-training W8A8 quantization (INT8 weights, INT8 activations) on Hexagon NPU requires a calibration pass: feed the model a small set of representative inputs, record per-tensor min/max activation ranges, compute scale + zero-point per tensor. Quality of the calibration set determines accuracy retention.

For CLIP-family vision-language models, the calibration set is normally the IMAGE side (text encoder takes int32 token IDs and is less sensitive). The team's existing pipeline uses W8A8 via QAI Hub built-in or local ONNX Runtime AIMET.

## Hard-won numbers (from autoresearch)

- **Qualcomm AI Hub recommendation:** 500–1000 representative samples for production deployment ([[sources/Qualcomm AI Hub Quantization Documentation]]).
- **Random data is NOT acceptable** for accuracy-sensitive deployment — only for "quick benchmark" runs.
- **The team's `context/PROBLEM_OVERVIEW.md` notes:** "Local ONNX Runtime W8A8 needs 500+ representative images; 50–100 causes large accuracy drop." This matches Qualcomm's recommendation.

## What "representative" means for LPCVC

The LPCVC test set is ~300 organizer-annotated images of arbitrary objects. The team only sees a 56-image sample. Calibration set construction options, ranked:

1. **Best: union of LAION + LPCVC sample + open retrieval data** filtered for the object types likely to appear (general objects, not faces or specific verticals). Aim for 1000+ images.
2. **Good: a curated subset of MS-COCO val + Flickr30K + LPCVC sample** — covers everyday objects, varied lighting, ~150 categories. ≥500 images.
3. **Risky: LPCVC sample only (56 images)** — under-represents activation distribution; large accuracy drop expected per existing team note.

## QAI Hub built-in vs custom AIMET

- **QAI Hub built-in INT8 quantization** is the workflow currently in use. Reduces image encoder 39.3 ms → 13.7 ms (2.9× speedup) per the team's own measurement.
- **Custom AIMET** (Qualcomm's research toolkit) allows finer-grained control: per-tensor vs per-channel weight quantization, mixed precision, advanced calibration schemes (entropy, percentile, MSE).
- **Mixed precision is currently unsupported** across QAI Hub runtimes ([[sources/Qualcomm AI Hub Quantization Documentation]]). If pure INT8 hurts Recall@10, INT16 activations (still INT8 weights) on QNN are the next step *before* AIMET.

## Workflow recommendation (per Qualcomm docs + team context)

1. Source PyTorch / open_clip model
2. **Compile to optimized ONNX FIRST** — this lets graph passes simplify ops before quantization. Skipping this step is a common accuracy regression cause.
3. Quantize with calibration set (≥500 representative images)
4. Compile quantized ONNX to QNN context binary with `--target_runtime qnn_context_binary --truncate_64bit_io`
5. Profile on XR2 Gen 2 (verify combined latency < 35 ms)
6. Score Recall@10 on LPCVC sample set
7. If Recall@10 drop > 1–2%: try INT16 activations (INT8 weights kept)

## Verification step the team has not (visibly) done

The team's `context/PROBLEM_OVERVIEW.md` lists "Inspect `quant_model/*.h5` and run through sample harness to verify quantization" as a TODO. This is the load-bearing diagnostic — without it, you can't know whether INT8 has cost you 1% or 10% of Recall@10. **Should run this before submission.**

## Open questions

- What's the actual measured Recall@10 of MobileCLIP2-S4 INT8 on the LPCVC sample? Per the team's table, "TBD."
- Would per-channel weight quantization (vs per-tensor) recover any accuracy on FastViT-MCi2's depthwise convs?
- Is the text encoder quantization-friendly at INT8, or does it need INT16? (Tokenizer-fed integer inputs make it less sensitive, but the embedding lookup table can suffer.)

## Cross-references

- [[sources/Qualcomm AI Hub Quantization Documentation]]
- [[concepts/QNN Compile Pipeline for Mobile CLIP]]
