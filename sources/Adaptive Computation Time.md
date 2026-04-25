---
type: source
title: "Adaptive Computation Time for Recurrent Neural Networks (Graves 2016)"
source_type: paper
arxiv_id: "1603.08983"
venue: "arXiv (unpublished manuscript)"
date_published: 2016-03-29
authors:
  - "Alex Graves"
url: "https://arxiv.org/abs/1603.08983"
code_repo: "https://github.com/aakhundov/tf-rnn-adaptive"
has_weights: false
status: read
confidence: high
key_claims:
  - "ACT augments a recurrent network with a sigmoid halting unit h_t ∈ [0, 1] at each step; the network continues iterating until the cumulative halt probability ∑ h_t exceeds 1 − ε, at which point the remaining probability mass (the 'remainder') is assigned to the last step."
  - "Output and state at timestep t are the halt-weighted mean of intermediate states/outputs across the variable number of 'pondering' steps; the entire mechanism is deterministic and differentiable."
  - "A 'ponder cost' regularizer penalizes the expected number of computation steps: L_ponder = τ · E[N(t) + R(t)] with τ a scalar hyperparameter; this is the knob that trades compute for accuracy."
  - "On parity, logic, addition, and sorting synthetic tasks, ACT dramatically outperforms fixed-depth RNNs; on Hutter-prize character LM, ACT allocates more compute to low-entropy transitions (word/sentence boundaries)."
  - "The ponder-cost gradient is biased and requires tuning of τ; follow-up work ([[PonderNet]], Banino 2021) shows the biased-gradient issue is fatal for large-scale application and proposes a probabilistic (unbiased) reformulation."
projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Historical root of adaptive-depth / variable-compute neural networks. Every modern halting head (HRM, PonderLM-3, Mixture of Recursions) inherits from this paper. Essential genealogy node for the writeup."
  - slug: "branch-a"
    relevance: reference
    why: "ACT is not a scaling recipe but is the conceptual ancestor of Ouro/HRM which are depth-recurrent and therefore relevant to the scaling debate."
  - slug: "branch-b"
    relevance: reference
    why: "Variable-step BPTT via ACT is orthogonal to CODI's fixed-M detach axis; the ponder-cost gradient bias prefigures the detach-vs-BPTT trade-off."
  - slug: "branch-c"
    relevance: not-applicable
    why: "Unrelated to probe methodology."
  - slug: "branch-d"
    relevance: not-applicable
    why: "Unrelated to fusion axis."
last_reviewed: 2026-04-22
reviewed_by: autoreview
tags:
  - paper
  - domain/latent-reasoning
  - domain/adaptive-compute
  - family/halting
  - type/source
  - status/historical
related:
  - "[[PonderNet]]"
  - "[[Universal Transformers]]"
  - "[[Alex Graves]]"
  - "[[Hierarchical Reasoning Model]]"
  - "[[Ouro]]"
sources: []
---

# Adaptive Computation Time (Graves 2016)

## TL;DR

First fully differentiable mechanism for variable-depth neural computation. At each step, an RNN emits a sigmoid halting probability; iteration continues until cumulative halt probability saturates. Output is the halt-weighted mean of intermediate states. Trained with a "ponder cost" regularizer $L_{\text{ponder}} = \tau \cdot \mathbb{E}[N(t) + R(t)]$.

## Why this matters to our project

ACT is the **taxonomic root** of every variable-depth latent-reasoning design in the 2024–2026 wave:

1. **[[PonderNet]]** (Banino 2021) replaces the biased ponder-cost gradient with a Bernoulli halting probability and a KL-divergence to a geometric prior — fixes ACT's pathologies but inherits the core "halting head + shared block" architecture.
2. **[[Universal Transformers]]** (Dehghani 2019) ports the halting-head concept from RNNs to Transformers (per-position dynamic halting).
3. **[[Hierarchical Reasoning Model]]** (Wang 2025) replaces the analytic halting head with a Q-learning head but is fundamentally the same idea.
4. **[[Mixture of Recursions]]**, **[[Ouro]]**, **[[AdaPonderLM]]** — all depth-recurrent with halting heads descending from ACT.

Every "iterate a shared block a variable number of times until convergence" paper cites this lineage. The lineage runs **through** COCONUT's continuous-thought recycling but predates it by 8 years.

## Method (verbatim claims paraphrased)

- At each RNN step, emit sigmoid halt $h_t$; maintain cumulative $H_t = \sum h_i$; halt when $H_t \geq 1 - \epsilon$ (or after $N_{\max}$ steps).
- "Remainder" $R(t)$ = leftover probability mass at halt step, assigned to final pondering step.
- Final output = $\sum_i p_i \cdot y_i$ where $p_i$ are normalized halt probs.
- Ponder cost $L_{\text{ponder}} = \tau \cdot (N(t) + R(t))$ added to task loss.

## Results

- **Parity / addition / sorting:** dramatic improvement over fixed-depth RNN.
- **Character LM (Hutter-prize Wikipedia):** ACT learns to ponder more at low-entropy tokens (word/sentence boundaries). Confirms "think harder at hard tokens" intuition.

## Key limit

The ponder-cost gradient is **biased** (ACT uses a relaxation that's not a clean REINFORCE or reparam). Tuning $\tau$ is empirically brittle. [[PonderNet]] (2021) fixes this.

## Relevance to CODI / COCONUT contrast

ACT is *not* a CoT-compression method; it's a depth-adaptation method. The precursor signature in COCONUT is the "latent-thought replaces several language steps" insight — COCONUT chose fixed continuous-thought count c per stage, sidestepping ACT's halting question. Modern hybrid designs ([[Mixture of Recursions]], [[HRM]]) combine COCONUT-style latent thoughts with ACT-style halting.

## Citation links to chase

- [[PonderNet]] (Banino 2021) — probabilistic reformulation.
- [[Universal Transformers]] (Dehghani 2019) — ACT-in-Transformer.
- Dai et al. 2018 (Transformer-XL) — parameter-tied recurrent depth precursor without ACT.
