---
type: concept
title: "Compositionality Fine-Tuning for CLIP Retrieval"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Direct response to the team's contrastive-caption failure mode. Several recent methods (CLIC, NegCLIP, CoN-CLIP) preserve standard retrieval while improving fine-grained attribute discrimination."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Compositionality Fine-Tuning for CLIP Retrieval

## Why this matters

Standard CLIP fine-tunes (e.g., on MSCOCO, LAION) often *worsen* compositionality on benchmarks like SugarCrepe, ColorSwap, and WinoGround. Models learn bag-of-words shortcuts that work for retrieval-by-topic but fail on "the grey monitor" vs "the black monitor" — exactly the LPCVC 2026 organizer-caption style.

A small set of recent methods fine-tune for compositionality without breaking standard retrieval. CLIC and NegCLIP are the most-validated.

## Methods that preserve retrieval AND improve compositionality

| Method | Approach | SugarCrepe gain | MS-COCO impact |
|--------|----------|-----------------|----------------|
| **CLIC** | Frozen vision + text-only fine-tune on concatenated image pairs with hard-negative captions | Replace 86.5%, Swap 84.8% (ITT) | +1.3% text retrieval, +2.2% image retrieval |
| **NegCLIP** | Adds hard-negative captions to contrastive batches | Improves over baseline CLIP on SugarCrepe++ | Maintained or improved |
| **CoN-CLIP** | Constructs hard-negative captions via swapping | Improves SugarCrepe++ | Maintained or improved |

Per [[sources/CLIC - Compositional Awareness in CLIP]]: most fine-tunes degrade SugarCrepe++; only NegCLIP, CoN-CLIP, and CLIC explicitly maintain or improve.

## What does NOT work

- **Naive fine-tuning on retrieval data** (MSCOCO captions): improves benchmark Recall@K but *worsens* SugarCrepe and WinoGround compositionality.
- **Fine-tuning on Winoground itself:** "fails to enhance and may even diminish both recognition and compositionality" — Winoground is a test set, not training data.

## Why CLIC fits the LPCVC 2026 deadline

- **0.01% of pretraining compute** — runs in hours on a small GPU.
- **Vision encoder frozen** — preserves the team's MobileCLIP2-S4 image encoder, which is the latency-dominant graph and already QNN-validated. Only text encoder needs re-export and recompile.
- **Maintains MS-COCO retrieval** — won't break the team's existing 0.7527 R@10 sample baseline as a side effect.
- **Trained on recaptioned web data** (CogVLM/PixelProse) — not LPCVC-style captions specifically, but the contrastive-attribute pattern is the right shape.

## How to apply (for LPCVC team)

1. Take MobileCLIP2-S4's text encoder weights.
2. Apply CLIC-style fine-tune: concatenated image pairs with 4 positives + 1 hard negative, contrastive + hard-negative + uni-modal loss.
3. Evaluate on SugarCrepe + ColorSwap + LPCVC sample set BEFORE re-quantizing.
4. Re-export only the text encoder ONNX.
5. Recompile text encoder via QAI Hub. Image encoder compile job stays.
6. Re-run QAI Hub inference + scoring.

Estimated wall-clock to test: 1-2 days (training + eval + recompile + score).

## Open questions

- Does CLIC's recaptioned-web-data training transfer to LPCVC's narrow object-attribute caption style? Worth a small ablation on a single epoch.
- Can the same approach work with LoRA-on-text-encoder instead of full text-encoder fine-tune? Would further reduce risk of regression.
- Does NegCLIP outperform CLIC on the specific LPCVC sample contrastive captions? No directly comparable head-to-head was surfaced.

## Cross-references

- [[sources/CLIC - Compositional Awareness in CLIP]]
- [[sources/CLIP-LoRA - Low-Rank Few-Shot Adaptation]]
- [[concepts/Hard-Negative Loss for Vision-Language Models]]
