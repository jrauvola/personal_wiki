---
type: source
title: "OneLatent — Single-Token Compression for Visual Latent Reasoning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/multimodal
  - type/source
  - method/single-token-compression
  - method/ocr-supervision
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/2602.13738-onelatent]]"
source_type: paper
arxiv_id: "2602.13738"
venue: "arXiv"
date_published: 2026-02-14
authors:
  - "Bo Lv"
  - "Yasheng Sun"
  - "Junjie Wang"
  - "Haoxiang Shi"
url: "https://arxiv.org/abs/2602.13738"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "OneLatent compresses intermediate reasoning into a single latent token via supervision from rendered CoT images and DeepSeek-OCR hidden states."
  - "By rendering textual steps into images, we obtain a deterministic supervision signal that can be inspected and audited without requiring the model to output verbose textual rationales."
  - "OneLatent reduces average output length by 11× with only a 2.21% average accuracy drop relative to textual CoT, while improving output token contribution (OTC) by 6.8×."
  - "On long-chain logical reasoning, OneLatent reaches 99.80% on ProntoQA and 97.80% on ProsQA with one latent token, with compression up to 87.4×."
projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Multimodal visual-supervision approach; not a Qwen3 scaling signal."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No grad-stability discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: reference
    why: "Alternate anchoring strategy (render text → image → OCR hidden state) contrasts with LT-Tuning's in-model vocab-space anchoring. Reference only — not a recipe we'd adopt, but a taxonomic comparison point."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Extreme-compression result (87.4× on long-chain logic, 99.80% ProntoQA with ONE latent token) is a notable counterpoint to the literature's usual multi-token-budget framing. Worth citing in the SPAR writeup's compression-tradeoff section."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# OneLatent — Single-Token Compression for Visual Latent Reasoning

## TL;DR

Compresses an entire CoT into a **single latent token**, supervised by rendering the text CoT to an image and targeting **DeepSeek-OCR hidden states** at that token position. The OCR-derived supervision is deterministic, inspectable, and auditable. 11× avg output length reduction at 2.21% avg accuracy cost vs textual CoT; 6.8× OTC improvement. On long-chain logic: 99.80% ProntoQA, 97.80% ProsQA with **one** latent token (up to 87.4× compression).

## Method

- Render text CoT → image → feed through DeepSeek-OCR → extract hidden states.
- Use those hidden states as the supervision target for a single latent token in the main LM's reasoning pipeline.
- At inference: model emits one latent token instead of multi-token CoT.

## Recipe

- DeepSeek-OCR as external supervision tower.
- Base LM + loss weights in PDF.

## Results

- 11× output length reduction (avg).
- 2.21% avg accuracy drop relative to textual CoT.
- 6.8× OTC improvement.
- ProntoQA 99.80%, ProsQA 97.80% — near-saturation with one latent token.
- Up to 87.4× compression on long-chain logical reasoning.

## Relevance

- **Novel supervision source**: using a vision model's hidden states to anchor a language model's latent reasoning token. SIM-CoT uses the LM's own CoT-token heads; OneLatent uses an **external vision model's OCR pathway**.
- Single-token compression is a design extreme. Counter-signal: at 87.4× compression on ProntoQA, reasoning may be happening in the OCR model's pre-trained circuits rather than in the main LM's latent.
- Not a direct recipe for LT-Tuning / branch-d; conceptually interesting.

## Citations

- Discovered via SIM-CoT downstream citation graph.
