---
type: overview
title: "LPCVC 2026 Track 1 — Image-to-Text Retrieval (Team Manifold)"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: project home page
updated: 2026-04-25
---

# LPCVC 2026 Track 1 — Project Overview

**Team:** Manifold
**Competition:** [2026 LPCVC Track 1](https://lpcv.ai/2026LPCVC/image-text-retrieval/)
**Submission window:** March 1 – **April 30, 2026** (closes in days)
**Codebase:** `/Users/jrauvola/Desktop/lpcvc-submission-team-manifold/`
**Execution-artifact location:** see codebase `manifests/`, `results/`, `quant_model/`

## Task

Image-to-text retrieval. Given an image, retrieve top-K most-relevant text descriptions from a candidate pool by cosine similarity over learned embeddings.

- **Input:** image `float32 (1, 3, 224, 224)` in [0,1] + text tokens `int32 (1, 77)`
- **Tokenizer:** `openai/clip-vit-base-patch32` (fixed by organizers)
- **Metric:** Recall@10 on ~300 organizer-annotated images
- **Hardware:** Qualcomm XR2 Gen 2 via QAI Hub
- **Latency gate:** image + text encoders combined < 35 ms (must beat OpenAI CLIP baseline)

## Current state (as of 2026-04-25)

- **Best model:** MobileCLIP2-S4 — 0.7527 R@10 on sample (FP16 39.3ms image enc, INT8 13.7ms)
- **Pipeline:** export_onnx → compile_and_profile (XR2 Gen 2 target) → upload_dataset → inference → score
- **Active research:** self-training pipeline with LoRA + FAISS index + confidence/negative filters
- **Submission status:** awaiting profile job to verify combined latency budget

## Key constraints (load-bearing)

1. **Submission rule:** Only compiled QNN model cards submitted — no external preprocessing.
2. **Must bake into ONNX:** image resize (224→256 for MobileCLIP2-S4 native), CLIP normalize, L2 normalize.
3. **Text input dtype:** ONNX uses native int64; QNN compile flag `--truncate_64bit_io` handles int32↔int64 at I/O boundary. Do NOT add explicit Cast in graph.
4. **Compositional captions:** organizer captions are contrastively constructed ("grey monitor" vs "black monitor" vs "old monitor") — standard MSCOCO/Flickr benchmarks are saturated and non-predictive.

## Core technical levers

| Lever | Direction | Notes |
|-------|-----------|-------|
| Backbone | MobileCLIP2-S4 (current) → MobileCLIP2-S2 / S3 / B | Trade-off accuracy vs latency |
| Activation | swish/GELU → ReLU / ReLU² / Hard-Swish | swish is XR2 bottleneck per profiling; ReLU fuses into MMA |
| Quantization | QAI Hub INT8 (current) → custom AIMET W8A8 / mixed | Calibration set ≥500 images per the doc |
| Preprocessing | bake resize + normalize in ONNX | Already done; verify Resize is not CPU fallback |
| Fine-tuning | self-training with LoRA on harder data | active development |
| Resolution | 224-native variant (vs 256-native + resize) | distillation candidate |

## Reading order for new context

1. Codebase `AGENTS.md` — submission contract + QAI Hub state
2. Codebase `context/PROBLEM_OVERVIEW.md` — full technical framing
3. [[projects/lpcvc-2026-track1/hot]] — recent context cache
4. [[projects/lpcvc-2026-track1/index]] — page index
5. [[projects/lpcvc-2026-track1/experiments]] — experiment tracker
6. [[meta/projects/REGISTRY]] — project entry
