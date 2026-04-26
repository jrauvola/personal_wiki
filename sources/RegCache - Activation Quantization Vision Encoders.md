---
type: source
source_type: paper
title: "RegCache — Activation Quantization of Vision Encoders Needs Prefixing Registers"
arxiv_id: "2510.04547"
venue: "arXiv"
date_published: 2025-10
authors: []
url: "https://arxiv.org/abs/2510.04547"
code_repo: null
has_weights: false
status: triaged
confidence: medium
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Directly addresses vision-encoder activation quantization (THE problem the team is solving for INT8 R@10 retention on MobileCLIP image tower). Training-free. Vision-specific (not LLM-derived)."
key_claims:
  - "Vision encoders suffer from activation outliers during quantization, particularly at 8-bit and lower precision."
  - "Proposed method: insert outlier-prone yet semantically meaningless prefix tokens to the vision encoder. These tokens absorb outliers, preventing other tokens from having outliers."
  - "Two innovations distinguish from LLM-derived techniques: (a) middle-layer prefixing (rather than input-layer only), (b) token deletion."
  - "Method is training-free."
  - "Authors note vision-model outliers behave differently from LLM outliers — explicitly addresses why LLM tactics (SmoothQuant, AWQ) need adaptation."
  - "Specific INT8 accuracy gains not stated in abstract; emphasizes 'particularly in extremely low-bit regimes (e.g., 4-bit)'."
last_reviewed: 2026-04-25
reviewed_by: autoresearch-hybrid
---

# RegCache — Activation Quantization of Vision Encoders Needs Prefixing Registers

## Why this matters

Surfaced via S2 citation graph from MobileCLIP2 anchor — papers that cite MobileCLIP2 and address vision encoder quantization. **Not surfaced by WebSearch keyword search.** This paper is exactly aligned with the team's open question: **how do you quantize MobileCLIP image encoder to INT8 without losing R@10?**

## The technique (prefixing registers / "RegCache")

Vision encoders accumulate activation outliers at certain attention positions. These outliers force the calibrator to use a wide quantization range, which crushes precision for the bulk of (non-outlier) activations.

RegCache's fix:
1. Insert **prefix tokens** at the input — semantically meaningless, but designed to absorb outliers.
2. Outliers concentrate on these prefix tokens during inference.
3. Other tokens stay clean, quantize accurately at INT8.
4. **Token deletion** removes the prefix tokens before downstream use.

Two key differences from LLM-derived methods:
- **Middle-layer prefixing**, not just input layer (vision outliers emerge at depth)
- **Token deletion** as part of the pipeline

## Why LLM quantization tactics don't directly transfer

Per the abstract: "outliers behave differently in vision models versus language models." This is exactly why methods like AWQ ([[sources/AWQ - Activation-aware Weight Quantization]]) and SmoothQuant work for LLMs but show smaller gains on ViT/CLIP. RegCache is purpose-built for vision encoders.

## What this means for the team

If pure W8A8 hurts MobileCLIP2 R@10 retention, **RegCache is a more targeted fix than reaching for AIMET AdaRound** because:
- **Training-free** (no fine-tuning required)
- **Vision-specific** (not LLM-derived — matches the actual failure mode)
- Likely complementary with `--lite_mp` (Hub flag for partial mixed precision per [[sources/AIMET to QAI Hub Workflow]])

> [!gap] Concrete INT8 accuracy gains on CLIP/MobileCLIP not in the abstract. Need to fetch the full paper PDF to confirm magnitude of gain. Test on the team's actual MobileCLIP2-S2 INT8 export to know if it moves the needle.

> [!gap] Code availability not confirmed (no code_repo field on S2 record). Worth checking arXiv page for repo link.

## Cross-references

- [[sources/AWQ - Activation-aware Weight Quantization]] — alternative LLM-derived approach
- [[concepts/Activation-Aware Quantization Tactics for Vision Encoders]] — synthesis page
- [[sources/MobileCLIP2 Architecture and FastViT-MCi Family]] — the architecture this would target
