---
type: concept
title: "Adaptive Exit Gate"
created: 2026-04-22
updated: 2026-04-22
tags:
  - type/concept
  - domain/architecture
  - domain/latent-reasoning
status: seed
related:
  - "[[LoopLM]]"
  - "[[Fixed-Width Depth Recurrence]]"
  - "[[Ouro]]"
  - "[[RLTT]]"
  - "[[Think-at-Hard]]"
  - "[[Adaptive Loops and Memory]]"
sources:
  - "[[Ouro]]"
  - "[[RLTT]]"

complexity: intermediate
domain: architecture
aliases:
  - "Ponder Gate"
  - "Q-Exit"
  - "Adaptive Computation Gate"

projects:
  - slug: "spar-latent-reasoning"
    relevance: secondary
    why: "Dynamic-depth halting is a deployment knob worth understanding for any loop-based latent reasoning system we evaluate."
  - slug: "branch-a"
    relevance: not-applicable
    why: ""
  - slug: "branch-b"
    relevance: not-applicable
    why: ""
  - slug: "branch-c"
    relevance: not-applicable
    why: ""
  - slug: "branch-d"
    relevance: reference
    why: "Potential future mechanism if LT-Tuning adds a halting signal to fusion-anchored latents; not in current scope."

last_reviewed: 2026-04-22
reviewed_by: autoreview
---

# Adaptive Exit Gate

Learned per-step halting mechanism for depth-recurrent models. Lineage: ACT (Graves 2016) → PonderNet (Banino 2021) → Universal Transformer → Ouro.

## Training objective (Ouro form, Eq. 4)

$$\mathcal{L} = \sum_t p_\phi(t|x) \cdot \mathcal{L}^{(t)} - \beta \cdot H(p_\phi(\cdot|x))$$

- **Per-step halt prob:** $\lambda_t = \sigma(\text{Linear}(h^{(t)}))$.
- **Exit distribution:** cumulative product — $p_\phi(t|x) = \lambda_t \prod_{j<t}(1 - \lambda_j)$.
- **Loss component:** $\mathcal{L}^{(t)}$ = CE if the model had exited at step t.
- **Entropy regularizer:** β·H encourages using all depths (equivalent to KL(p_φ || uniform) up to constant).
- **Uniform prior beats geometric** (η=0.1…0.9) — geometric starves deep iterations of credit.

## Stage II training (Ouro)

- LM frozen; gate-only trained.
- BCE against a greedy label from per-step loss improvement: $I^{(t)} = \max(0, \mathcal{L}^{(t-1)} - \mathcal{L}^{(t)})$.
- Label form: $\sigma(k(I - \gamma))$ with k=50, γ=0.005 — sharp threshold on "is one more step worth it."

## Inference: Q-Exit

$$\text{CDF}(n|x) = 1 - \prod_{j=1}^{n}(1 - \lambda_j(x))$$
$$t_{\text{exit}} = \min\{m : \text{CDF}(m) \ge q\}$$

- `q ∈ [0, 1]` is a **deployment-time** knob for compute-accuracy tradeoff.
- No retrain needed to change q.

## Empirical Pareto (Ouro Fig. 5, MMLU)

1. **Trained Ponder Gate** — best at every compute budget (~66% @ 2.5 avg rounds).
2. **Untrained Ponder Gate (entropy reg only)** — ~64%, closely tracks trained.
3. **Hidden-state-difference threshold** $\|h_t - h_{t-1}\| < \epsilon$ — within 1-2% of trained gate.
4. **Static exit** — dominated.

## Interpretation

- Entropy regularization alone already learns a useful halting signal — no explicit supervision needed for most of the gain.
- Representation-stability proxies (hidden-state delta) capture most of the "done computing" information; adaptive loss captures a small residual.
- The gate is a **learned computation-allocator**, not a thresholded confidence score.

## Cross-links

- PonderNet / ACT — lineage.
- [[LoopLM]] — primary host.
- [[Fixed-Width Depth Recurrence]] — the compute axis the gate allocates over.
- [[RLTT]] — uses the gate's exit-probability distribution as one of three weightings for trajectory-level RL credit assignment (fixes Ouro's GRPO failure).
- [[Think-at-Hard]] — per-token finer-grained analog (neural decider gates each token's second iteration, rather than full-depth halting).
- [[Adaptive Loops and Memory]] — same halting-router lineage at per-layer granularity (200M scale).
