---
type: meta
title: "Page Index — lpcvc-2026-track1"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: project workspace surface
updated: 2026-04-25
---

# Index — LPCVC 2026 Track 1

## Workspace surfaces

- [[projects/lpcvc-2026-track1/overview]] — project overview
- [[projects/lpcvc-2026-track1/hot]] — recent context cache
- [[projects/lpcvc-2026-track1/log]] — operations + ingest log
- [[projects/lpcvc-2026-track1/experiments]] — experiment tracker

## Sources, concepts, entities (filtered to this project)

To find pages tagged with this project's slug, query the vault root:

- `sources/` — papers and external resources tagged `projects.slug == lpcvc-2026-track1`
- `concepts/` — methods/mechanisms relevant to this project
- `entities/` — people, orgs, model families
- `ideas/`, `questions/`, `comparisons/` — speculative + analytical pages

## Filed 2026-04-25 (autoresearch round 1+2)

**Synthesis:**
- [[questions/Research - LPCVC 2026 Track 1 Winning Recipes]]

**Sources:**
- [[sources/EfficientFormer Activation Function Ablation]] — Snap Research, NeurIPS 2022
- [[sources/CLIC - Compositional Awareness in CLIP]] — Tübingen, May 2025
- [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]] — CVPRW 2024
- [[sources/Qualcomm AI Hub Quantization Documentation]] — operational reference
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — Apple, TMLR 2025
- [[sources/AIMET to QAI Hub Workflow]] — operational reference (amended 2026-04-25 with lite_mp)
- [[sources/LPCVC 2025 Cross-Track Lessons]] — secondary writeup of 2025 winners
- [[sources/LPCV 2025 Evaluation Paper]] — primary organizer paper (arXiv 2604.19054)
- [[sources/AXERA MobileCLIP2 w8a16 Deployment]] — only public mobile-NPU MobileCLIP2 deployment (per-encoder latency table)
- [[sources/AWQ - Activation-aware Weight Quantization]] — Lin et al., MIT-Han Lab, 2023 (foundational)
- [[sources/RegCache - Activation Quantization Vision Encoders]] — vision-specific INT8 fix via prefix tokens (arXiv 2510.04547)

**Concepts (added 2026-04-25):**
- [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]] — 3-family decision tree (lite_mp → RegCache → AIMET+AdaRound)

**Synthesis (added 2026-04-25):**
- [[questions/Research - MobileCLIP2 R@10 on Hexagon NPU]] — autoresearch-hybrid validation run synthesis

**Concepts:**
- [[concepts/Activation Function Latency-Accuracy Tradeoff on Mobile NPU]]
- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]
- [[concepts/INT8 Calibration for Vision-Language Models]]
- [[concepts/Hard-Negative Loss for Vision-Language Models]]

**Entities:**
- [[entities/Snap Research]]
