---
type: source
source_type: paper
title: "AWQ — Activation-aware Weight Quantization for On-Device LLM/VLM Compression"
arxiv_id: "2306.00978"
venue: "MLSys 2024"
date_published: 2023-06-01
authors: ["Ji Lin", "Jiaming Tang", "Haotian Tang", "et al. (MIT-Han Lab)"]
url: "https://arxiv.org/abs/2306.00978"
code_repo: "https://github.com/mit-han-lab/llm-awq"
has_weights: false
status: triaged
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: secondary
    why: "Activation-aware quantization principle (use activation statistics to identify salient weight channels) directly applies to MobileCLIP image encoder calibration. Paper focuses on INT4 weight-only LLM quant; principle generalizes."
key_claims:
  - "Not all weights in an LLM are equally important — protecting only ~1% salient weights greatly reduces quantization error."
  - "Identifies salient channels via OFFLINE activation statistics (not via backprop or reconstruction). Generalizes across domains/modalities without overfitting calibration set."
  - "Applies equivalent transformations: scales salient weight channels rather than keeping them in higher precision."
  - "Reported for 4-bit weight-only quantization. Method principle generalizes to INT8/INT16 — needs adaptation."
  - "Not directly tested on CLIP / MobileCLIP in the paper. Vision-Language LLMs mentioned but no specific accuracy numbers given."
  - "1253 citations as of 2026-04-25 — foundational reference for activation-aware PTQ."
last_reviewed: 2026-04-25
reviewed_by: autoresearch-hybrid
---

# AWQ — Activation-aware Weight Quantization

## Why this matters

Surfaced via S2 citation graph from TernaryCLIP (a CLIP-quantization paper). **Not surfaced by WebSearch keyword search in 4 prior autoresearch rounds.** Foundational reference (1253 citations) for the principle behind activation-aware calibration.

## The principle (transferable to our INT8 problem)

> "Refer to the activation distribution" to identify critical weight channels.

Concretely: collect activation statistics offline → identify channels with high-magnitude activations → those channels' weights are "salient" → either keep them in higher precision OR apply equivalent transformations (scale them up, scale corresponding inputs down) so they survive quantization with minimal error.

This is the same insight behind:
- AIMET's per-channel weight quantization (per [[sources/AIMET to QAI Hub Workflow]])
- SmoothQuant (W8A8 LLM quant)
- The 99.99-percentile calibration strategy for transformer activations

## What the paper actually demonstrates

- Tests on LLMs (Llama-2-70B etc.) at **4-bit weight-only quantization**
- Mentions multimodal LMs (CLIP-related) but no specific Recall@K numbers in the abstract
- Demonstrates 70B Llama-2 on mobile GPUs

## What the team can take from it

1. **Calibration data quality > size beyond a threshold.** AWQ generalizes across domains because it uses *statistics*, not reconstruction objectives. The team's existing 500+ image calibration set ([[concepts/INT8 Calibration for Vision-Language Models]]) is enough — focus on representativeness, not volume.
2. **Per-channel weight scaling is the critical operation.** AWQ formalizes why per-channel matters. Per [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]], per-channel is mandatory for MCi depthwise convs anyway.
3. **The principle does NOT require AdaRound or QAT.** AWQ is post-training and offline. Cheaper than AIMET's AdaRound; complementary if applied together.

> [!gap] AWQ is INT4 weight-only. Direct application to INT8 weights + INT8/INT16 activations needs adaptation. Paper does not provide the adapted recipe.

## Cross-references

- [[concepts/INT8 Calibration for Vision-Language Models]] — calibration recipe
- [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]] — synthesizes this paper + RegCache
- [[sources/AIMET to QAI Hub Workflow]] — alternate path with AdaRound

## Sources used
- arXiv abstract: https://arxiv.org/abs/2306.00978
- S2 citation graph from TernaryCLIP (2510.21879)
