---
type: concept
title: "Matryoshka Embeddings for CLIP Retrieval"
projects:
  - slug: lpcvc-2026-track1
    relevance: primary
    why: "Single training run produces a model with selectable embedding dim at inference. For LPCVC's accuracy-vs-latency Pareto, this is a free tunable at submission time."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Matryoshka Embeddings for CLIP Retrieval

## What this concept is

Matryoshka Representation Learning (MRL, NeurIPS 2022, arXiv 2205.13147) trains a model with a stacked contrastive loss over a *nested* set of embedding dimensions. At inference, you truncate the embedding to any dim in the set; the first dimensions carry coarse information, later ones add fidelity.

```
L_MRL = Σ_d w_d · L_contrastive(emb[:d])
```

Typical dim set: {64, 128, 256, 512, 768}. Equal weights work well as default.

## Measured numbers

- **ImageNet-1K classification:** up to **14× embedding shrink at iso-accuracy**, 14× retrieval speedup at fixed accuracy.
- **STSBenchmark sentence similarity:** at 64-d (8.3% of original), Matryoshka retains **98.4%** of full-dim performance vs **96.5%** for a non-Matryoshka model truncated naively.
- **CLIP retrieval (Marqo):** the gap between 256-d and 512-d Matryoshka CLIP is **<0.019 nDCG** across reported splits.

> [!gap] No public CLIP+MRL Recall@K vs dim table on COCO/Flickr30K. Team should generate this — single training run produces it.

## Why this is high-ROI for LPCVC 2026 Track 1

**Single training run = entire accuracy/latency Pareto curve as a free tunable at submission time.**

LPCVC scoring depends on both Recall@10 and latency. With a Matryoshka MobileCLIP2 student trained on `matryoshka_dims=[64, 128, 256, 384, 512, 768]`:

- If submission-time profiling shows headroom under the 35 ms gate → use 768-d for max R@10.
- If profiling shows the team is over-budget → truncate to 256-d at submission for ~no R@10 loss but smaller embeddings, faster cosine-sim compute downstream.
- The image and text encoders themselves are not changed — only the output projection head. ONNX graph is identical for any dim.

**Compute cost:** training is comparable to a single regular fine-tune (the loss sum is cheap). One pass.

**Risk:** none structural. Worst case, R@10 at any dim equals what you'd get from a separately trained model at that dim.

## Operational shape (for self_training/ pipeline)

Modify the contrastive loss in `self_training/loss.py`:

```python
# Existing (sketch):
def contrastive_loss(image_emb, text_emb):
    sim = image_emb @ text_emb.T / temp
    return symmetric_cross_entropy(sim)

# Matryoshka-ified:
def matryoshka_contrastive_loss(image_emb, text_emb, dims=[64, 128, 256, 384, 512, 768]):
    total = 0.0
    for d in dims:
        i_d = F.normalize(image_emb[:, :d], dim=-1)
        t_d = F.normalize(text_emb[:, :d], dim=-1)
        total += contrastive_loss(i_d, t_d)
    return total / len(dims)
```

Re-normalize after truncation (slicing breaks unit norm). Train as normal.

## When NOT to use

- Pure latency-bound competition where embedding-dim doesn't affect on-device latency. (For LPCVC, image+text encoder latency matters most; cosine-sim is cheap. So MRL's main win is "post-hoc accuracy/dim trade" not on-device latency.)
- When you only ever serve at one dim and don't care about flexibility — single-dim training with regular loss is slightly cheaper.

## Composition with other ideas

- **+ CLIC text-only fine-tune:** apply MRL loss only on text encoder (image frozen). Keeps image graph intact, gains the trade-space.
- **+ LoRA:** apply MRL loss with LoRA adapters on text encoder. Maximally parameter-efficient.
- **+ Knowledge distillation:** distill from teacher's full-dim embedding into student's nested embeddings. Recipe is in MRL paper appendix.

## Cross-references

- [[concepts/Knowledge Distillation for Mobile CLIP Retrieval]]
- [[sources/CLIC - Compositional Awareness in CLIP]] — companion text-only fine-tune
- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]

## Sources used
- arXiv 2205.13147 — MRL paper (NeurIPS 2022)
- Marqo blog: Matryoshka Representation Learning with CLIP for Multimodal Retrieval
- HuggingFace blog: Matryoshka Embeddings (sentence-transformers recipes)
