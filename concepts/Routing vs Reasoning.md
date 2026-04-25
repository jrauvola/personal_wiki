---
type: concept
title: "Routing vs Reasoning"
created: 2026-04-23
updated: 2026-04-24
tags:
  - type/concept
  - domain/latent-reasoning
  - domain/failure-mode
  - domain/interpretability
status: evergreen
complexity: intermediate
domain: latent-reasoning
aliases:
  - "Routing-Mode Latents"
  - "Latent Routing Role"
related:
  - "[[Feature Collapse]]"
  - "[[Shortcut Behavior]]"
  - "[[Loop-Mode Emission]]"
  - "[[Context-Prediction-Fusion]]"
  - "[[SIM-CoT]]"
  - "[[ThinkRouter]]"
  - "[[SwiReasoning]]"
  - "[[HRPO]]"
  - "[[CODI]]"
sources:
  - "[[.raw/experiments/inert_latent_F1_F6]]"
projects:
  - slug: "branch-a"
    relevance: primary
    why: "Characterizes the failure mode of CODI V2 at Qwen3-4B scale; direct framing for Branch A's scaling diagnosis."
  - slug: "branch-d"
    relevance: primary
    why: "CPF is the principal mitigation for routing-mode latents; this concept motivates the fusion mechanism."
  - slug: "branch-b"
    relevance: secondary
    why: "Detach ablations shape whether latents develop routing or reasoning roles; relevant to the training-time side of the distinction."
  - slug: "branch-c"
    relevance: secondary
    why: "Probe methodology must distinguish routing from reasoning; F3 entropy is a candidate single-shot diagnostic."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Core framing for the writeup — synthesizes the F1-F6 battery into a compact functional-role claim."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Routing vs Reasoning

## Distinction

Two different roles latent tokens can play at inference:

- **Routing.** The latent KV exists as a geometric key the decoder needs to lock into a particular output attractor (e.g. `"The answer is: ..."` format-prior emission). The specific per-example content of the KV is largely downstream-invisible, but the KV must exist in a narrow geometric basin or the decoder's attention softmax fails to find the attractor.
- **Reasoning.** The latent KV carries per-example intermediate state that causally flows into answer generation: removing it, swapping it, or perturbing it should produce example-specific downstream changes.

## Empirical evidence for the distinction

From the SPAR F1-F6 battery (Qwen3-4B-Instruct-2507 + CODI V2 bf16 detach, num_latent=8, see `research_findings/inert_latent_hypothesis_tests.md`):

- Ablating latent KV before answer generation drops accuracy by only 25-29% and leaves loop rate at ~100% (F4).
- Swapping B's latent KV with A's leaves B's accuracy unchanged and only alters 13% of predictions (F5).
- Small (σ=0.1) Gaussian noise is absorbed; larger (σ=0.5) noise collapses accuracy to <3% (F6).
- Latents carry per-example KV variation (F5 proxy: 0.78 median pair cosine, 63 PCs for 95%), but that variation does not shape the output.

The pattern is consistent with the latent positions serving as a routing signal, not a reasoning trace.

## Why this matters

The CODI reimplementation at 4B is training its latents into routing mode rather than reasoning mode. This is distinct from classic feature collapse (latents are not degenerate — they carry content) and distinct from pure shortcut learning (the decoder is not bypassing latents entirely — ablation hurts ~25%).

A usable latent-reasoning model needs to push the latents from routing into reasoning. Interventions designed to do so include:
- [[Context-Prediction-Fusion]] — anchor each latent against the embedding space.
- Auxiliary step-decoder supervision ([[SIM-CoT]]) — force latents to be decoder-interpretable.
- Hybrid latent/discrete ([[ThinkRouter]], [[SwiReasoning]], [[HRPO]]) — give the model a discrete escape hatch when latents do not carry enough content.

## Related concepts

- [[Feature Collapse]] — the representational failure mode; routing-mode collapse is a functional variant.
- [[Shortcut Behavior]] — related but stronger: shortcut fully bypasses the latent; routing uses it non-informatively.
- [[Loop-Mode Emission]] — the output-side manifestation of routing-mode latents.

## Open questions

- Does routing mode universally emerge at scale, or is it Qwen3-4B + CODI-specific?
- Can training-time interventions move latents from routing to reasoning, or does it require architectural change?
- What diagnostic cleanly distinguishes routing from reasoning without the full F-battery? (Candidate: F3 trace entropy at step 3.)

## Sharpened floor (2026-04-24)

Stacking F4 latent-KV ablation with Track A first-sentence-trim regrading yields a sharper estimate of the real capability floor: on GSM8k n=1319, preserved ∩ Track-A-trim-correct = **112 / 1319 = 8.5%**, below both F4 alone (12.2%) and Track A alone (10.8%). F4 and Track A expose *different* failure layers — 86% of F4-lost examples are still Track-A-trim-correct — so neither test independently captures the routing substrate. Phase 2 needs to clear ~15% on GSM8k to credibly beat the template-routing floor. See `research_findings/f4_per_example_diagnosis.md`.

## Layer-asymmetric refinement (2026-04-24)

Branch 1's layer-asymmetric probe on V2 bf16 (`research_findings/layer_probe/v2_bf16_step3/layer_asymmetric_probe_v2_bf16.md`, 500 GSM8k examples × 37 layers, step 3) refines the routing/reasoning distinction: the routing-key framing applies specifically to the **final-layer** decoder-facing KV basin, not stack-wide. Per-layer geometric dispersion traces a U — embed L0 through mid-stack peak L22-L30 (median pair cos 0.966 at L28; top-1 PC variance 0.137 at L30; 95%-PC count 213 at L22), then **re-collapses** at L31-L36 (final-layer L36: pair cos 0.989, top-1 PC 0.310, 95%-PC count 82). The mid-stack carries per-example geometric content; the last 6 layers compress that content into the routing template before it is written to KV cache. F5's swap-null is therefore mechanistically explained — swapping final-layer KV swaps two copies of the template. The "template" characterization (F3) belongs to the decoder-facing readout, not the model's internal state.
