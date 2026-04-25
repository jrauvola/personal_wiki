---
type: entity
entity_type: organization
title: "Snap Research"
projects:
  - slug: lpcvc-2026-track1
    relevance: secondary
    why: "Authors of EfficientFormer / EfficientFormerV2 — the canonical mobile vision transformer reference for NPU latency."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Snap Research

## Role

Snap Inc.'s research arm. For LPCVC 2026 Track 1 purposes, the relevant body of work is mobile vision transformer architectures, specifically the EfficientFormer series.

## Relevant publications

- **EfficientFormer** (NeurIPS 2022) — vision transformers at MobileNet speed. Established the dimension-consistent 4D/3D block design, fast patch embedding, and CONV-BN normalization tactics. [[sources/EfficientFormer Activation Function Ablation]]
- **EfficientFormerV2** (ICCV 2023, "Rethinking Vision Transformers for MobileNet Size and Speed") — follow-up with further latency improvements; achieves 3.5% higher top-1 than MobileNetV2 with similar latency.

## GitHub

- `snap-research/EfficientFormer` — both V1 and V2 code, weights, and per-device latency tables (iPhone 12 ANE measured).

## Why the team should care

EfficientFormer's latency-driven slimming methodology and per-hardware activation ablation are the most useful published reference for what works on mobile NPU. The numbers don't transfer 1:1 to Qualcomm Hexagon (different compiler, different kernel coverage), but the methodology — measure on target, swap for measured wins, prefer architectural to activation-level changes — is correct.
