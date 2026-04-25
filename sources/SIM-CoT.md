---
type: source
title: "SIM-CoT — Supervised Implicit Chain-of-Thought"
created: 2026-04-22
updated: 2026-04-23
tags:
  - domain/latent-reasoning
  - type/source
  - method/strong-supervision
status: read
related:
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[Feature Collapse]]"
  - "[[Curriculum Distillation]]"
  - "[[Token Efficiency]]"
  - "[[InternLM]]"
sources:
  - "[[.raw/papers/2509.20317-sim-cot]]"
  - "[[.raw/papers/research.md]]"
source_type: paper
arxiv_id: "2509.20317"
venue: "arXiv"
date_published: 2025-09-24
authors:
  - "Xilin Wei"
  - "Xiaoran Liu"
  - "Yuhang Zang"
  - "Xiaoyi Dong"
  - "Yuhang Cao"
  - "Jiaqi Wang"
  - "Xipeng Qiu"
  - "Dahua Lin"
url: "https://arxiv.org/abs/2509.20317"
code_repo: "https://github.com/InternLM/SIM-CoT"
has_weights: true
status: read
confidence: high
key_claims:
  - "We identify a core latent instability issue when scaling the computational budget of implicit CoT: as the number of reasoning tokens increases, training often becomes unstable and collapses."
  - "This instability arises from latent representations becoming homogeneous and losing semantic diversity, caused by insufficient step-level supervision in current implicit CoT methods."
  - "SIM-CoT employs an auxiliary decoder during training to align each implicit token with its corresponding explicit reasoning step, ensuring latent states capture distinct and meaningful information; the auxiliary decoder is removed at inference, preserving the efficiency of implicit CoT with no added overhead."
  - "On GPT-2, SIM-CoT surpasses both the strong explicit baseline (supervised fine-tuning on explicit CoT data) by 2.1%, and outperforms existing implicit methods Coconut and CODI by 8.2% and 4.3%, respectively."
  - "SIM-CoT achieves improvements over CODI of 3.4% (LLaMA-3.2 1B), 1.5% (LLaMA-3.2 3B), and 3.0% (LLaMA-3.1 8B)."
  - "SIM-CoT remains stable and continues to boost performance when scaling to 8–16 tokens where previous implicit CoT approaches collapse."
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Auxiliary-decoder anti-collapse mechanism directly complements LT-Tuning CPF; referenced in branch-d secondary interests as related anti-collapse method."
  - slug: "branch-a"
    relevance: primary
    why: "Production-ready Llama 3.1 8B Hugging Face weights are the most reliable public scaling artifact; directly usable for Qwen3 scaling comparisons."
  - slug: "branch-b"
    relevance: secondary
    why: "Strong-supervision framing is relevant context for detach/grad-stability ablations but is not the specific subject of the ablation."
  - slug: "branch-c"
    relevance: reference
    why: "General method context only; no direct bearing on Qwen3 probe methodology or configuration debugging."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "North-star explicitly targets synthesizing SIM-CoT lessons; taxonomic framing paper for strong-supervision school."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# SIM-CoT — Supervised Implicit Chain-of-Thought

Wei, Liu, Zang, Dong, Cao, Wang, Qiu, Lin, [arXiv:2509.20317](https://arxiv.org/abs/2509.20317) — *SIM-CoT: Supervised Implicit Chain-of-Thought* (Fudan / Shanghai AI Lab / CUHK / Shanghai Innovation Institute, v1 24 Sep 2025, v2 25 Sep 2025). Code: [InternLM/SIM-CoT](https://github.com/InternLM/SIM-CoT).

## Core thesis

A decisive intervention against latent instability. As the computational budget of implicit reasoning is scaled by increasing the number of continuous tokens, weakly supervised models frequently suffer from training collapse. The underlying pathology is homogenization of latent representations: without discrete language boundaries, continuous vectors lose semantic diversity and fail to preserve operator information needed for complex multi-step deductions.

The core innovation is a rigorous, step-level supervision mechanism that forces the latent space to maintain semantic distinctiveness. A plug-and-play auxiliary decoder translates continuous implicit tokens back into the explicit reasoning vocabulary during optimization. This mathematically anchors each point in the continuous trajectory to a verifiable, human-readable logical step, immunizing the model against feature collapse while preserving the rich representational capacity of the hidden states.

## Training pipeline

Highly modular; operates sequentially following initialization of a base latent model.

1. **Latent baseline preparation** — typically an architecture previously conditioned via curriculum learning or distillation.
2. **Attach auxiliary decoder** — lightweight projection head on the final hidden layers at the designated implicit token positions.
3. **Supervised alignment phase** — dataset of questions paired with explicit step-by-step rationales; cross-entropy loss through the auxiliary decoder penalizes divergence between decoded latent state and ground-truth textual reasoning step. Forces continuous vectors to capture distinct and meaningful cognitive transitions.
4. **Decoder removal** — upon convergence, the auxiliary decoder is completely removed. Only primary latent model parameters are serialized for deployment; explicit decoding overhead is eliminated at inference.

## Public artifacts

Exemplary — highly accessible for immediate deployment.

- Codebase: [InternLM/SIM-CoT](https://github.com/InternLM/SIM-CoT)
- Checkpoints (HF):
  - `internlm/SIM_COT-GPT2-Coconut`
  - `internlm/SIM_COT-GPT2-CODI`
  - `internlm/SIM_COT-LLaMA3-CODI-1B`
  - `internlm/SIM_COT-LLaMA3-CODI-3B`
  - `internlm/SIM_COT-LLaMA3-CODI-8B`

## Empirical results

- On GPT-2: surpasses explicit SFT-CoT baseline by +2.1%; outperforms Coconut by +8.2% and CODI by +4.3%.
- Over CODI: +3.4% (LLaMA-3.2 1B), +1.5% (LLaMA-3.2 3B), +3.0% (LLaMA-3.1 8B).
- 2.3× speedup over explicit CoT on GPT-2 while surpassing it by 2.1 percentage points.
- Remains stable when scaling to 8–16 latent tokens where previous implicit CoT approaches collapse.

## Integration notes

Optimal current public training method for a blend of architectural stability, comprehensive public artifacts, and proven scalability. Project fit for the local harness is exceptionally high — the repo structure already allocates a planned slot (`methodology.md:203`). With Llama 3.1 weights available, transitioning this slot from planned to executable should be prioritized.

## SPAR empirical follow-up (2026-04-23)

Our [[CODI]] V2 bf16 F-battery (see `research_findings/inert_latent_hypothesis_tests.md`) gives SIM-CoT a concrete, pre-registered success criterion when ported to Qwen3-4B-Instruct-2507:

- **F3 entropy should rise.** V2 baseline has 7/8 latent positions collapsed to a fixed template (entropy <0.4 bits, dominant token ≥93%). An aux decoder that actually forces each implicit token to carry a distinct explicit step should push these entropies up and break the `The → 0 → 0 → ? → . → . → . → .` lock.
- **F5 swap should move accuracy.** Currently, swapping latent KV across examples leaves accuracy unchanged (0.10 → 0.10 at N=30; 13% text change). If latents carry step-identifiable content, swapping must hurt.
- **F1 unique-correct set should grow** beyond our current 2.8%.

Engineering status: the full-LM aux decoder OOMs at Qwen3-4B on our current GH200 budget; the shared-`lm_head` variant is the active path. SIM-CoT is one of three north-star synthesis inputs alongside [[CODI]] and [[Latent Thoughts Tuning]]; see [[Routing vs Reasoning]].
