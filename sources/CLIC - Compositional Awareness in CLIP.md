---
type: source
source_type: paper
title: "CLIC — Advancing Compositional Awareness in CLIP with Efficient Fine-Tuning"
arxiv_id: "2505.24424"
venue: "arXiv"
date_published: 2025-05-30
authors: ["Amit Peleg", "Naman Deep Singh", "Matthias Hein"]
url: "https://arxiv.org/abs/2505.24424"
code_repo: null
has_weights: true
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Compositionality fine-tuning at 0.01% of pretraining cost — directly addresses the team's contrastive-caption failure mode, fits the 5-day deadline."
key_claims:
  - "Freezes the vision encoder and fine-tunes only the text encoder — costs ~0.01% of CLIP pretraining compute."
  - "Concatenated image-pair training: 4 positive captions + 1 hard negative per image pair, with combined contrastive + hard-negative + uni-modal loss."
  - "On SugarCrepe Replace: 86.5% ITT (image-to-text), 84.8% on Swap. On SugarCrepe++ Replace: 76.0% ITT, 61.5% Swap."
  - "Improves WinoGround text/image/group scores over baseline CLIP."
  - "Maintains MS-COCO retrieval — CLIPS+CLIC reports +1.3% text retrieval and +2.2% image retrieval over baseline."
  - "Training data: 1M samples from CogVLM-recaptioned LAION + PixelProse-recaptioned RedCaps + CC12M subsets, deliberately independent of MS-COCO for zero-shot integrity."
  - "Maintains zero-shot classification capabilities with minimal degradation."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# CLIC — Compositional Awareness in CLIP

## Summary

CLIC (Peleg, Singh, Hein, Tübingen, May 2025) is a parameter-efficient compositionality fine-tune for CLIP. The headline number — 0.01% of pretraining compute for substantial SugarCrepe / WinoGround gains — makes it the highest-yield candidate for improving Recall@10 on LPCVC's contrastive captions inside the 5-day window.

## Method

- **Frozen vision encoder.** Only the text encoder is fine-tuned. Avoids breaking the strong MobileCLIP2 vision backbone the team has already validated.
- **Concatenated image pairs.** Two images glued side-by-side, with 4 positive captions (referring to either constituent or composition) and 1 hard negative.
- **Loss:** weighted combination of contrastive loss, hard-negative loss, and uni-modal (text–text) loss.

## Numbers that matter

**SugarCrepe (image-to-text accuracy):**
- Replace: 86.5%
- Swap: 84.8%

**SugarCrepe++ (harder, with paraphrase distractors):**
- Replace: 76.0%
- Swap: 61.5%

**WinoGround:** improvements across text/image/group scores over baseline CLIP.

**MS-COCO retrieval (no degradation):** CLIPS+CLIC reports +1.3% text retrieval and +2.2% image retrieval relative to baseline.

## Why this fits LPCVC 2026 Track 1

The competition's organizer captions are deliberately constructed in a contrastive style — "the grey monitor" vs. "the black monitor" vs. "the old monitor" — exactly the failure mode CLIC targets. Standard CLIP fine-tunes can hurt compositionality (per ARO and SugarCrepe++ literature); CLIC explicitly avoids this and *improves* it.

**Compute cost:** 0.01% of pretraining means a single run on a small GPU finishes in hours, not days — viable inside a 5-day deadline.

## Operational considerations

- **Compatible with MobileCLIP2-S4?** The method requires only a separable text encoder. MobileCLIP2 has independent text and image encoders, so yes — replace the text encoder weights post-fine-tune.
- **Affects ONNX export?** Only the text encoder ONNX needs re-exporting. Image encoder graph (the latency-dominant one at 39.3 ms FP16) is untouched.
- **Affects QNN compile?** Same as above — only text encoder needs recompile.
- **Risk:** Training data is recaptioned web data; quality depends on caption-generator (CogVLM, PixelProse). May not transfer to LPCVC's narrow object-attribute style perfectly.

## Cross-references

- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]
- [[concepts/Hard-Negative Loss for Vision-Language Models]]
- [[entities/University of Tübingen ML Group]]
