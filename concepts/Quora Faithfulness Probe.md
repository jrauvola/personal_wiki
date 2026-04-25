---
type: concept
title: "Quora Faithfulness Probe"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/interpretability
  - domain/latent-reasoning
status: seed
related:
  - "[[Ouro]]"
  - "[[LoopLM]]"
sources:
  - "[[Ouro]]"

complexity: intermediate
domain: interpretability
aliases:
  - "Quora Pair Probe"
  - "QQP Faithfulness Probe"
  - "Step-Agreement Faithfulness"

projects:
  - slug: "spar-latent-reasoning"
    relevance: primary
    why: "Directly reusable protocol — probe each latent position on ambiguous pairs to test whether CODI / KaVa / LT-Tuning latents actually update decisions or post-hoc rationalize. Sharper than existing CoT-faithfulness evals."
  - slug: "branch-a"
    relevance: reference
    why: "Would distinguish architectures that actually refine vs post-hoc rationalize at Qwen3 scale."
  - slug: "branch-b"
    relevance: reference
    why: "If detach-ablation changes whether latent states update decisions across steps, this protocol surfaces it."
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "branch-d"
    relevance: secondary
    why: "Test whether CPF-anchored latents update predictions between loops or just refine a pre-committed answer."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Quora Faithfulness Probe

Methodological protocol (Ouro §7.2) for testing whether a multi-step (CoT or latent-reasoning) model's intermediate reasoning is **causally faithful** — i.e., intermediate states genuinely determine the final answer — or **post-hoc rationalization** — the answer is committed early and intermediate states just decorate it.

## Protocol

1. **Dataset:** Quora Question Pairs (QQP). Each item is a pair of questions; label is "duplicate" vs "not duplicate." Ambiguous pairs are chosen so the answer is not lexically obvious.
2. **Probe:** train a linear classifier on hidden states at a chosen layer to predict the **final step's** answer.
3. **Cut:** probe at the hidden state at the **end of step (i−1)** (e.g., layer 24(i−1) in a 24-layer-per-loop LoopLM). Report ROC AUC predicting step-i answer for i ∈ {2, 3, 4}.
4. **Agreement matrix:** over N items, record for each pair of steps (i, j) the fraction of examples where step-i and step-j predicted the same label.

## Ouro results (baseline claims)

- **Qwen3-4B-Thinking (token CoT):** linear probe at early layers achieves **0.99 ROC AUC** predicting the final answer. **Post-hoc rationalization** — decision is already made before the thinking process.
- **Ouro-1.4B (R=4, LoopLM):** probes at end of step (i−1) do **NOT** reliably predict the step-i answer for i ∈ {2, 3, 4}.
- **Step-agreement:** over 1000 Quora pairs:
  - Step 2 ↔ Step 3: **55.1%**
  - Step 2 ↔ Step 4: **36.1%** (near chance — each loop genuinely updates the decision)
  - Beyond T=4 (extrapolation): jumps to ~90% (fixed point — model stops reasoning past trained depth).

## Interpretation

- A probe AUC near 0.5 at step (i−1) for step-i is evidence of **causal update** between steps.
- A probe AUC near 1.0 at an early layer is evidence of **post-hoc rationalization**.
- The agreement matrix converts this into a per-step metric: low early-vs-late agreement = meaningful refinement; high agreement = fixed-point behavior.

## Why it's a sharper eval than existing CoT-faithfulness work

- Prior CoT faithfulness (e.g., perturbation-based, Turpin 2023) asks: "does perturbing the CoT change the answer?" Confounded by surface-form sensitivity.
- QQP-ambiguous makes the answer non-trivially dependent on the full reasoning trajectory, so linear-probe + agreement-matrix gives a direct measure of **representational update** across steps.
- Works for both token CoT and latent CoT — universal.

## Porting to CODI / KaVa / LT-Tuning

For a latent-CoT model with K latent positions at layer L:

1. Train linear probe on hidden state at latent position k, layer L, predicting final answer.
2. If probe at early k has AUC ≈ 1.0 → post-hoc rationalization.
3. Compute agreement matrix across latent positions.
4. Compare to Qwen3-Thinking (post-hoc baseline) and Ouro (causal-refinement baseline).

Direct test of the informal "latent reasoning is faithful" claim made by CODI-family papers.

## Caveats

- QQP is a binary-classification task; results may not generalize to open-ended generation.
- Linear probes can miss non-linear representations of the answer, so high AUC is strong evidence but low AUC is only weak evidence of update.
- The protocol scores **representational** faithfulness; behavioral faithfulness (does the model actually use the latent state in a causally intervenable way?) requires activation patching on top.
