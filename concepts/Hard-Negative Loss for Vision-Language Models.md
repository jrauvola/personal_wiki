---
type: concept
title: "Hard-Negative Loss for Vision-Language Models"
projects:
  - slug: lpcvc-2026-track1
    relevance: secondary
    why: "Mechanism behind CLIC, NegCLIP, CoN-CLIP. Understanding it lets the team adapt or simplify the recipe to their constraints."
last_reviewed: 2026-04-25
reviewed_by: autoresearch
---

# Hard-Negative Loss for Vision-Language Models

## Concept

Vanilla CLIP contrastive loss treats all in-batch text-image pairs as positives, all others as negatives. With large batches, most negatives are trivially distinct ("a cat" vs "a parking garage"), giving weak gradient signal for fine-grained discrimination.

Hard-negative loss explicitly constructs *near-misses* — captions that differ from the positive only in one attribute, object, or relation — and uses them as negatives. This forces the model to attend to the discriminating word.

## Mechanism

For an image with positive caption "a grey monitor on a desk":
- Hard negatives: "a black monitor on a desk", "the old monitor on a desk", "a grey laptop on a desk"
- These share most words with the positive but differ in one binding

Loss term (sketch):
```
L_hard = -log( sim(image, pos) / [sim(image, pos) + Σ sim(image, hard_neg_i)] )
```

The denominator only contains hard negatives (or hard negatives weighted higher), not all in-batch negatives.

## Generation strategies

| Strategy | Source paper | How |
|----------|--------------|-----|
| Word swap | NegCLIP, ARO | Swap one word in the positive caption (object, attribute, color, location) |
| LLM-generated | SugarCrepe (eval), CLIC (train) | Prompt an LLM to generate hard distractors that flip one attribute |
| Concatenated images | [[sources/CLIC - Compositional Awareness in CLIP]] | Pair two images, generate captions for either alone or both |
| Color swap | ColorSwap | Swap color words specifically; targets color-binding failure |

## Why this fits LPCVC 2026 Track 1

The organizer captions are *constructed* as hard negatives — that's the entire challenge. Models that have not been trained against hard-negative captions will fail on attribute discrimination by design.

The most efficient recipe combining this with deployment constraints:
1. Take MobileCLIP2-S4 base.
2. Generate hard-negative captions for a small training set (LPCVC sample + open data).
3. Fine-tune text encoder only with contrastive + hard-negative loss (CLIC-style or NegCLIP-style).
4. Re-export and recompile only text encoder.

## Failure modes to avoid

- **Training on Winoground or SugarCrepe directly:** These are evaluation benchmarks. Contamination invalidates the score and is sometimes detectable.
- **Over-weighting hard-negative loss:** Empirically can collapse the embedding to memorize the contrastive examples without generalizing. CLIC uses a *combination* of contrastive + hard-negative + uni-modal loss for this reason.
- **Generating hard negatives only via word substitution:** Limited diversity. LLM-generated negatives (CogVLM, GPT-4) cover more relation/attribute swaps.

## Cross-references

- [[sources/CLIC - Compositional Awareness in CLIP]]
- [[concepts/Compositionality Fine-Tuning for CLIP Retrieval]]
