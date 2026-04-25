---
type: source
title: "Dynamics Within Latent Chain-of-Thought — Causal Structure Study"
created: 2026-04-23
updated: 2026-04-23
tags:
  - domain/interpretability
  - domain/latent-reasoning
  - type/source
  - method/causal-intervention
  - method/scm
status: read
related:
  - "[[CODI]]"
  - "[[COCONUT]]"
  - "[[Feature Collapse]]"
sources:
  - "[[.raw/papers/2602.08783-dynamics-latent-cot]]"
source_type: paper
arxiv_id: "2602.08783"
venue: "arXiv"
date_published: 2026-02-09
authors:
  - "Zirui Li"
  - "Xuefeng Bai"
  - "Kehai Chen"
  - "Yizhi Li"
  - "Jian Yang"
  - "Chenghua Lin"
  - "Min Zhang"
url: "https://arxiv.org/abs/2602.08783"
code_repo: "https://github.com/J1mL1/causal-latent-cot"
has_weights: false
confidence: high
key_claims:
  - "We view latent chain-of-thought as a manipulable causal process in representation space by modeling latent steps as variables in a structural causal model (SCM) and analyzing their effects through step-wise do-interventions."
  - "We study two representative paradigms (i.e., Coconut and CODI) on both mathematical and general reasoning tasks."
  - "Latent-step budgets behave less like homogeneous extra depth and more like staged functionality with non-local routing."
  - "We identify a persistent gap between early output bias and late representational commitment."
  - "These results motivate mode-conditional and stability-aware analyses — and corresponding training/decoding objectives — as more reliable tools for interpreting and improving latent reasoning systems."
projects:
  - slug: "branch-d"
    relevance: primary
    why: "Directly studies CODI causally. Findings on 'staged functionality with non-local routing' and early-output-bias / late-representational-commitment gap are exactly the kind of structure LT-Tuning CPF should preserve — a concrete diagnostic frame for evaluating CPF ablations."
  - slug: "branch-a"
    relevance: secondary
    why: "Causal analysis is architecture-agnostic but tested on GPT-2/Llama-scale; useful framing for Qwen3 comparison."
  - slug: "branch-b"
    relevance: secondary
    why: "SCM + do-intervention methodology is a natural complement to detach/stability diagnostics."
  - slug: "branch-c"
    relevance: primary
    why: "Directly engages probe methodology — do-interventions vs correlation-based probes — highly relevant to probe-validity debugging."
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "First causal analysis of CODI+COCONUT; central interpretability paper for the fellowship writeup."
last_reviewed: 2026-04-23
reviewed_by: autoreview
---

# Dynamics Within Latent Chain-of-Thought — Causal Structure Study

Li, Bai, Chen, Li, Yang, Lin, Zhang, [arXiv:2602.08783](https://arxiv.org/abs/2602.08783). Code: [J1mL1/causal-latent-cot](https://github.com/J1mL1/causal-latent-cot).

## TL;DR

First causal-interpretability study of CODI + COCONUT. Views latent steps as SCM variables, uses step-wise do-interventions to answer: (1) which steps are causally necessary, (2) how does influence propagate, (3) do intermediate trajectories retain competing answer modes? Key findings: latent-step budgets act as **staged functionality with non-local routing** (not homogeneous depth), and there is a **persistent gap between early output bias and late representational commitment**.

## Method

- Each latent step is an SCM variable.
- Step-wise do-interventions perturb individual latent states and measure downstream effect.
- Compare Coconut and CODI on math + general reasoning.

## Findings

1. Latent steps ≠ uniform depth — they serve **staged functions** with non-local routing.
2. Output commits early; representations commit late — persistent gap.
3. Intermediate trajectories do retain competing answer modes in representation, but outputs often commit earlier than this diversity warrants.
4. Motivates mode-conditional, stability-aware training/decoding.

## Relevance

Anchor reference for branch-d and branch-c. The "early output bias vs late representational commitment" gap is a **directly testable diagnostic**: if LT-Tuning CPF closes this gap (by tying every step to the vocab manifold), that's a measurable anti-collapse signal beyond accuracy. For branch-c, SCM + do-intervention is the **right probe family** — stronger than correlation probes.

## Citation links to chase

- CODI, COCONUT (study subjects).
- Mode-conditional analysis papers (new line implied by this work).

## SPAR empirical follow-up (2026-04-23)

This paper's "early output bias vs late representational commitment" gap is consistent with our F-battery on CODI V2 bf16 at Qwen3-4B-Instruct-2507 (`research_findings/inert_latent_hypothesis_tests.md`). The gap manifests in two concrete signatures we quantify:

- **F3** — 7/8 latent positions decode via logit-lens to a fixed template `The → 0 → 0 → ? → . → . → . → .` (entropy <0.4 bits for 7 of 8 steps). The "early commitment" is a format-prior template, not per-example output.
- **F5** — cross-example latent-KV swap leaves accuracy unchanged (0.10 → 0.10, N=30, 13% text change; proxy: 0.78 median pair cosine, 63 PCs for 95% variance). The KV content exists but is downstream-irrelevant — "representation without computation."

Our battery operationalizes the paper's causal claim as a falsifiable diagnostic and adds a finer distinction this paper did not cleanly separate: the F4 (25-29% drop under ablation) + F5 (0% drop under swap) + F6 (collapse to <3% at σ=0.5) combination distinguishes *routing-mode* latents from *reasoning-mode* latents. [[Routing vs Reasoning]] elaborates the taxonomy; a useful follow-up is porting F3/F4/F5/F6 to the COCONUT checkpoints studied here.
