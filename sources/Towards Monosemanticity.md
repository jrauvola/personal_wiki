---
type: source
source_type: paper
title: "Towards Monosemanticity: Decomposing Language Models With Dictionary Learning"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/mechanistic
  - type/source
  - tool/sparse-autoencoder
status: triaged
arxiv_id: null
venue: "Transformer Circuits Thread (Anthropic)"
date_published: 2023-10-05
authors:
  - "Trenton Bricken"
  - "Adly Templeton"
  - "Joshua Batson"
  - "Brian Chen"
  - "Adam Jermyn"
  - "Tom Conerly"
  - "Nick Turner"
  - "Cem Anil"
  - "Carson Denison"
  - "Amanda Askell"
  - "Robert Lasenby"
  - "Yifan Wu"
  - "Shauna Kravec"
  - "Nicholas Schiefer"
  - "Tim Maxwell"
  - "Nicholas Joseph"
  - "Zac Hatfield-Dodds"
  - "Alex Tamkin"
  - "Karina Nguyen"
  - "Brayden McLean"
  - "Josiah E Burke"
  - "Tristan Hume"
  - "Shan Carter"
  - "Tom Henighan"
  - "Christopher Olah"
url: "https://transformer-circuits.pub/2023/monosemantic-features"
code_repo: null
has_weights: false
confidence: high
key_claims:
  - "Sparse autoencoders on transformer residual-stream activations recover monosemantic features from superposed polysemantic neurons."
  - "SAE features can be used to causally steer model behavior — activating a feature makes the model produce the associated concept."
  - "Feature splitting: widening the SAE dictionary splits broad features into more specific children (e.g. generic-Arabic → Koranic-Arabic, legal-Arabic)."
  - "SAE training loss is L_recon + λ · L_sparsity with λ controlling monosemanticity / reconstruction tradeoff."
  - "Most learned features are interpretable by human inspection, unlike base neurons."
  - "The same activation is decomposed in multiple equivalent ways at different dictionary widths — a geometric 'feature manifold'."
related:
  - "[[Toy Models of Superposition]]"
  - "[[Sparse Feature Circuits]]"
  - "[[How does Chain of Thought Think]]"
  - "[[Sparse Autoencoder]]"
  - "[[Feature Absorption and Splitting]]"
sources:
  - "[[.raw/external/monosemanticity-2023]]"
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Direct tool for extracting per-example features from CODI latents; if successful would replace the logit-lens probe with a principled monosemantic basis."
  - slug: "branch-c"
    relevance: primary
    why: "Branch C's probe-typology contest (LTO vs DDR) is resolvable by a monosemantic SAE — features found this way are the 'principled basis' both probes approximate."
  - slug: "branch-d"
    relevance: secondary
    why: "SAE on CPF-trained vs non-CPF CODI would measure whether CPF actually disentangles — a direct test of the fusion mechanism."
  - slug: "branch-a"
    relevance: reference
    why: "Scaling context only."
  - slug: "branch-b"
    relevance: not-applicable
    why: "Not a detach concern."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Towards Monosemanticity

Anthropic's 2023 follow-up to [[Toy Models of Superposition]]. Empirically demonstrates that sparse autoencoders on a one-layer transformer's MLP activations recover largely monosemantic features from superposed polysemantic neurons.

## SAE formulation

Encoder–decoder with tied or untied weights:
```
h     = ReLU(W_enc (x − b_dec) + b_enc)    # sparse code
x̂     = W_dec h + b_dec                    # reconstruction
L     = ||x − x̂||² + λ · ||h||_1
```
- `x ∈ R^d` = residual-stream or MLP activation.
- `h ∈ R^k`, `k ≫ d` (overcomplete dictionary).
- `λ` controls sparsity / reconstruction tradeoff.

## Feature splitting

Training wider SAEs on the same activations splits "big" features into more specific children. Example in the paper: a broad Arabic-script feature splits into Koranic-Arabic, legal-Arabic, social-media-Arabic when the dictionary widens. This gives a scale-dependent "feature manifold" — the same activation is equivalently decomposed at many levels of granularity.

## Monosemanticity evaluation

- **Activation examples.** Top-activating tokens / contexts for each feature, hand-rated for coherence.
- **A/B testing.** Feature ablation predicts the presence/absence of the concept downstream.
- **Steering.** Manually clamping a feature to a value causes the model to produce the feature's concept.

## Causal steering examples

- Base64 feature → forcing high activation makes the model output base64-looking text.
- Arabic-script feature → Arabic output.
- "DNA sequence" feature → GCTA sequences.

Steering demonstrates features are causal, not correlational.

## Implications for latent reasoning

- **F3 template lock.** An SAE on CODI latent positions would test whether the 7 collapsed positions share one feature direction or distinct directions hidden by superposition.
- **F5 cross-example swap.** If latents carry per-example content invisible to decoding, an SAE should recover features that vary across examples even where logit-lens readout is uniform.
- **Steering as intervention.** Clamping a discovered reasoning feature and running the decoder tests whether the latent is functional (reasoning) or decorative (routing).

## Cross-references

- [[Toy Models of Superposition]] — theoretical motivation.
- [[Sparse Autoencoder]] — concept page.
- [[Feature Absorption and Splitting]] — the failure mode that limits naïve SAEs.
- [[Sparse Feature Circuits]] — how SAE features are assembled into circuits.
