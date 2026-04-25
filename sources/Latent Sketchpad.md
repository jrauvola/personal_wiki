---
type: source
title: "Latent Sketchpad: Sketching Visual Thoughts to Elicit Multimodal Reasoning in MLLMs"
created: 2026-04-22
updated: 2026-04-22
tags:
  - domain/latent-reasoning
  - domain/multimodal
  - source/paper
status: read
source_type: paper
arxiv_id: "2510.24514"
venue: "arXiv"
date_published: 2025-10-28
authors:
  - "Huanyu Zhang"
  - "et al. (12 authors total)"
url: "https://arxiv.org/abs/2510.24514"
code_repo: "https://github.com/hwanyu112/Latent-Sketchpad"
has_weights: true
confidence: high
projects:
  - slug: spar-latent-reasoning
    relevance: primary
    why: "Closest precedent to user's Latent Scratchpad proposal — interleaves text reasoning with an interpretable side-channel (visual latents → sketch images), gated by autoregressive control. Visual analogue of the discrete-note scratchpad."
  - slug: branch-a
    relevance: not-applicable
    why: "Multimodal; not Qwen3 text-only scaling."
  - slug: branch-b
    relevance: not-applicable
    why: "Not a detach ablation."
  - slug: branch-c
    relevance: not-applicable
    why: "Not probe methodology."
  - slug: branch-d
    relevance: reference
    why: "Side-channel idea composes with CPF but domain (vision) differs from branch-d scope."
last_reviewed: 2026-04-22
reviewed_by: autoreview
key_claims:
  - "Latent Sketchpad equips MLLMs with an internal visual scratchpad by repurposing MLLM internal visual representations for generative visual thought."
  - "The model interleaves textual reasoning with generation of visual latents, which guide internal thought and can be translated to sketch images for interpretability."
  - "Two components: a Context-Aware Vision Head that autoregressively produces visual representations, and a pretrained Sketch Decoder that renders these to human-interpretable images."
  - "Evaluated on MazePlanning dataset; delivers comparable or superior reasoning performance vs backbone across Gemma3 and Qwen2.5-VL."
  - "Side-channel is continuous visual latents decoded through a separate Sketch Decoder, NOT discrete human-readable tokens in the LLM vocabulary."
related:
  - "[[Huanyu Zhang]]"
  - "[[Latent Scratchpad Architecture]]"
  - "[[Research - Latent Scratchpad Precedence]]"
  - "[[Token Assorted]]"
sources: []
---

# Latent Sketchpad

**arXiv:** [2510.24514](https://arxiv.org/abs/2510.24514) | **Code:** [hwanyu112/Latent-Sketchpad](https://github.com/hwanyu112/Latent-Sketchpad) | **Project page:** [latent-sketchpad.github.io](https://latent-sketchpad.github.io/) | **Date:** 2025-10-28

## Abstract (verbatim)

"While Multimodal Large Language Models (MLLMs) excel at visual understanding, they often struggle in complex scenarios that require visual planning and imagination. Inspired by how humans use sketching as a form of visual thinking to develop and communicate ideas, we introduce Latent Sketchpad, a framework that equips MLLMs with an internal visual scratchpad. The internal visual representations of MLLMs have traditionally been confined to perceptual understanding. We repurpose them to support generative visual thought without compromising reasoning ability. Building on frontier MLLMs, our approach integrates visual generation directly into their native autoregressive reasoning process. It allows the model to interleave textual reasoning with the generation of visual latents. These latents guide the internal thought process and can be translated into sketch images for interpretability. To realize this, we introduce two components: a Context-Aware Vision Head autoregressively produces visual representations, and a pretrained Sketch Decoder renders these into human-interpretable images. We evaluate the framework on our new dataset MazePlanning. Experiments across various MLLMs show that Latent Sketchpad delivers comparable or even superior reasoning performance to their backbone."

## Relevance to Latent Scratchpad (W3.5) — CLOSEST PRIOR ART

This is the single closest match for the user's proposal in spirit, though the modality differs:

| Dimension | User's Latent Scratchpad (W3.5) | Latent Sketchpad |
|---|---|---|
| Primary channel | Continuous latent reasoning tokens (CODI-like) | Textual autoregressive reasoning |
| Side channel | Sparse **discrete** tokens from LM vocab | Continuous **visual latents** → Sketch Decoder → images |
| Interpretability | Tokens directly readable as words | Images interpretable via decoder |
| Gating | Learned gate decides when to emit | Autoregressive — model "decides" in place |
| Modality | Text-only | Multimodal (MLLM) |

The **architectural pattern is the same:** primary reasoning stream + an interpretability side-channel that is "written" at model-chosen positions and rendered via a lightweight decoder. The W3.5 contribution is to (a) port this pattern to a **text-only** setting, (b) use **discrete vocab tokens** (not continuous latents) so the side-channel is natively interpretable without a separate decoder, and (c) place it on top of a **latent primary** stream (CODI/COCONUT) rather than a textual primary.

This is the paper we should cite as the direct inspiration / closest prior art.

## Code / weights

Code + resources released on GitHub + HF. `has_weights: true` (Sketch Decoder at minimum is described as pretrained and released).
