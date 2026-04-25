---
type: source
title: "OneVL — One-Step Latent Reasoning and Planning with Vision-Language Explanation"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - domain/autonomous-driving
  - type/source
  - method/auxiliary-decoder
  - method/curriculum
  - method/world-model
status: triaged
related:
  - "[[SIM-CoT]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[LaRA-VLA]]"
  - "[[DualCoT-VLA]]"
sources:
  - "[[.raw/papers/2604.18486-onevl]]"
source_type: paper
arxiv_id: "2604.18486"
venue: "arXiv"
date_published: 2026-04-20
authors:
  - "Jinghui Lu"
  - "Jiayi Guan"
  - "Zhijian Huang"
  - "Jinlong Li"
  - "Guang Li"
  - "Lingdong Kong"
  - "et al. (Xiaomi Embodied Intelligence, 50 authors total)"
url: "https://arxiv.org/abs/2604.18486"
code_repo: null
has_weights: false
status: triaged
confidence: medium
key_claims:
  - "OneVL routes reasoning through compact latent tokens supervised by dual auxiliary decoders: a language decoder that reconstructs text CoT and a visual world model decoder that predicts future-frame tokens, forcing the latent space to internalize causal dynamics of road geometry, agent motion, and environmental change."
  - "A three-stage training pipeline progressively aligns these latents with trajectory, language, and visual objectives, ensuring stable joint optimization."
  - "At inference, the auxiliary decoders are discarded and all latent tokens are prefilled in a single parallel pass, matching the speed of answer-only prediction."
  - "Across four benchmarks, OneVL becomes the first latent CoT method to surpass explicit CoT, delivering state-of-the-art accuracy at answer-only latency."
  - "Tighter compression, when guided in both language and world-model supervision, produces more generalizable representations than verbose token-by-token reasoning."
projects:
  - slug: "branch-a"
    relevance: not-applicable
    why: "Autonomous-driving domain; no direct read on Qwen3 architecture-dependence scaling."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach/fp32 grad-stability discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to Qwen3 probe methodology."
  - slug: "branch-d"
    relevance: secondary
    why: "Direct multi-decoder generalization of SIM-CoT's auxiliary-decoder recipe. Confirms auxiliary-decoder supervision is portable beyond math reasoning and supports stacking multi-modal targets (text CoT + world-model future frames). Informs LT-Tuning CPF framing: CPF anchors to vocab embedding, OneVL anchors to vocab + visual-world-model hidden state. Secondary (not primary) because domain-specific evaluation limits transfer — but the dual-decoder loss stacking is a recipe LT-Tuning extensions could borrow if we later evaluate multimodal variants."
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Claim of 'first latent CoT to surpass explicit CoT' is domain-specific (autonomous driving benchmarks), and MARCOS reported a similar milestone earlier on GSM8K (+4.7%). Dual-decoder recipe is a notable SIM-CoT extension worth tracking but not a north-star synthesis input. Downgraded primary → secondary this sweep to keep spar-primary reserved for methods actively running or load-bearing framing."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# OneVL — One-Step Latent Reasoning and Planning with Vision-Language Explanation

> [!contradiction] 'First latent CoT to surpass explicit CoT' vs [[MARCOS]]
> OneVL (2026-04, Xiaomi) claims to be the "first latent CoT method to surpass explicit CoT" on four driving benchmarks. [[MARCOS]] (2025-09, Yee Whye Teh group) claimed surpassing token CoT on GSM8K earlier (+4.7%). Not strictly contradictory — OneVL's claim is scoped to autonomous-driving benchmarks and trajectory-supervised dual-decoder setups, while MARCOS's is on GSM8K math. But "first" should be stated carefully: MARCOS precedes OneVL by ~7 months on at least one math benchmark. Both papers deserve careful reading before either claim is cited as a primacy milestone.

## TL;DR

Unified VLA + World Model framework for autonomous driving. Routes reasoning through **compact latent tokens** supervised by **dual auxiliary decoders** (language + visual world model). Three-stage curriculum progressively aligns latents with trajectory, language, and visual objectives. At inference, both auxiliary decoders are discarded and all latent tokens are prefilled in a single parallel pass. Claimed as the first latent-CoT method to surpass explicit CoT (in driving benchmarks).

## Method

- **Compact latent tokens** — reasoning bottleneck.
- **Dual auxiliary decoders** (training-time, both discarded at inference):
  - **Language decoder** → reconstructs explicit text CoT.
  - **Visual world model decoder** → predicts future-frame tokens, forcing latents to internalize causal dynamics (road geometry, agent motion, environmental change).
- **Inference**: all latent tokens prefilled in one parallel forward pass, matching answer-only latency.

## Recipe

- **Three-stage training** (names not in abstract; from the motivation they are ordered to stabilize joint optimization across trajectory / language / visual objectives).
- 49-page technical report, 22 figures, 10 tables — full recipe in PDF.

## Results

- **First latent CoT method to surpass explicit CoT** across 4 benchmarks (names not in abstract).
- Answer-only latency (via one-pass prefill).

## Relevance

- **Direct, well-resourced confirmation of SIM-CoT's recipe** in a new modality: the dual-decoder supervision pattern scales, and the main claim (latent > explicit) is the strongest such claim we have seen in 2026 literature.
- **SPAR writeup implication**: if the "latent > explicit" claim holds under scrutiny, it inverts the weak-sauce finding from explicit baselines in COCONUT/CODI-era work. Worth a careful read of the PDF for ablations isolating the visual decoder's contribution.
- **LT-Tuning CPF comparison**: OneVL supervises the **latent token itself** via dual reconstruction heads; LT-Tuning fuses predictive embedding from vocab space into the latent input. Different anchor strategies; both aim to prevent feature collapse.

## Citations

- Project: https://xiaomi-embodied-intelligence.github.io/OneVL/
- Discovered via SIM-CoT downstream citation graph (isInfluential=true).
