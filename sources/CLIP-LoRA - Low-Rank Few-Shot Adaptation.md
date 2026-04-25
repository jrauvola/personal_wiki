---
type: source
source_type: paper
title: "CLIP-LoRA — Low-Rank Few-Shot Adaptation of Vision-Language Models"
arxiv_id: "2405.18541"
venue: "CVPRW 2024"
date_published: 2024-05-28
authors: ["Maxime Zanella", "Ismail Ben Ayed"]
url: "https://github.com/MaxZanella/CLIP-LoRA"
code_repo: "https://github.com/MaxZanella/CLIP-LoRA"
has_weights: false
status: integrated
confidence: high
projects:
  - slug: lpcvc-2026-track1
    relevance: secondary
    why: "Reference LoRA recipe for CLIP — applicable but team's existing self_training/lora_setup.py already exists. Use for sanity-check on rank/alpha defaults and which attention projections to adapt."
key_claims:
  - "LoRA applied to Q/K/V/O linear projections in the attention blocks via PlainMultiheadAttentionLoRA wrapper."
  - "Default demo rank: r=4, lora_alpha=2 (i.e., low rank for parameter efficiency)."
  - "Targets few-shot classification (ImageNet + 10 fine-grained datasets), not retrieval directly."
  - "Block-LoRA (follow-up, arXiv 2501.16720, Jan 2026) outperforms CLIP-LoRA in few-shot accuracy with fewer parameters via block-matrix structure."
  - "One reported MS-COCO retrieval result (separate work, RN50 CLIP): 76.02% mean recall (+17.63% over zero-shot 58.39%)."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# CLIP-LoRA — Low-Rank Few-Shot Adaptation

## Summary

CLIP-LoRA (Zanella & Ben Ayed, CVPRW 2024) is the canonical LoRA-for-CLIP reference. It applies LoRA to the Q/K/V/O attention projections, with rank typically as low as 4. Demonstrated for few-shot classification, not retrieval — but the recipe transfers.

## Method

```python
PlainMultiheadAttentionLoRA(
    existing_mha,
    enable_lora=['q', 'k', 'v', 'o'],
    r=4,
    lora_alpha=2,
)
```

This wraps each attention block's linear projections with LoRA adapters. Frozen base model, only adapter weights train. ~0.01–1% of full-tune parameters.

## What it tested

- Datasets: ImageNet + 10 fine-grained classification (StanfordCars, FGVCAircraft, etc.)
- Setting: few-shot (1, 2, 4, 8, 16-shot)
- Metric: classification accuracy

**Not tested:** image-to-text retrieval (Recall@K). The recipe should generalize but was not directly validated for this task in the paper.

## Block-LoRA follow-up

A January 2026 paper "One Head Eight Arms" (arXiv 2501.16720) introduces Block-LoRA, a block-matrix variant that:
- Outperforms CLIP-LoRA in average few-shot accuracy
- Uses fewer parameters
- Lower computational overhead

If iterating on a LoRA fine-tune for LPCVC, Block-LoRA is the more recent baseline.

## Operational notes for the team

- The team already has `self_training/lora_setup.py` in the codebase. Verify against CLIP-LoRA defaults: are Q/K/V/O all enabled? Is rank around 4-16? If only Q/V are adapted (common LoRA shortcut from LLM literature), enabling K and O is a low-cost experiment.
- For a **retrieval** target (not classification), the self-training pipeline's loss matters more than the LoRA placement. CLIP's contrastive loss with hard negatives is the right base.
- **Combining with CLIC's text-encoder-only fine-tune:** if CLIC works for the team, LoRA on the text encoder alone (vision frozen) is the parameter-efficient version of CLIC's approach.

> [!gap] No retrieval-specific Recall@K numbers from the CLIP-LoRA paper itself. The 76.02% MSCOCO result mentioned in the search summary is from a separate work (likely COSMIC/other), not CLIP-LoRA.

## Cross-references

- [[concepts/LoRA for CLIP Retrieval]]
- [[entities/Maxime Zanella]]
- [[sources/CLIC - Compositional Awareness in CLIP]] (alternative: full text-encoder fine-tune)
