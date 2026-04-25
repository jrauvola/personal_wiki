---
type: source
source_type: competition_analysis
title: "LPCVC 2025 Cross-Track Winning Patterns"
venue: "LPCVC 2025 (CVPR Workshop)"
date_published: 2025-06-01
authors: ["LPCVC Organizers (compiled)"]
url: "https://lpcv.ai/2025LPCVC/winners/"
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "LPCVC 2025 is the only relevant prior — 2024 didn't run. 2025 used the same QAI Hub workflow as 2026. Track 2 (text-conditioned segmentation) is the closest VL analog."
key_claims:
  - "There was no LPCVC 2024 — the series went on hiatus and relaunched 2025 under Qualcomm sponsorship with QAI Hub workflow."
  - "Track 1 winner LabLVM (Ajou U.) — image classification, Snapdragon 8 Elite, 0.974 acc, 1.6 ms. Lead's quote: 'Vision-language models proved surprisingly effective; synthetic data underperformed expectations.'"
  - "Track 2 winner SICer (Southeast U.) — text-conditioned segmentation (open-vocab), Snapdragon X Elite. SEUDecoder approach: 0.61 mIoU vs 0.46 baseline, 515 ms vs 863 ms."
  - "Track 2 pattern (most relevant to LPCVC 2026 Track 1): frozen vision-language backbone + small fine-tuned decoder/head. 3rd-place team explicitly fine-tuned XDecoder rather than replacing backbone."
  - "Track 3 (monocular depth) winner Sailor Moon (UMN) — EfficientDepth, F=83.8 in 29.8 ms vs baseline 62.4/24.1. Lead's quote: 'Reducing image resolution significantly improves running time while having only a minor impact on accuracy, especially for ViT-based architectures.'"
  - "2025 had 59 teams, 14 countries, 516 submissions. Student teams beat industry teams (founder's quote). Iteration count and AI Hub fluency mattered more than headcount."
  - "Cross-cutting patterns: (a) frozen well-quantising VL backbone + small fine-tuned head, (b) resolution down-shifting for ViT latency wins, (c) avoid bleeding-edge SOTA backbones — pick architectures known to quantize well, (d) calibration must be in-domain not external, (e) re-parameterization at inference."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# LPCVC 2025 Cross-Track Winning Patterns

## Why this matters

LPCVC 2026 Track 1 (image-to-text retrieval) is novel. LPCVC 2024 never ran. **LPCVC 2025 is the only relevant prior** — same Qualcomm AI Hub submission workflow, same compile-job-share pattern, same XR2/X-Elite-class Snapdragon hardware.

Track 2 specifically (open-vocabulary segmentation conditioned on a text prompt) is the closest vision-language analog — same dual-encoder retrieval-style pattern.

## Track-by-track summary

### Track 1 — Image Classification (Snapdragon 8 Elite)
**Winner:** LabLVM (Ajou University, Korea). Score 0.974 / latency 1.6 ms.

Key quote from team lead: *"Vision-language models proved surprisingly effective; synthetic data underperformed expectations."*

**Read-across to LPCVC 2026:** even on a classification task, VLM-derived encoders out-competed pure CV models. Strong prior that CLIP-family is the right starting point for our retrieval task.

### Track 2 — Open-Vocabulary Segmentation (Snapdragon X Elite) ⭐ MOST RELEVANT
**Winner:** SICer (Southeast University). SEUDecoder. 0.61 mIoU vs 0.46 baseline, 515 ms vs 863 ms.

This is the closest analog to LPCVC 2026 Track 1: a text-conditioned vision task with both image and text encoders. Pattern that won:

- **Frozen vision-language backbone** (no full retraining)
- **Small fine-tuned decoder/head** (the part that actually adapts to task)
- 3rd-place team **explicitly fine-tuned the XDecoder baseline** rather than replacing the backbone

**For LPCVC 2026 retrieval, the analog is:** freeze a well-quantizing CLIP/MobileCLIP backbone, fine-tune only what's necessary (text encoder via CLIC, or a thin projection head). Don't replace the well-validated INT8 image graph.

> [!gap] No public per-team writeup for SICer/SEUDecoder. Architecture and quantization details not published. Worth direct outreach to Southeast U. SoIC team or scraping conference talk slides if available.

### Track 3 — Monocular Depth (Snapdragon 8 Elite)
**Winner:** Sailor Moon (UMN). EfficientDepth, F=83.8 in 29.8 ms vs baseline 62.4/24.1.

Key quote from team lead: *"Reducing image resolution significantly improves running time while having only a minor impact on accuracy, especially for ViT-based architectures."*

**For LPCVC 2026:** test 192px and 160px CLIP variants. The MobileCLIP family is natively 256px; the team is already accepting a 224 input for the contract. Going below 224 may give meaningful latency wins for small accuracy cost.

2nd and 3rd place both used DepthAnything-V2 derivatives — established architecture wins over novel.

## Cross-cutting recipes that repeat

Patterns that appear in LPCVC 2023 and LPCVC 2025 (cross-validated):

1. **Encoder split + separate compilation.** Image and text encoders deploy as independent QNN binaries. Text embeddings precomputable for fixed candidate pool — almost all wall-clock budget should go into image encoder.
2. **Frozen well-quantising backbone + small fine-tuned head.** SICer (2025 T2), XDecoder fine-tunes (2025 T2), AidgetRock (2023 podium #2 with KD+pruning).
3. **Resolution down-shifting** — cheapest single latency win for ViT-class encoders.
4. **Knowledge distillation from a larger teacher onto deployed student** — used by 2/3 podium teams in 2023. Most-repeated tactic across LPCV history.
5. **Re-parameterization** — fold multi-branch training blocks into single convs at export. ModelTC (2023 winner) and FastViT/MobileOne literature both rely on this.
6. **Avoid bleeding-edge SOTA backbones** unless evidence they quantize cleanly. PSPNet/SegFormer/SeaFormer were tried and lost in 2023; 2025 winners stuck to MobileNetV2 / XDecoder / DepthAnythingV2 — established, well-tooled architectures.
7. **W8A16 baseline for transformer/attention models.** Pure W8A8 typically fails on attention activation outliers.
8. **Calibration set must come from in-domain data**, not external. (2023 organizers' explicit finding.) For LPCVC retrieval, calibrate on the LPCVC sample + retrieval-distribution data, not LAION subsamples.
9. **Iteration speed beats headcount.** Student teams (1-3 people) won most 2025 tracks. The QAI Hub compile-and-profile cycle is fast — budget for tens of iterations per day, not 2-3.

## Direct application to LPCVC 2026 Track 1

**P0:** Adopt the SEUDecoder pattern — freeze the CLIP image backbone, fine-tune only what's necessary on the text side. Validates the [[sources/CLIC - Compositional Awareness in CLIP]] approach the team is already considering.

**P1:** Try input resolution down-shift to 192px (Track 3 lesson). The team's contract is 224px, so they're already shrinking from native 256; 192 is the next step.

**P2:** Distill from a larger CLIP teacher (e.g., DFN2B-CLIP-ViT-L-14 or SigLIP2-SO400M image encoder) into the deployed MobileCLIP student. Track 2/3 winners used this; pattern repeats across years.

## Cross-references

- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]] — why frozen-vision works
- [[concepts/Knowledge Distillation for Mobile CLIP Retrieval]] — distillation recipe details
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — architecture truth source

## Sources used
- https://lpcv.ai/2025LPCVC/winners/ — official 2025 winners list
- https://www.computer.org/publications/tech-news/insider-membership-news/2025-low-power-computer-vision-challenge — IEEE writeup with team-lead quotes
- https://www.edge-ai-vision.com/2025/06/low-power-computer-vision-challenge-empowering-ai-development-on-edge-devices/ — confirms target devices and AI Hub workflow
- arXiv 2403.07153 — LPCVC 2023 results paper (cross-cutting patterns)
- https://github.com/lpcvai/LPCVC_AIHub_Guide — canonical submission walkthrough
