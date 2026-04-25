---
type: source
title: "Implicit Reasoning in Large Language Models: A Comprehensive Survey"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - type/survey
status: read
related:
  - "[[HRPO]]"
  - "[[COCONUT]]"
  - "[[CODI]]"
  - "[[Latent Thoughts Tuning]]"
  - "[[Capabilities and Limits of Latent CoT]]"
  - "[[Dynamics of Latent CoT]]"
sources:
  - "[[.raw/papers/2509.02350-implicit-reasoning-survey]]"
source_type: paper
arxiv_id: "2509.02350"
venue: "arXiv"
date_published: 2025-09-02
authors:
  - "Jindong Li"
  - "Yali Fu"
  - "Li Fan"
  - "Jiahong Liu"
  - "Yao Shu"
  - "Chengwei Qin"
  - "Menglin Yang"
  - "Irwin King"
  - "Rex Ying"
url: "https://arxiv.org/abs/2509.02350"
code_repo: "https://github.com/digailab/awesome-llm-implicit-reasoning"
has_weights: false
confidence: high
key_claims:
  - "Implicit reasoning is characterized by a functional taxonomy over execution paradigms (how and where computation unfolds internally), not by representational form."
  - "Three execution paradigms span the field: latent optimization, signal-guided control, and layer-recurrent execution."
  - "Latent optimization decomposes into token-level, trajectory-level (with subtypes: semantic anchoring, adaptive efficiency, progressive refinement, exploratory diversification), and internal-state-level manipulation."
  - "HRPO is taxonomized as 'internal-state-level latent optimization' alongside ICoT-KD, System-2 Distillation, LTMs, System-1.5 Reasoning, Beyond Words, ReaRec."
  - "Existing implicit-reasoning work faces six cross-cutting challenges: limited interpretability, limited control/reliability, performance gap vs explicit CoT, lack of standardized evaluation, architecture/generalization constraints, and dependence on explicit supervision."
projects:
  - slug: "branch-d"
    relevance: reference
    why: "Taxonomy helps frame CPF as 'semantic anchoring' (trajectory-level) or a hybrid with 'internal-state-level' — useful for writeup but no direct recipe signal."
  - slug: "branch-a"
    relevance: reference
    why: "Does not address architecture-dependence scaling empirics; taxonomic framing only."
  - slug: "branch-b"
    relevance: not-applicable
    why: "No detach/fp32/BPTT discussion."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Not probe-methodology."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Most complete public taxonomy for the writeup's introduction/related work. Explicit categorization of HRPO, CODI, Coconut, CoLaR, Soft Thinking, SoftCoT, and layer-recurrent LoopLM literature into coherent paradigms. Directly reusable as the synthesis chapter's organizing skeleton."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Implicit Reasoning in LLMs — Comprehensive Survey

Li, Fu, Fan, Liu, Shu, Qin, Yang, King, Ying (HKUST-GZ / Jilin / CUHK / Yale), [arXiv:2509.02350](https://arxiv.org/abs/2509.02350), Sep 2025. Continuously updated project: [github.com/digailab/awesome-llm-implicit-reasoning](https://github.com/digailab/awesome-llm-implicit-reasoning).

## TL;DR

A mechanism-level survey of implicit reasoning in LLMs, organized by **execution paradigm** rather than representational form. Three top-level categories: latent optimization (token/trajectory/internal-state levels), signal-guided control (pause/filler/planning tokens), and layer-recurrent execution (looped transformers). Comprehensive mapping of 60+ methods into this taxonomy, plus evidence review (structural, behavioral, representation-based) and benchmark coverage. Most complete public taxonomy as of Sep 2025; ideal organizing frame for our writeup.

## The three execution paradigms

### 1. Latent Optimization (§3.1)

Computation unfolds over learned latent representations instead of discrete tokens.

- **Token-Level** (§3.1.1) — augment input/output vocab with learned latent tokens. CoCoMix, Latent Token, LPC, [[Token Assorted]].
- **Trajectory-Level** (§3.1.2):
  - **Semantic Anchoring** — align latent trajectory with explicit reasoning steps. CCoT, HCoT, [[CODI]], [[SynAdapt]].
  - **Adaptive Efficiency** — dynamically compress chains. LightThinker, CoT-Valve, [[CoLaR]].
  - **Progressive Refinement** — iterative refinement of latents. ICoT-SI, [[COCONUT]], Heima, PonderingLM, BoLT.
  - **Exploratory Diversification** — maintain multiple latent alternatives. LaTRO, [[Soft Thinking]], SoftCoT, [[SoftCoT Plus Plus]], CoT2.
- **Internal-State-Level** (§3.1.3) — manipulate internal states (KV cache, hidden states) directly. ICoT-KD, System-2 Distillation, LTMs, [[System-1.5 Reasoning]], Beyond Words, ReaRec, **[[HRPO]]**.

### 2. Signal-Guided Control (§3.2)

Insert special control tokens (pause, filler, planning) to modulate how computation unfolds.

- **Single-Type Signal:** Thinking Tokens, Pause Tokens, Filler Tokens, Planning Tokens, Quiet-STaR, LatentSeek, DIT.
- **Multi-Type Signal:** Memory&Reasoning (Jin et al.), Thinkless (Fang et al.).

### 3. Layer-Recurrent Execution (§3.3)

Iterate the same set of layers to simulate deeper reasoning. ITT, Looped Transformer, CoTFormer, Huginn, RELAY. Our [[LoopLM]] / [[Ouro]] / [[Parcae]] lineage.

## Evidence review (§4)

- **Layer-wise structural evidence:** Jump to Conclusions (Din et al.), LM Implicit Reasoning (Lin et al.), Internal CoT (Yang et al.), [[Reasoning by Superposition]], To CoT or To Loop.
- **Behavioral signatures:** Grokked Transformer, Latent Multi-Hop Reasoning, Step-skipping, Beyond Chains of Thought.
- **Representation-based:** MechanisticProbe, TTT (test-time training), Distributional Reasoning, Steering Vector Intervention, Backward Chaining Circuits, CoE.

## Cross-cutting challenges (§6)

1. Limited interpretability and latent opacity.
2. Limited control and reliability.
3. Performance gap vs explicit reasoning.
4. Lack of standardized evaluation.
5. Architecture and generalization constraints.
6. Dependence on explicit supervision.

## Relevance

**Primary for spar-latent-reasoning.** Single most complete organizing frame for the writeup. Lets us:

- Position CPF as a trajectory-level "semantic anchoring" mechanism that partially imports internal-state-level tricks (hidden-state fusion).
- Cite the taxonomy directly when motivating the V2 / SIM-CoT / LT-Tuning synthesis: these belong to three different paradigms (internal-state KV distillation / trajectory semantic-anchoring / trajectory semantic-anchoring with internal-state fusion).
- Adopt the six "challenges" as the writeup's problem-statement skeleton.

## Reference-only for branch-d

No direct recipe — does not propose a new method. Useful for categorizing but not for implementation.

## Citation links to chase

- Most primary-tier papers in the vault already; the survey maps them into a common frame.
- New names not yet in vault worth flagging: CoCoMix, LPC, LaTRO, HCoT, Heima, BoLT, ReaRec, LTMs, LatentSeek, DIT, Huginn, CoTFormer, RELAY, ITT, Memory&Reasoning, Thinkless, Quiet-STaR. Consider as future crawl seeds if spar synthesis needs depth.
